from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

import hashlib

from .conf import ENCRYPTION_KEY

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def encrypt_data(plaintext):
    key_bytes = bytes(ENCRYPTION_KEY, "utf-8")
    aes_cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(bytearray(16)), backend=default_backend())
    aes_encryptor = aes_cipher.encryptor()
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    plaintext_bytes = bytes(plaintext, "utf-8")
    padded_bytes = padder.update(plaintext_bytes) + padder.finalize()
    ciphertext_bytes = aes_encryptor.update(padded_bytes) + aes_encryptor.finalize()
    return ciphertext_bytes.hex()


def decrypt_data(ciphertext):
    key_bytes = bytes(ENCRYPTION_KEY, "utf-8")
    aes_cipher = Cipher(algorithms.AES(key_bytes), modes.CBC(bytearray(16)), backend=default_backend())
    aes_decryptor = aes_cipher.decryptor()
    unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
    ciphertext_bytes = bytes.fromhex(ciphertext)
    padded_bytes = aes_decryptor.update(ciphertext_bytes) + aes_decryptor.finalize()
    plaintext_bytes = unpadder.update(padded_bytes) + unpadder.finalize()
    return plaintext_bytes.decode("utf-8")


# For data stored in dictionaries
def encrypt_personal_data(personal_data):
    encrypted_personal_data = {}
    for key, value in personal_data.items():
        encrypted_personal_data[key] = encrypt_data(value)
    return encrypted_personal_data


def decrypt_personal_data(encrypted_personal_data):
    decrypted_personal_data = {}
    for key, value in encrypted_personal_data.items():
        decrypted_personal_data[key] = decrypt_data(value)
    return decrypted_personal_data