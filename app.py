from flask import Flask, render_template, request, jsonify
import os
import time  # Ensures files are fully saved before processing
from verification.templatecheck import check_template_and_proceed
from verification.textextract import extract_text, match_with_database
from verification.checkqr import extract_qr_data, extract_text_from_image, compare_qr_and_text
from verification.facerecog import capture_live_image, compare_faces  # Import face recognition
from verification.smartcardverify import verify_smartcard_details  # Import Smart Card verification

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
            os.remove(aadhaar_path)
            os.remove(smartcard_path)
            return jsonify({"message": "❌ Fake Aadhaar detected!"}), 400

        # **Step 4: Extract Text and Match with Database**
        extracted_text, extracted_aadhaar = extract_text(aadhaar_path)

        if extracted_aadhaar is None:
            os.remove(aadhaar_path)
            os.remove(smartcard_path)
            return jsonify({"message": "❌ Aadhaar number not found in extracted text!"}), 400

        if not match_with_database(extracted_text, extracted_aadhaar):
            os.remove(aadhaar_path)
            os.remove(smartcard_path)
            return jsonify({"message": "❌ Aadhaar details do not match the database!"}), 400

        # **Step 5: QR Code Extraction and Validation**
        print(f"📌 Verifying Aadhaar file exists before QR check: {aadhaar_path}")
        time.sleep(1)  # Ensuring file access stability

        qr_data = extract_qr_data(aadhaar_path)
        image_data = extract_text_from_image(aadhaar_path)

        if qr_data is None:
            os.remove(aadhaar_path)
            os.remove(smartcard_path)
            return jsonify({"message": "❌ No QR Code found in Aadhaar image!"}), 400

        if not compare_qr_and_text(qr_data, image_data):
            os.remove(aadhaar_path)
            os.remove(smartcard_path)
            return jsonify({"message": "❌ QR code data does not match extracted text!"}), 400

        # **Step 6: Open Camera and Perform Face Recognition**
        print("📷 Opening webcam for face verification...")
        live_frame = capture_live_image()
        if live_frame is None:
            os.remove(aadhaar_path)
            os.remove(smartcard_path)
            return jsonify({"message": "❌ Face capture failed or canceled!"}), 400

        # Compare faces
        print("🔍 Comparing captured face with Aadhaar image...")
        match_result = compare_faces(live_frame, aadhaar_path)

        if not match_result:
            os.remove(aadhaar_path)  # Delete Aadhaar image if face doesn't match
            os.remove(smartcard_path)
            return jsonify({"message": "❌ Not Aadhaar Valid. Not the Same User. Permission Denied."}), 400

        # **Step 7: Smart Card Verification**
        print("🔍 Verifying Smart Card details...")
        smartcard_verified = verify_smartcard_details(smartcard_path, aadhaar_path)

        if smartcard_verified == True:
            os.remove(aadhaar_path)
            os.remove(smartcard_path)
            return jsonify({"message": "✅ Aadhaar, Face, and Smart Card Verification successful! User is eligible for loan."}), 200
        else:
            os.remove(aadhaar_path)
            os.remove(smartcard_path)
            return jsonify({"message": "❌ Smart Card verification failed!"}), 400

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return jsonify({"message": f"Error processing files: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
