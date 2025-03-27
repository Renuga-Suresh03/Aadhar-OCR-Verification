import pymongo
from cryptography.fernet import Fernet

# Load the encryption key
with open("aes_key.key", "rb") as key_file:
    SECRET_KEY = key_file.read()

fernet = Fernet(SECRET_KEY)

# Database Connection
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["aadhar_db"]
collection = db["smart_card_details"]  # New collection for Smart Cards

# Smart Card details
smart_card_data = {
    "smart_card_number": fernet.encrypt("587654321012".encode()).decode(),
    "family_members": [
        fernet.encrypt("1234 5678 9012".encode()).decode(),
        fernet.encrypt("2345 6789 0123".encode()).decode(),
        fernet.encrypt("3456 7890 1234".encode()).decode()
    ]
}



# Insert encrypted Smart Card details into MongoDB
collection.insert_one(smart_card_data)

print("✅ Encrypted Smart Card details stored in MongoDB.")
