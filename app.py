from flask import Flask, request, jsonify
import os

app = Flask(__name__)

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'jpg', 'jpeg', 'png', 'tiff'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route("/")
def index():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Aadhar & Smart Card Verification</title>
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
        <style>
            body { font-family: Arial, sans-serif; background: linear-gradient(to right, #ddeefc, #b1dcf7); text-align: center; padding: 50px; }
            .container { display: flex; justify-content: center; gap: 20px; }
            .upload-box { width: 300px; padding: 20px; border: 2px solid #3b8beb; text-align: center; background: white; border-radius: 12px; box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1); }
            .drop-area { padding: 20px; cursor: pointer; border-radius: 8px; border: 2px dashed #3b8beb; }
            .upload-btn { background: #aaa; color: white; padding: 10px 20px; border: none; border-radius: 5px; cursor: not-allowed; margin-top: 20px; font-size: 16px; }
            .upload-btn.active { background: #28a745; cursor: pointer; }
            .spinner { width: 30px; height: 30px; border: 4px solid rgba(0, 0, 255, 0.3); border-top-color: blue; border-radius: 50%; animation: spin 1s linear infinite; margin: 10px auto; display: none; }
            @keyframes spin { to { transform: rotate(360deg); } }
        </style>
    </head>
    <body>

        <h1>Aadhar & Smart Card Verification</h1>

        <div class="container">
            <div class="upload-box">
                <h3>Upload Aadhar</h3>
                <div class="drop-area" id="drop-aadhar">Click to choose file</div>
                <input type="file" id="aadhar-file" class="hidden" accept="image/png, image/jpeg, image/tiff">
                <div id="aadhar-preview" class="hidden"></div>
            </div>

            <div class="upload-box">
                <h3>Upload Smart Card</h3>
                <div class="drop-area" id="drop-smartcard">Click to choose file</div>
                <input type="file" id="smartcard-file" class="hidden" accept="image/png, image/jpeg, image/tiff">
                <div id="smartcard-preview" class="hidden"></div>
            </div>
        </div>

        <button class="upload-btn" id="upload-btn" disabled>Upload Both Documents</button>
        <div class="spinner" id="upload-spinner"></div>

        <script>
            function setupFileUpload(dropAreaId, inputFileId, previewId) {
                let dropArea = document.getElementById(dropAreaId);
                let inputFile = document.getElementById(inputFileId);
                let preview = document.getElementById(previewId);

                dropArea.addEventListener("click", () => inputFile.click());

                inputFile.addEventListener("change", function () {
                    let file = this.files[0];
                    if (file) {
                        preview.innerHTML = `<span>${file.name} (${(file.size / 1024).toFixed(1)} KB)</span>`;
                        preview.classList.remove("hidden");
                        updateUploadButton();
                    }
                });
            }

            function updateUploadButton() {
                let aadharSelected = document.getElementById("aadhar-file").files.length > 0;
                let smartcardSelected = document.getElementById("smartcard-file").files.length > 0;
                let uploadBtn = document.getElementById("upload-btn");

                if (aadharSelected && smartcardSelected) {
                    uploadBtn.disabled = false;
                    uploadBtn.classList.add("active");
                } else {
                    uploadBtn.disabled = true;
                    uploadBtn.classList.remove("active");
                }
            }

            document.getElementById("upload-btn").addEventListener("click", function () {
                let formData = new FormData();
                formData.append("aadhar", document.getElementById("aadhar-file").files[0]);
                formData.append("smartcard", document.getElementById("smartcard-file").files[0]);

                let uploadBtn = document.getElementById("upload-btn");
                let spinner = document.getElementById("upload-spinner");

                // Show "Verification in Process..."
                uploadBtn.innerText = "Verification in Process...";
                uploadBtn.disabled = true;
                uploadBtn.classList.remove("active");
                spinner.style.display = "block";

                fetch("/upload", {
                    method: "POST",
                    body: formData
                })
                .then(response => response.json())
                .then(data => {
                    console.log("Upload successful:", data);
                    // Keep showing "Verification in Process..."
                })
                .catch(error => {
                    console.error("Error:", error);
                    uploadBtn.innerText = "Upload Failed! Try Again";
                    uploadBtn.disabled = false;
                    uploadBtn.classList.add("active");
                    spinner.style.display = "none";
                });
            });

            setupFileUpload("drop-aadhar", "aadhar-file", "aadhar-preview");
            setupFileUpload("drop-smartcard", "smartcard-file", "smartcard-preview");
        </script>

    </body>
    </html>
    """

@app.route("/upload", methods=["POST"])
def upload_file():
    if "aadhar" not in request.files or "smartcard" not in request.files:
        return jsonify({"error": "Both files are required!"}), 400

    aadhar = request.files["aadhar"]
    smartcard = request.files["smartcard"]

    if aadhar.filename == "" or smartcard.filename == "":
        return jsonify({"error": "Both files must be selected!"}), 400

    aadhar_path = os.path.join(app.config['UPLOAD_FOLDER'], aadhar.filename)
    smartcard_path = os.path.join(app.config['UPLOAD_FOLDER'], smartcard.filename)

    aadhar.save(aadhar_path)
    smartcard.save(smartcard_path)

    return jsonify({
        "message": "Files uploaded successfully!",
        "aadhar_path": aadhar_path,
        "smartcard_path": smartcard_path
    })

if __name__ == "__main__":
    app.run(debug=True)
