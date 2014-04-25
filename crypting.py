import string
import base64
import random
try:
    from simplecrypt import encrypt
    from simplecrypt import decrypt
except ImportError:
    print("module simplecrypt not found")


def generate_key(keylength=64):
    """Generates a random key (string) used for encryption"""
    chars = string.ascii_uppercase + string.digits
    key = ''
    for i in range(keylength):
        key = key + random.choice(chars)
    return key

def encrypting(data, key):
    """Returns a crypted string of data using key as encryption key"""
    bin_crypt = encrypt(key, data)
    base_crypt = base64.b64encode(bin_crypt)
    return base_crypt.decode(encoding='UTF-8')

def decrypting(data, key):
    """Returns a decrypted data(string) using key as decryption key"""
    bin_crypt = base64.b64decode(data)
    return decrypt(key, bin_crypt).decode(encoding='UTF-8')
