# DFA Simulator
# Language: Strings ending with "ab"

# States
states = ["q0", "q1", "q2"]

# Input Alphabet
alphabet = ["a", "b"]

# Transition Table
transitions = {
    ("q0", "a"): "q1",
    ("q0", "b"): "q0",
    ("q1", "a"): "q1",
    ("q1", "b"): "q2",
    ("q2", "a"): "q1",
    ("q2", "b"): "q0"
}

# Initial State
initial_state = "q0"

# Final State
final_states = ["q2"]

# Number of strings
n = int(input("Enter number of input strings: "))

for i in range(n):
    string = input("\nEnter String: ")

    current_state = initial_state
    path = [current_state]
    valid = True

    for symbol in string:
        if symbol not in alphabet:
            valid = False
            break
        current_state = transitions[(current_state, symbol)]
        path.append(current_state)

    if not valid:
        print("Invalid Input (Only a and b are allowed)")
        continue

    print("Transition Path:")
    print(" → ".join(path))

    if current_state in final_states:
        print("Accepted")
    else:
        print("Rejected")