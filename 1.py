import re

# Sample text
text = "My email is student123@gmail.com and my phone number is 9876543210."

# 1. Match - checks only at the beginning of the string
pattern1 = r"My"

match = re.match(pattern1, text)

if match:
    print("Match found:", match.group())
else:
    print("No match found.")

# 2. Search - finds the first occurrence anywhere in the string
pattern2 = r"\d{10}"  # 10-digit phone number

search = re.search(pattern2, text)

if search:
    print("Phone number found:", search.group())
else:
    print("Phone number not found.")

# 3. Search for an email address
email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

email = re.search(email_pattern, text)

if email:
    print("Email found:", email.group())
else:
    print("Email not found.")