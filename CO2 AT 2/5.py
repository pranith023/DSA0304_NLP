words = ["create","creates","creating"]

def normalize(word):

    suffix = ""
    category = ""
    root = "create"

    if word == "create":
        category = "Base Form"

    elif word.endswith("s"):
        suffix = "-s"
        category = "Third Person Singular"

    elif word.endswith("ing"):
        suffix = "-ing"
        category = "Present Participle"

    normalized = "create"

    return [word,suffix,category,root,normalized]

print("{:<15}{:<10}{:<25}{:<12}{:<12}".format(
    "Word","Suffix","Category","Root","Normalized"))

for w in words:
    print("{:<15}{:<10}{:<25}{:<12}{:<12}".format(*normalize(w)))