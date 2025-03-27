import os
import cv2
import easyocr
from pyzbar.pyzbar import decode

reader = easyocr.Reader(["en"])

def extract_qr_data(image_path):
    """Scans and extracts text from a QR code in the image."""
    if not os.path.exists(image_path):
        print(f"❌ ERROR: File not found at {image_path} before QR extraction!")
        return None

    image = cv2.imread(image_path)
    if image is None:
        print(f"❌ ERROR: OpenCV failed to read {image_path}. Check file format.")
        return None

    qr_codes = decode(image)
    if not qr_codes:
        print("🚨 No QR code found in the image!")
        return None

    qr_text = qr_codes[0].data.decode("utf-8").strip()
    print("\n✅ QR Code Data Extracted:\n", qr_text)

    qr_data = {}
    for line in qr_text.split("\n"):
        if ": " in line:
            key, value = line.split(": ", 1)
            qr_data[key.strip()] = value.strip()

    return qr_data

def extract_text_from_image(image_path):
    """Extracts text from the image using EasyOCR."""
    if not os.path.exists(image_path):
        print(f"❌ ERROR: File not found at {image_path} before text extraction!")
        return None

    result = reader.readtext(image_path, detail=0)
    extracted_data = [text.strip() for text in result]
    
    print("\n📝 Extracted Text from Image:", extracted_data)

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

def compare_qr_and_text(qr_data, image_data):
    """Compares QR code data with extracted text and returns True/False instead of deleting."""
    if not qr_data or not image_data:
        print("\n🚨 Unable to verify Aadhaar details due to missing data.")
        return False

    all_match = True  

    if qr_data.get("Aadhaar No") == image_data.get("Aadhaar No"):
        print("✅ Aadhaar Number matches QR Code!")
    else:
        print(f"❌ Mismatch: QR Aadhaar: '{qr_data.get('Aadhaar No')}' | Extracted: '{image_data.get('Aadhaar No')}'")
        all_match = False

    for key in ["Name", "DOB", "Gender"]:
        if qr_data.get(key) and qr_data.get(key) == image_data.get(key):
            print(f"✅ {key} matches QR Code!")
        else:
            print(f"❌ Mismatch: QR Data '{key}: {qr_data.get(key)}' ≠ Extracted Text")
            all_match = False

    return all_match
