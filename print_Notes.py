#!/usr/bin/env python

import sys
import getpass
import json
import argparse
import os
import re

try:
    import requests
except ImportError:
    print("requests module not found")
    print("Install with pip install requests")
    print("For JLT: dans C:\\python34\scripts\pip")
    sys.exit()
try:
    from bs4 import BeautifulSoup
except ImportError:
    print("beautifulsoup module not found")
    print("install with pip install beautifulsoup4")
    print("For JLT: dans C:\\python34\scripts\pip")
    sys.exit()

from config import menu_config,  read_config
import constants as c
from mail import send_email

def getNotes(previousConnection):
        """Return a soup with content of page with marks in"""
        try:
                newConnection = requests.get('https://fee.heig-vd.ch/etudiants/bulletinNotes.php', cookies=previousConnection.cookies)
        except requests.exceptions.RequestException:
                print ("Connection to server lost")
                sys.exit()
        soup = BeautifulSoup(newConnection.text)
        return soup


def printNotes(soup,  consoleprint=True):
    """Returns a dict with all marks based on input soup oboject"""
    dictNotes = {}
    moduleName = ' '
    for unite in soup.find_all(class_ = 'nomUnite'):
        if moduleName != re.sub(r'\(.+\)', '', unite.find_previous('h3').get_text()).strip():
            moduleName = re.sub(r'\(.+\)', '', unite.find_previous('h3').get_text()).strip()
            if consoleprint:
                print (moduleName)
            dictNotes[moduleName] = {}
        if consoleprint:
            print ("\t", unite.get_text())
        dictNotes[moduleName][unite.get_text()] = []
        notesList = [ ]
        for note in unite.parent.find_all(class_ = 'noteTest'):
            if note.get_text() == u'\xa0':
                notesList.append(' ')
            else:
                notesList.append(note.get_text())
        if consoleprint:
            print ("\t\tNotes :\t\t", notesList[:-3])
            print ("\t\tExamen :\t", notesList[-2:-1])
            print ("\t\tMoyenne :\t", notesList[-1:])
        dictNotes[moduleName][unite.get_text()] = {}
        dictNotes[moduleName][unite.get_text()]['year'] = notesList[:-3]
        dictNotes[moduleName][unite.get_text()]['exam'] = notesList[-2]
        dictNotes[moduleName][unite.get_text()]['average'] = notesList[-1]
    return dictNotes


def login(username, password):
    """Connects to intranet and return connection if connection was succefull"""
    try:
        siteConnection = requests.post('https://fee.heig-vd.ch/etudiants/index.php',
                                                            data={'username': username, 'password': password})
    except requests.exceptions.RequestException:
        print ("Connection to server not possible")
        sys.exit()
    if siteConnection.status_code == 200:
        soup = BeautifulSoup(siteConnection.text)
        if soup.find('a', {'href': '/etudiants/index.php?delog=true'}) != None :
            return siteConnection
        else :
            return False

def check_auto():
    """checks available marks base on config"""
    config = read_config()
    siteConnection = login(config[c.FEE_USER],  config[c.FEE_PW])
    message = ''
    if siteConnection != False:
        notes = getNotes(siteConnection)
        notes = printNotes(notes,  consoleprint=False)
        if os.path.isfile('notes.txt'):
            with open('notes.txt',  'r') as file:
                oldnotes = json.load(file)
            if oldnotes == notes:
                message = 'pas de nouvelles notes'
            else:
                for module in notes:
                    if module in oldnotes:
                        if notes[module] != oldnotes[module]:
                            message = message + 'Dans le module {}\n'.format(module)
                            for unit in notes[module]:
                                if unit in oldnotes[module]:
                                    if notes[module][unit] != oldnotes[module][unit]:
                                        message = message + '\t dans l\'unité {}\n'.format(unit)
                                        if notes[module][unit]['year'] != oldnotes[module][unit]['year']:
                                            for item in range(len(notes[module][unit]['year'])):
                                                if notes[module][unit]['year'][item] != oldnotes[module][unit]['year'][item]:
                                                    message = message + '\t\tnouvelle note: {}\n'.format(str(notes[module][unit]['year'][item]))
                                        if notes[module][unit]['exam'] != oldnotes[module][unit]['exam']:
                                            message = message + '\t\tnouvelle note examen: {}\n'.format(notes[module][unit]['exam'])
                                else:
                                    message = message + 'nouvelle unité: {}\n'.format(unit)
                                    message = message + 'notes : {}\n'.format(str(notes[module][unit]['year']))
                                    message = message + 'examen : {}\n'.format(str(notes[module][unit]['exam']))
                                    message = message + 'moyenne : {}\n'.format(str(notes[module][unit]['average']))
                    else:
                        message = 'nouveau module {}\n'.format(module)
                        for unit in notes[module]:
                            message = message + 'nouvelle unité: {}\n'.format(unit)
                            message = message + '\tnotes : {}\n'.format(str(notes[module][unit]['year']))
                            message = message + '\texamen : {}\n'.format(notes[module][unit]['exam'])
                            message = message + '\tmoyenne : {}\n'.format(notes[module][unit]['average'])
                if config[c.GMAIL_USE]:
                    send_email(config[c.GMAIL_EMAIL],  config[c.GMAIL_PW],  config[c.GMAIL_EMAIL],  [config[c.GMAIL_EMAIL]],  'nouvelle notes fee',  message)
        else:
            message = 'pas de fichier pour comparer'
        with open('notes.txt',  'w') as file:
            json.dump(notes,  file)
    else:
        message = 'Connection failed'
    print(message)


def main():
    """main function that checks cmd arguments and launches required actions"""
    parser = argparse.ArgumentParser(description='impression des notes sur fee.heig-vd.ch')
    parser.add_argument('-u', '--username',
                                        help='nom d\'utilisateur pour fee.heig-vd.ch')
    parser.add_argument('-p', '--password',
                                        help='mot de passe pour fee.heig-d.ch')
    parser.add_argument('-c', '--configuration', action='store_true',
                                        help='lancement du menu de configuration')
    parser.add_argument('-a', '--auto', action='store_true',
                                        help='vérification automatique selon configuration')
    args = parser.parse_args()

    if args.configuration:
        print('lancement du menu de config')
        menu_config()
        sys.exit()

    if args.auto:
        print('lancement de la vérification automatique')
        check_auto()
        sys.exit()

    if args.username:
        userName = args.username
    else:
        userName = input('Nom d\'utilisateur fee: ')
    if args.password:
        userPassword = args.password
    else:
        userPassword = getpass.getpass('Mot de passe fee: ')

    siteConnection = login(userName, userPassword)

    if siteConnection != False:
        print("Login OK")
        notes = getNotes(siteConnection)
        printNotes(notes)            
    else:
        print ("Error during login")

if __name__ == '__main__':
        main()
