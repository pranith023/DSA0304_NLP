# Finite State Automaton to recognize strings ending with "ab"

def fsa_ends_with_ab(string):
    state = 0

    for char in string:
        if state == 0:
            if char == 'a':
                state = 1
            else:
                state = 0

        elif state == 1:
            if char == 'b':
                state = 2
            elif char == 'a':
                state = 1
            else:
                state = 0

        elif state == 2:
            if char == 'a':
                state = 1
            else:
                state = 0

    if state == 2:
        return "Accepted"
    else:
        return "Rejected"


# Test cases
strings = ["ab", "aab", "babab", "aba", "abb", "bba", "aaab"]

for s in strings:
    print(f"{s} --> {fsa_ends_with_ab(s)}")