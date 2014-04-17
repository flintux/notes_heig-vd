#!/usr/bin/env python

import sys
import re
import getpass
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

# Get notes page in a soup format
def getNotes(previousConnection):
        try:
                newConnection = requests.get('https://fee.heig-vd.ch/etudiants/bulletinNotes.php', cookies=previousConnection.cookies)
        except requests.exceptions.RequestException:
                print ("Connection to server lost")
                sys.exit()
        soup = BeautifulSoup(newConnection.text)
        return soup

#print notes from soup
def printNotes(soup):
        moduleName = ' '
        for unite in soup.find_all(class_ = 'nomUnite'):
                if moduleName != unite.find_previous('h3').get_text().strip():
                        moduleName = unite.find_previous('h3').get_text().strip()
                        print (moduleName)
                print ("\t", unite.get_text())
                notesList = [ ]
                for note in unite.parent.find_all(class_ = 'noteTest'):
                        #print (note.get_text())
                        if note.get_text() == u'\xa0':
                                notesList.append(' ')
                                #print('Empty note')
                        else:
                                notesList.append(note.get_text())
                print ("\t\tNotes :\t\t", notesList[:-3])
                print ("\t\tExamen :\t", notesList[-2:-1])
                print ("\t\tMoyenne :\t", notesList[-1:])

#check login
def login(username, password):
        try:
                siteConnection = requests.post('https://fee.heig-vd.ch/etudiants/index.php', data={'username': username, 'password': password})
        except requests.exceptions.RequestException:
                print ("Connection to server not possible")
                sys.exit()
        if siteConnection.status_code == 200:
                soup = BeautifulSoup(siteConnection.text)
                if soup.find('a', {'href': '/etudiants/index.php?delog=true'}) != None :
                        return siteConnection
                else :
                        return False


#MAIN starts here

if len(sys.argv) == 3:
        userName = sys.argv[1]
        userPassword = sys.argv[2]
else:
        userName = input("Username: ")
        userPassword = getpass.getpass("Password: ")

siteConnection = login(userName, userPassword)

if siteConnection != False:
        print("Login OK")
        notes = getNotes(siteConnection)
        printNotes(notes)
else:
        print ("Error during login")

