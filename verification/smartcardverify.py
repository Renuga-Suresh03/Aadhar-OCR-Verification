import pymongo
from cryptography.fernet import Fernet
import easyocr
import re

# Load the encryption key
with open(r"C:\Projects\Aadhar-OCR-Verification\sampledata\aes_key.key", "rb") as key_file:
    SECRET_KEY = key_file.read()

fernet = Fernet(SECRET_KEY)

# Database Connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["aadhar_db"]
collection = db["smart_card_details"]  # Collection storing Smart Card data

# OCR Reader
reader = easyocr.Reader(["en"])  # English OCR


def extract_text(image_path):
    """Extract text from an image using EasyOCR."""
    results = reader.readtext(image_path, detail=0)
    return " ".join(results)


def extract_smartcard_number(text):
    """Extract a 12-digit Smart Card number from text."""
    match = re.search(r"\b\d{12}\b", text)  # Looks for a 12-digit number
    return match.group() if match else None


def extract_aadhaar_numbers(text):
    """Extract Aadhaar number (12-digit format with spaces)."""
    aadhaar_numbers = re.findall(r"\b\d{4} \d{4} \d{4}\b", text)  # Aadhaar format
    return aadhaar_numbers[0] if aadhaar_numbers else None  # Return first Aadhaar found


def verify_smartcard(smartcard_number, aadhaar_number):
    """Verify if the Smart Card exists and Aadhaar number is linked."""
    # Fetch smart card details from DB
    encrypted_smart_cards = collection.find({})

    for record in encrypted_smart_cards:
        # Decrypt stored Smart Card number
        stored_smartcard_number = fernet.decrypt(record["smart_card_number"].encode()).decode()

        if stored_smartcard_number == smartcard_number:
            print(f"✅ Smart Card {smartcard_number} found in DB.")

            # Decrypt stored family Aadhaar numbers
            stored_aadhaar_numbers = [fernet.decrypt(num.encode()).decode() for num in record["family_members"]]

            if aadhaar_number in stored_aadhaar_numbers:
                print(f"✅ Aadhaar {aadhaar_number} is linked to Smart Card {smartcard_number}. Verification Success!")
                return True
            else:
                print(f"❌ Aadhaar {aadhaar_number} NOT linked to Smart Card {smartcard_number}. Verification Failed!")
                return False

    print(f"❌ Smart Card {smartcard_number} NOT found in Database.")
    return False


# **Main Execution**
def verify_smartcard_details(smartcard_image, aadhaar_image):
    """Extract & Verify Smart Card and Aadhaar details from images."""
    
    # Extract text from Smart Card image
    smartcard_text = extract_text(smartcard_image)
    print("\n📄 Extracted Text from Smart Card:\n" + smartcard_text + "\n")

    # Extract text from Aadhaar image
    aadhaar_text = extract_text(aadhaar_image)
    print("\n📄 Extracted Text from Aadhaar:\n" + aadhaar_text + "\n")

    # Extract numbers
    smartcard_number = extract_smartcard_number(smartcard_text)
    aadhaar_number = extract_aadhaar_numbers(aadhaar_text)

    if not smartcard_number:
        print("❌ Smart Card number not found!")
        return

    if not aadhaar_number:
        print("❌ Aadhaar number not found!")
        return

    print(f"Extracted Smart Card: {smartcard_number}")
    print(f"Extracted Aadhaar: {aadhaar_number}")

    # Verify details
    verify_smartcard(smartcard_number, aadhaar_number)


# **Run Verification**
if __name__ == "__main__":
    smartcard_image = r"C:\Projects\Aadhar-OCR-Verification\uploads\smart.png"  # Smart Card image
    aadhaar_image = r"C:\Projects\Aadhar-OCR-Verification\uploads\aadhaar.png"  # Aadhaar image

    verify_smartcard_details(smartcard_image, aadhaar_image)
