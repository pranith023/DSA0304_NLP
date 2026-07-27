import re

products = [
    "Laptop",
    "Laptop Bag",
    "Mouse",
    "Wireless Mouse",
    "Keyboard",
    "Gaming Laptop",
    "Phone",
    "Smart Phone",
    "Phone Case"
]

keyword = input("Enter keyword: ")

print("\nExact Match")
exact = [p for p in products if re.fullmatch(keyword, p, re.IGNORECASE)]
print(exact)

print("\nPrefix Match")
prefix = [p for p in products if re.match(keyword, p, re.IGNORECASE)]
print(prefix)

print("\nSuffix Match")
suffix = [p for p in products if re.search(keyword + r"$", p, re.IGNORECASE)]
print(suffix)

print("\nPartial Match")
partial = [p for p in products if re.search(keyword, p, re.IGNORECASE)]
print(partial)

print("\nCase-Insensitive Match")
case = partial
print(case)

print("\n------ Report ------")
print("Exact:", len(exact))
print("Prefix:", len(prefix))
print("Suffix:", len(suffix))
print("Partial:", len(partial))
