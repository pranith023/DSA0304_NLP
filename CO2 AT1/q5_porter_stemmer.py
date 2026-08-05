from nltk.stem import PorterStemmer

ps = PorterStemmer()
words = ["relational", "relation", "relate"]

print("\nQ5 Porter Stemming\n")
print("{:<12} {:<10}".format("Word","Stem"))

for w in words:
    print("{:<12} {:<10}".format(w, ps.stem(w)))