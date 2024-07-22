from cryptography.fernet import Fernet
import base64

# Global variables for save the key
key = Fernet.generate_key()
cipher_suite: Fernet = Fernet(key)

# Encode the data
def encoder(telegram_id):
    # Encode the data
    data = str(telegram_id).encode()
    cipher_text = cipher_suite.encrypt(data)
    encoded_cipher_text = base64.urlsafe_b64encode(cipher_text).decode('utf-8')
    print(encoded_cipher_text)

    return encoded_cipher_text


# Decode the encryption
def decoder(encoded_cipher_text):
    loaded_key = load_key()
    cipher_suite = Fernet(loaded_key)
    cipher_text = base64.urlsafe_b64decode(encoded_cipher_text.encode('utf-8'))

    try:
        plain_text = cipher_suite.decrypt(cipher_text)
        return plain_text.decode()

    except Exception as e:
        print(f"Decryption failed: {e}")
        return None


def load_key():
    with open("secret.key", "rb") as key_file:
        return key_file.read()


# Re-upload key and decode the encryption
loaded_key = load_key()
cipher_suite = Fernet(loaded_key)
