# Finite-State Machine for Morphological Parsing
# Generates plural forms of English nouns

def pluralize(noun):
    # Nouns ending with 'y' preceded by a consonant
    if noun.endswith("y") and noun[-2].lower() not in "aeiou":
        return noun[:-1] + "ies"

    # Nouns ending with s, x, z, ch, sh
    elif noun.endswith(("s", "x", "z", "ch", "sh")):
        return noun + "es"

    # Default rule
    else:
        return noun + "s"


# Test nouns
nouns = ["cat", "dog", "baby", "box", "bus", "brush", "church"]

print("Finite-State Machine for Morphological Parsing")
print("----------------------------------------------")

for noun in nouns:
    print(f"Singular: {noun} --> Plural: {pluralize(noun)}")