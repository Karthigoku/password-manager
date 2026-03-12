import json
import os
from cryptography.fernet import Fernet
import base64
import hashlib

DATA_FILE = "passwords.json"

def generate_key(master_password):
    key = hashlib.sha256(master_password.encode()).digest()
    return base64.urlsafe_b64encode(key)

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as file:
        return json.load(file)

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file)

def add_password(cipher):
    site = input("Website: ")
    username = input("Username: ")
    password = input("Password: ")

    encrypted = cipher.encrypt(password.encode()).decode()

    data = load_data()
    data[site] = {"username": username, "password": encrypted}

    save_data(data)
    print("Password saved!")

def get_password(cipher):
    site = input("Enter website: ")
    data = load_data()

    if site in data:
        encrypted = data[site]["password"]
        decrypted = cipher.decrypt(encrypted.encode()).decode()

        print("Username:", data[site]["username"])
        print("Password:", decrypted)
    else:
        print("No entry found.")

def delete_password():
    site = input("Enter website to delete: ")
    data = load_data()

    if site in data:
        del data[site]
        save_data(data)
        print("Entry deleted.")
    else:
        print("Website not found.")

def search_password():
    keyword = input("Search site: ")
    data = load_data()

    for site in data:
        if keyword.lower() in site.lower():
            print("Found:", site)

def main():
    master = input("Enter master password: ")
    key = generate_key(master)
    cipher = Fernet(key)

    while True:
        print("\nPassword Manager")
        print("1 Add Password")
        print("2 Retrieve Password")
        print("3 Delete Password")
        print("4 Search")
        print("5 Exit")

        choice = input("Choose: ")

        if choice == "1":
            add_password(cipher)
        elif choice == "2":
            get_password(cipher)
        elif choice == "3":
            delete_password()
        elif choice == "4":
            search_password()
        elif choice == "5":
            break
        else:
            print("Invalid choice")

main()