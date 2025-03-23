from PIL import Image, ImageDraw, ImageFont
import qrcode

# Create Aadhaar card template
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

# **Add "भारत सरकार | Government of India" Inside the Stripes**
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

# **Profile Picture Placeholder with Gray Silhouette**
profile_x, profile_y = 50, 150  # Position
profile_width, profile_height = 130, 130  # Size

# Draw Gray Background for Profile Picture
draw.rectangle([(profile_x, profile_y), (profile_x + profile_width, profile_y + profile_height)], fill="lightgray", outline="black", width=3)

# Draw Head
head_x = profile_x + profile_width // 2  # Center X
draw.ellipse([(head_x - 25, profile_y + 20), (head_x + 25, profile_y + 70)], fill="gray")  # Circular head

# Draw Body
draw.rectangle([(head_x - 35, profile_y + 70), (head_x + 35, profile_y + 120)], fill="gray")  # Rounded body


# User Details
details_x = 200  # X-position for text
details_y = 150  # Starting Y-position for text
line_spacing = 40

user_details = [
    "Name: XXXXXXXXXX",
    "DOB: XXXXXXX",
    "Gender: XXXX"
]

for i, detail in enumerate(user_details):
    draw.text((details_x, details_y + i * line_spacing), detail, font=font_bold, fill="black")

# **Generate and Paste QR Code**
qr_data = "Aadhaar No: XXXX XXXX XXXX\nName: John Doe\nDOB: 01-01-1990\nGender: Male"
qr = qrcode.make(qr_data)
qr = qr.resize((120, 120))  # Resize QR Code

# Place QR Code at bottom right
card.paste(qr, (700, 150))



# Aadhaar Number
draw.line([(50, 320), (850, 320)], fill="red", width=5)  # Red line separator
aadhaar_number = "XXXX XXXX XXXX"
draw.text((320, 350), aadhaar_number, font=font_bold, fill="black")

# Save and Show
card.save("aadhaar_template.png")
card.show()


#task assigned to anova

#must create a template image with same template as of createaadhar.py file
#must store in templates folder as atemplate.png/jpg
