words = ["unhappy", "happiness", "happily"]

def parse(word):
    prefix = ""
    suffix = ""
    
    if word.startswith("un"):
        prefix = "un"
        word = word[2:]
    
    if word.endswith("ness"):
        suffix = "ness"
        base = word[:-4]
    elif word.endswith("ly"):
        suffix = "ly"
        base = word[:-2]
    else:
        base = word

    return prefix, base, suffix, "Derivational"

print("\nQ2 Morphological Parsing\n")
print("{:<12} {:<10} {:<10} {:<10} {:<15}".format("Word","Prefix","Base","Suffix","Type"))

for w in words:
    p, b, s, t = parse(w)
    print("{:<12} {:<10} {:<10} {:<10} {:<15}".format(w, p, b, s, t))