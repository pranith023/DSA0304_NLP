words = ["activate","activation","reactivation"]

def parse(word):

    prefix = ""
    suffix = ""
    root = "activate"

    if word == "activate":
        sequence = "Base Verb"

    elif word == "activation":
        suffix = "-ion"
        sequence = "activate + ion"

    elif word == "reactivation":
        prefix = "re-"
        suffix = "-ion"
        sequence = "re + activate + ion"

    normalized = "activate"

    return [word,prefix,root,suffix,sequence,normalized]

print("{:<18}{:<8}{:<12}{:<10}{:<25}{:<12}".format(
    "Word","Prefix","Root","Suffix","Sequence","Normalized"))

for w in words:
    print("{:<18}{:<8}{:<12}{:<10}{:<25}{:<12}".format(*parse(w)))