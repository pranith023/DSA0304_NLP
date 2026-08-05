words = ["writes", "writing", "written"]

def fsm(word):
    if word == "written":
        return "write", "Irregular", "write → written"
    elif word.endswith("s"):
        return word[:-1], "Regular", "write → writes"
    elif word.endswith("ing"):
        return word[:-3], "Regular", "write → writing"
    else:
        return word, "Unknown", ""

print("\nQ4 Finite State Morphological Parsing\n")
print("{:<12} {:<10} {:<12} {:<20}".format("Word","Root","Type","State Transition"))

for w in words:
    root, typ, path = fsm(w)
    print("{:<12} {:<10} {:<12} {:<20}".format(w, root, typ, path))