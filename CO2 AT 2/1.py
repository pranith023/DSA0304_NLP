# Rule-Based Morphological Processing

words = ["analyzing", "analysis", "analytical"]

def analyze_word(word):
    root = ""
    affix = ""
    transformation = ""

    if word.endswith("ing"):
        root = word[:-3]
        if root.endswith("z"):
            root = root[:-1] + "ze"
        affix = "-ing"
        transformation = "Inflectional"

    elif word.endswith("sis"):
        root = "analyze"
        affix = "-sis"
        transformation = "Derivational"

    elif word.endswith("ical"):
        root = "analyze"
        affix = "-ical"
        transformation = "Derivational"

    else:
        root = word
        transformation = "Base"

    normalized = "analyze"

    return [word, root, affix, transformation, normalized]

print("{:<15}{:<12}{:<10}{:<15}{:<12}".format(
    "Word","Root","Affix","Type","Normalized"))

for w in words:
    result = analyze_word(w)
    print("{:<15}{:<12}{:<10}{:<15}{:<12}".format(*result))