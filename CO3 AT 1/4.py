import re
import math
from collections import Counter, defaultdict


# =========================================================
# PENN TREEBANK TAGSET - BASIC TAGS
# =========================================================

TAG_DESCRIPTIONS = {
    "NN": "Noun, singular",
    "NNS": "Noun, plural",
    "VB": "Verb, base form",
    "VBD": "Verb, past tense",
    "VBG": "Verb, gerund/present participle",
    "VBN": "Verb, past participle",
    "VBZ": "Verb, 3rd person singular",
    "JJ": "Adjective",
    "RB": "Adverb",
    "PRP": "Personal pronoun",
    "DT": "Determiner",
    "IN": "Preposition/subordinating conjunction",
    "CC": "Coordinating conjunction",
    "TO": "to",
    "MD": "Modal",
    "CD": "Cardinal number",
}


# =========================================================
# TRAINING DATA
# =========================================================
#
# Format:
# sentence = [(word, correct_tag), ...]
#
# This small tagged corpus is used to calculate
# lexical and transition probabilities.
# =========================================================

training_data = [

    [
        ("the", "DT"),
        ("student", "NN"),
        ("is", "VBZ"),
        ("reading", "VBG"),
        ("a", "DT"),
        ("book", "NN")
    ],

    [
        ("the", "DT"),
        ("student", "NN"),
        ("is", "VBZ"),
        ("writing", "VBG"),
        ("a", "DT"),
        ("program", "NN")
    ],

    [
        ("the", "DT"),
        ("teacher", "NN"),
        ("is", "VBZ"),
        ("teaching", "VBG"),
        ("the", "DT"),
        ("student", "NN")
    ],

    [
        ("the", "DT"),
        ("programmer", "NN"),
        ("is", "VBZ"),
        ("writing", "VBG"),
        ("python", "NN")
    ],

    [
        ("the", "DT"),
        ("student", "NN"),
        ("learns", "VBZ"),
        ("python", "NN"),
        ("programming", "NN")
    ],

    [
        ("the", "DT"),
        ("teacher", "NN"),
        ("explains", "VBZ"),
        ("natural", "JJ"),
        ("language", "NN")
    ],

    [
        ("the", "DT"),
        ("student", "NN"),
        ("quickly", "RB"),
        ("reads", "VBZ"),
        ("the", "DT"),
        ("book", "NN")
    ],

    [
        ("the", "DT"),
        ("programmer", "NN"),
        ("carefully", "RB"),
        ("writes", "VBZ"),
        ("code", "NN")
    ],

    [
        ("i", "PRP"),
        ("am", "VBP"),
        ("learning", "VBG"),
        ("python", "NN")
    ],

    [
        ("we", "PRP"),
        ("are", "VBP"),
        ("studying", "VBG"),
        ("natural", "JJ"),
        ("language", "NN"),
        ("processing", "NN")
    ],

    [
        ("the", "DT"),
        ("student", "NN"),
        ("can", "MD"),
        ("write", "VB"),
        ("python", "NN")
    ],

    [
        ("the", "DT"),
        ("student", "NN"),
        ("will", "MD"),
        ("learn", "VB"),
        ("programming", "NN")
    ],

    [
        ("the", "DT"),
        ("teacher", "NN"),
        ("and", "CC"),
        ("student", "NN"),
        ("read", "VB"),
        ("together", "RB")
    ],

    [
        ("the", "DT"),
        ("programmer", "NN"),
        ("uses", "VBZ"),
        ("python", "NN")
    ]
]


# =========================================================
# PREPROCESSING
# =========================================================

def tokenize(sentence):

    return re.findall(
        r"\b[a-zA-Z]+\b",
        sentence.lower()
    )


# =========================================================
# BUILD STATISTICS
# =========================================================

def build_statistics(training_data):

    word_tag_counts = defaultdict(Counter)
    tag_counts = Counter()
    transition_counts = defaultdict(Counter)

    vocabulary = set()

    for sentence in training_data:

        previous_tag = "<START>"

        for word, tag in sentence:

            vocabulary.add(word)

            word_tag_counts[word][tag] += 1

            tag_counts[tag] += 1

            transition_counts[
                previous_tag
            ][tag] += 1

            previous_tag = tag

        transition_counts[
            previous_tag
        ]["<END>"] += 1

    return (
        word_tag_counts,
        tag_counts,
        transition_counts,
        vocabulary
    )


word_tag_counts, tag_counts, transition_counts, vocabulary = \
    build_statistics(training_data)


# =========================================================
# LEXICAL DICTIONARIES FOR RULE-BASED TAGGING
# =========================================================

LEXICON = {

    "the": "DT",
    "a": "DT",
    "an": "DT",

    "i": "PRP",
    "we": "PRP",
    "you": "PRP",
    "he": "PRP",
    "she": "PRP",
    "they": "PRP",

    "is": "VBZ",
    "are": "VBP",
    "am": "VBP",

    "can": "MD",
    "will": "MD",
    "should": "MD",
    "must": "MD",

    "and": "CC",
    "or": "CC",
    "but": "CC",

    "to": "TO",

    "in": "IN",
    "on": "IN",
    "at": "IN",
    "for": "IN",
    "with": "IN",
    "from": "IN",

    "student": "NN",
    "teacher": "NN",
    "programmer": "NN",
    "book": "NN",
    "program": "NN",
    "python": "NN",
    "language": "NN",
    "processing": "NN",
    "code": "NN",
    "programming": "NN",

    "natural": "JJ",

    "quickly": "RB",
    "carefully": "RB",
    "together": "RB"
}


# =========================================================
# RULE-BASED POS TAGGER
# =========================================================

def rule_based_tag(sentence):

    words = tokenize(sentence)

    tagged = []

    previous_word = None

    for word in words:

        # -----------------------------------------------
        # Rule 1: Lexical dictionary
        # -----------------------------------------------

        if word in LEXICON:

            tag = LEXICON[word]

        # -----------------------------------------------
        # Rule 2: Number
        # -----------------------------------------------

        elif word.isdigit():

            tag = "CD"

        # -----------------------------------------------
        # Rule 3: -ly → adverb
        # -----------------------------------------------

        elif word.endswith("ly"):

            tag = "RB"

        # -----------------------------------------------
        # Rule 4: -ing → gerund
        # -----------------------------------------------

        elif word.endswith("ing"):

            tag = "VBG"

        # -----------------------------------------------
        # Rule 5: -ed → past tense
        # -----------------------------------------------

        elif word.endswith("ed"):

            tag = "VBD"

        # -----------------------------------------------
        # Rule 6: -ous, -ful, -able → adjective
        # -----------------------------------------------

        elif (
            word.endswith("ous")
            or word.endswith("ful")
            or word.endswith("able")
        ):

            tag = "JJ"

        # -----------------------------------------------
        # Rule 7: After modal → base verb
        # -----------------------------------------------

        elif previous_word in {
            "can",
            "will",
            "should",
            "must"
        }:

            tag = "VB"

        # -----------------------------------------------
        # Rule 8: Default unknown word → noun
        # -----------------------------------------------

        else:

            tag = "NN"

        tagged.append(
            (word, tag)
        )

        previous_word = word

    return tagged


# =========================================================
# STOCHASTIC POS TAGGER
# =========================================================

def emission_probability(word, tag):

    total = tag_counts[tag]

    if total == 0:
        return 0

    return (
        word_tag_counts[word][tag]
        / total
    )


def transition_probability(
        previous_tag,
        current_tag):

    total = sum(
        transition_counts[
            previous_tag
        ].values()
    )

    if total == 0:
        return 0

    return (
        transition_counts[
            previous_tag
        ][current_tag]
        / total
    )


def stochastic_tag(sentence):

    words = tokenize(sentence)

    all_tags = list(
        tag_counts.keys()
    )

    result = []

    previous_tag = "<START>"

    for word in words:

        best_tag = None
        best_score = -1

        for tag in all_tags:

            # -----------------------------------------
            # Emission probability
            # -----------------------------------------

            emission = (
                word_tag_counts[word][tag]
                + 1
            ) / (
                tag_counts[tag]
                + len(vocabulary)
            )

            # -----------------------------------------
            # Transition probability
            # -----------------------------------------

            transition = (
                transition_counts[
                    previous_tag
                ][tag]
                + 1
            ) / (
                sum(
                    transition_counts[
                        previous_tag
                    ].values()
                )
                + len(all_tags)
            )

            # -----------------------------------------
            # Combined probability
            # -----------------------------------------

            score = (
                math.log(emission)
                + math.log(transition)
            )

            if score > best_score:

                best_score = score
                best_tag = tag

        result.append(
            (word, best_tag)
        )

        previous_tag = best_tag

    return result


# =========================================================
# TRANSFORMATION-BASED TAGGER
# =========================================================

def transformation_based_tag(sentence):

    # Start with rule-based tags
    tagged = rule_based_tag(sentence)

    # -----------------------------------------------
    # Transformation Rule 1:
    #
    # After a pronoun or modal, an unknown noun
    # can become a verb.
    # -----------------------------------------------

    for i in range(1, len(tagged)):

        word, tag = tagged[i]

        previous_word, previous_tag = \
            tagged[i - 1]

        if (
            previous_tag == "PRP"
            and tag == "NN"
        ):

            tagged[i] = (
                word,
                "VB"
            )

        elif (
            previous_tag == "MD"
            and tag == "NN"
        ):

            tagged[i] = (
                word,
                "VB"
            )

    # -----------------------------------------------
    # Transformation Rule 2:
    #
    # Words ending in -ing after an auxiliary
    # are VBG.
    # -----------------------------------------------

    for i in range(len(tagged)):

        word, tag = tagged[i]

        if (
            word.endswith("ing")
            and i > 0
        ):

            previous_word, previous_tag = \
                tagged[i - 1]

            if previous_tag in {
                "VBZ",
                "VBP",
                "VBD"
            }:

                tagged[i] = (
                    word,
                    "VBG"
                )

    # -----------------------------------------------
    # Transformation Rule 3:
    #
    # Words ending in -ly are adverbs.
    # -----------------------------------------------

    for i in range(len(tagged)):

        word, tag = tagged[i]

        if word.endswith("ly"):

            tagged[i] = (
                word,
                "RB"
            )

    return tagged


# =========================================================
# DISPLAY TAGGED SENTENCE
# =========================================================

def display_result(title, tagged):

    print("\n" + "=" * 60)

    print(title)

    print("=" * 60)

    for word, tag in tagged:

        print(
            f"{word:15} -> "
            f"{tag:5} "
            f"{TAG_DESCRIPTIONS.get(tag, '')}"
        )


# =========================================================
# COMPARE THREE TAGGERS
# =========================================================

def compare_taggers(sentence):

    print("\n\n")
    print("#" * 60)
    print("INPUT SENTENCE")
    print("#" * 60)

    print(sentence)

    rule_result = rule_based_tag(
        sentence
    )

    stochastic_result = stochastic_tag(
        sentence
    )

    transformation_result = \
        transformation_based_tag(
            sentence
        )

    display_result(
        "1. RULE-BASED POS TAGGER",
        rule_result
    )

    display_result(
        "2. STOCHASTIC POS TAGGER",
        stochastic_result
    )

    display_result(
        "3. TRANSFORMATION-BASED POS TAGGER",
        transformation_result
    )


# =========================================================
# EVALUATION AGAINST TRAINING DATA
# =========================================================

def calculate_accuracy(
        predicted,
        actual):

    correct = 0
    total = 0

    for predicted_item, actual_item in zip(
        predicted,
        actual
    ):

        if predicted_item[1] == actual_item[1]:

            correct += 1

        total += 1

    if total == 0:
        return 0

    return (
        correct / total
    ) * 100


def evaluate_systems():

    rule_correct = 0
    stochastic_correct = 0
    transformation_correct = 0

    total = 0

    for sentence in training_data:

        text = " ".join(
            word
            for word, tag in sentence
        )

        actual = sentence

        rule_prediction = \
            rule_based_tag(text)

        stochastic_prediction = \
            stochastic_tag(text)

        transformation_prediction = \
            transformation_based_tag(text)

        for i in range(len(actual)):

            total += 1

            if (
                rule_prediction[i][1]
                == actual[i][1]
            ):

                rule_correct += 1

            if (
                stochastic_prediction[i][1]
                == actual[i][1]
            ):

                stochastic_correct += 1

            if (
                transformation_prediction[i][1]
                == actual[i][1]
            ):

                transformation_correct += 1

    print("\n")
    print("=" * 60)
    print("POS TAGGER EVALUATION")
    print("=" * 60)

    print(
        f"Rule-Based Accuracy          : "
        f"{rule_correct / total * 100:.2f}%"
    )

    print(
        f"Stochastic Accuracy          : "
        f"{stochastic_correct / total * 100:.2f}%"
    )

    print(
        f"Transformation-Based Accuracy: "
        f"{transformation_correct / total * 100:.2f}%"
    )


# =========================================================
# MAIN PROGRAM
# =========================================================

print("=" * 60)
print("       PART-OF-SPEECH TAGGING SYSTEM")
print("=" * 60)

while True:

    print("\n")
    print("1. Rule-Based POS Tagging")
    print("2. Stochastic POS Tagging")
    print("3. Transformation-Based Tagging")
    print("4. Compare All Three")
    print("5. Evaluate Taggers")
    print("6. Display Tagset")
    print("7. Exit")

    choice = input(
        "\nEnter your choice: "
    )

    if choice == "1":

        sentence = input(
            "Enter an English sentence: "
        )

        result = rule_based_tag(
            sentence
        )

        display_result(
            "RULE-BASED POS TAGGING",
            result
        )

    elif choice == "2":

        sentence = input(
            "Enter an English sentence: "
        )

        result = stochastic_tag(
            sentence
        )

        display_result(
            "STOCHASTIC POS TAGGING",
            result
        )

    elif choice == "3":

        sentence = input(
            "Enter an English sentence: "
        )

        result = transformation_based_tag(
            sentence
        )

        display_result(
            "TRANSFORMATION-BASED POS TAGGING",
            result
        )

    elif choice == "4":

        sentence = input(
            "Enter an English sentence: "
        )

        compare_taggers(
            sentence
        )

    elif choice == "5":

        evaluate_systems()

    elif choice == "6":

        print("\nPENN TREEBANK TAGSET")
        print("-" * 60)

        for tag, description in \
                TAG_DESCRIPTIONS.items():

            print(
                f"{tag:5} -> {description}"
            )

    elif choice == "7":

        print(
            "\nProgram terminated."
        )

        break

    else:

        print(
            "\nInvalid choice."
        )