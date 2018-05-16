# April 7, 2017
# Alexandra Leonidova
# Description: This program converts an NFA to a DFA

import re, itertools
from itertools import chain, product, combinations
import sys

# This method populates array_list with the transition functions of the DFA
# @param f - the input file
# @param array_list - a list of arrays, each of which is a transition function of a DFA
# @return temp - the last line read from file
def getTransitionStates(f, array_list):
    #read transition states and store them in the array_list
    temp = f.readline()
    while (pattern.match(temp)):
        temp_t = temp.split(' ')
        array_list.append([temp_t[0], (temp_t[1])[1], temp_t[2].rstrip()])
        temp = f.readline()
    #read an empty line in the end of the transition states
    temp = f.readline()
    return temp

# This method returns the next state of FA, given its current state
# @param x = scanned symbol
# @paraam curr_state = current state of FA
# @alpha = alphabet of the FA
# @array_list = list contayning the arrays, each of which is a transition function of our FA
# @return = the next state, where FA has to transit to
def getNextState(x, curr_state, alpha, array_list):
    
    # check if the read symbol is in the alphabet
    if x not in alpha:
        print("Error: character is not in alphabet")
        print(x)
    else:
        # simulating DFA
        for y in array_list:
            # if we found a matching state and symbol in the array_list of
            # transition states, then change states as per the transition function
            if ((y[0] == curr_state) and (y[1] == x)):
                return y[2]

# This method returns the powerset of an iterable data type
# @ iterable = set of which to return the power set
# @ return = power set of iterable
def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return_list = []
    for x in chain.from_iterable(combinations(s, r) for r in range(len(s)+1)):
        return_list.append(list(x))
    return return_list

# This method consists of a for-loop inside of a while loop that together convert an NFA into a DFA.
# The method then writes the DFA to a file.
# @nfa_alphabet = alphabet of the NFA
# @transition_function_list_nfa = list of arrays representing NFA transitions
# @start_state_nfa = start state of the NFA
# @accept_states_nfa = set of accept states of the NFA
# @output_file_name = name of file to which to write DFA
def convertNFAtoDFA(nfa_alphabet, transition_function_list_nfa, start_state_nfa, accept_states_nfa, output_file_name):

    # convert the start state to a set containing one item, the nfa start state
    set_of_start_states = set(start_state_nfa)
    # add states reachable by epsilon transitions to the set of start states
    set_of_start_states = addEpsilonTransitions(transition_function_list_nfa, set_of_start_states)
    counter = 1 # counter is the label of state numbers for the resulting DFA
    dfa_states_map = {} # a map of "set of states" -> "state number"
    # map the start states to state 1. State 1 is always the start state of the resulting DFA.
    dfa_states_map[set_of_start_states] = counter
    set_of_current_states =  set_of_start_states
    done = False

    # This will be a list of DFA transitions that will be written to the output file.
    dfa_transition_function_list = []
    nfa_alphabet = nfa_alphabet.strip()

    # The stack is used to keep track of sets of states whose transitions
    # still need to be considered.
    stack = []
    stack.append(set_of_current_states)

    # We will keep looking through the NFA states until we have looked through all the possible
    # resulting DFA states
    while((not done or len(stack) > 0)):

        done = True
        set_of_current_states = set(stack.pop())

        for letter in nfa_alphabet:

            set_of_next_states = {}
            set_of_next_states = addLetterTransitions(transition_function_list_nfa, set_of_current_states, letter)
            set_of_next_states = addEpsilonTransitions(transition_function_list_nfa, set_of_next_states)

            # use a "frozenset" here because it is hashable and can be used
            # as a key to a dictionary (map data type)
            if (frozenset(set_of_next_states) in dfa_states_map):
                # If the next state has already been encountered, then add the new transition
                # to the list of DFA transitions. The "value" in key -> value mapping
                # of state -> integer is used as the DFA state number.
                dfa_transition_function_list.append([dfa_states_map[frozenset(set_of_current_states)], letter, dfa_states_map[frozenset(set_of_next_states)]])
            else:
                counter = counter + 1 # create a new label for this state
                dfa_states_map[frozenset(set_of_next_states)] = counter # map a new state to the map of states, dfa_states_map_map

                # add this transition to the DFA list of transitions
                dfa_transition_function_list.append(
                    [dfa_states_map[frozenset(set_of_current_states)], letter, dfa_states_map[frozenset(set_of_next_states)]])

                # push set of next states to the stack so as to consider its transitions in
                # subsequent iterations
                stack.append(set_of_next_states)

                # done is false because we have encountered a new set of states to consider
                done = False

    # store to external file
    output_file_name_file = open(output_file_name, "w")

    output_file_name_file.write(str(len(dfa_states_map)) + "\n")
    output_file_name_file.write(nfa_alphabet + "\n")

    for transition in dfa_transition_function_list:
        output_file_name_file.write(str(transition[0]) + " \'" + str(transition[1]) + "\' " + str(transition[2]) + "\n")

    set_of_accept_states = getSetOfAcceptingStates(dfa_states_map, set(accept_states_nfa))

    output_file_name_file.write(str(1) + "\n")

    for state in set_of_accept_states:
        output_file_name_file.write(str(state) + " ")
    output_file_name_file.write("\n")

# This method takes in a dictionary (a map) of sets of states, compares each
# set of states in the dictionary to the set of accept states, and if the first
# set of states has any states that are in the set of accept states, then this
# first set of states is an accepting set of states.
# @ dictionary_of_states = a map of states, but only the list of states is used here, not the mapped values
# @ set_of_accept_states_nfa = original NFA's set of accept states
# @ return = DFA's set of accept states
def getSetOfAcceptingStates(dictionary_of_states, set_of_accept_states_nfa):

    set_of_accept_states = set()
    for state in dictionary_of_states:
        if (len(state.intersection(set_of_accept_states_nfa)) > 0):
            set_of_accept_states.add(dictionary_of_states[state])

    return set_of_accept_states

# parameter transition_function_list_nfa is a list of transition functions
# parameter letter is the symbol in the alphabet for which transitions are sought
# returns a set of states that can be reached by letter transitions from each of the
# states in the current_set_of_states
def addLetterTransitions(transition_function_list_nfa, current_set_of_states, letter):

    set_of_resulting_states = set()
    list_of_current_states = list(current_set_of_states)
    index = 0

    # For loop would have worked but the while loop makes this similar to
    # the addEpsilonTransitions method implementation.
    while (index < len(list_of_current_states)):

        for transition_function in transition_function_list_nfa:

            # transition_function_nfa is a transition function that composes a single element of array_list.
            # transition_function_nfa[0] is the current state, array_trans[1] is the character read,
            # array_trans[2] is the state that NFA would enter.

            if (transition_function[0] == list_of_current_states[index] and transition_function[1] == letter and transition_function[2] not in set_of_resulting_states):
                set_of_resulting_states.add(transition_function[2])

        index = index + 1

    return sorted(set(set_of_resulting_states))


# @ transition_function_list_nfa =  a list of transition functions
# @ start_state_nfa = the start state
# @ returns a set of states that can be reached by epsilon transitions from the
# start_state_nfa parameter
def addEpsilonTransitions(transition_function_list_nfa, set_of_start_states):

    # search for start state in [0] index of transition function list. If found, check whether index[1] is 'e' and if so,
    # add to the set of start states. After adding, start over from the list again. Return after list has been entirely
    # perused without a new addition.

    list_of_start_states = list(set_of_start_states)
    index = 0

    while (index < len(list_of_start_states)):
        for transition_function in transition_function_list_nfa:
            if (transition_function[0] == list_of_start_states[index] and transition_function[1] == 'e' and transition_function[2] not in list_of_start_states):
                list_of_start_states.append(transition_function[2])
                index = -1 #start iteration from the beginning
                break
        index = index + 1

    return frozenset(sorted(set(list_of_start_states)))

if __name__ == '__main__':

    try:
        input_file_name = sys.argv[1] #first command line argument is dfa text file
        output_file_name = sys.argv[2] #second command line argument is a name of the file where the converted nfa to dfa will be stored

    # read from file and break it into variables
    except FileNotFoundError:
        print("This file does not exist")
        exit()
    # open the file for reading
    f = open(input_file_name, "r")
    # get number of states
    num_states_nfa = int(f.readline())
    
    # get alphabet
    alpha_nfa = f.readline()
    if 'e' in alpha_nfa:
        print("Alphabet cannot contein e, it is reserved for epsilon transition")

    # this is a regex pattern for recognizing transition functions
    pattern = re.compile("\d* '.' \d*")
    
    # transition_function_list_nfa is a list of transition functions.
    transition_function_list_nfa = []
    
    # transition_function_nfa is a transition function that composes a single element of array_list.
    # transition_function_nfa[0] is the current state, array_trans[1] is the character read,
    # array_trans[2] is the state that NFA would enter.
    transition_function_nfa = []
    
    # reads transition states and stores them in the transition_function_list_nfa, return the last line read
    temp = getTransitionStates(f, transition_function_list_nfa)
    
    #read start state
    start_state_nfa = temp.rstrip()
    
    #read a set of accepting states
    accept_states_nfa = f.readline().split()

    convertNFAtoDFA(alpha_nfa, transition_function_list_nfa, start_state_nfa, accept_states_nfa, output_file_name)


# don't forget to close the file
f.close()

