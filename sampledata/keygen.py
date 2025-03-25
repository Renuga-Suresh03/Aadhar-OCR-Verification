from cryptography.fernet import Fernet

# Generate a key
key = Fernet.generate_key()

# Save the key to a file
with open("aes_key.key", "wb") as key_file:
    key_file.write(key)

print("✅ Encryption key generated and saved as 'aes_key.key'.")
