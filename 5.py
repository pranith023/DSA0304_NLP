import nltk
from nltk.stem import PorterStemmer

# Download NLTK data (run once)
nltk.download('punkt')

# Create Porter Stemmer object
stemmer = PorterStemmer()

# List of words
words = ["running", "jumps", "playing", "studies", "happiness", "easily", "connected"]

print("Porter Stemmer Results")
print("----------------------")

# Perform stemming
for word in words:
    stemmed_word = stemmer.stem(word)
    print(f"Original: {word} --> Stemmed: {stemmed_word}")