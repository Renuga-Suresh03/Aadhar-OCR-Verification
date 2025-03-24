import os
import base64
from PIL import Image, ImageDraw, ImageFont
import qrcode
import pymongo
from cryptography.fernet import Fernet

# MongoDB Connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["aadhar_db"]
collection = db["aadhar_details"]

# Ensure the generated_aadhars folder exists
output_folder = "generated_aadhars"
os.makedirs(output_folder, exist_ok=True)

# Generate AES encryption key (only generate once and reuse)
key_path = "aes_key.key"

if os.path.exists(key_path):
    with open(key_path, "rb") as key_file:
        key = key_file.read()
else:
    key = Fernet.generate_key()
    with open(key_path, "wb") as key_file:
        key_file.write(key)

cipher = Fernet(key)

def encrypt_data(data):
    """Encrypts data using AES encryption."""
    return cipher.encrypt(data.encode()).decode()

def decrypt_data(encrypted_data):
    """Decrypts data using AES decryption."""
    return cipher.decrypt(encrypted_data.encode()).decode()

def store_aadhaar_in_db(username, dob, gender, aadhaar_number):
    """Stores encrypted Aadhaar details in MongoDB."""
    encrypted_details = {
        "name": encrypt_data(username),
        "dob": encrypt_data(dob),
        "gender": encrypt_data(gender),
        "aadhaar_number": encrypt_data(aadhaar_number)
    }
    
    # Insert encrypted data into MongoDB
    collection.insert_one(encrypted_details)
    print(f"🔒 Aadhaar details for {username} stored securely in MongoDB.")

def create_aadhaar_card(username, dob, gender, aadhaar_number, user_image_path):
    """Generates Aadhaar card, encrypts details, stores in MongoDB, and saves as an image."""
    
    # Store encrypted Aadhaar details in MongoDB
    store_aadhaar_in_db(username, dob, gender, aadhaar_number)
    
    # Aadhaar card dimensions
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
    gov_logo = Image.open("gov_logo.png").convert("RGBA")
    gov_logo = gov_logo.resize((60, 60))
    card.paste(gov_logo, (30, 40), gov_logo)

    # Load and Paste Aadhaar Logo (Top Right)
    aadhaar_logo = Image.open("aadhaar_logo.png").convert("RGBA")
    aadhaar_logo = aadhaar_logo.resize((100, 60))
    card.paste(aadhaar_logo, (780, 40), aadhaar_logo)

    # Load and Paste User Image
    if os.path.exists(user_image_path):
        user_image = Image.open(user_image_path).convert("RGB")
        user_image = user_image.resize((130, 130))
        card.paste(user_image, (50, 150))
    else:
        # Placeholder Profile Picture (Gray silhouette)
        profile_x, profile_y = 50, 150  # Position
        profile_width, profile_height = 130, 130  # Size
        draw.rectangle([(profile_x, profile_y), (profile_x + profile_width, profile_y + profile_height)], fill="lightgray", outline="black", width=3)
        head_x = profile_x + profile_width // 2
        draw.ellipse([(head_x - 25, profile_y + 20), (head_x + 25, profile_y + 70)], fill="gray")  # Circular head
        draw.rectangle([(head_x - 35, profile_y + 70), (head_x + 35, profile_y + 120)], fill="gray")  # Rounded body

    # User Details
    details_x = 200  # X-position for text
    details_y = 150  # Starting Y-position for text
    line_spacing = 40

    user_details = [
        f"Name: {username}",
        f"DOB: {dob}",
        f"Gender: {gender}"
    ]

    for i, detail in enumerate(user_details):
        draw.text((details_x, details_y + i * line_spacing), detail, font=font_bold, fill="black")

    # Generate and Paste QR Code
    qr_data = f"Aadhaar No: {aadhaar_number}\nName: {username}\nDOB: {dob}\nGender: {gender}"
    qr = qrcode.make(qr_data)
    qr = qr.resize((120, 120))  # Resize QR Code
    card.paste(qr, (700, 150))  # Place QR Code at bottom right

    # Aadhaar Number
    draw.line([(50, 320), (850, 320)], fill="red", width=5)  # Red line separator
    draw.text((320, 350), aadhaar_number, font=font_bold, fill="black")

    # Save Aadhaar card
    output_path = os.path.join(output_folder, f"{username}.png")
    card.save(output_path)
    print(f"✅ Aadhaar card saved: {output_path}")

# Example usage
create_aadhaar_card("Renu", "01-01-1990", "Female", "1234 5678 9012", r"C:\Users\renug\Downloads\RENUGA S IMAGE.jpg")
