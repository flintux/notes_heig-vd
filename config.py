#Module part of heig-vd-notes
#
#Provides methods for handling configuration

import json
import os
import sys
import getpass

try:
    from crypting import generate_key, encrypting, decrypting
except ImportError:
    print("module crypting not found")
    sys.exit()

import constants as c
def read_config(config_file=c.CONFIG_FILE):
    """Returns a dict with configuration based on input file"""
    if os.path.isfile(config_file):
        with open(config_file, 'r') as file:
            config = json.load(file)
        if c.CRYPT_KEY in config:
            key = config[c.CRYPT_KEY]
            if c.FEE_PW in config:
                config[c.FEE_PW] = decrypting(config[c.FEE_PW], key)
            if c.GMAIL_EMAIL in config:
                config[c.GMAIL_PW] = decrypting(config[c.GMAIL_PW], key)
        return config
    else:
        print('config file does not exist')
        return None

def save_config(config, config_file=c.CONFIG_FILE):
    """Saves the config dict to a file using json format"""
    if c.CRYPT_KEY in config:
        key = config[c.CRYPT_KEY]
    else:
        key = generate_key()
        config[c.CRYPT_KEY] = key
    if c.FEE_PW in config:
        config[c.FEE_PW] = encrypting(config[c.FEE_PW], key)
    if c.GMAIL_PW in config:
        config[c.GMAIL_PW] = encrypting(config[c.GMAIL_PW], key)
    with open(config_file, 'w') as file:
        json.dump(config, file)
    return None
    
def menu_config():
    """prints out the menu for user configuration"""
    config = {}
    config[c.FEE_USER] = input('Nom d\'utilisateur fee: ')
    config[c.FEE_PW] = getpass.getpass('Mot de passe fee: ')
    mail_config = input('Voulez-vous configurer les emails gmail?')
    if mail_config.upper() == 'O' or mail_config.upper() == 'OUI':
        config[c.GMAIL_USE] = True
        config[c.GMAIL_EMAIL] = input('Adresse email gmail:')
        config[c.GMAIL_PW] = getpass.getpass('Mot de pass gmail')
    else:
        config[c.GMAIL_USE] = False
    save_config(config,  c.CONFIG_FILE)
    print('Sauvegarde configuration effectuée')
    return True
