import random

# Simple probability dictionary
pos_dict = {
    "book": ["NN", "VB"],
    "play": ["VB", "NN"],
    "run": ["VB", "NN"],
    "dog": ["NN"],
    "quickly": ["RB"]
}

sentence = ["book", "dog", "run", "quickly"]

print("Stochastic POS Tagging:")

for word in sentence:
    if word in pos_dict:
        tag = random.choice(pos_dict[word])
    else:
        tag = "NN"

    print(word, "->", tag)