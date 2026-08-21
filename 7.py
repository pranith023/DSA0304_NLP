# Simple POS Dictionary

pos_dict = {
    "The": "DT",
    "cat": "NN",
    "is": "VBZ",
    "sitting": "VBG",
    "on": "IN",
    "the": "DT",
    "mat": "NN"
}

sentence = "The cat is sitting on the mat"

words = sentence.split()

print("POS Tags:")

for word in words:
    tag = pos_dict.get(word, "Unknown")
    print(word, "->", tag)