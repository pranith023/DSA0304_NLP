words = ["disagree", "agreement", "agreeable"]

def parse(word):

    prefix = ""
    suffix = ""
    root = "agree"

    if word.startswith("dis"):
        prefix = "dis-"
        category = "Derivational"
        meaning = "Negation"

    elif word.endswith("ment"):
        suffix = "-ment"
        category = "Derivational"
        meaning = "Action/Result (Noun)"

    elif word.endswith("able"):
        suffix = "-able"
        category = "Derivational"
        meaning = "Capable of"

    else:
        category = "Base"
        meaning = "Agreement"

    normalized = "agree"

    return [word,prefix,root,suffix,category,meaning,normalized]

print("{:<15}{:<8}{:<10}{:<10}{:<15}{:<20}{:<12}".format(
    "Word","Prefix","Root","Suffix","Category","Meaning","Normalized"))

for w in words:
    print("{:<15}{:<8}{:<10}{:<10}{:<15}{:<20}{:<12}".format(*parse(w)))