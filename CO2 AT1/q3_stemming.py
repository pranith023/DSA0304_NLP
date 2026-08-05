words = ["played", "player", "playing"]

def stem(word):
    if word.endswith("ed"):
        return word[:-2], "ed", "Inflectional"
    elif word.endswith("ing"):
        return word[:-3], "ing", "Inflectional"
    elif word.endswith("er"):
        return word[:-2], "er", "Derivational"
    else:
        return word, "", "Unknown"

print("\nQ3 Stemming\n")
print("{:<12} {:<10} {:<10} {:<15}".format("Word","Stem","Removed","Type"))

for w in words:
    stem_word, affix, typ = stem(w)
    print("{:<12} {:<10} {:<10} {:<15}".format(w, stem_word, affix, typ))