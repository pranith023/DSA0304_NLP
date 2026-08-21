# Initial tagging
sentence = ["I", "can", "play", "football"]

tags = [
    ("I", "PRP"),
    ("can", "NN"),      # Initially tagged as Noun
    ("play", "VB"),
    ("football", "NN")
]

print("Before Transformation:")
print(tags)

# Transformation Rule:
# If the word is "can", change NN -> MD (Modal Verb)

new_tags = []

for word, tag in tags:
    if word.lower() == "can" and tag == "NN":
        tag = "MD"

    new_tags.append((word, tag))

print("\nAfter Transformation:")
print(new_tags)