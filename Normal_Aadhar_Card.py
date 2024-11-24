import random

unique_id = []
name = []
number = []
DOB = []
gender = []
address = []
aadhaar = []  # List to store all Aadhaar numbers
users = {}
credentials = {}  # Store combinations of username and password

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

    user_data = {
        "aadhaar": generate_aadhaar(),
        "name": input("Enter Name: "),
        "number": int(input("Enter Number: ")),
        "DOB": input("Enter Date Of Birth (DD/MM/YYYY): "),
        "gender": input("Enter Gender: "),
        "address": input("Enter Address: "),
        "credentials": []
    }
    
    print("**** Register ****")
    while True:
        username = input("Create New Username: ")
        password = input("Create New Password: ")

        if (username, password) in credentials:
            print("Username and Password combination already exists. Please try a different one.")
        else:
            break
    
    user_data['credentials'] = [username, password]
    users[id] = user_data
    credentials[(username, password)] = id
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
            print(f"Password: {user_data['credentials'][1]}")
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
            update_field = input("What do you want to update (Name, Number, DOB, Gender, Address, Username, Password)? ").lower()
            if update_field in user_data:
                user_data[update_field] = input(f"Enter new {update_field.capitalize()}: ")
                users[update_id] = user_data
                print(f"User {update_field} updated successfully!")
            elif update_field == "username":
                while True:
                    new_username = input("Enter New Username: ")
                    new_password = users[update_id]['credentials'][1]  # Use the existing password
                    if (new_username, new_password) in credentials:
                        print("Username and Password combination already exists. Please try a different one.")
                    else:
                        old_username, old_password = users[update_id]['credentials']
                        credentials.pop((old_username, old_password))
                        credentials[(new_username, new_password)] = update_id
                        users[update_id]['credentials'][0] = new_username
                        print("Username updated successfully!")
                        break
            elif update_field == "password":
                while True:
                    new_password = input("Enter New Password: ")
                    new_username = users[update_id]['credentials'][0]  # Use the existing username
                    if (new_username, new_password) in credentials:
                        print("Username and Password combination already exists. Please try a different one.")
                    else:
                        old_username, old_password = users[update_id]['credentials']
                        credentials.pop((old_username, old_password))
                        credentials[(new_username, new_password)] = update_id
                        users[update_id]['credentials'][1] = new_password
                        print("Password updated successfully!")
                        break
            else:
                print("Invalid field. Please enter (Name, Number, DOB, Gender, Address, Username, Password).")
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
        else:
            print("User not found.")

def admin_mode():
    while True:
        print("-----------------------")
        print("Admin Menu:")
        print("1). Add User")
        print("2). Show User Details")
        print("3). Update User Details")
        print("4). Delete User")
        print("5). Exit Admin Mode")
        print("-----------------------")
        admin_choice = int(input("Enter Your Choice (1-5): "))
        if admin_choice == 1:
            add_user()
        elif admin_choice == 2:
            show_user_details()
        elif admin_choice == 3:
            update_user_details()
        elif admin_choice == 4:
            delete_user()
        elif admin_choice == 5:
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

def user_mode():
    while True:
        print("-----------------------")
        print("User Menu:")
        print("1). Show Identity")
        print("2). Exit User Mode")
        print("-----------------------")
        user_choice = int(input("Enter Your Choice (1 or 2): "))
        if user_choice == 1:
            selected_id = int(input("Enter Your ID to show your details (or 0 to exit): "))
            if selected_id == 0:
                break
            if selected_id in users:
                print("***** Login *****")
                username = input("Enter Username: ")
                password = input("Enter Password: ")
                if users[selected_id]['credentials'] == [username, password]:
                    user_data = users[selected_id]
                    print("-----------------------------")
                    for key, value in user_data.items():
                        if key != "credentials":
                            print(f"{key.capitalize()}: {value}")
                    print("-----------------------------")
                else:
                    print("Wrong Username or Password.")
            else:
                print("ID does not exist.")
        elif user_choice == 2:
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")

# Display the welcome message at the start
print("Welcome to 'AadhaarAdmin'")

while True:
    print("-------------")
    print("1). Admin")
    print("2). User")
    print("3). Exit")
    print("-------------")
    choice = int(input("Enter Your Choice (1, 2, or 3): "))
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
        print("Exiting the program.")
        break
    else:
        print("Invalid choice. Please enter 1, 2, or 3.")
