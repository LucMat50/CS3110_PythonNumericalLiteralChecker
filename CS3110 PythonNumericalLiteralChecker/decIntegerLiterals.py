#CS3110 - FORMAL LANGUAGES AND AUTOMATA
#RECOGNIZING DECINTEGER
#NAME: LUCIA MATURINO INIGUEZ

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

        #Format: { "state": {"symbol": {next_state1, next_state2, ...}}}
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
                return "REJECT"

            # Sets next_states to the next state in the transitions dictionary
            next_states = set()
            for state in current_states:
                if symbol in self.transitions.get(state, {}):
                    next_states.update(self.transitions[state][symbol])

            # Sets current_states to next_states
            current_states = next_states

            # Rejects user's input if no transitions were defined for current symbol (current_state is empty)
            if not current_states:
                return "REJECT"
        
        # If current_states is in accept_state then accept
        if bool(current_states.intersection(self.accept_states)) == True:
            return "ACCEPT"
        # if current_states is not in accept_state then reject
        else: 
            return "REJECT"

#MAIN FUNCTION
# - Defines the decInteger NFA's transitions
# - Defines the decInteger nfa with the NFA class
# - Allows user to test their inputs    
def main():
    
    #Transitions for NFA that recognizes Decinteger values
    decInteger_transitions = {
        #Out transitions for state q0
        'q0':{
            ('1', '2', '3', '4', '5', '6', '7', '8', '9'): {'q1'}
            #'1': {'q1'},
            #'2': {'q1'},
            #'3': {'q1'},
            #'4': {'q1'},
            #'5': {'q1'},
            #'6': {'q1'},
            #'7': {'q1'},
            #'8': {'q1'},
            #'9': {'q1'}
        },

        #Out transitions for state q1
        'q1':{
            ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'): {'q1'},
            #'0': {'q1'},
            #'1': {'q1'},
            #'2': {'q1'},
            #'3': {'q1'},
            #'4': {'q1'},
            #'5': {'q1'},
            #'6': {'q1'},
            #'7': {'q1'},
            #'8': {'q1'},
            #'9': {'q1'},
            '_': {'q2'}
        },

        #Out transitions for state q2
        'q2':{
            ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9'): {'q1'}
            #'0': {'q1'},
            #'1': {'q1'},
            #'2': {'q1'},
            #'3': {'q1'},
            #'4': {'q1'},
            #'5': {'q1'},
            #'6': {'q1'},
            #'7': {'q1'},
            #'8': {'q1'},
            #'9': {'q1'}
        }
    }

    #Define NFA that recognizes Decinteger values
    decInteger_nfa = NFA(
        states = ['q0', 'q1', 'q2'],
        alphabet = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '_'],
        start_state = 'q0',
        accept_states = ['q1'],
        transitions = decInteger_transitions
    )

    # While loop that will allow user to test multiple inputs until they press any other character besides 'y'
    continue_input = 'y'
    while(continue_input == 'y'):

        user_input = input("Enter your value: ")
        print(f"{user_input} : {decInteger_nfa.run(user_input)}")

        continue_input = input("Would you like to continue? Press (y/n): ")
        if continue_input != 'y':
            print("Thank you for testing the decInteger NFA")
            break

if __name__ == "__main__":
    main()