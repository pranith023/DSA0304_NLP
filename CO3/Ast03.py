import re

# ------------------ Email Validation ------------------
def validate_email(email):
    pattern = r'^[A-Za-z][A-Za-z0-9._-]*@[A-Za-z]+\.(com|org|edu|net|in)$'
    if re.fullmatch(pattern, email):
        return "Valid Email"
    else:
        return "Invalid Email"

# ------------------ Password Validation ------------------
def validate_password(password):
    pattern = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@#$%&!]).{8,}$'
    if re.fullmatch(pattern, password):
        return "Strong Password"
    else:
        return "Weak Password"

# ------------------ Mobile Number Validation ------------------
def validate_mobile(mobile):
    pattern = r'^[6-9]\d{9}$'
    if re.fullmatch(pattern, mobile):
        return "Valid Mobile Number"
    else:
        return "Invalid Mobile Number"

# ------------------ User Input ------------------
email = input("Enter Email Address: ")
password = input("Enter Password: ")
mobile = input("Enter Mobile Number: ")

# ------------------ Output ------------------
print("\nValidation Results")
print("------------------")
print(validate_email(email))
print(validate_password(password))
print(validate_mobile(mobile))