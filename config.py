#Module part of heig-vd-notes
#
#Provides methods for handling configuration

import json
import os
import sys

try:
    from crypting import generate_key, encrypting, decrypting
except ImportError:
    print("module crypting not found")
    sys.exit()


CONFIG_FILE = 'heig-vd.config'
CRYPT_KEY = 'key'
FEE_USER = 'fee_username'
FEE_PW = 'fee_password'
GMAIL_EMAIL = 'gmail_email'
GMAIL_PW = 'gmail_password'

def read_config(config_file=CONFIG_FILE):
    """Returns a dict with configuration based on input file"""
    if os.path.isfile(config_file):
        with open(config_file, 'r') as file:
            config = json.load(file)
        if CRYPT_KEY in config:
            key = config[CRYPT_KEY]
            if FEE_PW in config:
                config[FEE_PW] = decrypting(config[FEE_PW], key)
            if GMAIL_EMAIL in config:
                config[GMAIL_PW] = decrypting(config[GMAIL_PW], key)
        return config
    else:
        print('config file does not exist')
        return None

def save_config(config, config_file=CONFIG_FILE):
    """Saves the config dict to a file using json format"""
    if CRYPT_KEY in config:
        key = config[CRYPT_KEY]
    else:
        key = generate_key()
        config[CRYPT_KEY] = key
    if FEE_PW in config:
        config[FEE_PW] = encrypting(config[FEE_PW], key)
    if GMAIL_PW in config:
        config[GMAIL_PW] = encrypting(config[GMAIL_PW], key)
    with open(config_file, 'w') as file:
        json.dump(config, file)
    return None
    
