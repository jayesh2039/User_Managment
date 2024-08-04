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
