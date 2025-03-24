#task assigned to visa

#ui for file upload
#get aadhar card only
#good ui
#must store the uploaded file as following in uploads folder
#aadhar.jpg/png
#should not store in db
#dont create a separate file to add html and css , add everything inline itself

from flask import Flask, render_template_string, request, send_from_directory
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
ASSESSTS_FOLDER = "assessts"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(ASSESSTS_FOLDER, exist_ok=True)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Aadhaar OCR Verification</title>
    <style>
        * {
            box-sizing: border-box;
        }
        body {
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #e0e0f5, #c2bfff);
            color: #333;
            display: flex;
            flex-direction: column;
            align-items: center;
            min-height: 100vh;
            position: relative;
        }
        .wrapper {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: flex-start;
            margin-top: 40px;
            width: 100%;
        }
        .header {
            text-align: center;
            margin-bottom: 20px;
        }
        .header img {
            width: 50px;
            vertical-align: middle;
            margin-right: 10px;
            animation: float 3s ease-in-out infinite;
        }
        .header h1 {
            display: inline;
            font-size: 28px;
            font-weight: bold;
            color: #4B0082;
        }
        .container {
            background: rgba(255, 255, 255, 0.85);
            padding: 30px;
            border-radius: 20px;
            width: 340px;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.2);
            text-align: center;
            backdrop-filter: blur(8px);
        }
        .container img {
            width: 60px;
            margin-bottom: 10px;
            animation: float-slow 4s ease-in-out infinite;
        }
        h2 {
            margin-top: 5px;
            margin-bottom: 15px;
            font-size: 20px;
            color: #4B0082;
        }
        .upload-container {
            border: 2px dashed #7B68EE;
            padding: 12px;
            cursor: pointer;
            border-radius: 10px;
            transition: all 0.3s ease;
            margin-bottom: 10px;
        }
        .upload-container:hover {
            background: rgba(230, 230, 250, 0.5);
            transform: translateY(-3px);
            box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
        }
        input[type="file"] {
            display: none;
        }
        #status {
            margin-top: 10px;
            font-weight: bold;
        }
        #size {
            margin-top: 5px;
        }
        @keyframes float {
            0% { transform: translateY(0); }
            50% { transform: translateY(-5px); }
            100% { transform: translateY(0); }
        }
        @keyframes float-slow {
            0% { transform: translateY(0); }
            50% { transform: translateY(-8px); }
            100% { transform: translateY(0); }
        }
        .spinner {
            border: 5px solid rgba(0,0,0,0.1);
            border-top: 5px solid #7B68EE;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 2s linear infinite;
            margin: 15px auto;
            display: none;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>

<body>
    <div class="wrapper">
        <div class="header">
            <img src="{{ url_for('static_assessts', filename='doc.png') }}" alt="Doc Logo">
            <h1>Aadhaar OCR Verification</h1>
        </div>

        <div class="container">
            <img src="{{ url_for('static_assessts', filename='aadhaar_logo.png') }}" alt="Aadhaar Logo">
            <h2>Upload Your Aadhaar</h2>
            <div class="upload-container" onclick="document.getElementById('fileInput').click()">
                Drag & Drop or Click to Upload
            </div>
            <input type="file" id="fileInput" accept="image/*" onchange="uploadFile()">
            <div class="spinner" id="spinner"></div>
            <p id="status"></p>
            <p id="size"></p>
        </div>
    </div>

    <script>
        function uploadFile() {
            let file = document.getElementById('fileInput').files[0];
            if (!file) return;
            let formData = new FormData();
            formData.append('file', file);

            document.getElementById('spinner').style.display = 'block';
            document.getElementById('status').innerText = '';
            document.getElementById('size').innerText = '';

            fetch('/upload', { method: 'POST', body: formData })
                .then(response => response.json())
                .then(data => {
                    setTimeout(() => {
                        document.getElementById('spinner').style.display = 'none';
                        document.getElementById('status').innerText = data.message;
                        document.getElementById('size').innerText = 'File Size: ' + data.size;
                    }, 3000); // Spinner time set to 3 seconds
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

@app.route('/assessts/<path:filename>')
def static_assessts(filename):
    return send_from_directory(ASSESSTS_FOLDER, filename)

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return {"message": "No file uploaded!", "size": "0 KB"}
    file = request.files['file']
    if file.filename == '':
        return {"message": "No selected file!", "size": "0 KB"}
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    size = os.path.getsize(filepath) / 1024
    return {"message": "Aadhaar uploaded successfully!", "size": f"{size:.2f} KB"}

if __name__ == '__main__':
    app.run(debug=True)
