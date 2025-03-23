#assigned to renu

#from uploads take image
#extract text
#compare with db 
#if match can proceed to face matching
#else del file from uploads and display as fake aadhar detected

import easyocr
import cv2
import numpy as np
import re

# Initialize EasyOCR Reader
reader = easyocr.Reader(['en'])

# Load Image
image_path = r"C:\Projects\Aadhar-OCR-Verification\secret\Swarna Latha.V_Aadhaar_Card.png"

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Adaptive thresholding for better text recognition
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                                   cv2.THRESH_BINARY, 11, 2)
    return thresh

# Apply preprocessing
preprocessed_image = preprocess_image(image_path)

# Perform OCR
results = reader.readtext(preprocessed_image, detail=0)

# Combine OCR output into a single string
extracted_text = " ".join(results)
print("Extracted Text:\n", extracted_text)

# Extract Name (More flexible regex)
name_match = re.search(r"Name[:\s]+([A-Za-z. ]+)(?=\sDOB|\sGender|\sAadhaar)", extracted_text)
name = name_match.group(1).strip() if name_match else "Not Found"

# Extract DOB
dob_match = re.search(r'\b(\d{2}-\d{2}-\d{4})\b', extracted_text)
dob = dob_match.group(1) if dob_match else "Not Found"

# Extract Gender
gender_match = re.search(r'\b(Male|Female)\b', extracted_text, re.IGNORECASE)
gender = gender_match.group(1) if gender_match else "Not Found"

# Extract Aadhaar Number
aadhaar_match = re.search(r'\b\d{12}\b', extracted_text)
aadhaar_number = aadhaar_match.group(0) if aadhaar_match else "Not Found"

# Display Extracted Details
print("\nExtracted Aadhaar Details:")
print(f"Name: {name}")
print(f"DOB: {dob}")
print(f"Gender: {gender}")
print(f"Aadhaar Number: {aadhaar_number}")
