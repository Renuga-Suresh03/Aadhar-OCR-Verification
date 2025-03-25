import os

key_path = "aes_key.key"

if os.path.exists(key_path):
    with open(key_path, "rb") as key_file:
        stored_key = key_file.read()
        print("🔑 Loaded Key:", stored_key)  # Debugging line
else:
    print("❌ Key file not found!")
