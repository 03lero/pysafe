import os
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
    global maindir 
    global saltloc
    global entrydir

    maindir = os.path.join(os.path.expanduser('~'), '.pysafe')
    saltloc = os.path.join(maindir, '.salt')
    entrydir = os.path.join(maindir, 'entries')
    
    if os.path.isdir(maindir) == False:
        os.mkdir(maindir)

    if os.path.isdir(entrydir) == False:
        os.mkdir(entrydir)

    if os.path.exists(saltloc) == False:
        gen()
  
    ferinit()
    ui()

def new():
    fname = input("Type a filename for the new entry.\n> ")
    filename = os.path.join(entrydir, fname)
    os.system("nano %s" % filename)
    with open(filename, "rb") as file:
        file_data = file.read()
    encrypted_data = fkey.encrypt(file_data)
    with open(filename, "wb") as file:
        file.write(encrypted_data)
    print("\nSuccess. New file encrypted!")
    input("Type any key to proceed...")

def decrypt():
    print("Saved entries:\n", '\n'.join(os.listdir(entrydir)))
    fname = input("Enter a filename to decrypt\n> ")
    filename = os.path.join(entrydir, fname)
    with open(filename, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = fkey.decrypt(encrypted_data)
    with open(filename, "wb") as file:
        file.write(decrypted_data)
    print("\nSuccess!")
    input("Type any key to proceed...")

def encrypt():
    while True:
        filename = input("Enter a filename to encrypt\n- Original file will be deleted\n- Include extension if applicable\n- Specify path if not in this directory\n> ")
        if os.path.exists(filename) != True:
            print("File does not exist")
            continue
        break

    with open(filename, "rb") as file:
        file_data = file.read()
    writename = os.path.join(entrydir, filename)
    encrypted_data = fkey.encrypt(file_data)

    with open(writename, "wb") as file:
        file.write(encrypted_data)
    print("\nSuccess. Data encrypted!")
    input("Type any key to proceed...")

def read():
    fname = input("Enter a filename to read\n> ")
    filename = os.path.join(entrydir, fname)
    with open(filename, "rb") as file:
        encrypted_data = file.read()
    decrypted_data = fkey.decrypt(encrypted_data)
    print(decrypted_data.decode("utf-8"))
    input("Type any key to proceed...")

def lister():
    print("\n", os.listdir(entrydir), "\n")
    input("Type any key to proceed...")

def gen():
    while True:
        entry = input("Create Password.\n- If you lose this passphrase, you will not be able to access your entries again\n- 32 character maximum, 10 character minimum\n- Must include letters and numbers\n> ")
        if len(entry) < 12:
            print("Password is too short. 12 characters minimum.")
            continue
        checkpass(entry)
        if alpha == False or numeric == False:
            print("Must include letters AND numbers.")
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
    char = open(saltloc, 'w')
    char.write(salt)
    
    print("Password generated.\nNever touch salt file or you will be locked out of your entries.\nProceeding...")

def checkpass(str): 
    global alpha
    global numeric

    alpha = False
    numeric = False 

    for i in str: 
        if i.isalpha(): 
            alpha = True

        if i.isdigit(): 
            numeric = True

    return alpha and numeric 

def ferinit():
    global fkey
    char = open(saltloc, 'r')
    salt = char.read()

    while True:
        login = input("Enter your password.\n> ")
        checkpass(login)
        if len(login) < 12 or alpha == False or numeric == False :
            print("Invalid entry.")
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
