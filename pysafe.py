import os
import os.path
from os import path
from cryptography.fernet import Fernet
import string
import random
import base64
from cursesmenu import *
from cursesmenu.items import *

def ui():
    menu = CursesMenu("PySafe", "Main Menu")

    f1 = FunctionItem("Create a new entry", new)
    f2 = FunctionItem("Read an existing entry", read)
    f3 = FunctionItem("Decrypt an existing entry", decrypt)
    f4 = FunctionItem("Encrypt a decrypted/plaintext entry", encrypt)
    f5 = FunctionItem("List saved entries", lister)
    f6 = FunctionItem("Generate new password (you will lose access to all old entries)", gen)
 
    menu.append_item(f1)    
    menu.append_item(f2)
    menu.append_item(f3)
    menu.append_item(f4)
    menu.append_item(f5)
    menu.append_item(f6)

    menu.show()

def main():
    if path.exists(".salt") == False:
        gen()
    if os.path.isdir(".entries") == False:
        os.mkdir(".entries")
    ferinit()
    ui()

def new():
    fname = input("Type a filename for the new entry.\n> ")
    filename = '.entries/' + fname
    os.system("nano %s" % filename)
    with open(filename, "rb") as file:
        file_data = file.read()
    encrypted_data = fkey.encrypt(file_data)
    with open(filename, "wb") as file:
        file.write(encrypted_data)
    print("\nSuccess. New file encrypted!")
    input("Type any key to proceed...")

def decrypt():
    fname = input("Enter a filename to decrypt\n> ")
    filename = '.entries/' + fname
    with open(filename, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = fkey.decrypt(encrypted_data)
    with open(filename, "wb") as file:
        file.write(decrypted_data)
    print("\nSuccess!")
    input("Type any key to proceed...")

def encrypt():
    fname = input("Enter a filename to encrypt\n> ")
    filename = '.entries/' + fname
    with open(filename, "rb") as file:
        file_data = file.read()
    encrypted_data = fkey.encrypt(file_data)
    with open(filename, "wb") as file:
        file.write(encrypted_data)
    print("\nSuccess. Data encrypted!")
    input("Type any key to proceed...")

def read():
    fname = input("Enter a filename to read\n> ")
    filename = '.entries/' + fname
    with open(filename, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = fkey.decrypt(encrypted_data)
    print(decrypted_data.decode("utf-8"))
    input("Type any key to proceed...")

def lister():
    print("\n", os.listdir(".entries/"), "\n")
    input("Type any key to proceed...")

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
