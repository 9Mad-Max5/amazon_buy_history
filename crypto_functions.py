import pickle
from cryptography.fernet import Fernet
import hashlib
import base64

# Funktion zur Erstellung eines Schlüssels aus dem Passwort
def generate_key(password):
    key = hashlib.sha256(password.encode()).digest()
    key_base64 = base64.urlsafe_b64encode(key)
    return key_base64

# Funktion zum Verschlüsseln der Daten
def encrypt_data(data, password):
    fernet = Fernet(generate_key(password))
    encrypted_data = fernet.encrypt(pickle.dumps(data))
    return encrypted_data

# Funktion zum Entschlüsseln der Daten
def decrypt_data(encrypted_data, password):
    fernet = Fernet(generate_key(password))
    decrypted_data = pickle.loads(fernet.decrypt(encrypted_data))
    return decrypted_data