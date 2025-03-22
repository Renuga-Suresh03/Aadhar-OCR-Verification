from PIL import Image, ImageDraw, ImageFont
import qrcode
import pymongo
import os

# MongoDB Connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["aadhar_db"]
collection = db["aadhar_details"]

def generate_qr(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill="black", back_color="white")
    return img

def save_to_db(name, dob, gender, aadhar_number):
    record = {
        "name": name,
        "dob": dob,
        "gender": gender,
        "aadhar_number": aadhar_number
    }
    collection.insert_one(record)

def create_template():
    width, height = 800, 400
    template = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(template)
    
    # Fonts (Ensure required font files are available)
    font_large = ImageFont.truetype("arial.ttf", 40)
    font_small = ImageFont.truetype("arial.ttf", 30)
    
    # Placeholder Aadhaar & Government Logos
    aadhar_logo = Image.new("RGB", (100, 100), "gray")
    govt_logo = Image.new("RGB", (100, 100), "gray")
    template.paste(aadhar_logo, (20, 20))
    template.paste(govt_logo, (680, 20))
    
    # Placeholder User Image
    user_img = Image.new("RGB", (100, 100), "gray")
    template.paste(user_img, (650, 150))
    
    # Placeholder Text
    draw.text((150, 50), "Government of India", fill="black", font=font_large)
    draw.text((50, 150), "Name: __________", fill="black", font=font_small)
    draw.text((50, 200), "DOB: __________", fill="black", font=font_small)
    draw.text((50, 250), "Gender: __________", fill="black", font=font_small)
    draw.text((50, 300), "Aadhaar No: __________", fill="black", font=font_small)
    
    # Placeholder QR Code
    qr_img = Image.new("RGB", (100, 100), "gray")
    template.paste(qr_img, (650, 270))
    
    # Ensure templates directory exists
    os.makedirs("templates", exist_ok=True)
    template_path = "templates/atemplate.png"
    template.save(template_path)
    print(f"Template saved at {template_path}")

def generate_aadhar_card(name, dob, gender, aadhar_number, image_path):
    width, height = 800, 400
    card = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(card)
    
    # Fonts (Ensure required font files are available)
    font_large = ImageFont.truetype("arial.ttf", 40)
    font_small = ImageFont.truetype("arial.ttf", 30)
    
    # Aadhaar & Government Logos (Placeholder paths)
    aadhar_logo = Image.open("aadhar_logo.png").resize((100, 100))
    govt_logo = Image.open("govt_logo.png").resize((100, 100))
    card.paste(aadhar_logo, (20, 20))
    card.paste(govt_logo, (680, 20))
    
    # User Image
    user_img = Image.open(image_path).resize((100, 100))
    card.paste(user_img, (650, 150))
    
    # Details Placement
    draw.text((150, 50), "Government of India", fill="black", font=font_large)
    draw.text((50, 150), f"Name: {name}", fill="black", font=font_small)
    draw.text((50, 200), f"DOB: {dob}", fill="black", font=font_small)
    draw.text((50, 250), f"Gender: {gender}", fill="black", font=font_small)
    draw.text((50, 300), f"Aadhaar No: {aadhar_number}", fill="black", font=font_small)
    
    # Generate QR Code
    qr_data = f"Name: {name}\nDOB: {dob}\nGender: {gender}\nAadhaar No: {aadhar_number}"
    qr_img = generate_qr(qr_data).resize((100, 100))
    card.paste(qr_img, (650, 270))
    
    # Save Card
    card.save("aadhar_card.png")
    save_to_db(name, dob, gender, aadhar_number)
    print("Aadhar Card Generated & Details Stored in DB")

# Generate template
template_created = create_template()
#task assigned to anova

#must create a template image with same template as of createaadhar.py file
#must store in templates folder as atemplate.png/jpg
