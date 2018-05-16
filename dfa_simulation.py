# Alexandra Leonidova
# Saturday, March 4

import re

# This method asks user for a file name and returns that name to the
# calling method
# @return input_file_name - the name of the input file the usr wants to use
def getFileName():
    try:
        input_file_name = input('Enter the name of the input file describing DFA \n')
        return input_file_name
    except FileNotFoundError:
        print("This file does not exist")
        exit()

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

    return temp

# This method returns the next state of DFA, given its current state
# @param x = scanned symbol
# @paraam curr_state = current state of DFA
# @alpha = alphabet of the DFA
# @array_list = list contayning the arrays, each of which is a transition function of our DFA
# @return = the next state, where DFA has to transit to
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



if __name__ == '__main__':

    input_file_name = getFileName()

    # open the file for reading
    f = open(input_file_name, "r")

    # get number of states
    num_states = f.readline()

    # get alphabet
    alpha = f.readline()

    # this is a regex pattern for recognizing transition functions
    pattern = re.compile("\d* '.' \d*")

    # array_list is a list of transition functions.
    array_list = []

    # array_trans is a transition function that composes a single element of array_list.
    # array_trans[0] is the current state, array_trans[1] is the character read,
    # array_trans[2] is the state that DFA would enter.
    array_trans = []

    # reads transition states and stores them in the array_list, return the last line read
    temp = getTransitionStates(f, array_list)

    #read start state
    start_s = temp.rstrip()

    #read a set of accepting states
    accept_s = f.readline().split()

    for curr_word in f:
        curr_word = curr_word.strip()

        # check if word is an empty string
        if(curr_word is ""):
            if start_s in accept_s: print("Accept")
            else: print("Reject")
        else:
            # move the states forward to the last state
            for x in curr_word:
                final_state = getNextState(x, start_s, alpha, array_list)

            if final_state in accept_s:
                print("Accept")
            else:
                print("Reject")

    # don't forget to close the file
    f.close()

