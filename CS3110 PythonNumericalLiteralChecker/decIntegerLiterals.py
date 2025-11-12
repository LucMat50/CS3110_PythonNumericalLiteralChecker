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
        self.start_state = set(start_state)

        #Set of accept states
        self.accept_states = set(accept_states)

        #Format: { "state": {"symbol": {next_state1, next_state2, ...}}}
        self.transitions = set(transitions)

#RUN FUNCTION 
# - Simulates input_string through NFA
# - Returns ACCEPT or REJECT
def run(self, input_string):
    current_states = {self.start_state}

    for symbol in input_string: 
        if symbol not in self.alphabet:
            return False
        
        next_states = set()
        for state in current_states:
            if symbol in self.transitions.get(state, {}):
                next_states.update(self.transitions[state][symbol])
        
        current_states = next_states

        if not current_states:
            return False
        
    if bool(current_states.intersection(self.accept_states)) == True:
        return "ACCEPT"
    else: 
        return "REJECT"