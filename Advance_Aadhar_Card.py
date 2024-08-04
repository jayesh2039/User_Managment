import random
import re
import json
import datetime
from cryptography.fernet import Fernet

# Define global variables
unique_id = []
aadhaar = []
users = {}
credentials = {}
feedback = {}

# Generate and manage encryption key
key = Fernet.generate_key()
cipher_suite = Fernet(key)

# Utility functions
def is_strong_password(password):
    return (len(password) >= 8 and re.search(r'[A-Za-z]', password) and 
            re.search(r'\d', password) and re.search(r'[!@#$%^&*(),.?"\'{}|<>]', password))

def encrypt_password(password):
    return cipher_suite.encrypt(password.encode())

def decrypt_password(encrypted_password):
    return cipher_suite.decrypt(encrypted_password).decode()

def send_verification_email(email, verification_code):
    import smtplib
    from email.mime.text import MIMEText

    msg = MIMEText(f"Your verification code is: {verification_code}")
    msg['Subject'] = 'Email Verification'
    msg['From'] = 'admin@example.com'
    msg['To'] = email

    with smtplib.SMTP('smtp.example.com', 587) as server:
        server.starttls()
        server.login('admin@example.com', 'password')
        server.sendmail(msg['From'], [msg['To']], msg.as_string())

def log_activity(user_id, action):
    with open('activity_log.txt', 'a') as file:
        file.write(f"{datetime.datetime.now()}: User {user_id} performed {action}\n")

def backup_data():
    try:
        backup_data = {
            'users': {
                user_id: {
                    **user_data,
                    'credentials': [user_data['credentials'][0], decrypt_password(user_data['credentials'][1])]
                }
                for user_id, user_data in users.items()
            },
            'credentials': [(username, decrypt_password(encrypted_password))
                            for (username, encrypted_password), user_id in credentials.items()],
        }
        
        with open('backup.json', 'w') as file:
            json.dump(backup_data, file, indent=4)
        print("Backup completed successfully.")
    except Exception as e:
        print(f"An error occurred during backup: {e}")

import re

def is_valid_phone_number(number):
    # Check if the number is exactly 10 digits
    return re.fullmatch(r'\d{10}', number) is not None



def generate_aadhaar():
    while True:
        aadhaar_number = ''.join([str(random.randint(0, 9)) for _ in range(12)])
        if aadhaar_number not in aadhaar:
            aadhaar.append(aadhaar_number)
            return aadhaar_number

def add_user():
    id = int(input("Enter Unique_Id: "))
    if id in users:
        print("Entered Id already exists in the database. Please enter a unique ID.")
        return

    while True:
        number = input("Enter Number (10 digits): ")
        if is_valid_phone_number(number):
            break
        else:
            print("Invalid number. Please enter exactly 10 digits.")

    user_data = {
        "aadhaar": generate_aadhaar(),
        "name": input("Enter Name: "),
        "number": number,
        "DOB": input("Enter Date Of Birth (DD/MM/YYYY): "),
        "gender": input("Enter Gender: "),
        "address": input("Enter Address: "),
        "email": input("Enter Email: "),
        "role": "user",  # Default role to "user"
        "credentials": []
    }

    while True:
        username = input("Create New Username: ")
        password = input("Create New Password: ")

        if not is_strong_password(password):
            print("Password is too weak. Please use a stronger password.")
            continue

        if (username, encrypt_password(password)) in credentials:
            print("Username and Password combination already exists. Please try a different one.")
        else:
            break

    user_data['credentials'] = [username, encrypt_password(password)]
    users[id] = user_data
    credentials[(username, encrypt_password(password))] = id
    print(f"User added successfully! Aadhaar Number: {user_data['aadhaar']}")


def show_user_details():
    if not users:
        print("No users in the database.")
        return

    for id in users:
        print(f"User ID: {id}")

    while True:
        search_id = input("Enter ID to show user details (or 'exit' to exit): ")
        if search_id.lower() == 'exit':
            break
        try:
            search_id = int(search_id)
        except ValueError:
            print("Invalid input. Please enter a valid ID or 'exit' to exit.")
            continue

        if search_id in users:
            user_data = users[search_id]
            print("-----------------------------")
            for key, value in user_data.items():
                if key != "credentials":
                    print(f"{key.capitalize()}: {value}")
            print(f"Username: {user_data['credentials'][0]}")
            print(f"Password: {decrypt_password(user_data['credentials'][1])}")
            print("-----------------------------")
        else:
            print("No user found. Please try again.")

def update_user_details():
    if not users:
        print("No users in the database.")
        return

    for id in users:
        print(f"User ID: {id}")

    while True:
        update_id = int(input("Enter User ID to update details (or 0 to exit): "))
        if update_id == 0:
            break

        if update_id in users:
            user_data = users[update_id]
            update_field = input("What do you want to update (Name, Number, DOB, Gender, Address, Email, Role, Username, Password)? ").lower()
            if update_field in user_data:
                user_data[update_field] = input(f"Enter new {update_field.capitalize()}: ")
                users[update_id] = user_data
                print(f"User {update_field} updated successfully!")
                log_activity(update_id, f"Updated {update_field}")
            elif update_field == "username":
                while True:
                    new_username = input("Enter New Username: ")
                    new_password = decrypt_password(user_data['credentials'][1])  # Use the existing password
                    if (new_username, encrypt_password(new_password)) in credentials:
                        print("Username and Password combination already exists. Please try a different one.")
                    else:
                        old_username, old_password = user_data['credentials']
                        credentials.pop((old_username, old_password))
                        credentials[(new_username, encrypt_password(new_password))] = update_id
                        users[update_id]['credentials'][0] = new_username
                        print("Username updated successfully!")
                        break
            elif update_field == "password":
                while True:
                    new_password = input("Enter New Password: ")
                    if not is_strong_password(new_password):
                        print("Password is too weak. Please use a stronger password.")
                        continue
                    new_username = user_data['credentials'][0]  # Use the existing username
                    if (new_username, encrypt_password(new_password)) in credentials:
                        print("Username and Password combination already exists. Please try a different one.")
                    else:
                        old_username, old_password = user_data['credentials']
                        credentials.pop((old_username, old_password))
                        credentials[(new_username, encrypt_password(new_password))] = update_id
                        users[update_id]['credentials'][1] = encrypt_password(new_password)
                        print("Password updated successfully!")
                        break
            else:
                print("Invalid field. Please enter (Name, Number, DOB, Gender, Address, Email, Role, Username, Password).")
        else:
            print("No user found.")

def delete_user():
    if not users:
        print("No users in the database.")
        return

    for id in users:
        print(f"User ID: {id}")

    while True:
        delete_id = int(input("Enter User ID to delete (or 0 to exit): "))
        if delete_id == 0:
            break

        if delete_id in users:
            aadhaar_number = users[delete_id]['aadhaar']
            aadhaar.remove(aadhaar_number)
            username, password = users[delete_id]['credentials']
            del users[delete_id]
            del credentials[(username, password)]
            print(f"User with ID {delete_id} has been deleted.")
            log_activity(delete_id, "Deleted user")
        else:
            print("User not found.")

def admin_mode():
    while True:
        print("\nAdmin Menu:")
        print("1. Add User")
        print("2. Show User Details")
        print("3. Update User Details")
        print("4. Delete User")
        print("5. Backup Data")
        print("6. Exit Admin Mode")
        admin_choice = int(input("Enter Your Choice (1-6): "))
        if admin_choice == 1:
            add_user()
        elif admin_choice == 2:
            show_user_details()
        elif admin_choice == 3:
            update_user_details()
        elif admin_choice == 4:
            delete_user()
        elif admin_choice == 5:
            backup_data()
        elif admin_choice == 6:
            print("Exiting Admin Mode...")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 6.")

def user_mode():
    while True:
        print("\nUser Menu:")
        print("1. Show Identity")
        print("2. Exit User Mode")
        user_choice = int(input("Enter Your Choice (1-2): "))
        if user_choice == 1:
            selected_id = int(input("Enter Your ID to show your details (or 0 to exit): "))
            if selected_id == 0:
                break
            if selected_id in users:
                print("***** Login *****")
                username = input("Enter Username: ")
                password = input("Enter Password: ")
                encrypted_password = encrypt_password(password)
                stored_username, stored_encrypted_password = users[selected_id]['credentials']
                
                # Decrypt the stored password to compare
                try:
                    decrypted_stored_password = decrypt_password(stored_encrypted_password)
                except Exception as e:
                    print(f"Error decrypting stored password: {e}")
                    decrypted_stored_password = None
                
                # Check if the provided username and encrypted password match the stored values
                if username == stored_username and decrypted_stored_password == password:
                    user_data = users[selected_id]
                    print("-----------------------------")
                    for key, value in user_data.items():
                        if key != "credentials":
                            print(f"{key.capitalize()}: {value}")
                    print("-----------------------------")
                    log_activity(selected_id, "Viewed details")
                else:
                    print("Wrong Username or Password.")
            else:
                print("ID does not exist.")
        elif user_choice == 2:
            print("Exiting User Mode...")
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")


def main():
    while True:
        print("\nMain Menu:")
        print("1. Admin Login")
        print("2. User Login")
        print("3. Exit")
        choice = int(input("Enter Your Choice (1-3): "))
        if choice == 1:
            print("***** Admin Login *****")
            admin_user = input("Enter Username: ")
            admin_pass = input("Enter Password: ")
            if admin_user == "admin" and admin_pass == "admin":
                admin_mode()
            else:
                print("Wrong Username or Password.")
        elif choice == 2:
            user_mode()
        elif choice == 3:
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
