import os
import cv2
import easyocr
from pyzbar.pyzbar import decode

# Image path (Modify as needed)
image_path = r"C:\Projects\Aadhar-OCR-Verification\uploads\aadhaar.png"

# Initialize EasyOCR
reader = easyocr.Reader(["en"])

def extract_qr_data(image_path):
    """Scans and extracts text from a QR code in the image."""
    image = cv2.imread(image_path)
    qr_codes = decode(image)
    
    if not qr_codes:
        print("🚨 No QR code found in the image!")
        return None

    qr_text = qr_codes[0].data.decode("utf-8").strip()  # Extract and clean text
    print("\n✅ QR Code Data Extracted:\n", qr_text)
    
    # Convert QR text into a dictionary for easy comparison
    qr_data = {}
    for line in qr_text.split("\n"):
        if ": " in line:
            key, value = line.split(": ", 1)
            qr_data[key.strip()] = value.strip()
    
    return qr_data

def extract_text_from_image(image_path):
    """Extracts text from the image using EasyOCR."""
    result = reader.readtext(image_path, detail=0)
    extracted_data = [text.strip() for text in result]
    
    print("\n📝 Extracted Text from Image:", extracted_data)
    
    # Convert extracted data into a dictionary
    image_data = {}
    for i in range(len(extracted_data)):
        if "Name:" in extracted_data[i]:
            image_data["Name"] = extracted_data[i].split("Name:")[-1].strip()
        elif "DOB:" in extracted_data[i]:
            image_data["DOB"] = extracted_data[i].split("DOB:")[-1].strip()
        elif "Gender:" in extracted_data[i]:
            image_data["Gender"] = extracted_data[i].split("Gender:")[-1].strip()
        elif len(extracted_data[i].replace(" ", "")) == 12 and extracted_data[i].replace(" ", "").isdigit():
            image_data["Aadhaar No"] = extracted_data[i]

    return image_data

def compare_qr_and_text(qr_data, image_data, image_path):
    """Compares QR code data with extracted image text and detects mismatches."""
    if not qr_data or not image_data:
        print("\n🚨 Unable to verify Aadhaar details due to missing data.")
        return

    all_match = True  # Flag to track if all details match

    # Check if Aadhaar number matches
    if qr_data.get("Aadhaar No") == image_data.get("Aadhaar No"):
        print("✅ Aadhaar Number matches QR Code!")
    else:
        print(f"❌ Mismatch found! QR Aadhaar: '{qr_data.get('Aadhaar No')}' | Extracted: '{image_data.get('Aadhaar No')}'")
        all_match = False

    # Check Name, DOB, Gender
    for key in ["Name", "DOB", "Gender"]:
        if qr_data.get(key) and qr_data.get(key) == image_data.get(key):
            print(f"✅ {key} matches QR Code!")
        else:
            print(f"❌ Mismatch found! QR Data: '{key}: {qr_data.get(key)}' not in Extracted Image Text")
            all_match = False

    if all_match:
        print("\n✅ Aadhaar details **MATCH** QR code. No tampering detected! 🎉")
    else:
        print("\n🚨 Aadhaar details **DO NOT MATCH** QR code! Possible tampering detected.")
        
        # Delete the file if details do not match
        if os.path.exists(image_path):
            os.remove(image_path)
            print(f"🗑️ File '{image_path}' has been deleted due to mismatch.")

# Run verification process
qr_data = extract_qr_data(image_path)
image_data = extract_text_from_image(image_path)
compare_qr_and_text(qr_data, image_data, image_path)
