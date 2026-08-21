import re

words = ["running", "played", "beautiful", "quickly", "books"]

print("Rule-Based POS Tags:")

for word in words:
    if re.search(r'ing$', word):
        tag = "VBG"     # Verb (Gerund)

    elif re.search(r'ed$', word):
        tag = "VBD"     # Verb (Past)

    elif re.search(r'ly$', word):
        tag = "RB"      # Adverb

    elif re.search(r'ful$', word):
        tag = "JJ"      # Adjective

    elif re.search(r's$', word):
        tag = "NNS"     # Plural Noun

    else:
        tag = "NN"

    print(word, "->", tag)