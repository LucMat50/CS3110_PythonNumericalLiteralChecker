#CS3110 - FORMAL LANGUAGES AND AUTOMATA
#RECOGNIZING DECINTEGER, OCTINTEGER, HEXINTEGER, FLOATING POINT LITERAL

#NFA CLASS we can use for all NFAs
class NFA:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        #Set of states
        self.states = set(states)

        #Alphabet
        self.alphabet = set(alphabet)

        #Start state --> most likely q0 for all NFAs
        self.start_state = start_state

        #Set of accept states
        self.accept_states = set(accept_states)

        #Format: { "state": set("symbols") or 'symbol': {next_state1, next_state2, ...}}
        self.transitions = transitions

    # GET_TRANSITION FUNCTION
    # - Goes through tuple in transition dictionary
    # - Returns next state or REJECTS input string if next_state is empty    
    def get_transition(self, state, symbol):

        #Get inner transition dictionary for the current state
        state_transitions = self.transitions.get(state, {})

        #Checks for direct single-symbol key transition first
        if symbol in state_transitions:
            return state_transitions[symbol]
        
        #Checks transition where key is tuple containing symbol
        for keys, next_states, in state_transitions.items():
            if isinstance(keys, tuple) and symbol in keys:
                return next_states
            
        #Returns empty set if no transition is found    
        return set()
      

    #RUN FUNCTION 
    # - Simulates input_string through NFA
    # - Returns ACCEPT or REJECT
    def run(self, input_string):

        #Set the current state with the start state
        current_states = {self.start_state}

        for symbol in input_string: 
            # If the symbol in the user's input is not in the alphabet reject
            if symbol not in self.alphabet:
                return "reject"

            # Sets next_states to the next state in the transitions dictionary
            next_states = set()
            for state in current_states:

                #Use get_transition function to get transition for each current state
                transition_result = self.get_transition(state, symbol)

                #Updates next_states to the next state after transition
                next_states.update(transition_result)

            # Sets current_states to next_states
            current_states = next_states

            # Rejects user's input if no transitions were defined for current symbol (current_state is empty)
            if not current_states:
                return "reject"
        
        # If current_states is in accept_state then accept
        if bool(current_states.intersection(self.accept_states)) == True:
            return "accept"
        # if current_states is not in accept_state then reject
        else: 
            return "reject"

#TEST_INPUT_FILE FUNCTION
# - reads through input file and creates string with pass/fail tests
# - outputs in output file
def test_input_file(nfa):
    #Text file with test inputs for decinteger NFA
    #Must change name to in.txt
    test_input = open("in.txt", 'r')

    #Text file where results for the test inputs will be added/overwritten
    #Must change name to out.txt
    test_output = open("out.txt", 'w')

    #Reads through each line of test_input file
    with test_input as file:
        result = "DECINTEGER | OCTINTEGER | HEX | FLOAT TEST OUTPUT\n-------------------------------------\n\n"
        for line in file:

            #Splits line for first space --> stores first word (the test input)
            test_num = line.split(' ', 1)[0]

            #Splits line for first space --> stores second word (the expected result)
            expect_result = line.split(' ', 1)[1].rstrip()

            #Calls run function to test the input through NFA
            actual_result = nfa.run(test_num)

            #If the expected result matches the actual result set to pass else fail
            if (expect_result == actual_result):
                pass_fail = "pass"
            else:
                pass_fail = "fail"
            
            #String is appended to result
            result += f"TEST INPUT: {test_num} | EXPECTED RESULT: {expect_result} | ACTUAL RESULT: {actual_result} | PASS/FAIL: {pass_fail}\n"
            result += "-----------------------------------------------------------------------------\n\n"
    
    #Overwrites output file with resulting string
    with test_output as file:
        file.write(result)

    print(f"RESULTS CAN NOW BE SEEN IN FILE: out.txt\n")

#TEST_USER_INPUT FUNCTION
# - Takes in user input and determines whether NFA would accept or reject
def test_user_input(nfa):
    user_continue = 'y'
    
    while (user_continue == 'y'):
        user_input = input("Enter test string: ")
        reject_accept = nfa.run(user_input)
        result = f"TEST INPUT: {user_input} | ACCEPT/REJECT: {reject_accept}"

        print(f"{result}\n")

        user_continue = input("Would you like to continue? (y/n): ")
        print("")

#MAIN FUNCTION
# - Defines the decInteger NFA's transitions
# - Defines the decInteger nfa with the NFA class
# - Allows user to test their inputs    
def main():
    
    #Transitions for NFA that recognizes Decinteger values
    dec_oct_hex_float_transitions = {
        #Out transitions for state q0
        'q0':{
            ('1', '2', '3', '4', '5', '6', '7', '8', '9'): {'q1'}
        },

        #Out transitions for state q1
        'q1':{
            ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'): {'q1'},
            '_': {'q2'}
        },

        #Out transitions for state q2
        'q2':{
            ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'): {'q1'},
            'ε': {'q2'}
        }
    }

    #Define NFA that recognizes Decinteger values
    decInteger_nfa = NFA(
        states = ['q0', 'q1', 'q2'],
        alphabet = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '_', 'ε'],
        start_state = 'q0',
        accept_states = ['q1'],
        transitions = decInteger_transitions
    )

    #Prints menu options
    print("==================================")
    print("MENU: \n==================================\n")
    print("----------------------------------")
    print("1 : TEST INPUT FILE")
    print("----------------------------------")
    print("2 : TEST USER INPUT")
    print("----------------------------------")
    print("3: EXIT PROGRAM")
    print("----------------------------------")

    #Stores user's chosen option
    user_input = input("CHOOSE OPTION: ")

    #Infinite while loop
    # - Breaks when user chooses option 3 (quit)
    while True:
        
        #Calls test_input_file function
        if (user_input == '1'):
            test_input_file(decInteger_nfa)

        #Calls test_user_input function
        elif (user_input == '2'):
            test_user_input(decInteger_nfa)

        #Prints confirmation to quit and breaks out of while loop
        elif (user_input == '3'):
            print("\nEXITING PROGRAM...")
            print("THANK YOU FOR TESTING :D")
            break
        
        #Prints error message if option chosen is not on menu
        else:
            print("\nERROR: INVALID OPTION TRY AGAIN\n")

        user_input = input("CHOOSE OPTION: ")

if __name__ == "__main__":
    main()