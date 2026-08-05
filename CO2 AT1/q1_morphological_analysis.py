words = ["connected", "connecting", "connection"]

def analyze(word):
    if word.endswith("ed"):
        root = word[:-2]
        return root, "ed", "Inflectional"
    elif word.endswith("ing"):
        root = word[:-3]
        return root, "ing", "Inflectional"
    elif word.endswith("ion"):
        root = word[:-3] + "t"   # fix: connection → connect
        return root, "ion", "Derivational"
    else:
        return word, "", "Unknown"

print("\nQ1 Morphological Analysis\n")
print("{:<12} {:<10} {:<10} {:<15} {:<10}".format("Word","Root","Suffix","Type","Normalized"))

for w in words:
    root, suffix, typ = analyze(w)
    print("{:<12} {:<10} {:<10} {:<15} {:<10}".format(w, root, suffix, typ, root))