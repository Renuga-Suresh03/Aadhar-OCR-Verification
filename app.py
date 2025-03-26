from flask import Flask, render_template_string, request, jsonify
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aadhaar & Smart Card Verification</title>
    <style>
        * { box-sizing: border-box; }
        body {
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: var(--bg-color);
            color: var(--text-color);
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
            transition: all 0.3s ease-in-out;
        }
        :root {
            --bg-color: #1e1e1e;
            --container-bg: #2a2a2a;
            --text-color: #ffffff;
            --btn-bg: #28a745;
            --btn-hover: #218838;
            --border-color: #555;
        }
        .light-mode {
            --bg-color: #f4f4f4;
            --container-bg: #ffffff;
            --text-color: #333;
            --btn-bg: #007BFF;
            --btn-hover: #0056b3;
            --border-color: #ddd;
        }
        .wrapper { margin-top: 40px; text-align: center; }
        .upload-container {
            display: flex;
            justify-content: center;
            gap: 20px;
            flex-wrap: wrap;
        }
        .container {
            background: var(--container-bg);
            padding: 30px;
            border-radius: 15px;
            width: 300px;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
            text-align: center;
        }
        .upload-box {
            border: 2px dashed var(--border-color);
            padding: 12px;
            cursor: pointer;
            border-radius: 10px;
            transition: all 0.3s ease;
            margin-bottom: 10px;
        }
        .upload-box:hover { background: rgba(200, 200, 200, 0.2); }
        input[type="file"] { display: none; }
        .btn {
            display: inline-block;
            padding: 10px 15px;
            font-size: 14px;
            border-radius: 5px;
            border: none;
            cursor: pointer;
            background: var(--btn-bg);
            color: white;
            transition: all 0.3s;
            width: 100%;
        }
        .btn:hover { background: var(--btn-hover); }
        .preview-container {
            display: none;
            margin-top: 10px;
            text-align: center;
        }
        .preview-container img {
            width: 80px;
            height: auto;
            border-radius: 5px;
            margin-right: 10px;
        }
        .spinner {
            border: 5px solid rgba(0,0,0,0.1);
            border-top: 5px solid var(--btn-bg);
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 2s linear infinite;
            display: none;
            margin: 15px auto;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        .toggle-switch {
            position: absolute;
            top: 10px;
            right: 10px;
            cursor: pointer;
            font-size: 14px;
            padding: 5px 10px;
            border-radius: 5px;
            background: var(--btn-bg);
            color: white;
        }
        .upload-btn-container {
            margin-top: 20px;
            text-align: center;
            width: 100%;
        }
    </style>
</head>

<body>
    <button id="themeToggle" class="toggle-switch" onclick="toggleTheme()">Light Mode</button>
    <div class="wrapper">
        <h1>Aadhaar & Smart Card Verification</h1>
        <div class="upload-container">
            <div class="container">
                <h2>Upload Your Aadhaar</h2>
                <div class="upload-box" onclick="document.getElementById('aadhaarInput').click()">
                    Click to Browse or Drag & Drop
                </div>
                <input type="file" id="aadhaarInput" accept="image/png, image/jpeg" onchange="handleFileSelect('aadhaar')">
                <div class="preview-container" id="aadhaarPreviewContainer">
                    <img id="aadhaarPreviewImage" alt="Preview">
                    <button class="btn" onclick="removeFile('aadhaar')">Delete</button>
                </div>
            </div>

            <div class="container">
                <h2>Upload Your Smart Card</h2>
                <div class="upload-box" onclick="document.getElementById('smartcardInput').click()">
                    Click to Browse or Drag & Drop
                </div>
                <input type="file" id="smartcardInput" accept="image/png, image/jpeg" onchange="handleFileSelect('smartcard')">
                <div class="preview-container" id="smartcardPreviewContainer">
                    <img id="smartcardPreviewImage" alt="Preview">
                    <button class="btn" onclick="removeFile('smartcard')">Delete</button>
                </div>
            </div>
        </div>

        <div class="upload-btn-container">
            <button class="btn" id="uploadBtn" onclick="uploadFiles()" disabled>Upload</button>
        </div>
        
        <div class="spinner" id="spinner"></div>
        <p id="status"></p>
    </div>

    <script>
        function toggleTheme() {
            let body = document.body;
            let toggleBtn = document.getElementById("themeToggle");

            body.classList.toggle("light-mode");

            if (body.classList.contains("light-mode")) {
                toggleBtn.innerText = "Dark Mode";
            } else {
                toggleBtn.innerText = "Light Mode";
            }
        }

        function handleFileSelect(type) {
            let input = document.getElementById(type + 'Input');
            let file = input.files[0];
            if (!file) return;

            let reader = new FileReader();
            reader.onload = function (e) {
                document.getElementById(type + 'PreviewImage').src = e.target.result;
                document.getElementById(type + 'PreviewContainer').style.display = 'flex';
            };
            reader.readAsDataURL(file);
            checkUploadButton();
        }

        function removeFile(type) {
            document.getElementById(type + 'Input').value = "";
            document.getElementById(type + 'PreviewContainer').style.display = 'none';
            checkUploadButton();
        }

        function checkUploadButton() {
            let aadhaarFile = document.getElementById('aadhaarInput').files.length > 0;
            let smartCardFile = document.getElementById('smartcardInput').files.length > 0;
            document.getElementById('uploadBtn').disabled = !(aadhaarFile && smartCardFile);
        }

        function uploadFiles() {
            let formData = new FormData();
            formData.append('aadhaar', document.getElementById('aadhaarInput').files[0]);
            formData.append('smartcard', document.getElementById('smartcardInput').files[0]);

            document.getElementById('spinner').style.display = 'block';
            document.getElementById('status').innerText = '';

            fetch('/upload', { method: 'POST', body: formData })
                .then(response => response.json())
                .then(data => {
                    setTimeout(() => {
                        document.getElementById('spinner').style.display = 'none';
                        document.getElementById('status').innerText = data.message;
                    }, 3000);
                })
                .catch(error => console.error('Error:', error));
        }
    </script>
</body>
</html>
"""

@app.route('/')
def upload_page():
    return render_template_string(HTML_TEMPLATE)


@app.route('/upload', methods=['POST'])
def upload_file():
    if 'aadhaar' not in request.files or 'smartcard' not in request.files:
        return jsonify({"message": "Both Aadhaar and Smart Card files are required!"}), 400

    aadhaar = request.files['aadhaar']
    smartcard = request.files['smartcard']

    if aadhaar.filename == '' or smartcard.filename == '':
        return jsonify({"message": "Invalid file uploaded!"}), 400

    # Save files with fixed names
    aadhaar_path = os.path.join(UPLOAD_FOLDER, "aadhaar.png")
    smartcard_path = os.path.join(UPLOAD_FOLDER, "smart.png")

    aadhaar.save(aadhaar_path)
    smartcard.save(smartcard_path)

    return jsonify({"message": "Files uploaded successfully!"})



if __name__ == '__main__':
    app.run(debug=True)