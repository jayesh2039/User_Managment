# User_Managment_System_Script
This Python script is designed to manage user data, including registration, updating user details, viewing user information, and deleting users. It includes functionalities for both administrators and regular users, along with encrypted password storage, logging, and data backup.

# Features
1. Strong Password Validation :
The script includes a function is_strong_password that checks if a password is at least 8 characters long and contains at least one letter, one number, and one special character.

2. Password Encryption :
Passwords are encrypted using the cryptography library to ensure they are securely stored. Functions encrypt_password and decrypt_password handle encryption and decryption, respectively.

3. Email Verification :
The send_verification_email function simulates sending a verification email to users during the registration process.

4. Activity Logging :
The log_activity function logs user activities to a file named activity_log.txt.

5. Data Backup :
The backup_data function saves user data to a file named backup.json, with passwords decrypted for readability in the backup file.

6. Aadhaar Number Generation :
A unique 12-digit Aadhaar number is generated for each user using the generate_aadhaar function.

7. User Registration and Management :
The script provides functions to add, update, delete, and display user details. These functions are accessible through an admin mode.

8. Admin and User Modes :
Admin Mode: Allows administrators to add, view, update, and delete user details, as well as backup data.

User Mode: Allows users to view their own details after logging in with their credentials.

# How to Use

--> Prerequisites : 
Install the cryptography library: `pip install cryptography`

--> Running the Script :
Save the script to a file named `user_management.py` and run it using Python

`python user_management.py`

# Main Menu
After running the script, you will see the main menu:

`Main Menu:`

`1. Admin Login`

`2. User Login`

`3. Exit`

`Enter Your Choice (1-3):`

# Admin Login
Use the default admin credentials:

Username: `admin`

Password: `admin`

After logging in, you can access the following admin menu:

`Admin Menu:`

`1. Add User`

`2. Show User Details`

`3. Update User Details`

`4. Delete User`

`5. Backup Data`

`6. Exit Admin Mode`

# Adding a User
Follow the prompts to add a new user. A unique Aadhaar number will be generated for each user.

# Viewing User Details
Select a user ID to view their details.

# Updating User Details
Select a user ID and the field to update (Name, Number, DOB, Gender, Address, Email, Role, Username, Password).

# Deleting a User
Select a user ID to delete the user from the system.

# Data Backup
Creates a backup of user data in a file named backup.json.

# User Login
Users can log in with their ID, username, and password to view their details.

# User Menu:

`1. Show Identity :` Allows users to view their own details after logging in with their credentials

`3. Exit User Mode :` Exit The User Mode And Go To Main Manu.

