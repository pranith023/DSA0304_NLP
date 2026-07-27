import re

resume = """
Name: Rahul Sharma
Email: rahul123@gmail.com
Mobile: 9876543210
Skills: Python, Java, SQL, Machine Learning, NLP
Experience: 3 years
"""

name = re.search(r"Name:\s*(.*)", resume)
email = re.findall(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", resume)
mobile = re.findall(r"\b[6-9]\d{9}\b", resume)

skills = ["Python", "Java", "SQL", "Machine Learning", "NLP"]
found_skills = [skill for skill in skills if re.search(skill, resume, re.IGNORECASE)]

exp = re.search(r"(\d+)\s+years", resume)
experience = int(exp.group(1)) if exp else 0

print("------ Candidate Summary ------")
print("Name:", name.group(1))
print("Email:", email)
print("Mobile:", mobile)
print("Skills:", found_skills)
print("Experience:", experience, "Years")

if experience >= 2 and "Python" in found_skills:
    print("Status: Eligible for Shortlisting")
else:
    print("Status: Not Eligible")
