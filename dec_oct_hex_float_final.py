# CS3110 - FORMAL LANGUAGES AND AUTOMATA
# RECOGNIZING DECINTEGER, OCTINTEGER, and HEXINTEGER
# NAME: JEANNETTE RUIZ

# For handling UNION of NFAs and more.
epsilon = 'ε'

# Basic number definitions
digits = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9')
non_zero_digits = ('1', '2', '3', '4', '5', '6', '7', '8', '9')
octal_digits = ('0', '1', '2', '3', '4', '5', '6', '7')
hex_digits = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 
        'a', 'b', 'c', 'd', 'e', 'f', 
        'A', 'B', 'C', 'D', 'E', 'F')

underscore = '_'
period = '.'



#NFA CLASS we can use for all NFAs
class NFA:
    def __init__(self, states, alphabet, transitions, start_state, accept_states):
        # Set of states
        self.states = set(states)

        # Alphabet
        self.alphabet = set(alphabet)

        # Format: { "state": {"symbol": {next_state1, next_state2, ...}}}
        self.transitions = transitions

        # Start state --> most likely q0 for all NFAs
        self.start_state = start_state

        # Set of accept states
        self.accept_states = set(accept_states)



    # Check if symbol in string is in alphabet
    def in_alphabet(self, symbol):
        for a in self.alphabet:
            # (1) Checking if current symbol in str == a CHARACTER in our alphabet
            if symbol == a:
                return True
            # (2) Checking if current symbol in str == a character in a TUPLE in our alphabet
            if isinstance(a, tuple) and symbol in a:
                return True
        # Otherwise, return false
        return False
        


    # Epsilon Closure - Reaching an NFA with epsilon
    # We will return all states that are reachable by epsilon
    def epsilon_closure(self, states):
        # To keep track of the states who HAVE epsilon transitions but have not explored the epsilon transitions yet.
        stack = list(states)
        # To keep track of ALL states we have visited so far.
        closure = set(states)
        
        # Process states until there are no more epsilon transitions
        while stack:
            curr_state = stack.pop()
            # Get the dictionary of transitions from curr_state
            # From this dictionary, get the transitions reachable by EPSILON and place in a set
            for next_state in self.transitions.get(curr_state, {}).get(epsilon, set()):
                # Only adding states we have NOT visited
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
        
        # Return the set of states that ARE reachable by epsilon
        return closure



    # GET_TRANSITION FUNCTION
    # - Goes through tuple in transition dictionary
    # - Returns next state or REJECTS input string if next_state is empty    
    def get_transition(self, state, symbol):

        # Get the OUTgoing transitions for this state.
        state_transitions = self.transitions.get(state, {})

        # Getting all possible next states
        resulting_states = set()

        # Example 1: 'q1' : {'a': {'q2'}}
        # (1) If there is an EXACT-symbol transition, add those next states
        if symbol in state_transitions:
            exact_next = state_transitions[symbol]
            for next_states in exact_next:
                resulting_states.add(next_states)
        
        # Example 2: 'q1' : {digits: {'q2'}} 
        # (So there are MULTIPLE symbol transitions, not just one exact one)
        # (2) Checks transitions where key is tuple containing symbol
        for key, next_states, in state_transitions.items():
            # Skipping epsilon since its a free transition
            if key == epsilon:
                continue
            
            # If our symbol is in a tuple, add those next_states
            if isinstance(key, tuple) and symbol in key:
                for state in next_states: 
                    resulting_states.add(state)
            
        # Returns empty set if no transition is found    
        return resulting_states



    #RUN FUNCTION 
    # - Simulates input_string through NFA
    # - Returns ACCEPT or REJECT
    def run(self, input_string):

        # Set the current state with the start state but handling any possible epsilon transitions
        current_states = self.epsilon_closure({self.start_state})

        # Iterate through each symbol in the input string
        for symbol in input_string: 
            #  If current symbol in string is NOT in the alphabet -> REJECT
            if not self.in_alphabet(symbol):
                return "reject"

            # The set of all states we can go to after reading the current symbol
            next_states = set()

            # Iterate through all states we could be in right now (recall NFA, we can be in multiple states, we split up.)
            for state in current_states:
                # User function get_transition to get transition of our current state
                transition_result = self.get_transition(state, symbol)

                # We will add the new states from our transition_results into next_states
                # Basically unioning them.
                next_states.update(transition_result)

            # After processing all of the possible current states, we will replace this with our next states that we could be in after transitioning.
            current_states = self.epsilon_closure(next_states)

            # If current_states is empty now, meaning there are no possible states AFTER processing this character, we will reject.
            if not current_states:
                return "reject"
        
        # If any of our current states is an accept state, we accept.
        # AKA If any of our transitions lead to an accept state.
        # We are checking the overlap in current states, and accept states.
        if bool(current_states.intersection(self.accept_states)) == True:
            return "accept"
        # Otherwise, if none of our current states are an accept state, we reject.
        else: 
            return "reject"



#############################################################################



#TEST_INPUT_FILE FUNCTION
# - reads through input file and creates string with pass/fail tests
# - outputs in output file
def test_input_file(nfa):
    #Text file with test inputs for decinteger NFA
    test_input = open("in.txt", 'r')

    #Text file where results for the test inputs will be added/overwritten
    test_output = open("out.txt", 'w')

    #Reads through each line of test_input file
    with test_input as file:
        result = "DECINTEGER | OCTINTEGER | HEXINTEGER | FLOATING POINT TEST OUTPUT\n-------------------------------------\n\n"
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

    print(f"RESULTS CAN NOW BE SEEN IN FILE: {test_output}\n")

#############################################################################



#TEST_USER_INPUT FUNCTION
# - Takes in user input and determines whether NFA would accept or reject
# - Outputs user's input, whether NFA accepts or rejects and which NFA specifically would accept
def test_user_input(labeled_nfas):
    # function to recognize nfa but with label
    # Example: ("decinteger", decInteger_nfa)
    #             pair[0]        pair[1]
    
    # To store the labels where the users string was accepted by NFA
    user_continue = 'y'

    while (user_continue == 'y'):

        user_input = input("Enter test string: ")
        accepted_labels = []

        for pair in labeled_nfas:
            label = pair[0]
            nfa_object = pair[1]

            # Run the users string input through NFA
            reject_accept = nfa_object.run(user_input)
            if reject_accept == "accept":
                accepted_labels.append(label)

        # If accepted_labels is empty, it was rejected by all NFA's
        if len(accepted_labels) == 0:
            reject_accept = "reject"
    
        # At this point, at least 1 NFA accepted:
        recognized_nfas = accepted_labels[0]

        # If perchance the label was accepted by more than 1 NFA
        i = 1
        while i < len(accepted_labels):
            recognized_nfas = recognized_nfas + "," + accepted_labels[i]
            i += 1  # apparently there is no i++ in python. Bruh.

        result = f"TEST INPUT: {user_input} | ACCEPT/REJECT: {reject_accept} | NFA(S): {recognized_nfas}"
        print(f"{result}\n")
        user_continue = input("Would you like to continue? (y/n): ")



#############################################################################


#MAIN FUNCTION
# - Defines the decInteger NFA's transitions
# - Defines the decInteger nfa with the NFA class
# - Allows user to test their inputs    
def main():

    # DECINTEGER #########################################
    # (1a) DECinteger transitions
    decInteger_transitions = {
        #Out transitions for state q1
        'q1':{
            non_zero_digits : {'q2'}
        },

        #Out transitions for state q2
        'q2':{
            digits: {'q2'},
            underscore : {'q3'}
        },

        #Out transitions for state q3
        'q3':{
            digits: {'q2'}
        }
    }
    # (1b) DECinteger NFA (states, alphabet, transitions, start state, accept state)
    decInteger_nfa = NFA(
        states = ['q1', 'q2', 'q3'],
        alphabet = [digits, underscore],
        transitions = decInteger_transitions,
        start_state = 'q1',
        accept_states = ['q2']
    )


    # OCTINTEGER #########################################
    # (2a) OCTinteger transitions
    octInteger_transitions = {
        #Out transitions for state q0
        'q4':{
            '0' : {'q5'}
        },

        'q5':{
            ('O', 'o') : {'q6'}
        },

        'q6':{
            underscore : {'q7'},
            epsilon : {'q7'}
        },

        'q7':{
            octal_digits : {'q8'}
        },

        'q8':{
            octal_digits : {'q8'}, # Loop
            underscore : {'q7'}
        }
    }
    # (2b) OCTinteger NFA
    octInteger_nfa = NFA(
        states = ['q4', 'q5', 'q6', 'q7', 'q8'],
        alphabet = [octal_digits, underscore, epsilon, 'o', 'O'],
        transitions = octInteger_transitions,
        start_state = 'q4',
        accept_states = ['q8']
    )

    # HEXINTEGER #########################################
    # (3a) HEXinteger transitions
    hexInteger_transitions = {
        #Out transitions for state q0
        'q9':{
            '0' : {'q10'}
        },

        'q10':{
            ('X', 'x') : {'q11'}
        },

        'q11':{
            underscore : {'q12'},
            epsilon : {'q12'}
        },

        'q12':{
            hex_digits : {'q13'}
        },

        'q13':{
            hex_digits : {'q13'}, # Loop
            underscore : {'q12'}
        }
    }

    # (3b) HEXinteger NFA
    hexInteger_nfa = NFA(
        states = ['q9', 'q10', 'q11', 'q12', 'q13'],
        alphabet = [hex_digits, underscore, epsilon, 'x', 'X'],
        transitions = hexInteger_transitions,
        start_state = 'q9',
        accept_states = ['q13']
    )

    # FLOATING POINT #########################################
    # (4a) Floating point transitions
    floatingPoint_transitions1 = {
        'q15':{
            digits: {'q16'}
        },

        'q16':{
            digits: {'q16'},
            underscore: {'q17'},
            period : {'q18'}
        },

        'q17':{
            digits: {'q16'}
        },

        'q18':{
            digits: {'q21'}
        },

        'q21':{
            digits: {'q21'},
            underscore: {'q22'},
            ('E', 'e'): {'q23'}
        },

        'q23':{
            epsilon : {'q24'},
            ('-', '+'): {'q24'}
        },

        'q24':{
            digits: {'q25'}
        },

        'q25':{
            digits: {'q25'},
            underscore: {'q26'}
        },

        'q26':{
            digits: {'q25'}
        }
    }

    floatingPoint_transitions2 = {
        'q19':{
            period: {'q20'}
        },

        'q20':{
            digits: {'q21'}
        },

        'q21':{
            digits: {'q21'},
            underscore: {'q22'},
            ('E', 'e'): {'q23'}
        },

        'q22':{
            digits: {'q21'}
        },

        'q23':{
            epsilon : {'q24'},
            ('-', '+'): {'q24'}
        },

        'q24':{
            digits: {'q25'}
        },

        'q25':{
            digits: {'q25'},
            underscore: {'q26'}
        },

        'q26':{
            digits: {'q25'}
        }
    }

    # (4b) Floating Point NFA
    floatingPoint_nfa1 = NFA(
        states = ['q14', 'q15', 'q16', 'q17', 'q18', 'q21', 'q23', 'q24', 'q25', 'q26'],
        alphabet = [digits, underscore, epsilon, period, '-', '+', 'e', 'E'],
        transitions = floatingPoint_transitions1,
        start_state = 'q15',
        accept_states = ['q18','q21', 'q25']
    )

    floatingPoint_nfa2 = NFA(
        states = ['q14', 'q19', 'q20', 'q21', 'q22', 'q23', 'q24', 'q25', 'q26'],
        alphabet = [digits, underscore, epsilon, period, '-', '+', 'e', 'E'],
        transitions = floatingPoint_transitions2,
        start_state = 'q19',
        accept_states = ['q21', 'q25']
    )

    # Pairs of NFAS we have created in file
    pairs = [
                ("decinteger", decInteger_nfa),
                ("octinteger",  octInteger_nfa),
                ("hexinteger",  hexInteger_nfa),
                ("floating point", floatingPoint_nfa1),
                ("floating point", floatingPoint_nfa2)
            ]
    
    # PRINT MENU
    print("==================================")
    print("MENU: \n==================================\n")
    print("----------------------------------")
    print("1 : TEST INPUT FILE")
    print("----------------------------------")
    print("2 : TEST USER INPUT")
    print("----------------------------------")
    print("3: EXIT PROGRAM")
    print("----------------------------------")

    user_input = input("CHOOSE OPTION: ")
    
    while True:

        if (user_input == '1'):
            test_input_file(decInteger_nfa)

        elif (user_input == '2'):
            label = test_user_input(pairs)
            #print("RESULT: ", label)

        elif (user_input == '3'):
            print("\n EXITING PROGRAM")
            print("THANK YOU FOR TESTING :D")
            break

        else:
            print("\nERROR: INVALID OPTION TRY AGAIN")

        user_input = input("CHOOSE OPTION: ")

if __name__ == "__main__":
    main()