from collections import defaultdict
import random

text = "I love natural language processing and I love Python"

words = text.split()

# Build bigram model
bigrams = defaultdict(list)

for i in range(len(words) - 1):
    bigrams[words[i]].append(words[i + 1])

# Generate text
word = random.choice(words)
generated = [word]

for _ in range(10):
    if word in bigrams:
        word = random.choice(bigrams[word])
        generated.append(word)
    else:
        break

print("Generated Text:")
print(" ".join(generated))