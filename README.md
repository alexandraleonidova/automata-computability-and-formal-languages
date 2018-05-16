# Automata, Computability & Formal Languages

Automata, Computability and Formal Languages

## Project 1: DFA Simulation

### Description
This program simulates the computation of a DFA on a series of input strings, and reports the results of those computations. It reads input from a file that is specified as the command line argument to the program, and writes output to standard output.

### Build & Run
1. Pull from `master` if you have not done it yet.
2. Open `terminal` (`Command + Space`, then search for "terminal").
3. `cd` into the same directory as where your code for algorithms is stored.
For example, if my code is on the Desktop, then I'll need to use `cd Desktop/automata_computability_and_formal_languages`.
4. Create an input `.txt` file, using the format specifyed in "Input File" Section.
5. Complile and run the program, using `python dfa_simulation.py input_name.txt`

### Input File
Input consists of a description of the DFA to simulate, followed by a series of strings for which the DFA’s computation should be simulated.
The format of the DFA description is as follows:
1. An integer that is the number of states in the DFA. This appears by itself on the first line of input. (In the remainder of the description, each state must be referred to by an integer in the range `[1, 2, ..., n]`, where `n` is the number of states.)
2. The alphabet of the DFA. This appears by itself on the second line of input. Every character in the line (not including the terminating newline character) is a symbol of the alphabet.
3. The transition function of the DFA. There will be one line of input per entry in the transition function table, starting with the third line of input. The format of an entry is
`qa ’c’ qb`
This entry indicates that if the DFA is in state `qa` and the next symbol scanned
is a `c`, then the DFA transitions to `qb`.
`qa` and `qb` must be valid states; that is, `qa ∈ {1,2,...,n}` and `qb ∈ {1,2,...,n}`.
`c` must be in the alphabet, and the single quotes must be present. The entries of the transition function can appear in any order.
4. An integer that is the start state of the DFA. This appears by itself on the first line after the transition function lines.
5. The set of accept states of the DFA. These appear together on the line following the line containing the start state.

Multiple entries on a line are separated by 1 or more whitespace characters. The first entry on a line is preceded by 0 or more whitespace characters, and the last entry on a line is followed by 0 or more whitespace characters (not counting the newline character).
Following the DFA specification are the string inputs to be simulated on the DFA, one string per line. All characters on each line (except the terminating newline character) are part of the input string. The input strings should start on the line following the last line of the DFA specification. They end with the last line of the file.

### Output
The program outputs one line per input string to standard output, and the line contains `Accept` if the DFA accepts the input string, and `Reject` if the DFA rejects the input string.

### Example
If the input file contains
```
6
01
1 ’0’ 4
1 ’1’ 2
2 ’0’ 4
2 ’1’ 3
3 ’0’ 3
3 ’1’ 3
4 ’0’ 4
4 ’1’ 5
5 ’0’ 4
5 ’1’ 6
6 ’0’ 4
6 ’1’ 6
1
36 010101010
111011110
01110011
11111
01010000
```
Correct output for that sample input is
```
Reject
Accept
Accept
Accept
Reject
```
---

## Project 2: NFA to DFA Conversion

### Description
This program converts an NFA to a DFA.
It reads input from a file that is specified as the first command line argument to the program, and write output to a file whose name is specified as the second command line argument to the program.

### Build & Run
1. Pull from `master` if you have not done it yet.
2. Open `terminal` (`Command + Space`, then search for "terminal").
3. `cd` into the same directory as where your code for algorithms is stored.
For example, if my code is on the Desktop, then I'll need to use `cd Desktop/automata_computability_and_formal_languages`.
4. Create an input `.txt` file, using the format specifyed in "Input File" Section.
5. Complile and run the program, using `python nfa_to_dfa_conversion.py input_name.txt output_name.txt`

### Input File
The format of the NFA description is as follows (this is close to the same as the DFA specification in the `Project 1`, except that there can be nondeterminism, epsilon transitions, and a transition does not have to be specified for all state/symbol combinations):
1. An integer that is the number of states in the NFA. This appears by itself on the first line of input. (In the remainder of the description, each state must be referred to by an integer in the range  `[1, 2, ..., n]`, where `n` is the number of states.)
2. The alphabet of the NFA. This appears by itself on the second line of input. Every character in the line (not including the terminating newline character) is a symbol of the alphabet. The alphabet cannot include the letter `e`, as this is reserved for specifying epsilon transitions.
3. The transition function of the NFA. There will be one line of input per possible transition in the transition function, starting with the third line of input. The format of an entry is
`qa ’c’ qb`
This entry indicates that if the NFA is in state `qb` and the next symbol scanned is a `c`, then the NFA can transition to `qb`.` c` can also be the letter `e`, in which case is represents an epsilon transition.
`qa` and `qb` must be valid states; that is, `qa ∈ {1,2,...,n}` and `qb ∈ {1,2,...,n}`. `c` must be in the alphabet or be the letter `e` (representing epsilon), and the single quotes must be present (even for the letter `e`)
The entries of the transition function can appear in any order.
4. A blank line terminates the transition function entries. We need this because we don’t know in advance how many transition function entries there will be.
5. An integer that is the start state of the NFA. This appears by itself on the first line after the transition function lines.
6. The set of accept states of the NFA. These appear together on the line following the line containing the start state.

### Output
The format of the DFA description is as follows (this is the same as for the first programming assignment):
1. An integer that is the number of states in the DFA. This appears by itself on the first line of input. (In the remainder of the description, each state is referred to by an integer in the range `[1, 2, ..., n]`, where `n` is the number of states.)
2. The alphabet of the DFA. This appears by itself on the second line of input. Every character in the line (not including the terminating newline character) is a symbol of the alphabet.
3. The transition function of the DFA. There is one line of input per entry in the transition function table, starting with the third line of input. The format of an entry is
`qa ’c’ qb`
This entry indicates that if the DFA is in state `qb` and the next symbol scanned is a `c`, then the DFA transitions to `qb`. `qa` and `qb` must be valid states; that is, `qa ∈ {1,2,...,n}` and `qb ∈ {1,2,...,n}`.  The entries of the transition function can appear in any order.
4. An integer that is the start state of the DFA.
5. The set of accept states of the DFA.

---

## Project 3: Searching text for string that are in the language of a regular expression

### Description
This program reads an alphabet and a regular expression from a file, and then determine if a series of strings belong to the language of the regular expression.
The input and output files are specified by the user on the command line.

#### Algorithm
1. Convert the regular expression to an equivalent NFA (More on this further down).
2. Convert the NFA into an equivalent DFA, using the algorithm from `Project 2`, but keepinf DFA in memory.
3. For each of the strings, determine if it is in the language of the DFA by simulating the DFA on the string. Simulating the DFA is based on the algorithm from `Project 1`.
4. Write the results to a file, which will have one line per string, indicating if the string is (`true`) or is not (`false`) in the language of the regular expression.

Here is how you will convert the regular expression into an equivalent NFA:
1. Parse the regular expression into an abstract syntax tree. In an abstract syntax tree, the interior nodes represent the operators, and the leaf nodes represent symbols in the alphabet. The children of the interior nodes are the operand(s) of the operator. Here is how you will construct the syntax tree:
(a) Create two initially empty stacks: a operand stack that will contain references to nodes in the syntax tree; and an operator stack that will contain operators (plus the left parenthesis).
(b) Scan the regular expression character by character, ignoring space characters.
2.
i. If a symbol from the alphabet is encountered, then create a syntax tree node containing that symbol, and push it onto the operand stack.
ii. If a left paren is encountered, then push it onto the operator stack.
iii. If an operator (`star`, `union`, or implied `concatenation`) is encountered, then, as long as the stack is not empty, and the top of the stack is an operator is precedence is greater than or equal to the precedence of the operator just scanned, pop the operator off the stack and create a syntax tree node from it (popping its operand(s) off the operand stack), and push the new syntax tree node back onto the operand stack. When either the stack is empty, or the top of the stack is not an operator with precedence greater than or equal to the precedence of the operator just scanned, push the operator just scanned onto the operator stack.
iv. If a right parenthesis is encountered, then pop operators off the operator stack until the left parenthesis is popped off the operator stack. For each operator popped off the stack, create a new syntax tree node from it (popping its operand(s) off the operand stack), and push it onto the operand stack.
(c) Empty the operator stack. For each operator popped off the stack, create a new syntax tree node from it (popping its operand(s) off the operand stack), and push it onto the operand stack.
(d) Pop the root of the syntax tree off of the operand stack.
(e) If any problems are encountered that indicate an invalid expression, then terminate parsing an print the `error` message to the output file as described above.
2. Create an NFA from the abstract syntax tree by doing a depthfirst traversal of the syntax tree. (Remember here that each node of the syntax tree is the root of a subtree that represents a regular expression.) For each node, an NFA is created that is equivalent to the regular expression represented by the subtree rooted at the node. If the node is a leaf node, then we have a base case, and the NFA is straightforward to create. If the node is an interior node (representing an operator), then the NFA is created from the NFA’s of the child nodes.
3. And now you have an NFA equivalent to the regular expression.

### Build & Run
1. Pull from `master` if you have not done it yet.
2. Open `terminal` (`Command + Space`, then search for "terminal").
3. `cd` into the same directory as where your code for algorithms is stored.
For example, if my code is on the Desktop, then I'll need to use `cd Desktop/automata_computability_and_formal_languages`.
4. Create an input `.txt` file, using the format specifyed in "Input File" Section.
5. Complile and run the program, using `python regex_search.py input_name.txt output_name.txt`

### Input File
1. The input file name is the first command line argument.
2. The alphabet of the language appears by itself on the first line of the input file. Every character in the line (not including the terminating newline character, or any space characters) is a symbol of the alphabet. The alphabet cannot include the letter `e`, the letter `N`, the symbol `*`, the symbol `|`, or the left or right parenthesis, as these have specific meanings in the regular expressions. See below for more on the format of regular expressions. (Note: the space character is not allowed to be in the alphabet of the language. This is so that spaces can be put into regular expressions, to improve readability, without being treated as symbols.)
3. A regular expression appears by itself on the second line of the input file. See below for more on the format of regular expressions.
4. Following the regular expressions are a sequence of strings, one per line for the remainder of the input file.

#### Format of the regular expressions
Here is detail on the format of the regular expressions that the program handles.
• The letter `e` represents `ε` (`epsilon`, the `empty string`) in a regular expression.
• The letter `N` reperesents `∅` (the `empty set`) in a regular expression.
• The character `|` represents `∪` (the `union operator`) in a regular expression.
• The character `∗` represents the `star operator` in a regular expression.
• The `concatenation operator` is implied in a regular expression. For example, in the regular expression `(ab∗)(c|ba)` is short for `(a ◦ b∗) ◦ (c|b ◦ a)`.
• Spaces can be embedded in a regular expression to help readability. So, for example, the above regular expression could be written `(a b∗) (c | ba)`.
• Recall that the `star operator` has highest precedence, then `concatenation`, and finally `union`. Parentheses are used to change the order of operation.

### Output
1. The output file name is the second command line argument.
2. The program writes `true` or `false` for each string in the input file, `true` if the string is in the language described by the regular expression, and `false` if not. The output file contains one true or false value per line.
3. If an invalid regular expression is encountered, the program prins `Invalid expression` to the output file on a single line.
