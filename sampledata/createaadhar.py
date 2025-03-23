
from PIL import Image, ImageDraw, ImageFont
import qrcode
from pymongo import MongoClient
import random

# MongoDB Connection
client = MongoClient("mongodb://localhost:27017/")
db = client["aadhar_db"]
collection = db["aadhar_details"]

# Function to generate a random Aadhaar Number
def generate_aadhar_number():
    return " ".join(str(random.randint(1000, 9999)) for _ in range(3))

# User Details
user_details = {
    "name": "John Doe",
    "dob": "01-01-1990",
    "gender": "Male",
    "aadhar_number": generate_aadhar_number()
}

# Save to Database
collection.insert_one(user_details)

# Create Aadhaar Card Template
width, height = 900, 450
card = Image.new("RGB", (width, height), "white")
draw = ImageDraw.Draw(card)

# Load Fonts
try:
    font_bold = ImageFont.truetype("arialbd.ttf", 24)
    font_regular = ImageFont.truetype("arial.ttf", 18)
except:
    font_bold = font_regular = ImageFont.load_default()

# Draw Rounded Border
border_color = (150, 150, 150)
draw.rounded_rectangle([(5, 5), (width - 5, height - 5)], radius=30, outline=border_color, width=5)

# Draw Tricolor Stripes
draw.rectangle([(120, 40), (780, 70)], fill="orange")  # Orange stripe
draw.rectangle([(120, 75), (780, 105)], fill="green")  # Green stripe

# Add "Government of India" text
gov_text = "Government of India"
text_width = draw.textbbox((0, 0), gov_text, font=font_bold)[2]
text_x = (width - text_width) // 2
draw.text((text_x, 45), gov_text, font=font_bold, fill="white")

# Load and Paste Government Logo (Top Left)
gov_logo = Image.open("gov_logo.png").convert("RGBA").resize((60, 60))
card.paste(gov_logo, (30, 40), gov_logo)

# Load and Paste Aadhaar Logo (Top Right)
aadhaar_logo = Image.open("aadhaar_logo.png").convert("RGBA").resize((100, 60))
card.paste(aadhaar_logo, (780, 40), aadhaar_logo)

# Profile Picture Placeholder
profile_x, profile_y = 50, 150
profile_width, profile_height = 130, 130
draw.rectangle([(profile_x, profile_y), (profile_x + profile_width, profile_y + profile_height)], fill="lightgray", outline="black", width=3)

# Draw Profile Icon
head_x = profile_x + profile_width // 2
draw.ellipse([(head_x - 25, profile_y + 20), (head_x + 25, profile_y + 70)], fill="gray")
draw.rectangle([(head_x - 35, profile_y + 70), (head_x + 35, profile_y + 120)], fill="gray")

# User Details
details_x = 200
details_y = 150
line_spacing = 40
details_list = [
    f"Name: {user_details['name']}",
    f"DOB: {user_details['dob']}",
    f"Gender: {user_details['gender']}",
]

for i, detail in enumerate(details_list):
    draw.text((details_x, details_y + i * line_spacing), detail, font=font_bold, fill="black")

# Generate and Paste QR Code
qr_data = f"Aadhaar No: {user_details['aadhar_number']}\nName: {user_details['name']}\nDOB: {user_details['dob']}\nGender: {user_details['gender']}"
qr = qrcode.make(qr_data).resize((120, 120))
card.paste(qr, (700, 150))

# Draw Red Line Separator
draw.line([(50, 320), (850, 320)], fill="red", width=5)

# Aadhaar Number
draw.text((320, 350), user_details["aadhar_number"], font=font_bold, fill="black")

# Save Aadhaar Template
card.save("aadhaar_template.png")
card.show()


# Connect to MongoDB (Local or Atlas)
client = MongoClient("mongodb://localhost:27017/")  # Change for MongoDB Atlas
db = client["aadhar_db"]
collection = db["aadhar_details"]

# Aadhaar User Data
user_data = {
    "name": "John Doe",
    "dob": "01-01-1990",
    "gender": "Male",
    "aadhar_number": "1234 5678 9012"
}

# Insert into MongoDB
collection.insert_one(user_data)
print("Aadhaar details saved!")

# Retrieve and display all records
for record in collection.find():
    print(record)


#task assigned to anova

#this script must generate a aadhar card
#the generated card must replicate the original aadhar to atleast 80%
#only 1 side
#details
#name.....name:renuga
#dob
#gender
#aadhar number
#image
#qr(generate code in such a way that if i scan qr i must be able to see the aadhar details in text like format)
#add aadhar logos and indian government logos also

#the following details alone  must be stored in db once we create a new aadhar(db name: aadhar_db, collection name: aadhar_details)

#name
#dob
#gender
#aadhar number

#must encrypt and store...use aes
