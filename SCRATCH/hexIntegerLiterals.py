# CS 3310 - Formal Languages and Automata
# Program 1
# Recognizing an HexInteger
# Name: Medha Swarnachandrabalaji

# takes in a string s and returns True if s is a valid HexInteger, False otherwise
def is_valid_hexinteger(s: str) -> bool:
    # Must start with 0x or 0X and have at least one more character
    if len(s) < 3 or s[0] != '0' or (s[1] != 'x' and s[1] != 'X'):
        return False

    # true when it sees at least one hex digit
    # used at end to make sure there is not just underscores
    seen_hex_digit = False
    previous_was_underscore = False

    # for loop for every character after the 0x or 0X
    for ch in s[2:]:
        if ch == '_':
            # reject double underscore
            if previous_was_underscore:
                return False
            previous_was_underscore = True

        # for valid hex digits
        elif ('0' <= ch <= '9') or ('a' <= ch <= 'f') or ('A' <= ch <= 'F'):
            seen_hex_digit = True
            previous_was_underscore = False

        else:
            return False

    return seen_hex_digit and not previous_was_underscore

# Keep prompting user to run program until they decide to end it.
run_program = 'y'

while run_program == 'y' or run_program == 'Y':
    # store user input as a string in user_input
    user_input = input("Enter your value: ")
    print(user_input)

    # Call function to evaluate if the user's string is a valid HexInteger
    validHex = is_valid_hexinteger(user_input)

    # Print Results
    if validHex:
        print("The value", user_input, "IS a valid HexInteger")
    else:
        print("The value", user_input, "is NOT a valid HexInteger")

    # Ask user if they want to test another number
    run_program = input(
        "\nWould you like to test another value?\n"
        "Enter 'y' for yes and any other character for no: "
    )
