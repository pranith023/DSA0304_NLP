import re
from collections import Counter


# =========================================================
# ENGLISH TRAINING CORPUS
# =========================================================

corpus = """
The student is studying natural language processing.
The student is learning Python programming.
The student is reading an English book.
The student is writing a Python program.
The student is using Python for language processing.
The student is solving a programming problem.
The student is practicing Python programming.
The student is predicting the next word.

The teacher is explaining natural language processing.
The teacher is teaching the student.
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
# PREPROCESSING
# =========================================================

def preprocess(text):

    text = text.lower()

    sentences = re.split(r'[.!?]+', text)

    processed = []

    for sentence in sentences:

        words = re.findall(r'\b[a-z]+\b', sentence)

        if words:
            words = ['<START>'] + words + ['<END>']
            processed.append(words)

    return processed


# =========================================================
# N-GRAM COUNTING
# =========================================================

def build_models(sentences):

    unigram = Counter()
    bigram = Counter()
    trigram = Counter()

    for sentence in sentences:

        # Unigram
        for word in sentence:
            unigram[word] += 1

        # Bigram
        for i in range(len(sentence) - 1):

            pair = (
                sentence[i],
                sentence[i + 1]
            )

            bigram[pair] += 1

        # Trigram
        for i in range(len(sentence) - 2):

            triple = (
                sentence[i],
                sentence[i + 1],
                sentence[i + 2]
            )

            trigram[triple] += 1

    return unigram, bigram, trigram


# =========================================================
# PROBABILITY FUNCTIONS
# =========================================================

def unigram_probability(word, unigram):

    total = sum(unigram.values())

    if total == 0:
        return 0

    return unigram[word] / total


def bigram_probability(word1, word2,
                       unigram, bigram):

    denominator = unigram[word1]

    if denominator == 0:
        return 0

    return bigram[(word1, word2)] / denominator


def trigram_probability(word1, word2, word3,
                        bigram, trigram):

    denominator = bigram[(word1, word2)]

    if denominator == 0:
        return 0

    return trigram[
        (word1, word2, word3)
    ] / denominator


# =========================================================
# UNSMOOTHED TRIGRAM MODEL
# =========================================================

def unsmoothed_probability(w1, w2, word,
                           unigram,
                           bigram,
                           trigram):

    return trigram_probability(
        w1,
        w2,
        word,
        bigram,
        trigram
    )


# =========================================================
# BACKOFF MODEL
# =========================================================

def backoff_probability(w1, w2, word,
                        unigram,
                        bigram,
                        trigram):

    # Step 1: Try trigram
    p_tri = trigram_probability(
        w1, w2, word,
        bigram,
        trigram
    )

    if p_tri > 0:
        return p_tri, "Trigram"

    # Step 2: Backoff to bigram
    p_bi = bigram_probability(
        w2,
        word,
        unigram,
        bigram
    )

    if p_bi > 0:
        return p_bi, "Bigram"

    # Step 3: Backoff to unigram
    p_uni = unigram_probability(
        word,
        unigram
    )

    if p_uni > 0:
        return p_uni, "Unigram"

    return 0, "None"


# =========================================================
# DELETED INTERPOLATION
# =========================================================

def interpolation_probability(
        w1, w2, word,
        unigram,
        bigram,
        trigram):

    # Interpolation weights
    lambda1 = 0.2
    lambda2 = 0.3
    lambda3 = 0.5

    p_uni = unigram_probability(
        word,
        unigram
    )

    p_bi = bigram_probability(
        w2,
        word,
        unigram,
        bigram
    )

    p_tri = trigram_probability(
        w1,
        w2,
        word,
        bigram,
        trigram
    )

    probability = (
        lambda1 * p_uni
        + lambda2 * p_bi
        + lambda3 * p_tri
    )

    return probability


# =========================================================
# GET CANDIDATE WORDS
# =========================================================

def get_candidates(unigram):

    candidates = []

    for word in unigram:

        if word not in [
            '<START>',
            '<END>'
        ]:

            candidates.append(word)

    return candidates


# =========================================================
# PREDICTION
# =========================================================

def predict(sentence,
            unigram,
            bigram,
            trigram):

    words = re.findall(
        r'\b[a-z]+\b',
        sentence.lower()
    )

    if len(words) < 2:

        print(
            "Please enter at least two words."
        )

        return

    w1 = words[-2]
    w2 = words[-1]

    candidates = get_candidates(
        unigram
    )

    unsmoothed_results = []
    backoff_results = []
    interpolation_results = []

    for word in candidates:

        # -----------------------------------------
        # UNSMOOTHED
        # -----------------------------------------

        p_unsmoothed = unsmoothed_probability(
            w1,
            w2,
            word,
            unigram,
            bigram,
            trigram
        )

        unsmoothed_results.append(
            (word, p_unsmoothed)
        )

        # -----------------------------------------
        # BACKOFF
        # -----------------------------------------

        p_backoff, source = backoff_probability(
            w1,
            w2,
            word,
            unigram,
            bigram,
            trigram
        )

        backoff_results.append(
            (word, p_backoff, source)
        )

        # -----------------------------------------
        # DELETED INTERPOLATION
        # -----------------------------------------

        p_interpolation = interpolation_probability(
            w1,
            w2,
            word,
            unigram,
            bigram,
            trigram
        )

        interpolation_results.append(
            (word, p_interpolation)
        )

    # Sort results
    unsmoothed_results.sort(
        key=lambda x: x[1],
        reverse=True
    )

    backoff_results.sort(
        key=lambda x: x[1],
        reverse=True
    )

    interpolation_results.sort(
        key=lambda x: x[1],
        reverse=True
    )

    # =====================================================
    # DISPLAY
    # =====================================================

    print("\n==========================================")
    print("INPUT:", sentence)
    print("CONTEXT:", w1, w2)
    print("==========================================")

    print("\nUNSMOOTHED TRIGRAM MODEL")
    print("------------------------------------------")

    count = 0

    for word, probability in unsmoothed_results:

        if probability > 0:

            count += 1

            print(
                f"{count}. {word:15}"
                f"P = {probability:.4f}"
            )

            if count == 5:
                break

    if count == 0:
        print("No prediction. Trigram is unseen.")

    print("\nBACKOFF MODEL")
    print("------------------------------------------")

    count = 0

    for word, probability, source in backoff_results:

        if probability > 0:

            count += 1

            print(
                f"{count}. {word:15}"
                f"P = {probability:.4f}"
                f"  Source = {source}"
            )

            if count == 5:
                break

    print("\nDELETED INTERPOLATION")
    print("------------------------------------------")

    for i, (word, probability) in enumerate(
            interpolation_results[:5],
            start=1):

        print(
            f"{i}. {word:15}"
            f"P = {probability:.4f}"
        )


# =========================================================
# SHOW MODEL STATISTICS
# =========================================================

def show_statistics(unigram,
                    bigram,
                    trigram):

    print("\n==========================================")
    print("MODEL STATISTICS")
    print("==========================================")

    print(
        "Unique unigrams :",
        len(unigram)
    )

    print(
        "Unique bigrams  :",
        len(bigram)
    )

    print(
        "Unique trigrams :",
        len(trigram)
    )

    print(
        "Total unigram occurrences:",
        sum(unigram.values())
    )


# =========================================================
# ZERO PROBABILITY DEMONSTRATION
# =========================================================

def demonstrate_zero_probability(
        unigram,
        bigram,
        trigram):

    print("\n==========================================")
    print("ZERO PROBABILITY DEMONSTRATION")
    print("==========================================")

    w1 = "student"
    w2 = "is"
    word = "elephant"

    p_tri = trigram_probability(
        w1,
        w2,
        word,
        bigram,
        trigram
    )

    print(
        f"\nUnsmoothed:"
        f" P({word}|{w1},{w2}) = {p_tri:.4f}"
    )

    p_backoff, source = backoff_probability(
        w1,
        w2,
        word,
        unigram,
        bigram,
        trigram
    )

    print(
        f"Backoff:"
        f" P({word}|{w1},{w2}) = {p_backoff:.4f}"
        f"  Source = {source}"
    )

    p_interpolation = interpolation_probability(
        w1,
        w2,
        word,
        unigram,
        bigram,
        trigram
    )

    print(
        f"Deleted Interpolation:"
        f" P({word}|{w1},{w2})"
        f" = {p_interpolation:.4f}"
    )


# =========================================================
# MAIN PROGRAM
# =========================================================

sentences = preprocess(corpus)

unigram, bigram, trigram = build_models(
    sentences
)

print("==========================================")
print(" SMOOTHING AND BACKOFF LANGUAGE MODEL")
print("==========================================")

show_statistics(
    unigram,
    bigram,
    trigram
)


while True:

    print("\n==========================================")
    print("MENU")
    print("==========================================")

    print("1. Predict next word")
    print("2. Show model statistics")
    print("3. Demonstrate zero probability")
    print("4. Exit")

    choice = input(
        "\nEnter your choice: "
    )

    if choice == "1":

        sentence = input(
            "\nEnter a sentence/query "
            "(at least two words): "
        )

        predict(
            sentence,
            unigram,
            bigram,
            trigram
        )

    elif choice == "2":

        show_statistics(
            unigram,
            bigram,
            trigram
        )

    elif choice == "3":

        demonstrate_zero_probability(
            unigram,
            bigram,
            trigram
        )

    elif choice == "4":

        print(
            "\nProgram terminated."
        )

        break

    else:

        print(
            "\nInvalid choice."
        )