import os
import os.path
from os import path
from cryptography.fernet import Fernet
import string
import random
import base64

def main():
    if path.exists(".salt") == False:
        gen()
    if os.path.isdir(".entries") == False:
        os.mkdir(".entries")
    ferinit()
    action()

def action():
    while True:
        action = input("\nType 'new' to write a new encrypted entry.\nType 'read' to read an encrypted entry.\nType 'decrypt' to decrypt an old entry.\nType 'encrypt' to encrypt a decrypted/plaintext entry.\nType 'list' to see all saved entries.\n> ")
        if action.lower() == 'new':
            tnew = input("Type a filename for the new entry.\n> ")
            new(tnew)
        elif action.lower() == 'decrypt':
            old = input("Enter a filename to decrypt\n> ")
            decrypt(old)
        elif action.lower() == 'encrypt':
           existing = input("Enter a filename to encrypt.\n> ")
           encrypt(existing)
        elif action.lower() == 'read':
            readf = input("Enter a filename to read.\n> ")
            print("\n")
            read(readf)
        elif action.lower() == 'list':
            print("\n", os.listdir(".entries/", "\n"))
            continue
        else:
            print("Invalid entry.")
            continue

def new(fname):
    filename = '.entries/' + fname
    os.system("nano %s" % filename)
    with open(filename, "rb") as file:
        file_data = file.read()
    encrypted_data = fkey.encrypt(file_data)
    with open(filename, "wb") as file:
        file.write(encrypted_data)
    print("\nSuccess. New file encrypted!")

def decrypt(fname):
    filename = '.entries/' + fname
    with open(filename, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = fkey.decrypt(encrypted_data)
    with open(filename, "wb") as file:
        file.write(decrypted_data)
    print("\nSuccess!")

def encrypt(fname):
    filename = '.entries/' + fname
    with open(filename, "rb") as file:
        file_data = file.read()
    encrypted_data = fkey.encrypt(file_data)
    with open(filename, "wb") as file:
        file.write(encrypted_data)
    print("\nSuccess. Data encrypted!")

def read(fname):
    filename = '.entries/' + fname
    with open(filename, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = fkey.decrypt(encrypted_data)
    print(decrypted_data.decode("utf-8"))
    
def gen():
    while True:
        entry = input("Create Password + Key\nIf you lose this passphrase, you will not be able to access your entries again.\n32 chars max, 10 char minimum\n> ")
        if len(entry) < 10:
            print("Password is too short. 10 characters minimum.")
            continue

        verify = input("Verify passphrase.\n> ")

        if entry != verify:
            print("Passwords did not match.")
            continue

        break

    curlen = len(entry)
    tarlen = 32 - curlen
    
    letters = string.ascii_lowercase
    salt = ''.join(random.choice(letters) for i in range(tarlen))    
    char = open('.salt', 'w')
    char.write(salt)
    
    print("Password generated.\nNever touch salt file or you will be locked out of your entries.\nProceeding...")

def ferinit():
    global fkey
    char = open('.salt', 'r')
    salt = char.read()
 
    while True:
        login = input("Enter created password. If this is incorrect, you will not be able to decrypt your entries.\n> ")
        
        if len(login) < 10:
            print("Password is too short. 10 characters minimum.")
            continue
       
        verify = input("Verify passphrase.\n> ")
        
        if login != verify:
            print("Passwords did not match.")
            continue

        pkey = login + salt
        
        if len(pkey) != 32:
            print("Detected incorrect passphrase length.")
            continue        

        break
        
    bytekey = bytes(pkey, 'utf-8')
    b64key = base64.urlsafe_b64encode(bytekey)      
    fkey = Fernet(b64key)
main()
