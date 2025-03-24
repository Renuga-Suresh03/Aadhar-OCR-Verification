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

# Folder paths
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
    <title>Document Verification & Aadhaar Upload</title>
    <style>
        body { font-family: Arial, sans-serif; padding: 20px; text-align: center; }
        .header { display: flex; justify-content: center; align-items: center; margin-bottom: 30px; }
        .header img { width: 50px; margin-right: 10px; }
        .header h1 { margin: 0; font-size: 26px; }
        .upload-section { margin-top: 20px; }
        .upload-container { border: 2px dashed #ccc; padding: 20px; cursor: pointer; width: 300px; margin: 20px auto; }
        .upload-container:hover { background-color: #f9f9f9; }
        input[type="file"] { display: none; }
        .aadhaar-logo { width: 80px; margin-bottom: 10px; }
    </style>
</head>
<body>
    <!-- Document Verification with logo left -->
    <div class="header">
        <img src="{{ url_for('static_assessts', filename='doc.png') }}" alt="Doc Logo">
        <h1>Document Verification</h1>
    </div>

    <!-- Aadhaar Upload Section -->
    <div class="upload-section">
        <img class="aadhaar-logo" src="{{ url_for('static_assessts', filename='aadhaar_logo.png') }}" alt="Aadhaar Logo">
        <h2>Upload Your Aadhaar</h2>
        <div class="upload-container" onclick="document.getElementById('fileInput').click()">
            Drag & Drop or Click to Upload
        </div>
        <input type="file" id="fileInput" accept="image/*" onchange="uploadFile()">
        <p id="status"></p>
    </div>

    <script>
        function uploadFile() {
            let file = document.getElementById("fileInput").files[0];
            if (!file) return;
            let formData = new FormData();
            formData.append("file", file);
            fetch("/upload", { method: "POST", body: formData })
                .then(response => response.text())
                .then(data => document.getElementById("status").innerText = data)
                .catch(error => console.error("Error:", error));
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
        return "No file uploaded!"
    file = request.files['file']
    if file.filename == '':
        return "No selected file!"
    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    return "✅ Aadhaar uploaded successfully!"

if __name__ == '__main__':
    app.run(debug=True)
