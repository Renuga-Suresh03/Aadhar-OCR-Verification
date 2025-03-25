import os
import pymongo
import easyocr
from cryptography.fernet import Fernet

# Load encryption key
with open(r"C:\Projects\Aadhar-OCR-Verification\sampledata\aes_key.key", "rb") as key_file:
    SECRET_KEY = key_file.read()

fernet = Fernet(SECRET_KEY)

# Database Connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["aadhar_db"]
collection = db["aadhar_details"]

UPLOAD_FOLDER = r"C:\Projects\Aadhar-OCR-Verification\uploads"

# Initialize EasyOCR
reader = easyocr.Reader(["en"])  # English OCR model

def decrypt_data(encrypted_text):
    """Decrypts the stored Aadhaar details."""
    return fernet.decrypt(encrypted_text.encode()).decode()

def extract_text(image_path):
    """Extracts text from the Aadhaar image using EasyOCR."""
    result = reader.readtext(image_path, detail=0)
    extracted_data = [text.strip() for text in result]
    
    # Extract Aadhaar number dynamically
    aadhaar_number = next(
        (text.replace(" ", "") for text in extracted_data if text.replace(" ", "").isdigit() and len(text.replace(" ", "")) == 12), 
        None
    )
    
    return extracted_data, aadhaar_number

def contains_value(extracted_data, stored_value):
    """Checks if any extracted text contains the stored value."""
    return any(stored_value in text for text in extracted_data)

def match_with_database(extracted_data, extracted_aadhar):
    """Matches extracted text with stored Aadhaar details in the database."""
    
    for record in collection.find():
        stored_name = decrypt_data(record["name"])
        stored_dob = decrypt_data(record["dob"])
        stored_gender = decrypt_data(record["gender"])
        stored_aadhar = decrypt_data(record["aadhaar_number"]).replace(" ", "").strip()  # Normalize stored Aadhaar

        print(f"\n🔎 Checking:\nStored -> {stored_name}, {stored_dob}, {stored_gender}, {stored_aadhar}\nExtracted -> {extracted_data}\nExtracted Aadhaar -> {extracted_aadhar}")

        name_match = contains_value(extracted_data, stored_name)
        dob_match = contains_value(extracted_data, stored_dob)
        gender_match = contains_value(extracted_data, stored_gender)
        aadhaar_match = stored_aadhar == extracted_aadhar  # Exact match

        if not name_match:
            print(f"❌ Name mismatch! Stored: {stored_name}, Extracted: {extracted_data}")
        if not dob_match:
            print(f"❌ DOB mismatch! Stored: {stored_dob}, Extracted: {extracted_data}")
        if not gender_match:
            print(f"❌ Gender mismatch! Stored: {stored_gender}, Extracted: {extracted_data}")
        if not aadhaar_match:
            print(f"❌ Aadhaar mismatch! Stored: {stored_aadhar}, Extracted: {extracted_aadhar}")

        if name_match and dob_match and gender_match and aadhaar_match:
            print(f"✅ Aadhaar Verified: {stored_name}")
            return True

    return False

def check_template_and_proceed(filename):
    """Checks template similarity, extracts text, verifies against the database, and proceeds to face matching."""
    uploaded_file_path = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(uploaded_file_path):
        print(f"❌ File {filename} not found in {UPLOAD_FOLDER}.")
        return

    # Extract text and Aadhaar number from uploaded image
    extracted_text, extracted_aadhar = extract_text(uploaded_file_path)
    print("📝 Extracted Text:", extracted_text)

    if extracted_aadhar is None:
        print("🚨 Aadhaar number not found in extracted text! Deleting file...")
        os.remove(uploaded_file_path)
        return

    # Match extracted details with database
    if match_with_database(extracted_text, extracted_aadhar):
        print("✅ Aadhaar details match the database. Proceeding to face matching...")
        # Call face matching function here (not implemented yet)
    else:
        print("🚨 Fake Aadhaar detected! Deleting file...")
        os.remove(uploaded_file_path)

# Example usage
check_template_and_proceed("Renu.png")  # Change filename accordingly
