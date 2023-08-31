from cryptography.fernet import Fernet

'''
From: https://stackoverflow.com/a/66250021
'''


def generate_key():
    """
    Generates a key and save it into a file
    """
    key: bytes = Fernet.generate_key()
    with open("secret.key", "wb") as key_file:
        key_file.write(key)

def load_key() -> bytes:
    """
    Load the previously generated key
    """
    return open("secret.key", "rb").read()

def encrypt_message(message: str) -> bytes:
    """
    Encrypts a message
    """
    key: bytes = load_key()
    encoded_message = message.encode()
    f = Fernet(key)
    return f.encrypt(encoded_message)

def decrypt_message(encrypted_message: bytes) -> str:
    """
    Decrypts an encrypted message
    """
    key: bytes = load_key()
    f = Fernet(key)
    return f.decrypt(encrypted_message)