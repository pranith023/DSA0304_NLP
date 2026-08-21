import re
import math
from collections import Counter


# =========================================================
# TRAINING CORPUS
# =========================================================

training_corpus = """
The student is studying natural language processing.
The student is learning Python programming.
The student is reading an English book.
The student is writing a Python program.
The student is using Python for language processing.
The student is solving a programming problem.
The student is practicing Python programming.
The teacher is teaching the student.
The teacher is explaining natural language processing.
The teacher is reading an English book.
The teacher is giving a programming lesson.
The programmer is writing a Python program.
The programmer is learning natural language processing.
The programmer is developing a language model.
The language model is predicting the next word.
The language model is learning from text.
The language model is processing English text.
"""


# =========================================================
# SEPARATE TEST CORPUS
# =========================================================

test_corpus = """
The student is learning Python programming.
The teacher is reading an English book.
The programmer is developing a language model.
The language model is predicting the next word.
"""


# =========================================================
# PREPROCESSING
# =========================================================

def preprocess(text):

    text = text.lower()

    sentences = re.split(r'[.!?]+', text)

    processed_sentences = []

    for sentence in sentences:

        words = re.findall(
            r'\b[a-z]+\b',
            sentence
        )

        if words:
            words = (
                ['<START>']
                + words
                + ['<END>']
            )

            processed_sentences.append(words)

    return processed_sentences


# =========================================================
# BUILD N-GRAM COUNTS
# =========================================================

def build_ngrams(sentences):

    unigram = Counter()
    bigram = Counter()
    trigram = Counter()

    for sentence in sentences:

        # Unigram
        for word in sentence:
            unigram[word] += 1

        # Bigram
        for i in range(len(sentence) - 1):

            bigram[
                (sentence[i], sentence[i + 1])
            ] += 1

        # Trigram
        for i in range(len(sentence) - 2):

            trigram[
                (
                    sentence[i],
                    sentence[i + 1],
                    sentence[i + 2]
                )
            ] += 1

    return unigram, bigram, trigram


# =========================================================
# PROBABILITY FUNCTIONS
# =========================================================

def unigram_probability(word, unigram):

    total = sum(unigram.values())

    if total == 0:
        return 0

    return unigram[word] / total


def bigram_probability(
        word1,
        word2,
        unigram,
        bigram):

    denominator = unigram[word1]

    if denominator == 0:
        return 0

    return (
        bigram[(word1, word2)]
        / denominator
    )


def trigram_probability(
        word1,
        word2,
        word3,
        bigram,
        trigram):

    denominator = bigram[
        (word1, word2)
    ]

    if denominator == 0:
        return 0

    return (
        trigram[
            (word1, word2, word3)
        ]
        / denominator
    )


# =========================================================
# LAPLACE SMOOTHING
# =========================================================

def smoothed_unigram_probability(
        word,
        unigram,
        vocabulary_size):

    total = sum(unigram.values())

    return (
        unigram[word] + 1
    ) / (
        total + vocabulary_size
    )


def smoothed_bigram_probability(
        word1,
        word2,
        unigram,
        bigram,
        vocabulary_size):

    numerator = (
        bigram[(word1, word2)] + 1
    )

    denominator = (
        unigram[word1]
        + vocabulary_size
    )

    return numerator / denominator


def smoothed_trigram_probability(
        word1,
        word2,
        word3,
        bigram,
        trigram,
        vocabulary_size):

    numerator = (
        trigram[
            (word1, word2, word3)
        ] + 1
    )

    denominator = (
        bigram[(word1, word2)]
        + vocabulary_size
    )

    return numerator / denominator


# =========================================================
# ENTROPY CALCULATION
# =========================================================

def calculate_entropy(probabilities):

    if len(probabilities) == 0:
        return float('inf')

    total_log_probability = 0

    for probability in probabilities:

        if probability <= 0:
            return float('inf')

        total_log_probability += (
            math.log2(probability)
        )

    entropy = (
        -total_log_probability
        / len(probabilities)
    )

    return entropy


# =========================================================
# EVALUATE UNIGRAM MODEL
# =========================================================

def evaluate_unigram(
        test_sentences,
        unigram):

    probabilities = []

    for sentence in test_sentences:

        for word in sentence:

            if word == '<START>':
                continue

            probability = unigram_probability(
                word,
                unigram
            )

            probabilities.append(
                probability
            )

    return calculate_entropy(
        probabilities
    )


# =========================================================
# EVALUATE BIGRAM MODEL
# =========================================================

def evaluate_bigram(
        test_sentences,
        unigram,
        bigram):

    probabilities = []

    for sentence in test_sentences:

        for i in range(1, len(sentence)):

            previous_word = sentence[i - 1]
            current_word = sentence[i]

            probability = bigram_probability(
                previous_word,
                current_word,
                unigram,
                bigram
            )

            probabilities.append(
                probability
            )

    return calculate_entropy(
        probabilities
    )


# =========================================================
# EVALUATE TRIGRAM MODEL
# =========================================================

def evaluate_trigram(
        test_sentences,
        bigram,
        trigram):

    probabilities = []

    for sentence in test_sentences:

        for i in range(2, len(sentence)):

            word1 = sentence[i - 2]
            word2 = sentence[i - 1]
            word3 = sentence[i]

            probability = trigram_probability(
                word1,
                word2,
                word3,
                bigram,
                trigram
            )

            probabilities.append(
                probability
            )

    return calculate_entropy(
        probabilities
    )


# =========================================================
# SMOOTHED TRIGRAM ENTROPY
# =========================================================

def evaluate_smoothed_trigram(
        test_sentences,
        bigram,
        trigram,
        vocabulary_size):

    probabilities = []

    for sentence in test_sentences:

        for i in range(2, len(sentence)):

            word1 = sentence[i - 2]
            word2 = sentence[i - 1]
            word3 = sentence[i]

            probability = (
                smoothed_trigram_probability(
                    word1,
                    word2,
                    word3,
                    bigram,
                    trigram,
                    vocabulary_size
                )
            )

            probabilities.append(
                probability
            )

    return calculate_entropy(
        probabilities
    )


# =========================================================
# SENTENCE ENTROPY
# =========================================================

def sentence_trigram_entropy(
        sentence,
        bigram,
        trigram):

    probabilities = []

    for i in range(2, len(sentence)):

        w1 = sentence[i - 2]
        w2 = sentence[i - 1]
        w3 = sentence[i]

        probability = trigram_probability(
            w1,
            w2,
            w3,
            bigram,
            trigram
        )

        probabilities.append(
            probability
        )

    return calculate_entropy(
        probabilities
    )


# =========================================================
# MAIN PROGRAM
# =========================================================

train_sentences = preprocess(
    training_corpus
)

test_sentences = preprocess(
    test_corpus
)


# Build models

unigram, bigram, trigram = build_ngrams(
    train_sentences
)


vocabulary = set(unigram.keys())

vocabulary_size = len(vocabulary)


# =========================================================
# DISPLAY INFORMATION
# =========================================================

print("==============================================")
print(" ENTROPY-BASED N-GRAM LANGUAGE MODEL")
print("==============================================")

print(
    "\nTraining sentences:",
    len(train_sentences)
)

print(
    "Testing sentences:",
    len(test_sentences)
)

print(
    "Vocabulary size:",
    vocabulary_size
)

print(
    "Unique unigrams:",
    len(unigram)
)

print(
    "Unique bigrams:",
    len(bigram)
)

print(
    "Unique trigrams:",
    len(trigram)
)


# =========================================================
# CALCULATE ENTROPY
# =========================================================

unigram_entropy = evaluate_unigram(
    test_sentences,
    unigram
)

bigram_entropy = evaluate_bigram(
    test_sentences,
    unigram,
    bigram
)

trigram_entropy = evaluate_trigram(
    test_sentences,
    bigram,
    trigram
)

smoothed_trigram_entropy = (
    evaluate_smoothed_trigram(
        test_sentences,
        bigram,
        trigram,
        vocabulary_size
    )
)


# =========================================================
# DISPLAY ENTROPY
# =========================================================

print("\n==============================================")
print(" ENTROPY RESULTS")
print("==============================================")

print(
    f"Unigram Entropy : "
    f"{unigram_entropy:.4f}"
)

print(
    f"Bigram Entropy  : "
    f"{bigram_entropy:.4f}"
)

print(
    f"Trigram Entropy : "
    f"{trigram_entropy:.4f}"
)

print(
    f"Smoothed Trigram Entropy : "
    f"{smoothed_trigram_entropy:.4f}"
)


# =========================================================
# SENTENCE LEVEL ANALYSIS
# =========================================================

print("\n==============================================")
print(" SENTENCE-LEVEL ENTROPY")
print("==============================================")


sentence_results = []

for sentence in test_sentences:

    entropy = sentence_trigram_entropy(
        sentence,
        bigram,
        trigram
    )

    sentence_text = " ".join(
        word
        for word in sentence
        if word not in [
            "<START>",
            "<END>"
        ]
    )

    sentence_results.append(
        (
            sentence_text,
            entropy
        )
    )

    print(
        f"\nSentence: {sentence_text}"
    )

    if entropy == float('inf'):

        print(
            "Entropy: Infinity "
            "(unseen trigram)"
        )

    else:

        print(
            f"Entropy: {entropy:.4f}"
        )


# =========================================================
# HIGH / LOW ENTROPY
# =========================================================

finite_results = [
    item
    for item in sentence_results
    if item[1] != float('inf')
]


print("\n==============================================")
print(" HIGH / LOW ENTROPY ANALYSIS")
print("==============================================")


if finite_results:

    lowest = min(
        finite_results,
        key=lambda x: x[1]
    )

    highest = max(
        finite_results,
        key=lambda x: x[1]
    )

    print(
        "\nLowest entropy sentence:"
    )

    print(
        lowest[0]
    )

    print(
        f"Entropy = {lowest[1]:.4f}"
    )

    print(
        "\nHighest finite entropy sentence:"
    )

    print(
        highest[0]
    )

    print(
        f"Entropy = {highest[1]:.4f}"
    )


# =========================================================
# INTERPRETATION
# =========================================================

print("\n==============================================")
print(" INTERPRETATION")
print("==============================================")

print("""
Low entropy means that the next words are relatively
predictable from their context.

High entropy means that the model has greater uncertainty
about the next word.

The trigram model uses more context than the unigram and
bigram models.

Smoothing assigns non-zero probabilities to unseen N-grams,
which makes entropy calculation possible for test sequences
containing unseen combinations.
""")