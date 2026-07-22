import nltk
from nltk.stem import PorterStemmer, WordNetLemmatizer

# Download required NLTK resources (run once)
nltk.download('wordnet')
nltk.download('omw-1.4')

# Sample words
words = ["running", "flies", "better", "studies", "playing"]

# Create stemmer and lemmatizer objects
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

print("Morphological Analysis using NLTK")
print("----------------------------------")

for word in words:
    stem = stemmer.stem(word)
    lemma = lemmatizer.lemmatize(word)
    print(f"Word: {word}")
    print(f"Stem: {stem}")
    print(f"Lemma: {lemma}")
    print()