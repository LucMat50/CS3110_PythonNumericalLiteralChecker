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