from flask import Flask, render_template, request, jsonify
import os
from verification.templatecheck import check_template_and_proceed

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def upload_page():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'aadhaar' not in request.files or 'smartcard' not in request.files:
        return jsonify({"message": "Both Aadhaar and Smart Card files are required!"}), 400

    aadhaar = request.files['aadhaar']
    smartcard = request.files['smartcard']

    if aadhaar.filename == '' or smartcard.filename == '':
        return jsonify({"message": "Invalid file uploaded!"}), 400

    aadhaar_path = os.path.join(UPLOAD_FOLDER, "aadhaar.png")
    smartcard_path = os.path.join(UPLOAD_FOLDER, "smart.png")

    try:
        # **Step 1: Save Files First**
        aadhaar.save(aadhaar_path)
        smartcard.save(smartcard_path)

        print(f"✅ Aadhaar saved at: {aadhaar_path}")
        print(f"✅ Smart Card saved at: {smartcard_path}")

        # **Step 2: Check if the files exist**
        if not os.path.exists(aadhaar_path) or not os.path.exists(smartcard_path):
            return jsonify({"message": "❌ File not saved properly!"}), 500

        # **Step 3: Proceed with template check**
        if not check_template_and_proceed("aadhaar.png"):  # Only filename passed, function handles full path
            os.remove(aadhaar_path)  # Delete file if Aadhaar is fake
            return jsonify({"message": "❌ Fake Aadhaar detected!"}), 400

        return jsonify({"message": "✅ Aadhaar template is valid. Proceeding to text extraction..."})

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({"message": "Error processing files!"}), 500

if __name__ == '__main__':
    app.run(debug=True)
