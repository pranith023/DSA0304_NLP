import re
from collections import Counter, defaultdict


# ---------------------------------------------------------
# SAMPLE ENGLISH CORPUS
# ---------------------------------------------------------

corpus = """
The student is studying natural language processing.
The student is learning Python programming.
The student is reading an English book.
The student is writing a Python program.
The teacher is explaining natural language processing.
The teacher is teaching the student.
The teacher is reading an English book.
The programmer is writing a Python program.
The programmer is learning natural language processing.
The student is using Python for language processing.
The student is solving a programming problem.
The student is practicing Python programming.
The teacher is giving a programming lesson.
The programmer is developing a language model.
The language model is predicting the next word.
The language model is learning from text.
The student is predicting the next word.
"""


# ---------------------------------------------------------
# PREPROCESSING
# ---------------------------------------------------------

def preprocess(text):
    """
    Convert text to lowercase and split it into sentences.
    """
    text = text.lower()

    sentences = re.split(r'[.!?]+', text)

    processed_sentences = []

    for sentence in sentences:
        words = re.findall(r'\b[a-z]+\b', sentence)

        if words:
            words = ['<START>'] + words + ['<END>']
            processed_sentences.append(words)

    return processed_sentences


# ---------------------------------------------------------
# BUILD N-GRAM COUNTS
# ---------------------------------------------------------

def build_ngrams(sentences):
    unigram_counts = Counter()
    bigram_counts = Counter()
    trigram_counts = Counter()

    for sentence in sentences:

        # Unigrams
        for word in sentence:
            unigram_counts[word] += 1

        # Bigrams
        for i in range(len(sentence) - 1):
            bigram = (sentence[i], sentence[i + 1])
            bigram_counts[bigram] += 1

        # Trigrams
        for i in range(len(sentence) - 2):
            trigram = (sentence[i], sentence[i + 1], sentence[i + 2])
            trigram_counts[trigram] += 1

    return unigram_counts, bigram_counts, trigram_counts


# ---------------------------------------------------------
# PROBABILITY FUNCTIONS
# ---------------------------------------------------------

def unigram_probability(word, unigram_counts):
    total_words = sum(unigram_counts.values())

    return unigram_counts[word] / total_words


def bigram_probability(word1, word2, unigram_counts, bigram_counts):
    numerator = bigram_counts[(word1, word2)]
    denominator = unigram_counts[word1]

    if denominator == 0:
        return 0.0

    return numerator / denominator


def trigram_probability(
        word1,
        word2,
        word3,
        bigram_counts,
        trigram_counts):

    numerator = trigram_counts[(word1, word2, word3)]
    denominator = bigram_counts[(word1, word2)]

    if denominator == 0:
        return 0.0

    return numerator / denominator


# ---------------------------------------------------------
# DISPLAY COUNTS AND PROBABILITIES
# ---------------------------------------------------------

def display_unigrams(unigram_counts):
    print("\n========== UNIGRAMS ==========")

    total = sum(unigram_counts.values())

    for word, count in unigram_counts.most_common():
        probability = count / total
        print(f"{word:15} Count = {count:2}  Probability = {probability:.4f}")


def display_bigrams(unigram_counts, bigram_counts):
    print("\n========== BIGRAMS ==========")

    for (word1, word2), count in bigram_counts.most_common():
        probability = bigram_probability(
            word1,
            word2,
            unigram_counts,
            bigram_counts
        )

        print(
            f"({word1}, {word2})"
            f"\tCount = {count:2}"
            f"\tProbability = {probability:.4f}"
        )


def display_trigrams(bigram_counts, trigram_counts):
    print("\n========== TRIGRAMS ==========")

    for (word1, word2, word3), count in trigram_counts.most_common():
        probability = trigram_probability(
            word1,
            word2,
            word3,
            bigram_counts,
            trigram_counts
        )

        print(
            f"({word1}, {word2}, {word3})"
            f"\tCount = {count:2}"
            f"\tProbability = {probability:.4f}"
        )


# ---------------------------------------------------------
# NEXT WORD PREDICTION
# ---------------------------------------------------------

def predict_next_word(sentence, n, unigram_counts,
                       bigram_counts, trigram_counts):

    words = re.findall(r'\b[a-z]+\b', sentence.lower())

    if not words:
        return []

    candidates = []

    # -----------------------------------------------------
    # UNIGRAM MODEL
    # -----------------------------------------------------
    if n == 1:

        for word, count in unigram_counts.items():

            if word not in ['<START>', '<END>']:
                probability = unigram_probability(
                    word,
                    unigram_counts
                )

                candidates.append((word, probability))

    # -----------------------------------------------------
    # BIGRAM MODEL
    # -----------------------------------------------------
    elif n == 2:

        previous_word = words[-1]

        for word in unigram_counts:

            if word in ['<START>', '<END>']:
                continue

            probability = bigram_probability(
                previous_word,
                word,
                unigram_counts,
                bigram_counts
            )

            if probability > 0:
                candidates.append((word, probability))

    # -----------------------------------------------------
    # TRIGRAM MODEL
    # -----------------------------------------------------
    elif n == 3:

        if len(words) < 2:
            return []

        previous_word1 = words[-2]
        previous_word2 = words[-1]

        for word in unigram_counts:

            if word in ['<START>', '<END>']:
                continue

            probability = trigram_probability(
                previous_word1,
                previous_word2,
                word,
                bigram_counts,
                trigram_counts
            )

            if probability > 0:
                candidates.append((word, probability))

    candidates.sort(key=lambda x: x[1], reverse=True)

    return candidates[:5]


# ---------------------------------------------------------
# MAIN PROGRAM
# ---------------------------------------------------------

sentences = preprocess(corpus)

unigram_counts, bigram_counts, trigram_counts = build_ngrams(sentences)


print("==============================================")
print("       N-GRAM NEXT WORD PREDICTION")
print("==============================================")

print("\nNumber of sentences:", len(sentences))
print("Number of unique unigrams:", len(unigram_counts))
print("Number of unique bigrams:", len(bigram_counts))
print("Number of unique trigrams:", len(trigram_counts))


# ---------------------------------------------------------
# MENU
# ---------------------------------------------------------

while True:

    print("\n----------------------------------------------")
    print("1. Display Unigram Counts and Probabilities")
    print("2. Display Bigram Counts and Probabilities")
    print("3. Display Trigram Counts and Probabilities")
    print("4. Predict Next Word")
    print("5. Demonstrate Zero Probability")
    print("6. Exit")
    print("----------------------------------------------")

    choice = input("Enter your choice: ")

    if choice == "1":

        display_unigrams(unigram_counts)

    elif choice == "2":

        display_bigrams(
            unigram_counts,
            bigram_counts
        )

    elif choice == "3":

        display_trigrams(
            bigram_counts,
            trigram_counts
        )

    elif choice == "4":

        sentence = input(
            "\nEnter incomplete sentence: "
        )

        print("\nSelect N:")
        print("1. Unigram")
        print("2. Bigram")
        print("3. Trigram")

        n = int(input("Enter N: "))

        predictions = predict_next_word(
            sentence,
            n,
            unigram_counts,
            bigram_counts,
            trigram_counts
        )

        print("\nTop-5 Next Word Predictions:")

        if predictions:

            for rank, (word, probability) in enumerate(
                    predictions, start=1):

                print(
                    f"{rank}. {word:15}"
                    f" Probability = {probability:.4f}"
                )

        else:
            print("No prediction available.")

    elif choice == "5":

        print("\n========== ZERO PROBABILITY TEST ==========")

        test_bigram = ("student", "elephant")

        probability = bigram_probability(
            test_bigram[0],
            test_bigram[1],
            unigram_counts,
            bigram_counts
        )

        print(
            f"P({test_bigram[1]} | {test_bigram[0]})"
            f" = {probability:.4f}"
        )

        test_trigram = (
            "student",
            "is",
            "elephant"
        )

        probability = trigram_probability(
            test_trigram[0],
            test_trigram[1],
            test_trigram[2],
            bigram_counts,
            trigram_counts
        )

        print(
            f"P({test_trigram[2]} | "
            f"{test_trigram[0]}, {test_trigram[1]})"
            f" = {probability:.4f}"
        )

        print(
            "\nSince these N-grams do not occur in "
            "the training corpus, their probability is 0."
        )

    elif choice == "6":

        print("\nProgram terminated.")
        break

    else:

        print("Invalid choice. Please try again.")