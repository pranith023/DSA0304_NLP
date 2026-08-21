words = ["govern","government","governance"]

def normalize(word):

    root = "govern"
    affix = ""
    level = ""

    if word == "govern":
        level = "Level 0"

    elif word.endswith("ment"):
        affix = "-ment"
        level = "Level 1"

    elif word.endswith("ance"):
        affix = "-ance"
        level = "Level 1"

    normalized = "govern"

    return [word,root,affix,level,normalized]

print("{:<15}{:<10}{:<10}{:<15}{:<15}".format(
    "Word","Root","Affix","Hierarchy","Normalized"))

for w in words:
    print("{:<15}{:<10}{:<10}{:<15}{:<15}".format(*normalize(w)))