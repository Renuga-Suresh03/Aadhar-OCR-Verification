from PIL import Image, ImageDraw, ImageFont

# Create Smart Ration Card template
width, height = 900, 450
card = Image.new("RGB", (width, height), "#DFF2C2")  # Light green background
draw = ImageDraw.Draw(card)

# Load fonts
try:
    font_bold = ImageFont.truetype("arialbd.ttf", 24)
    font_regular = ImageFont.truetype("arial.ttf", 18)
except:
    font_bold = font_regular = ImageFont.load_default()

# Government Header (Center-Aligned)
header_text = "GOVERNMENT OF TAMILNADU\nCIVIL SUPPLIES & CONSUMER PROTECTION DEPARTMENT"
text_width = draw.textbbox((0, 0), "CIVIL SUPPLIES & CONSUMER PROTECTION DEPARTMENT", font=font_bold)[2]  # Get the widest line
center_x = (width - text_width) // 2  # Calculate center position

draw.text((center_x, 20), header_text, font=font_bold, fill="darkgreen", align="center")

# Tamil Nadu Government Logo (Top Left)
gov_logo = Image.open("gov_tn.png").convert("RGBA")
gov_logo = gov_logo.resize((60, 60))
card.paste(gov_logo, (30, 15), gov_logo)

# Dark Green "FAMILY CARD" Bar
draw.rectangle([(0, 80), (width, 120)], fill="#1C5720")
draw.text((350, 90), "FAMILY CARD", font=font_bold, fill="white")

# Profile Picture Placeholder
profile_x, profile_y = 50, 150
profile_width, profile_height = 130, 130
draw.rectangle([(profile_x, profile_y), (profile_x + profile_width, profile_y + profile_height)], 
               fill="lightgray", outline="black", width=3)
draw.text((profile_x + 40, profile_y + 50), "Photo", font=font_bold, fill="black")

# User Details (Aligned)
text_x = 200
text_y = 150
line_spacing = 40

# Details and values
details = [
    "Family Head Name",
    "Father's/Husband's Name",
    "Date of Birth",
    "Address"
]
values = [
    "XXXX",
    "XXXX",
    "XX-XX-XXXX",
    "XXXX, XXXX, XXXX"
]

# Find the longest text width to align all `:`
max_text_width = max(draw.textbbox((0, 0), text, font=font_regular)[2] for text in details)
colon_x = text_x + max_text_width + 10  # Position for colons
value_x = colon_x + 15  # Position for values

for i, (detail, value) in enumerate(zip(details, values)):
    draw.text((text_x, text_y + i * line_spacing), detail, font=font_regular, fill="black")
    draw.text((colon_x, text_y + i * line_spacing), ":", font=font_regular, fill="black")  # Colons aligned
    draw.text((value_x, text_y + i * line_spacing), value, font=font_regular, fill="black")

# ✅ Separate Boxes for "PHAA" and "Card Number"
box1_x, box1_y = 50, 320  # First box (PHAA)
box2_x, box2_y = 50, 370  # Second box (Card Number)
box_width, box_height = 130, 40

# Box 1 - PHAA
draw.rectangle([(box1_x, box1_y), (box1_x + box_width, box1_y + box_height)], outline="black", width=3)
draw.text((box1_x + 15, box1_y + 10), "XXXX", font=font_bold, fill="black")

# Box 2 - Card Number
draw.rectangle([(box2_x, box2_y), (box2_x + box_width, box2_y + box_height)], outline="black", width=3)
#draw.text((box2_x + 15, box2_y + 10), "XXXXXXXXXXXX", font=font_bold, fill="black")
# Reduce font size dynamically to fit within 130x20 box
card_number = "XXXXXXXXXXXX"
max_width, max_height = 130, 20  # Box dimensions

# Start with a reasonable font size and decrease if needed
font_size = 18
while True:
    temp_font = ImageFont.truetype("arialbd.ttf", font_size)
    text_width, text_height = draw.textbbox((0, 0), card_number, font=temp_font)[2:]
    if text_width <= max_width and text_height <= max_height:
        break  # Font fits, use this size
    font_size -= 1  # Reduce font size if it doesn't fit

# Draw text inside box
draw.text((box2_x + (max_width - text_width) // 2, box2_y + (max_height - text_height) // 2), 
          card_number, font=temp_font, fill="black")
#uuuuu

# Load and Paste Government Logo (Center with Low Opacity)
'''gov_logo_center = gov_logo.copy()
gov_logo_center = gov_logo_center.resize((180, 180))
gov_logo_center.putalpha(70)  # Reduce opacity
card.paste(gov_logo_center, (360, 150), gov_logo_center)'''

# Load and Paste Government Logo (Center with Low Opacity)
gov_logo_center = gov_logo.copy().convert("RGBA")  # Ensure it's in RGBA mode
gov_logo_center = gov_logo_center.resize((180, 180))

# Create a transparent layer
transparent_layer = Image.new("RGBA", card.size, (0, 0, 0, 0))

# Reduce opacity
alpha = gov_logo_center.getchannel("A")
alpha = alpha.point(lambda p: p * 0.6)  # Set opacity to 40% (adjust as needed)
gov_logo_center.putalpha(alpha)

# Paste logo on transparent layer
transparent_layer.paste(gov_logo_center, ((width - 180) // 2, 150), gov_logo_center)

# Merge with card
card = Image.alpha_composite(card.convert("RGBA"), transparent_layer)


# Save and Show
card.save("smart_ration_card.png")
card.show()
