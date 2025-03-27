from flask import Flask, render_template, request, jsonify
import os
import time  # Ensures files are fully saved before processing
from verification.templatecheck import check_template_and_proceed
from verification.textextract import extract_text, match_with_database
from verification.checkqr import extract_qr_data, extract_text_from_image, compare_qr_and_text

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
        # **Step 1: Save Files**
        aadhaar.save(aadhaar_path)
        smartcard.save(smartcard_path)

        print(f"✅ Aadhaar saved at: {aadhaar_path}")
        print(f"✅ Smart Card saved at: {smartcard_path}")

        # **Step 2: Ensure Files Exist**
        time.sleep(1)  # Small delay to prevent file not found errors
        if not os.path.exists(aadhaar_path) or not os.path.exists(smartcard_path):
            return jsonify({"message": "❌ File not saved properly!"}), 500

        print(f"📌 Confirming Aadhaar file exists before template check: {aadhaar_path}")

        # **Step 3: Template Check**
        if not check_template_and_proceed("aadhaar.png"):  # Pass only filename
            return jsonify({"message": "❌ Fake Aadhaar detected!"}), 400

        # **Step 4: Extract Text and Match with Database**
        extracted_text, extracted_aadhaar = extract_text(aadhaar_path)

        if extracted_aadhaar is None:
            return jsonify({"message": "❌ Aadhaar number not found in extracted text!"}), 400

        if not match_with_database(extracted_text, extracted_aadhaar):
            return jsonify({"message": "❌ Aadhaar details do not match the database!"}), 400

        # **Step 5: QR Code Extraction and Validation**
        print(f"📌 Verifying Aadhaar file exists before QR check: {aadhaar_path}")
        time.sleep(1)  # Ensuring file access stability

        qr_data = extract_qr_data(aadhaar_path)
        image_data = extract_text_from_image(aadhaar_path)

        if qr_data is None:
            return jsonify({"message": "❌ No QR Code found in Aadhaar image!"}), 400

        if not compare_qr_and_text(qr_data, image_data):
            return jsonify({"message": "❌ QR code data does not match extracted text!"}), 400

        return jsonify({"message": "✅ QR Verification successful! Proceeding to face matching..."})

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({"message": "Error processing files!"}), 500

if __name__ == '__main__':
    app.run(debug=True)
