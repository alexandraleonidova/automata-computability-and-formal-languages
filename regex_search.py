# Alexandra Leonidova
# 13 May 2017


import re, itertools
from itertools import chain, product, combinations
import sys


# BEGINNING OF SECTION WITH THE CODE OF CLASSES USED BY OUR PROGRAM

# This is the object for both NFA's and DFA. Mainly used for NFA troughout the program
class NfaObject:
    def __init__(self, nfa_num_states = 0, nfa_alphabet = "", nfa_transitions = [], nfa_start_state = 0, nfa_accept_states = []):
        self.nfa_num_states = nfa_num_states
        self.nfa_alphabet = nfa_alphabet
        self.nfa_transitions = nfa_transitions
        self.nfa_start_state = nfa_start_state
        self.nfa_accept_states = nfa_accept_states

    # getters
    def getNfaNumStates(self):
        return self.nfa_num_states

    def getNfaAlphabet(self):
        return self.nfa_alphabet

    def getNfaTransitions(self):
        return self.nfa_transitions

    def getNfaStartState(self):
        return self.nfa_start_state

    def getNfaAcceptStates(self):
        return self.nfa_accept_states

    # setters
    def setNfaNumStates(self, new_num_states):
        self.nfa_num_states = new_num_states

    def setNfaAlphabet(self, new_alphabet):
        self.nfa_alphabet = new_alphabet

    def setNfaTransitions(self, new_transitions):
        for x in new_transitions:
            x[0] = str(x[0])
            x[2] = str(x[2])
        self.nfa_transitions = new_transitions

    def setNfaStartState(self, new_start_state):
        self.nfa_start_state = new_start_state

    def setNfaAcceptStates(self, new_accept_states):
        self.nfa_accept_states = new_accept_states

    # Helpers
    def printNfa(self):
        print("__________________________________________")
        print("The parameters of the current NFA are: \n")
        print("The number of states: " + str(self.nfa_num_states))
        print("The alphabet: " + str(self.nfa_alphabet))
        print("The list of stransitions: ")
        for x in self.nfa_transitions:
            print(x)
        print("The start state " + str(self.nfa_start_state))
        print("The set of accepting states" + str(self.nfa_accept_states))
        print("__________________________________________")

    def printNfaToFile(self):
        f = open("nfaTest.txt", "w")
        f.write(str(self.nfa_num_states))
        f.write("\n")
        f.write(str(self.nfa_alphabet))
        f.write("\n")
        for x in self.nfa_transitions:
            f.write(str(int(x[0])) + " " + "\'" + str(x[1]) + "\'" + " " + str(int(x[0])) + "\n")
        f.write("\n")
        f.write(str(self.nfa_start_state))
        f.write("\n")
        for x in self.nfa_accept_states:
            f.write(str(x) + " ")
        f.write("\n")
        f.close()

    def renumberTransitions(self, num):
        for trans in self.nfa_transitions:
            trans[0] = str(int(num) + int(trans[0]))
            trans[2] = str(int(num) + int(trans[2]))

    def renumberAcceptStates(self, num):
        new_as = []
        for state in self.nfa_accept_states:
            new_as.append(state + num)
        self.nfa_accept_states = new_as

    def renumberStartState(self, num):
        self.nfa_start_state += num



# a binary tree class
class BinaryTree:

    def __init__(self, content, leftSubtree = None, rightSubtree = None):
        self.content = content
        self.leftSubtree = leftSubtree
        self.rightSubtree = rightSubtree

    def __repr__(self):
        return str(self.content)


    def __iter__(self):
        return traverse(self)

    def __str__(self):
        return str(self.content)

    def getNodeValue(self):
        return self.content

    def getLeftSubtree(self):
        return self.leftSubtree

    def getRightSubtree(self):
            return self.rightSubtree

# The below implements an post-order traversal of a
# binary tree. A binary tree is assumed to have all children
# larger than a parent node on the right branch of the parent node,
# and all children smaller than the parent node on the left branch
# of the parent node.
def traverse(tree):

    if tree.leftSubtree:
        for n in traverse(tree.leftSubtree):
            yield n
    if tree.rightSubtree:
        for n in traverse(tree.rightSubtree):
            yield n
    yield tree



Node = BinaryTree

# END OF SECTION WITH THE CODE OF CLASSES USED BY OUR PROGRAM

# BEGINNING OF SECTION WITH THE CODE FOR CONVERTING NFA TO DFA

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
# @param nfa_alphabet = alphabet of the NFA
# @param transition_function_list_nfa = list of arrays representing NFA transitions
# @param start_state_nfa = start state of the NFA
# @param accept_states = set of accept states of the NFA
# @return dfa - a dfa that is equivalent to a given NFA
def convertNFAtoDFA(nfa_alphabet, transition_function_list_nfa, start_state, accept_states):
    accept_states_nfa = []
    for x in accept_states:
        accept_states_nfa.append(str(x))
    start_state_nfa = str(start_state)
    dfa = NfaObject()
    # convert the start state to a set containing one item, the nfa start state
    set_of_start_states = set([start_state_nfa])

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

    # The stack is used to keep track of sets of states whose transitions
    # still need to be considered.
    stack = []
    stack.append(set_of_current_states)
    
    # We will keep looking through the NFA states until we have looked through all the possible
    # resulting DFA states
    while ((not done or len(stack) > 0)):
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
                dfa_transition_function_list.append([dfa_states_map[frozenset(set_of_current_states)], letter,
                                                     dfa_states_map[frozenset(set_of_next_states)]])
            else:
                counter = counter + 1  # create a new label for this state
                dfa_states_map[
                    frozenset(set_of_next_states)] = counter  # map a new state to the map of states, dfa_states_map_map

                # add this transition to the DFA list of transitions
                dfa_transition_function_list.append(
                    [dfa_states_map[frozenset(set_of_current_states)], letter,
                     dfa_states_map[frozenset(set_of_next_states)]])

                # push set of next states to the stack so as to consider its transitions in
                # subsequent iterations
                stack.append(set_of_next_states)

                # done is false because we have encountered a new set of states to consider
                done = False

    set_of_accept_states = getSetOfAcceptingStates(dfa_states_map, set(accept_states_nfa))

    dfa.setNfaNumStates(len(dfa_states_map))
    dfa.setNfaAlphabet(nfa_alphabet)
    dfa.setNfaTransitions(dfa_transition_function_list)
    dfa.setNfaStartState(1)
    dfa.setNfaAcceptStates(set_of_accept_states)

    return dfa


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



# @param transition_function_list_nfa is a list of transition functions
# @param letter is the symbol in the alphabet for which transitions are sought
# @param a set of states that can be reached by letter transitions from each of the
# @param in the current_set_of_states
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
            #print(type(transition_function[0]))
            #print(type(list_of_current_states[index]))
            if (transition_function[0] == list_of_current_states[index] and transition_function[1] == letter and transition_function[2] not in set_of_resulting_states):
                set_of_resulting_states.add(transition_function[2])

        index = index + 1

    return sorted(set(set_of_resulting_states))


# @param transition_function_list_nfa =  a list of transition functions
# @param start_state_nfa = the start state
# @param returns a set of states that can be reached by epsilon transitions from the
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

# END OF SECTION WITH THE CODE FOR CONVERTING NFA TO DFA

# BEGINNING OF SECTION THAT SIMULATES DFA

# This methon simulated a dfa on a set of strings and writes the result to an output file
# @param num_states - the number of states in a given NFA
# @param alpha = alphabet of the NFA
# @param array_list = list of arrays representing NFA transitions
# @param start_s = start state of the NFA
# @param accept_s = set of accept states of the NFA
# @param strings - a list of strings to be used for simulation
# @param output_file_name - a name of the file where the result will be stored
def simulateDfa(num_states, alpha, array_list, start_s, accept_s, strings, output_file_name):
    #read a string to analyze
    o = open(output_file_name, "w")

    for curr_word in strings:
        if(curr_word is ""):
            if start_s in accept_s:
                o.write("true\n")
            else:
                o.write("false\n")
        else:
            curr_state = start_s
            for x in curr_word:
                # check if the read symbol is in the alphabet
                if x not in alpha:
                    print("Error: character is not in alphabet")
                    print(x)
                else:
                    # simulating DFA
                    for y in array_list:
                        # if we found a matching state and symbol in the array_list of
                        # transition states, then change states as per the transition
                        # function
                        if ((y[0] == str(curr_state)) and (y[1] == x)):
                            # debug, print(curr_state + "  -" + x + "->  " + y[2])
                            curr_state = y[2]
                            break
            if (int(curr_state) in accept_s):
                o.write("true\n")
            else:
                o.write("false\n")
    f.close()

# END OF SECTION THAT SIMULATES DFA

# This method creates an NFA for a leaf
# @param value = the value of a leaf node
# @param alphabet = the alphabet of the given regular expression
# @return - an NFA equivalent to the given leaf node
def createLeafNFA(value, alphabet):
    local_transitions = []
    local_accept_states = []
    local_state_num = 2
    local_transitions.append(["1", value, "2"])
    local_start_state = 1
    local_accept_states.append(2)
    return NfaObject(local_state_num, alphabet, local_transitions, local_start_state, local_accept_states)

# This method creates an NFA for a star of an NFA
# @param value = the value of a leaf node
# @param alphabet = the alphabet of the given regular expression
# @return - an NFA equivalent to the star of given node
def createStarNFA(orig_nfa, alphabet):
    local_transitions = []
    local_accept_states = []
    local_state_num = 1 + orig_nfa.getNfaNumStates();
    local_start_state = local_state_num

    local_transitions = orig_nfa.getNfaTransitions()
    local_transitions.append([str(local_start_state), "e", str(orig_nfa.getNfaStartState())]) 
    for x in orig_nfa.getNfaAcceptStates():
        local_transitions.append([str(x), "e", str(orig_nfa.getNfaStartState())])

    local_accept_states.append(local_start_state)
    local_accept_states = orig_nfa.getNfaAcceptStates() + local_accept_states
    return NfaObject(local_state_num, alphabet, local_transitions, local_start_state, local_accept_states)

# This method creates an NFA for a union of two NFA's
# @param right_nfa = the NFA object of the first NFA in the union
# @param left_nfa = the NFA object of the second NFA in the union
# @param alphabet = the alphabet of the given regular expression
# @return - an NFA equivalent to the union of the two given NFA's
def createUnionNFA(left_nfa, right_nfa, alphabet):
    local_state_num = 1 + left_nfa.getNfaNumStates() + right_nfa.getNfaNumStates()
    local_start_state = local_state_num

    #leave right nfa transitions as they are, but do renumbering on the left nfs
    left_nfa.renumberStartState(right_nfa.getNfaNumStates())
    left_nfa.renumberTransitions(right_nfa.getNfaNumStates())
    left_nfa.renumberAcceptStates(right_nfa.getNfaNumStates())

    # the new list of transitions is the union of both nfa's transitions, plus e transitions from new start state to old start states
    local_transitions = left_nfa.getNfaTransitions() + right_nfa.getNfaTransitions()
    local_transitions.append([str(local_start_state), "e", str(right_nfa.getNfaStartState())])
    local_transitions.append([str(local_start_state), "e", str(left_nfa.getNfaStartState())])
    local_accept_states = right_nfa.getNfaAcceptStates() + left_nfa.getNfaAcceptStates()
    return NfaObject(local_state_num, alphabet, local_transitions, local_start_state, local_accept_states)

# This method creates an NFA for a concatenation of 2 NFA's
# @param right_nfa = the NFA object of the first NFA in the union
# @param left_nfa = the NFA object of the second NFA in the union
# @param alphabet = the alphabet of the given regular expression
# @return - an NFA equivalent to the concatenation of the two given NFA's
def createConcatenationNFA(left_nfa_temp, right_nfa_temp, alphabet):
    left_nfa = right_nfa_temp
    right_nfa = left_nfa_temp

    local_state_num = left_nfa.getNfaNumStates() + right_nfa.getNfaNumStates()

    #leave left nfa transitions as they are, but do renumbering on the right nfs
    right_nfa.renumberStartState(left_nfa.getNfaNumStates())
    right_nfa.renumberTransitions(left_nfa.getNfaNumStates())
    right_nfa.renumberAcceptStates(left_nfa.getNfaNumStates())
    local_start_state = right_nfa.getNfaStartState()

    #transition states ajustment
    local_transitions = left_nfa.getNfaTransitions() + right_nfa.getNfaTransitions()
    for state in right_nfa.getNfaAcceptStates():
        local_transitions.append([str(state), "e", str(left_nfa.getNfaStartState())])


    local_accept_states = left_nfa.getNfaAcceptStates()

    return NfaObject(local_state_num, alphabet, local_transitions, local_start_state, local_accept_states)

# BEGINNING OF SECTION WITH THE CODE OF METHODS FOR CREATING AN NFA

# This function converts a regular expression tree to NFA
# @regex_tree - a tree representation of the regural expression
# @alphabet - an alphabet of a regular expression
# @return nfa - a result of conversion
def convertTreeToNfa(regex_tree, alphabet):
    conversion_stack  = []
    for regex_node in regex_tree:
        node_value = regex_node.getNodeValue()
        if (isOperand(node_value, alphabet)):
            sub_nfa = createLeafNFA(node_value, alphabet)
            conversion_stack.append(sub_nfa)
        elif (isOperator(node_value)):
            if (node_value is "*"): # unary operator
              if(conversion_stack):
                operand = conversion_stack.pop()
              else:
                return(-1)
              sub_nfa = createStarNFA(operand, alphabet)
              conversion_stack.append(sub_nfa)
            else: #binary operator
              if(conversion_stack):
                  operand_one = conversion_stack.pop() #BUG MAY BE HERE
              else:
                return(-1)
              if(conversion_stack):
                operand_two = conversion_stack.pop()
              else:
                return(-1)
              if (node_value is "|"):
                sub_nfa = createUnionNFA(operand_one, operand_two, alphabet)
                conversion_stack.append(sub_nfa)
              elif (node_value is " "):
                sub_nfa = createConcatenationNFA(operand_one, operand_two, alphabet)
                conversion_stack.append(sub_nfa)
              else:
                print("Error in convertTreeToNfa. Unexpected operand node value: " + str(node_value))
        else:
              print("Error in convertTreeToNfa. Unexpected node value: " + str(node_value))
    if(not conversion_stack):
        return(-1)
    if (len(conversion_stack) != 1):
        print("Error in convertTreeToNfa. Stack has too many items at the end")
        for x in conversion_stack:
            print(x)
            return (-1)
    return(conversion_stack.pop())

# This method inserts spaces in each place of a regular expression where concatenation should be
# @param regex - regular expression
# @param alphabet - the alphabet of the language
# @return - the string with inserted spaces for denoting concat operator
def insertConcatenateSymbols(regex, alphabet):
    previous = " "
    index = -1
    return_string = regex

    for character in regex:
        index += 1
        if previous is " ":
            # this is the first scanned character, so just scan the next
            previous = character
            continue
        elif (isOperand(previous, alphabet) and isOperand(character, alphabet)):
            return_string = return_string[:index] + " " + return_string[index:]
            index += 1
        elif (isOperand(previous, alphabet) and (character is "(")):
            return_string = return_string[:index] + " " + return_string[index:]
            index += 1
        elif ((previous is ")") and isOperand(character, alphabet)):
            return_string = return_string[:index] + " " + return_string[index:]
            index += 1
        elif previous is ")" and character is "(":
            return_string = return_string[:index] + " " + return_string[index:]
            index += 1
        elif previous is "*" and isOperand(character, alphabet):
            return_string = return_string[:index] + " " + return_string[index:]
            index += 1
        elif previous is "*" and character is "(":
            return_string = return_string[:index] + " " + return_string[index:]
            index += 1
        previous = character
    return return_string

# This method determines whether the symbos passed to it is an operand or not
# @param character - a character to be classifyed as operand or not(including e and N)
# @alphabet - the alphabet of the language
# @return True if charactes is operand, else otherwise
def isOperand(character, alphabet):
    if character is " ":
        return False
    elif character in alphabet:
        return True
    elif ((character is "e") or (character is "N")):
        return True
    else:
        return False

# This method determines whether the symbos passed to it is an operator or not
# @param character - a character to be classifyed as operator or not
# @alphabet - the alphabet of the language
# @return True if charactes is operator, else otherwise
def isOperator(character):
    if character in "*| ":
        return True
    else:
        return False

# This method returns presedence for an operator
# @param operator - operator which precedence is to be determined
# @return - integer representing the precedence of an operatot. The bigger the int, the higher is precedence
def precedence(operator):
    if operator is "*":
        return 3
    elif operator is " ":
        return 2
    elif operator is "|":
        return 1
    else:
        return -1 # this operator does not have precedence

# Pop operator from operator from stack and corresponding
# operands from operand stack. Construct a subtree and push it back on the operand stack.
# This method takes care of special cases
# @param operand_stack - a stack containing operands (nodes/subtrees)
# @param operator_stack - a stack containing operators
# @return -1 if a case denoting the illegal expression was encounterred, nothing otherwise
def smartPop(operand_stack, operator_stack):

    node_operand_right = None
    node_operand_left = None
    # if a stack is empty before a pop, then the expression is empty
    if(operator_stack):
        node_operator = operator_stack.pop()
    else:
        return -1

    if (operand_stack):
        node_operand_left = operand_stack.pop()
    else:
        return -1

    if (node_operator is not "*"):
        if (operand_stack):
            node_operand_right = operand_stack.pop()

    # the below takes care of the R | N  = R special case
    if (node_operator is "|"):
        if(node_operand_left is "N"):
            operand_stack.append(BinaryTree(node_operand_right))
        elif(node_operand_right is "N"):
            operand_stack.append(BinaryTree(node_operand_left))
        else: #regular case
            operand_stack.append(BinaryTree(node_operator, node_operand_left, node_operand_right))

    # the below takes care of the R concatenate e = R and R concat N = N special cases
    elif (node_operator is " "):
        if((node_operand_left is "N") or (node_operand_right is "N")):
            operand_stack.append(BinaryTree("N"))
        elif(node_operand_left is "e"):
            operand_stack.append(BinaryTree(node_operand_right))
        elif (node_operand_right is "e"):
            operand_stack.append(BinaryTree(node_operand_left))
        else: # regural case
            operand_stack.append(BinaryTree(node_operator, node_operand_left, node_operand_right))

    elif (node_operator is "*"):
        if(node_operand_left is "N"): #if problem, look here
            operand_stack.append(BinaryTree("e"))
        else: #regular case
            operand_stack.append(BinaryTree(node_operator, node_operand_left))
    else:
        return(-1)

# This method converts a regular expression(read from a file) to a tree
# @param input_file_name - the name of the file that har data for regular expression //WHY IS IT HERE?????
# @param alphabet - an alphabet of a language generated by regular expression
# @param regex - a regular expression in a form of a string
# @return -1 if an error was detected(invalid expression); otherwese, return a tree constructed from regular expression
def convertRegexToTree(input_file_name, alphabet, regex):
    re.sub(' ','',regex)
    regex_temp = ""
    for x in regex:
        if(x is not " "):
            regex_temp += x
    regex = regex_temp

    # we have removed spaces and now will add a space where concatenation symbols are implied
    regex = insertConcatenateSymbols(regex, alphabet)

    operator_stack = []
    operand_stack = []

    for character in regex:
        if isOperand(character, alphabet):
            operand_stack.append(Node(character))
        elif character is "(":
            operator_stack.append("(")

        elif isOperator(character):
            # while operand stack is not empty and precedence of scanned character
            # is greater than precedence of character on top of the stack
            if(not operator_stack):
                u = 1
            else:
                while (operator_stack and operand_stack and precedence(character) <= precedence(operator_stack[len(operator_stack) - 1])):
                    smartPop(operand_stack, operator_stack)
            operator_stack.append(character)

        elif character is ")":
            while (operator_stack and (operator_stack[len(operator_stack) - 1] is not "(")):
                smartPop(operand_stack, operator_stack)
            if(operator_stack):
                read_bracket = operator_stack.pop()
            else:
                return(-1)
        else:
            return(-1)
    # empty the operator stack and create a tree out of it
    while(operator_stack):
        smartPop(operand_stack, operator_stack)
    if(operand_stack):
        return_tree = operand_stack.pop()
    else:
        return(-1)

    return return_tree


if __name__ == '__main__':

    try:
        input_file_name = sys.argv[1]  # first command line argument is regular expression text file
        output_file_name = sys.argv[2]  # second command line argument is a name of the output file

        # read from file and break it into variables
    except FileNotFoundError:
        print("This file does not exist")
        exit()
        # open the file for reading
    f = open(input_file_name, "r")

    # get alphabet
    alphabet = (f.readline()).strip("\n")
    if ('N' or '*' or '|') in alphabet:
        # store to external file
        output_file_name_file = open(output_file_name, "w")
        output_file_name_file.write("Invalid alphabet " + alphabet)
        output_file_name_file.close()
        exit()

    regex = (f.readline()).strip("\n")

    list_of_strings = []

    for curr_word in f:
        curr_word = curr_word.strip()
        list_of_strings.append(curr_word)

    root = convertRegexToTree(input_file_name, alphabet, regex)

    if(root is -1): #root is -1 when an invalid charact is in the regular expression
        # store to external file
        output_file_name_file = open(output_file_name, "w")
        output_file_name_file.write("Invalid expression")
        output_file_name_file.close()
        exit()

    if(regex is "e"):
        finalNfa = NfaObject(1, alphabet, [], 1, [1])
    elif(regex is "N"):
        finalNfa = NfaObject(1, alphabet, [], 1, [])
    else:
        finalNfa = convertTreeToNfa(root, alphabet)

    if(finalNfa is -1): #root is -1 when an invalid charact is in the regular expression
        # store to external file
        output_file_name_file = open(output_file_name, "w")
        output_file_name_file.write("Invalid expression")
        output_file_name_file.close()
        exit()

    finalDfa = convertNFAtoDFA(finalNfa.getNfaAlphabet(), finalNfa.getNfaTransitions(), finalNfa.getNfaStartState(), finalNfa.getNfaAcceptStates())
    simulateDfa(finalDfa.getNfaNumStates(), finalDfa.getNfaAlphabet(), finalDfa.getNfaTransitions(), finalDfa.getNfaStartState(), list(finalDfa.getNfaAcceptStates()), list_of_strings, output_file_name)

