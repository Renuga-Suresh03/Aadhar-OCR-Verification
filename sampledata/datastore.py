import pymongo
from cryptography.fernet import Fernet

# Load the encryption key
with open("aes_key.key", "rb") as key_file:
    SECRET_KEY = key_file.read()

fernet = Fernet(SECRET_KEY)

# Database Connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["aadhar_db"]
collection = db["aadhar_details"]

# Aadhaar details (Modify as needed)
aadhaar_data = {
    "name": fernet.encrypt("Swarna".encode()).decode(),
    "dob": fernet.encrypt("01-01-1999".encode()).decode(),
    "gender": fernet.encrypt("Female".encode()).decode(),
    "aadhaar_number": fernet.encrypt("1434 5678 9012".encode()).decode()  # Ensure spaces match OCR output
}

# Clear previous records (Optional: To avoid duplicates)
collection.delete_many({})

# Insert encrypted data into MongoDB
collection.insert_one(aadhaar_data)

print("✅ Encrypted Aadhaar details stored in MongoDB.")
