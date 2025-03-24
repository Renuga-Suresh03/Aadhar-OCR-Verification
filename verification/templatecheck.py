#assigned to renu

#check template correctness
#if correct proceed to textextract
#else del file from uploads and display as fake aadhar detected


import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

UPLOAD_FOLDER = r"C:\Projects\Aadhar-OCR-Verification\uploads"

def generate_reference_aadhar():
    """Generates a blank Aadhaar card template dynamically (without saving)."""

    width, height = 900, 450
    card = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(card)

    # Load fonts
    try:
        font_bold = ImageFont.truetype("arialbd.ttf", 24)
        font_regular = ImageFont.truetype("arial.ttf", 18)
    except:
        font_bold = font_regular = ImageFont.load_default()

    # Draw rounded border
    border_color = (150, 150, 150)
    draw.rounded_rectangle([(5, 5), (width - 5, height - 5)], radius=30, outline=border_color, width=5)

    # Draw tricolor stripes
    draw.rectangle([(120, 40), (780, 70)], fill="orange")  # Orange stripe
    draw.rectangle([(120, 75), (780, 105)], fill="green")  # Green stripe

    # Add "Government of India" text inside the stripe
    gov_text = "Government of India"
    text_width = draw.textbbox((0, 0), gov_text, font=font_bold)[2]
    text_x = (width - text_width) // 2  # Center align
    draw.text((text_x, 45), gov_text, font=font_bold, fill="white")  # Place in the Orange stripe

    # Load and Paste Government Logo (Top Left)
    if os.path.exists("gov_logo.png"):
        gov_logo = Image.open("gov_logo.png").convert("RGBA").resize((60, 60))
        card.paste(gov_logo, (30, 40), gov_logo)

    # Load and Paste Aadhaar Logo (Top Right)
    if os.path.exists("aadhaar_logo.png"):
        aadhaar_logo = Image.open("aadhaar_logo.png").convert("RGBA").resize((100, 60))
        card.paste(aadhaar_logo, (780, 40), aadhaar_logo)

    # Dummy User Image Placeholder
    profile_x, profile_y = 50, 150  # Position
    profile_width, profile_height = 130, 130  # Size
    draw.rectangle([(profile_x, profile_y), (profile_x + profile_width, profile_y + profile_height)], 
                   fill="lightgray", outline="black", width=3)

    # User Details (Dummy Text)
    details_x, details_y, line_spacing = 200, 150, 40
    user_details = ["Name: XXXXX", "DOB: XX-XX-XXXX", "Gender: X"]
    for i, detail in enumerate(user_details):
        draw.text((details_x, details_y + i * line_spacing), detail, font=font_bold, fill="black")

    # Red line separator
    draw.line([(50, 320), (850, 320)], fill="red", width=5)  

    # Convert to OpenCV format for comparison
    reference_template = np.array(card.convert("L"))  # Convert to grayscale numpy array
    return reference_template

def load_image(image_path):
    """Loads an uploaded Aadhaar image as a grayscale numpy array."""
    return cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

def compare_images(uploaded_img_path, threshold=80):
    """
    Compares the uploaded Aadhaar image with the dynamically generated template.
    Returns True if the similarity is above the threshold, otherwise False.
    """
    uploaded_img = load_image(uploaded_img_path)

    # Generate dynamic Aadhaar template
    reference_template = generate_reference_aadhar()

    # Resize uploaded image to match reference dimensions
    uploaded_img = cv2.resize(uploaded_img, (900, 450))

    # Compute Structural Similarity Index (SSI)
    difference = cv2.absdiff(uploaded_img, reference_template)
    similarity = 100 - np.mean(difference)  # Convert difference to similarity percentage

    print(f"🔍 Template Matching Similarity: {similarity:.2f}%")

    return similarity >= threshold

def check_template_and_proceed(filename):
    """Checks if the Aadhaar template matches. If yes, proceed to OCR; else, delete file."""
    uploaded_file_path = os.path.join(UPLOAD_FOLDER, filename)

    if not os.path.exists(uploaded_file_path):
        print(f"❌ File {filename} not found in {UPLOAD_FOLDER}.")
        return

    # Check template similarity
    if compare_images(uploaded_file_path):
        print("✅ Aadhaar template is valid. Proceeding to text extraction...")
        # Call text extraction function here (if implemented)
    else:
        print("🚨 Fake Aadhaar detected! Deleting file...")
        os.remove(uploaded_file_path)

# Example usage
check_template_and_proceed("renu.png")  # Change filename accordingly
