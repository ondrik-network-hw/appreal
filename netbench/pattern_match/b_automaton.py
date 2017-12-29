###############################################################################
#  b_automaton.py: Module for PATTERN MATCH - base virtual automaton class
#  Copyright (C) 2010 Brno University of Technology, ANT @ FIT
#  Author(s): Vlastimil Kosar <ikosar@fit.vutbr.cz>
###############################################################################
#
#  LICENSE TERMS
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions
#  are met:
#  1. Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#  2. Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in
#     the documentation and/or other materials provided with the
#     distribution.
#  3. All advertising materials mentioning features or use of this software
#     or firmware must display the following acknowledgement:
#
#       This product includes software developed by the University of
#       Technology, Faculty of Information Technology, Brno and its
#       contributors.
#
#  4. Neither the name of the Company nor the names of its contributors
#     may be used to endorse or promote products derived from this
#     software without specific prior written permission.
#
#  This software or firmware is provided ``as is'', and any express or implied
#  warranties, including, but not limited to, the implied warranties of
#  merchantability and fitness for a particular purpose are disclaimed.
#  In no event shall the company or contributors be liable for any
#  direct, indirect, incidental, special, exemplary, or consequential
#  damages (including, but not limited to, procurement of substitute
#  goods or services; loss of use, data, or profits; or business
#  interruption) however caused and on any theory of liability, whether
#  in contract, strict liability, or tort (including negligence or
#  otherwise) arising in any way out of the use of this software, even
#  if advised of the possibility of such damage.
#
#  $Id$

import nfa_data
import b_automaton
import b_state
import copy
from b_ptrn_match import b_ptrn_match
import sym_char
import sym_char_class
import sym_kchar
import b_symbol
import random
import pattern_exceptions
import aux_func

# import general python modules
from collections import deque

class b_Automaton(b_ptrn_match):
    """
        A base class for the pattern matching approaches based on finite automaton.
    """
    def __init__(self):
        """
            Constructor    - inits object atributes:
            _automaton     - Automaton data
            _mapper        - Used to map state to (symbol, target) list
            _statistic     - Dictionary of statistic informations
            _compute       - Flag call to compute()
            _multilanguage - Is automaton multilanguage? Determinates behavior\
                             of automata minimisation and reduction methods.  \
                             If set to True, methods preserves relation       \
                             between final states and coresponding regular    \
                             expresions (languages). If set to False, methods \
                             works exactly by their definitions - final states\
                             are joined if possible. Default value is True.
        """
        b_ptrn_match.__init__(self)
        self._automaton = nfa_data.nfa_data() # Automaton data
        self._mapper = None                   # Used to map state to (symbol, target) list
        self._statistic = dict()              # Dictionary of statistic informations
        self._compute = False                 # Flag call to compute()
        self._multilanguage = True            # See above.

    def set_multilanguage(self, value):
        """
            Sets value of _multilanguage attribute. Determinates behavior     \
            of automata minimisation and reduction methods. If set to True,   \
            methods preserves relation between final states and coresponding  \
            regular expresions (languages). If set to False, methods works    \
            exactly by their definitions - final states are joined if possible.

            :param value: New value of the _multilanguage attribute.
            :type value: boolean
        """
        self._multilanguage = value

    def get_multilanguage(self):
        """
            Returns value of _multilanguage attribute. Determinates behavior  \
            of automata minimisation and reduction methods. If set to True,   \
            methods preserves relation between final states and coresponding  \
            regular expresions (languages). If set to False, methods works    \
            exactly by their definitions - final states are joined if possible.

            :returns: Value of the _multilanguage attribute.
            :rtype: boolean
        """
        return self._multilanguage

    def show(self, fileName, sizeStr=" size=\"8,5\"\n"):
        """
            Save graphviz dot file, representing graph of automaton.

            :param fileName: Name of file into which nfa_data graphical representation will be saved.
            :type fileName: string
            :param sizeStr: Size of resulting image. Set to " " to set unbounded dimensions. Format of this parameter is / size="x,y"\\n/ to set width to x inches and height to y inches.
            :type sizeStr: string
            :returns: True if success, False otherwise.
            :rtype: boolean
        """
        self._automaton.show(fileName, sizeStr)

    def create_from_nfa_data(self, nfa, safe = True):
        """
            Create automaton from nfa_data object.

            :param nfa: nfa_data object, from which automaton is created.
            :type nfa: nfa_data
            :param safe: If True perform deep copy, otherwise set reference. Default value is True.
            :type safe: boolean

            This method sets _compute to False, and get_compute() will return False until compute() is called.
        """
        if safe:
            self._automaton = copy.deepcopy(nfa)
        else:
            self._automaton = nfa

        self._compute = False

    def create_by_parser(self, nfa_parser_class):
        """
            This function is used to create automaton from set of regular expressions.

            :param nfa_parser_class: An instation of nfa_parser class.
            :type nfa_parser_class: nfa_parser
            :returns: False if creation of automaton failed or True if creation was successful.
            :rtype: boolean

            This method sets _compute to False, and get_compute() will return False until compute() is called.
        """
        # Check if there are some regular expressions to parse.
        if nfa_parser_class.num_lines == 0:
            return False

        self._automaton = None
        while self._automaton == None:
            # get an automaton from nfa parser
            self._automaton = nfa_parser_class.get_nfa()
            if self._automaton == None:
                if nfa_parser_class.next_line() == False:
                    break

        # Check if we got the automaton
        if self._automaton == None:
            return False

        # Check if we have more than 1 regular expression
        if nfa_parser_class.num_lines > 1:
            # If there are, parse them
            while nfa_parser_class.next_line() == True:
                # get an automaton from nfa parser
                nfa = nfa_parser_class.get_nfa()
                # Check if we got the automaton
                if nfa == None:
                    print("WARNING: Regular expresion can't be parsed.")
                else:
                    # Join current automaton with parsed one
                    self.join(nfa, False)
            return True
        else:
            return True

        self._compute = False

    def get_automaton(self, safe = True):
        """
            Return nfa_data object from the automaton.

            :param safe: If True return deep copy, otherwise return reference. Default value is True.
            :type safe: boolean
            :returns: nfa_data object from the automaton.
            :rtype: nfa_data

            Warning: If safe=False is used, the result should be used as       \
            read-only (Only reference on self._automaton object is returned).  \
            Otherwise it can cause undefined behavior!
        """
        if safe:
            return copy.deepcopy(self._automaton)
        else:
            return self._automaton

    def join(self, nfa, modify_reg_exp_num = False):
        """
            Join two automata. Joins current automaton with second. Current automaton is modified.

            :param nfa: nfa_data object which contains second automaton.
            :type nfa: nfa_data
            :param modify_reg_exp_num: if set to True, regular expression numbers in final states are modified to not collide with current automaton numbers. The formula is NEW_NUMBER = MAX_CURRENT_NUMBER + OLD_NUMBER + 1. If set to False, regular expression numbers in final states are uneffected.
            :type modify_reg_exp_num: boolean
            :Flags: Sets flags Deterministic and Epsilon Free to False.

            This method sets _compute to False, and get_compute() will return False until compute() is called.
        """
        # Find max state number
        #max_state_num = self._automaton.start
        #for i in self._automaton.states.keys():
            #if self._automaton.states[i].get_id() > max_state_num:
                #max_state_num = self._automaton.states[i].get_id()
        #max_state_num += 1
        max_state_num = max(self._automaton.states.keys()) + 1

        # Creates mapping between alphabet char and its number. Also find max alphabet number.
        alphabetBack = dict()
        max_alphabet_num = -1
        for i in self._automaton.alphabet.keys():
            alphabetBack[self._automaton.alphabet[i]] = self._automaton.alphabet[i].get_id()
            if self._automaton.alphabet[i].get_id() > max_alphabet_num:
                max_alphabet_num = self._automaton.alphabet[i].get_id()
        max_alphabet_num += 1

        # Creates new states for states of second automaton.
        for i in nfa.states.keys():
            self._automaton.states[max_state_num + nfa.states[i].get_id()] = b_state.b_State(max_state_num + nfa.states[i].get_id(), nfa.states[i].get_regexp_number())

        # dictionary for transforming the alphabet.
        transform_alphabet = dict()

        # Join two alphabets, modify alphabet numbers if needed.
        for i in nfa.alphabet.keys():
            # If char is in current alphabet, just add to transformation dictionary.
            if alphabetBack.has_key(nfa.alphabet[i]) == True:
                transform_alphabet[i] = alphabetBack[nfa.alphabet[i]]
            else:
                # If not, add to current alphabet and add to transformation dictionary.
                self._automaton.alphabet[max_alphabet_num] = copy.deepcopy(nfa.alphabet[i])
                self._automaton.alphabet[max_alphabet_num]._id = max_alphabet_num
                alphabetBack[self._automaton.alphabet[max_alphabet_num]] = self._automaton.alphabet[max_alphabet_num].get_id()
                transform_alphabet[i] = alphabetBack[nfa.alphabet[i]]
                max_alphabet_num += 1

        # Add transitions from second automaton to current one. Modify state and alphabet numbers.
        for transition in nfa.transitions:
            self._automaton.transitions.add((max_state_num + transition[0], transform_alphabet[transition[1]], max_state_num + transition[2]))


        # Create new start state
        if isinstance(self._automaton.start, set) or isinstance(self._automaton.start, frozenset):
            old_start_id = self._automaton.start
        else:
            old_start_id = set([self._automaton.start])
        if isinstance(nfa.start, set) or isinstance(nfa.start, frozenset):
            other_start_id = nfa.start
        else:
            other_start_id = set([nfa.start])
        max_id_s = max(self._automaton.states) + 1
        self._automaton.states[max_id_s] = b_state.b_State(max_id_s, set())
        self._automaton.start = max_id_s
        # Add epsilon transition from new start state to old start state of second automaton.
        for oss in other_start_id:
            self._automaton.transitions.add((max_id_s, -1, max_state_num + oss))
        # Add epsilon transition from new start state to old start state of current automaton.
        for oss in old_start_id:
            self._automaton.transitions.add((max_id_s, -1, oss))

        # If reg. exp. numbers should be modified, find max reg. exp. number.
        if modify_reg_exp_num == True:
            max_rnum = -1
            rnums = set()
            for state in self._automaton.final:
                rnums |= self._automaton.states[state].get_regexp_number()
            max_rnum = max(rnums)
            max_rnum += 1

        # Add final states from second automaton, modify reg. exp. numbers if needed.
        for state in nfa.final:
            self._automaton.final.add(max_state_num + state)
            if modify_reg_exp_num == True:
                rnums = self._automaton.states[max_state_num + state].get_regexp_number()
                new_rnums = set()
                for rnum in rnums:
                    new_rnums.add(rnum + max_rnum)
                self._automaton.states[max_state_num + state].set_regexp_number(new_rnums)

        # Check if epsilon symbol exist
        try:
            dummy_val = self._automaton.alphabet[-1]
        # Otherwise create epsilon symbol
        except Exception:
            Tmp = sym_char.b_Sym_char("Epsilon", "",-1)
            self._automaton.alphabet[Tmp.get_id()] = Tmp

        # Clear flags.
        self._automaton.Flags["Deterministic"] = False
        self._automaton.Flags["Epsilon Free"] = False
        self._compute = False

    def epsilon_closure(self, state, StateOutSymbols):
        """
            Compute epsilon closure for selected state.

            :param state: State from which epsilon closure is computed.
            :type state: int
            :param StateOutSymbols: Mapping between states and their transitions.
            :type StateOutSymbols: dict(int, tuple(int, int))
            :returns: Set containing epsilon closure for state.
            :rtype: set(int)
        """
        Stack = list()

        #Specified state is first state to be processed
        Stack.append(state)

        Closure = set()
        while len(Stack) != 0 :         #Until there are states to be processed
            ActState = Stack.pop()      #Pick one of them
            if ActState in Closure:
                continue
            Closure.add(ActState)       #and add it into the eps closure set

            #If there are any outgoing transition from this state
            if ActState in StateOutSymbols.keys():

                #and if there is epsilon outgoing transition
                #Add all targets of eps transitions into stack for the further
                #processing
                for trans in StateOutSymbols[ActState]:
                    if trans[0] == -1:
                        Stack.append(trans[1])

        return Closure

    def remove_epsilons(self):
        """
            Remove all epsilon transitions from automaton. Also removes all isolated, unreachable and blind states.

            :Flags: Sets flag Epsilon Free to True.

            This method sets _compute to False, and get_compute() will return False until compute() is called.
        """

        # Dictionary mapping between states and their transitions.

        StateOutSymbols = dict()

        # Compute the mapping between states and their transitions.
        for transition in self._automaton.transitions:
            if StateOutSymbols.has_key(transition[0]) == True:
                StateOutSymbols[transition[0]].add((transition[1], transition[2]))
            else:
                StateOutSymbols[transition[0]] = set()
                StateOutSymbols[transition[0]].add((transition[1], transition[2]))

        # For all states remove epsilon transitions.
        for state in StateOutSymbols.keys():
            Clos = self.epsilon_closure(state, StateOutSymbols) # compute eps closure for the state
            Clos.remove(state)                  # Outgoing trans from specific state
                                                # do not have to be transformed (they
                                                # are already in right state)

            #If there is an intersection of closure and endStates, add current state to end states and update reg. exp. number.
            interEnd = Clos.intersection(self._automaton.final)
            if len(interEnd) != 0:
                for fstate in interEnd:
                    self._automaton.states[state].set_regexp_number(self._automaton.states[state].get_regexp_number() | self._automaton.states[fstate].get_regexp_number())
                self._automaton.final.add(state)

            if len(Clos) != 0:                # If there are any other states
                for St in Clos:
                    #Tests if St has any outgoing transition
                    if St in StateOutSymbols.keys():
                        #Test all of their outgouing transitions, add new transitions, update StateOutSymbols
                        for transition in StateOutSymbols[St]:
                            self._automaton.transitions.add((state, transition[0], transition[1]))
                            if StateOutSymbols.has_key(state) == True:
                                StateOutSymbols[state].add((transition[0], transition[1]))
                            else:
                                StateOutSymbols[state] = set()
                                StateOutSymbols[state].add((transition[0], transition[1]))

        # select all eps transitions
        epsTransitions = set()
        for transition in self._automaton.transitions:
            if transition[1] == -1:
                epsTransitions.add(transition)

        # remove all eps transitions
        for transition in epsTransitions:
            self._automaton.transitions.remove(transition)

        # remove eps char from alphabet
        if self._automaton.alphabet.has_key(-1):
            del self._automaton.alphabet[-1]

        # Also removes all isolated, unreachable and blind states.
        self.remove_unreachable()

        # Set flags
        self._automaton.Flags["Epsilon Free"] = True
        self._compute = False

    def remove_unreachable(self):
        """ Removes isolated, unreachable and blind states.

            This method sets _compute to False, and get_compute() will return False until compute() is called.

        """
        # TODO: change name to remove_unnecessary_states
        # set of states from which final state can be reached
        ending_prev = set()
        ending_current = self._automaton.final.copy()

        # set of states which can be reached from start state
        start_prev = set()
        start_current = set()

        # handle multiple start states
        if isinstance(self._automaton.start, set):
            start_current = self._automaton.start.copy()
        else:
            start_current.add(self._automaton.start)

        # create mapping from start to end state of transition
        mapper = dict()
        # create mapping from end to start state of transition
        mapper_rev = dict()
        for trans in self._automaton.transitions:
            if mapper_rev.has_key(trans[2]) == True:
                mapper_rev[trans[2]].add(trans[0])
            else:
                mapper_rev[trans[2]] = set()
                mapper_rev[trans[2]].add(trans[0])

            if mapper.has_key(trans[0]) == True:
                mapper[trans[0]].add(trans[2])
            else:
                mapper[trans[0]] = set()
                mapper[trans[0]].add(trans[2])

        # if state doesn't have ingress or outgress transition set coresponding mapper to empty set
        for state in self._automaton.states.keys():
            if mapper_rev.has_key(state) == False:
                mapper_rev[state] = set()
            if mapper.has_key(state) == False:
                mapper[state] = set()

        # compute set of states from which some final state can be reached
        while len(ending_prev) != len(ending_current):
            ending_prev = ending_current.copy()

            for state in ending_prev:
                ending_current |= mapper_rev[state]

        # compute set of states which can be reached from start state
        while len(start_prev) != len(start_current):
            start_prev = start_current.copy()

            for state in start_prev:
                start_current |= mapper[state]


        # remove all states and coresponding transitions which are not in both sets

        # set of removeable states
        remove = set()
        remove = set(self._automaton.states.keys()) - (start_current & ending_current)

        # Set of removeable transitions.
        removeableTrans = set()

        # Remove removeable states, remove them from final states if needed.
        for state in remove:
            del self._automaton.states[state]
            if state in self._automaton.final:
                self._automaton.final.remove(state)
            if isinstance(self._automaton.start, set):
                if state in self._automaton.start:
                    self._automaton.start.discard(state)
                if len(self._automaton.start) == 0:
                    self._automaton.start = -1
            else:
                if state == self._automaton.start:
                    self._automaton.start = -1

        # Add removeable transitions to theirs set.
        for trans in self._automaton.transitions:
            if trans[0] in remove:
                removeableTrans.add(trans)
            if trans[2] in remove:
                removeableTrans.add(trans)

        # Remove removeable transitions.
        for trans in removeableTrans:
            self._automaton.transitions.remove(trans)

        # Remove unused symbols
        all_symbols = set(self._automaton.alphabet.keys())
        used_symbols = set()

        for transition in self._automaton.transitions:
            used_symbols.add(transition[1])

        removeable_symbols = all_symbols - used_symbols

        for symbol in removeable_symbols:
           del self._automaton.alphabet[symbol]

        self._compute = False

    def search(self, input_string):
        """
            This function will find patterns in the given string by the specified approach. This default version uses nfa_data for it. Approaches should reimplement this function.

            :param input_string: Input string.
            :param input_string: string
            :returns: Bitmap of matched regular expressions.
            :rtype: list(int)
        """
        # Stack of states. State is list (tupple) consisting of state and unprocessed part of input string.
        Stack = list()
        # Set of actual states.
        ActState = set()

        # Create start state.
        ActState.add((self._automaton.start, input_string))
        # Add start state to stack.0
        Stack.append(ActState)

        # Create mapping between reg. exp. number and coresponding final states.
        sameFinal = dict()
        for fstate in self._automaton.final:
            rnums = self._automaton.states[fstate].get_regexp_number()
            for rnum in rnums:
                if sameFinal.has_key(rnum) == True:
                    sameFinal[rnum].add(fstate)
                else:
                    sameFinal[rnum] = set()
                    sameFinal[rnum].add(fstate)

        # Compute number of reg. exp.
        rules = len(sameFinal)
        # dictionary is no longer needed.
        sameFinal = None

        # Init bitmap to zeros.
        bitmap = [0] * rules

        # If needed create mapping between states and outgoing transitions.
        if self._mapper == None:
            self._mapper = dict()
            for transition in self._automaton.transitions:
                if self._mapper.has_key(transition[0]) == True:
                    self._mapper[transition[0]].add((transition[1], transition[2]))
                else:
                    self._mapper[transition[0]] = set()
                    self._mapper[transition[0]].add((transition[1], transition[2]))

        # Until stack is empty, search
        while len(Stack) != 0:
            # Pop state from stack.
            ActState = Stack.pop()
            newActState = set()
            # Create new state. Accept char if possible and add state to new state.
            for state in ActState:
                if self._mapper.has_key(state[0]):
                    for transition in self._mapper[state[0]]:
                        try:
                            res = self._automaton.alphabet[transition[0]].accept(state[1])
                        except:
                            pass
                        else:
                            newActState.add((transition[1],res))
                # If in final state, set coresponding bitmap field to 1.
                if self._automaton.states[state[0]].is_final() == True:
                    for rnum in self._automaton.states[state[0]].get_regexp_number():
                        bitmap[rnum] = 1
            # If possible add new state to stack.
            if len(newActState) > 0:
                Stack.append(newActState)

        # Return bitmap.
        return bitmap

    def remove_char_classes(self):
        """
            Remove char classes from automaton. Removed char classes are substituted with equivalent chars and coresponding transitions are added.

            :Flags: Sets Alphabet collision free flag to True

            This method sets _compute to False, and get_compute() will return False until compute() is called.
        """

        # Dict for mapping from chars to their numbers.
        charDict = dict()

        # Alphabet without character classes is collision free.
        self._automaton.Flags["Alphabet collision free"] = True

        # Find max index of alphabet chars. Create mapping from chars to their numbers.
        maxIndex = -1
        for symbol in self._automaton.alphabet.keys():
            if self._automaton.alphabet[symbol].get_type() == b_symbol.io_mapper["b_Sym_char"]:
                charDict[self._automaton.alphabet[symbol]] = symbol
            if self._automaton.alphabet[symbol].get_type() == b_symbol.io_mapper["b_Sym_kchar"]:
                charDict[self._automaton.alphabet[symbol]] = symbol
            #print(str(type(symbol)) + " - " + str(symbol))
            if symbol > maxIndex:
                maxIndex = symbol
        maxIndex += 1

        #print(str(charDict.keys()))

        # Set for removeable transitions.
        removeTransSet = set()
        # Set for added transitions.
        addTransSet = set()

        removeSymbolSet = set()

        # For all transitions remove transitions with char class symbol and add coresponding transitions with char symbols.
        for transition in self._automaton.transitions:
            # if symbol is char class.
            if self._automaton.alphabet[transition[1]].get_type() == b_symbol.io_mapper["b_Sym_char_class"]:
                # For all chars in char class.
                for char in self._automaton.alphabet[transition[1]].charClass:
                    # Create new char.
                    sym = sym_char.b_Sym_char(char, char, maxIndex)
                    # If new char is not in alphabet, add new char to alphabet and get index.
                    if charDict.has_key(sym) == False:
                        self._automaton.alphabet[maxIndex] = sym
                        charDict[sym] = maxIndex
                        maxIndex += 1
                        index = maxIndex - 1
                    else:
                        # Otherwise get index.
                        index = charDict[sym]
                    # Add transition with this char.
                    addTransSet.add((transition[0], index, transition[2]))
                    #print("ADD: " + str((transition[0], index, transition[2])))
                # Remove transition with char class. This transition was replaced with coresponding transitions with char symbols.
                removeTransSet.add(transition)
                #print("REMOVE: " + str(transition))
            # Remove char classes for strided automaton
            if self._automaton.alphabet[transition[1]].get_type() == b_symbol.io_mapper["b_Sym_kchar"]:
                # Check if symbol contains some char class
                is_class = False
                for i in range(0, len(self._automaton.alphabet[transition[1]].kchar)):
                    if isinstance(self._automaton.alphabet[transition[1]].kchar[i], frozenset):
                        is_class = True
                # If symbol contains some char class, remove them
                if is_class == True:
                    # Get all posible strings from kchar
                    all_kchar_str = self._automaton.alphabet[transition[1]]._get_texts()
                    # From each string one new kchar will be created
                    for kchar_str in all_kchar_str:
                        # Create representation of kchar
                        kchar = list()
                        for char in kchar_str:
                            kchar.append(char)
                        # Create it's description - will be printed when graph is created
                        description = "{" + kchar_str + "}"
                        # Create final representation of kchar
                        kchar = tuple(kchar)
                        # Create new kchar symbol
                        new_symbol = sym_kchar.b_Sym_kchar(description, kchar, maxIndex)
                        # If new kchar is not in alphabet, add new char to alphabet and get index.
                        if charDict.has_key(new_symbol) == False:
                            self._automaton.alphabet[maxIndex] = new_symbol
                            charDict[new_symbol] = maxIndex
                            maxIndex += 1
                            index = maxIndex - 1
                        else:
                            # Otherwise get index.
                            index = charDict[new_symbol]
                        # Add transition with this char.
                        addTransSet.add((transition[0], index, transition[2]))
                        #print("ADD: " + str((transition[0], index, transition[2])))
                    # Remove transition with char class. This transition was replaced with coresponding transitions with char symbols.
                    removeTransSet.add(transition)
                    removeSymbolSet.add(transition[1])


        #print(str(self._automaton.alphabet))
        # Remove transitions.
        for transitions in removeTransSet:
            self._automaton.transitions.remove(transitions)

        # Add transitions.
        for transitions in addTransSet:
            self._automaton.transitions.add(transitions)

        # Add char class symbols to removeable symbols set.
        for symbol in self._automaton.alphabet.keys():
            if self._automaton.alphabet[symbol].get_type() == b_symbol.io_mapper["b_Sym_char_class"]:
                removeSymbolSet.add(symbol)

        # Remove char class symbols from alphabet.
        for symbol in removeSymbolSet:
            del self._automaton.alphabet[symbol]

        self._compute = False

    def create_char_classes(self):
        """
            Creates char classes, if they can be created. Replaced transitions are removed. Unused symbols are removed after creation of char classes.

            :Flags: Sets Alphabet collision free flag to False

            This method sets _compute to False, and get_compute() will return False until compute() is called.
        """

        # Alphabet with character classes can have collisions
        self._automaton.Flags["Alphabet collision free"] = False
        print "Size of alphabet before " + str(len(self._automaton.alphabet))
        # Mapping between start and end state of transition and coresponding transitions.
        stateTupple = dict()
        for transition in self._automaton.transitions:
            if stateTupple.has_key((transition[0], transition[2])) == True:
                stateTupple[(transition[0], transition[2])].add(transition)
            else:
                stateTupple[(transition[0], transition[2])] = set()
                stateTupple[(transition[0], transition[2])].add(transition)

        # Find max alphabet index.
        maxIndex = -1
        for symbol in self._automaton.alphabet.keys():
            if symbol > maxIndex:
                maxIndex = symbol
        maxIndex += 1

        symbolDict = dict()

        # For all state tupple pairs perform creation of char classes.
        for key in stateTupple.keys():
            # If transition between states exist, continue.
            if len(stateTupple[key]) > 0:
                # Set of symbols.
                symbolSet = set()
                # List of kchar sets
                symbolList = list()
                if self._automaton.Flags.has_key("Stride") and self._automaton.Flags["Stride"] > 1:
                    for i in range(0, self._automaton.Flags["Stride"]):
                        symbolList.append(set())
                # Set this flag if epsilon or PCRE counting constraint was encountered
                is_epsilon = False
                is_cnt_str = False
                # Find all symbols on transitions between the states.
                for transition in stateTupple[key]:
                    # Do not process epsilons
                    if transition[1] != -1:
                        # If symbol is char class, add all chars.
                        if self._automaton.alphabet[transition[1]].get_type() == b_symbol.io_mapper["b_Sym_char_class"]:
                            symbolSet |= self._automaton.alphabet[transition[1]].charClass
                        # If symbol is char, add char.
                        if self._automaton.alphabet[transition[1]].get_type() == b_symbol.io_mapper["b_Sym_char"]:
                            symbolSet.add(self._automaton.alphabet[transition[1]].char)
                        if self._automaton.alphabet[transition[1]].get_type() == b_symbol.io_mapper["b_Sym_kchar"]:
                            for i in range(0, len(self._automaton.alphabet[transition[1]].kchar)):
                                if isinstance(self._automaton.alphabet[transition[1]].kchar[i], frozenset):
                                    symbolList[i] |= self._automaton.alphabet[transition[1]].kchar[i]
                                else:
                                    symbolList[i].add(self._automaton.alphabet[transition[1]].kchar[i])
                        if self._automaton.alphabet[transition[1]].get_type() == b_symbol.io_mapper["b_Sym_cnt_constr"]:
                            is_cnt_str = True
                        # Remove transition.
                        self._automaton.transitions.remove(transition)
                    else:
                        is_epsilon = True
                # If more than one char symbol exist, add char class.
                if len(symbolSet) > 1:
                    # Create char class name.
                    strSymSetMod = str()
                    for sym in symbolSet:
                        strSymSetMod += sym
                    strSymSetMod = "[" + strSymSetMod + "]"
                    # Create char class.
                    tmp = sym_char_class.b_Sym_char_class(strSymSetMod, symbolSet, maxIndex)
                    # If char class is not in alphabet add it.
                    if symbolDict.has_key(tmp) == False:
                        self._automaton.alphabet[maxIndex] = tmp
                        symbolDict[tmp] = maxIndex
                        index = maxIndex
                    else:
                        # Otherwise just look up char class index in alphabet.
                        index = symbolDict[tmp]
                elif len(symbolSet) == 1:
                    # Otherwise add char.
                    char = symbolSet.pop()
                    # Create char.
                    tmp = sym_char.b_Sym_char(char, char, maxIndex)
                    # If char is not in alphabet add it.
                    if symbolDict.has_key(tmp) == False:
                        self._automaton.alphabet[maxIndex] = tmp
                        symbolDict[tmp] = maxIndex
                        index = maxIndex
                    else:
                        # Otherwise just look up char index in alphabet.
                        index = symbolDict[tmp]
                # If only epsilon was between states, ignore the content of
                # symbolList
                elif len(symbolSet) == 0 and (is_epsilon == True or is_cnt_str == True):
                    break
                else:
                    # Otherwise add kchar_str
                    for i in range(0, len(symbolList)):
                        if len(symbolList[i]) == 1:
                            sym = symbolList[i].pop()
                            symbolList[i] = sym
                        else:
                            symbolList[i] = frozenset(symbolList[i])
                    symbolList = tuple(symbolList)
                    # create complete strided symbol description (will be shown in graphicasl representation)
                    complete_str = "{"

                    for i in range(0, len(symbolList)):
                        if len(symbolList[i]) == 1:
                            for char in symbolList[i]:
                                complete_str += str(char)
                        else:
                            complete_str += "["
                            complete_str_w = ""
                            for char in symbolList[i]:
                                complete_str_w += char
                            if len(complete_str_w) > 128:
                                s_a = []
                                for i in range(0, 256):
                                    s_a.append(chr(i))
                                for c in complete_str_w:
                                    if c in s_a:
                                        s_a.remove(c)
                                s = ""
                                for c in s_a:
                                    s += c
                                complete_str_w = "^" + s
                            complete_str +=  complete_str_w + "]"

                    complete_str += "}"

                    # Create strided symbol object
                    new_symbol = sym_kchar.b_Sym_kchar(complete_str, symbolList, maxIndex)

                    # If kchar is not in alphabet add it.
                    if symbolDict.has_key(new_symbol) == False:
                        self._automaton.alphabet[maxIndex] = new_symbol
                        symbolDict[new_symbol] = maxIndex
                        index = maxIndex
                    else:
                        # Otherwise just look up char index in alphabet.
                        index = symbolDict[new_symbol]
                # Add transition to automaton.
                self._automaton.transitions.add(((key[0], index, key[1])))
                maxIndex += 1

        # Create symbol occurancy count table.
        removeSymbolsDict = dict()
        for symbol in self._automaton.alphabet.keys():
            removeSymbolsDict[symbol] = 0

        # Update symbol occurancy count table, if symbol exists in transitions.
        for transition in self._automaton.transitions:
            removeSymbolsDict[transition[1]] += 1

        # Remove unused symbols from alphabet.
        for symbol in removeSymbolsDict.keys():
            if removeSymbolsDict[symbol] == 0:
                del self._automaton.alphabet[symbol]

        self._compute = False
        #self._fix_redundant_alphabet()

    def  reduce_alphabet(self):
        """
            Reduce alphabet by character classes. This create another type of char class compatibil with DFA. Alphabet should contain only symbols of b_sym_char class. This function reduces the alphabet into its equivalence class. Creates minimal deterministic alphabet.

            :Flags: Sets Alphabet collision free flag to True

            This method sets _compute to False, and get_compute() will return False until compute() is called.
        """
        self._automaton.Flags["Alphabet collision free"] = True
        # Automatom doesn't have any state = automaton is empty
        if self._automaton.is_empty():
            return
        # Automaton doesn't have any transition
        if len(self._automaton.alphabet.keys()) == 0:
            return

        # Number of rows in transition table.
        rows = max(self._automaton.states.keys()) + 1
        # Number of columns in transition table.
        columns = max(self._automaton.alphabet.keys()) + 1

        # Create transition table.
        matrix = list()
        for i in range(0, columns):
            column = [-1]*rows
            matrix.append(column)

        # Mark used columns.
        used = [False] * columns

        # Fill transition table.
        for trans in self._automaton.transitions:
            matrix[trans[1]][trans[0]] = trans[2]

        # Mark unfilled columns as used.
        for i in range(0, columns):
            if not i in self._automaton.alphabet.keys():
                used[i] = True
            else:
                if max(matrix[i]) == -1:
                    used[i] = True

        # Find which columns are same and can be grouped in DFA char class.
        classes = dict()
        for i in range(0, columns):
            if used[i] == False:
                same = set()
                same.add(i)
                for j in range(i+1, columns):
                    if used[j] == False:
                        if matrix[i] == matrix[j]:
                            same.add(j)
                            used[j] = True
                used[i] = True
                if len(same) > 1:
                    classes[self._automaton.alphabet[i].char] = same

        # Store transformation between alphbet index and new alphabet index.
        # Used for removal of transitions which have symbol which have been
        # included in char class and for creating transitions which have new
        # char class symbol
        transformDict = dict()

        # Count of alphabet classes.
        cnt = 0
        # Starting index of new alphabet symbols.
        start = max(self._automaton.alphabet.keys()) + 1
        # Create DFA alphabet classes.
        for symbol in classes.keys():
            # Create DFA char class name.
            strSymSetMod = str()
            charClass = set()
            for index in classes[symbol]:
                charClass.add(self._automaton.alphabet[index].char)
                transformDict[index] = start
                strSymSetMod += self._automaton.alphabet[index].char
            strSymSetMod = "[" + strSymSetMod + "]"
            # Create DFA char class object.
            symObject = sym_char_class.b_Sym_char_class(strSymSetMod, charClass, start)
            # Update count.
            cnt += 1
            # Update starting index.
            start += 1
            # Add symbol to the alphabet.
            self._automaton.alphabet[symObject.get_id()] = symObject

        # List of removeable transitions.
        transitionRemoveList = list()
        # Set of added transitions.
        transitionAddSet = set()
        # Find transitions for removal and find transitions for add.
        for trans in self._automaton.transitions:
            if transformDict.has_key(trans[1]):
                transitionRemoveList.append(trans)
                transitionAddSet.add(((trans[0], transformDict[trans[1]] , trans[2])))

        # Add transitions.
        for trans in transitionAddSet:
            self._automaton.transitions.add(trans)

        # Set count of DFA char classes into statistic.
        #self._statistic["DFA Char Classes"] = cnt

        # Remove transitions.
        for i in range(0, len(transitionRemoveList)):
            self._automaton.transitions.remove(transitionRemoveList[i])

        # Create symbol occurancy count table.
        removeSymbolsDict = dict()
        for symbol in self._automaton.alphabet.keys():
            removeSymbolsDict[symbol] = 0

        # Update symbol occurancy count table, if symbol exists in transitions.
        for transition in self._automaton.transitions:
            removeSymbolsDict[transition[1]] += 1

        # Remove unused symbols from alphabet.
        for symbol in removeSymbolsDict.keys():
            if removeSymbolsDict[symbol] == 0:
                del self._automaton.alphabet[symbol]

        self._compute = False

    def stride_2(self, all_chars = None):
        """
            Transform automaton to 2-stride automaton. This new automaton accept 2 chars per transition. If automaton is already strided, then 2*stride automaton will be created. In this case the automaton accept 2*stride chars per cycle. Removes Deterministic Flag. Input automaton must be eps free.

            :param all_chars: set of all chars in alphabet. If Not set, it defaults to ASCII 0 - 255.
            :type all_chars: set(char)
            :Flags: Sets Strided Flag to True and set Stride Flag to current stride.

            This method sets _compute to False, and get_compute() will return False until compute() is called.

            This algorithm is based on article: Brodie et al. A Scalable Architecture For High-Throughput Regular-Expression Pattern Matching, http://dx.doi.org/10.1109/ISCA.2006.7
        """

        # TODO: check if 2-strided automaton is deterministic if source automaton was deterministic
        # Automatom doesn't have any state = automaton is empty
        if self._automaton.is_empty():
            return

        self._automaton.Flags["Deterministic"] = False

        mapper = dict()

        # create mapper implemented as dict that maps state x symbol -> state
        for transition in self._automaton.transitions:
            if mapper.has_key(transition[0]) == True:
                if mapper[transition[0]].has_key(transition[1]) == True:
                    mapper[transition[0]][transition[1]].add(transition[2])
                else:
                    mapper[transition[0]][transition[1]] = set()
                    mapper[transition[0]][transition[1]].add(transition[2])
            else:
                mapper[transition[0]] = dict()
                mapper[transition[0]][transition[1]] = set()
                mapper[transition[0]][transition[1]].add(transition[2])

        # new transitions set
        new_transitions = set()
        # new alphabet dict (id->symbol)
        new_alphabet = dict()
        # new reverse alphabet dict (symbol->id)
        reverse_alphabet = dict()
        # reverse state dict (state->id)
        reverse_state = dict()
        # new states dict (id->states)
        new_states = dict()

        # next free state index
        state_index = max(self._automaton.states.keys()) + 1

        # next free alphabet index
        alphabet_index = 0

        # default automaton is 1 - strided
        add = 1

        # if automaton is strided, get the existing stride
        if self._automaton.Flags.has_key("Stride"):
            add = self._automaton.Flags["Stride"]

        # if complete alphabet is not defined, use default one - ASCII chars 0 - 255
        if all_chars == None:
            all_chars = set()
            for i in range(0, 256):
                all_chars.add(chr(i))

        # for all states compute strided transitions
        for state in self._automaton.states:
            # check if state has outgoing transitions
            if mapper.has_key(state):
                # for all symbols from state
                for symbol in mapper[state]:
                    # for all target states for given source state and symbol = intermediate states
                    for inner_state in mapper[state][symbol]:
                        # if intermediate state is final handle it
                        if inner_state in self._automaton.final:
                            # add new end state and add all chars char class to second position
                            # if state has outgoing transition continue follow them

                            # create local copy of complete alphabet. This copy is created for all uncovered strides
                            local_chars = list()
                            for i in range(0, add):
                                local_chars.append(copy.deepcopy(all_chars))

                            # if final state has outgoing transitions follow them
                            if mapper.has_key(inner_state):
                                # follow all symbol for intermediate state
                                for inner_symbol in mapper[inner_state]:
                                    # for all target states for given source state and symbol = target states
                                    for target_state in mapper[inner_state][inner_symbol]:

                                        target_symbol = 0

                                        res = self._automaton.alphabet[symbol].double_stride(self._automaton.alphabet[inner_symbol], 0, local_chars)

                                        # Create strided symbol object
                                        new_symbol = res[0]
                                        local_chars = res[1]
                                        new_symbol.set_id(alphabet_index)

                                        # Check if symbol is already not added
                                        if new_symbol not in reverse_alphabet:
                                            # add symbol to alphabet
                                            new_alphabet[alphabet_index] = new_symbol
                                            reverse_alphabet[new_symbol] = alphabet_index
                                            target_symbol = alphabet_index
                                            alphabet_index += 1
                                        else:
                                            # get symbol id
                                            target_symbol = reverse_alphabet[new_symbol]

                                        # add transition
                                        new_transitions.add((state, target_symbol, target_state))

                            target_symbol = 0
                            target_state = 0

                            first = 0
                            second = 0
                            complete = 0

                            # create transition to new final state, because otherwise the strided
                            # automaton wouldn't be equivalent to its non strided version.

                            # Uses symbol from first transition (State -> Intermediate State)
                            # Second symbol is created from local_chars
                            second = None
                            local_chars = list()
                            for i in range(0, add):
                                local_chars.append(copy.deepcopy(all_chars))
                            if add == 1:
                                if len(local_chars[0]) == 1:
                                    char = local_chars[0].pop()
                                    second = sym_char.b_Sym_char(char,char,0)
                                else:
                                    second = sym_char_class.b_Sym_char_class("", local_chars[0], 0)
                            else:
                                k_chars = list()
                                for i in range(0, add):
                                    k_chars.append(frozenset(local_chars[i]))
                                k_chars = tuple(k_chars)
                                second = sym_kchar.b_Sym_kchar("", k_chars, 0)

                            res = self._automaton.alphabet[symbol].double_stride(second, add, local_chars)

                            # Create strided symbol object
                            new_symbol = res[0]
                            new_symbol.set_id(alphabet_index)

                            # Check if symbol is already not added
                            if new_symbol not in reverse_alphabet:
                                # add symbol to alphabet
                                new_alphabet[alphabet_index] = new_symbol
                                reverse_alphabet[new_symbol] = alphabet_index
                                target_symbol = alphabet_index
                                alphabet_index += 1
                            else:
                                # get symbol id
                                target_symbol = reverse_alphabet[new_symbol]

                            # add new final state
                            # if new final state for final state reg exp number does not exist add the new final state, otherwise get its id
                            #if self._automaton.states[inner_state].get_regexp_number() not in reverse_state.keys():
                            #    new_state = b_state.b_State(state_index, self._automaton.states[inner_state].get_regexp_number())
                            #    #self._automaton.states[state_index] = new_state
                            #    new_states[state_index] = new_state
                            #    reverse_state[self._automaton.states[inner_state].get_regexp_number()] = state_index
                            #    target_state = state_index
                            #    self._automaton.final.add(state_index)
                            #    state_index += 1
                            #else:
                            #    target_state = reverse_state[self._automaton.states[inner_state].get_regexp_number()]
                            new_state = copy.deepcopy(self._automaton.states[inner_state])
                            new_state._id = state_index
                            new_states[state_index] = new_state
                            target_state = state_index
                            self._automaton.final.add(state_index)
                            state_index += 1

                            # add new transition
                            new_transitions.add((state, target_symbol, target_state))
                        else:
                            # create local copy of complete alphabet. This copy is created for all uncovered strides
                            local_chars = list()
                            for i in range(0, add):
                                local_chars.append(copy.deepcopy(all_chars))
                            # if final state has outgoing transitions follow them
                            if mapper.has_key(inner_state):
                                # follow all symbol for intermediate state
                                for inner_symbol in mapper[inner_state]:
                                    # for all target states for given source state and symbol = target states
                                    for target_state in mapper[inner_state][inner_symbol]:

                                        target_symbol = 0

                                        res = self._automaton.alphabet[symbol].double_stride(self._automaton.alphabet[inner_symbol], 0, local_chars)

                                        # Create strided symbol object
                                        new_symbol = res[0]
                                        local_chars = res[1]
                                        new_symbol.set_id(alphabet_index)

                                        # Check if symbol is already not added
                                        if new_symbol not in reverse_alphabet:
                                            # add symbol to alphabet
                                            new_alphabet[alphabet_index] = new_symbol
                                            reverse_alphabet[new_symbol] = alphabet_index
                                            target_symbol = alphabet_index
                                            alphabet_index += 1
                                        else:
                                            # get symbol id
                                            target_symbol = reverse_alphabet[new_symbol]

                                        # add transition
                                        new_transitions.add((state, target_symbol, target_state))

        # set transitions in automaton to new transition
        self._automaton.transitions = new_transitions
        # set alphabet in automaton to new alphabet
        self._automaton.alphabet = new_alphabet

        # add new states
        for state in new_states:
            self._automaton.states[state] = new_states[state]

        # set automaton flafs
        self._automaton.Flags["Stride"] = 2*add
        self._automaton.Flags["Strided"] = True

        # remove ureachable states
        self.remove_unreachable()

        self._compute = False

    def get_set_of_nondeterministic_states(self, mapper = None):
        """
            Computes set of nondeterministic states.

            :param mapper: Mapping between states and their transitions. If set to None the mapping is computed.
            :type mapper: dict(int, dict(int, set(int)))
            :returns: Nondeterministic states.
            :rtype: set(int)
        """
        states = set()
        if mapper == None:
            mapper = dict()
            for state in self._automaton.states.keys():
                mapper[state] = dict()
            for transition in self._automaton.transitions:
                if mapper[transition[0]].has_key(transition[1]) == True:
                    mapper[transition[0]][transition[1]].add(transition[2])
                    if len(mapper[transition[0]][transition[1]]) > 1:
                        #print(str(transition[0]) + " -> " + str(self._automaton.alphabet[transition[1]]) + " -> " + str(mapper[transition[0]][transition[1]]))
                        states.add(transition[0])
                else:
                    mapper[transition[0]][transition[1]] = set()
                    mapper[transition[0]][transition[1]].add(transition[2])
        else:
            for state in mapper.keys():
                for symbol in mapper[state].keys():
                    if len(mapper[state][symbol]) > 1:
                        #print(str(state) + " -> " + str(self._automaton.alphabet[symbol]) + " -> " + str(mapper[state][symbol]))
                        states.add(state)

        return states

    def get_state_num(self):
        """
            Number of states of nfa_data object
        """
        return len(self._automaton.states)

    def get_trans_num(self):
        """
            Number of transitions of nfa_data object
        """
        return len(self._automaton.transitions)

    def get_alpha_num(self):
        """
            Number of symbols in alphabet in nfa_data object
        """
        return len(self._automaton.alphabet)

    def set_flag(self, flag, value):
        """ Sets flag to the value.

            :param flag: String key (for example "Deterministic")
            :type flag: string
            :param value: Value of the key
            :type value: Any type
        """
        self._automaton.Flags[flag] = value

    def has_flag(self, flag):
        """
            Returns existence of flag, not value.

            :param flag: String key (for example "Deterministic")
            :type flag: string
            :returns: True if flag exists. Otherwise returns False.
            :rtype: boolean
        """
        return self._automaton.Flags.has_key(flag)

    def get_flag(self, flag):
        """
            Returns values of flag. If flag is not in dict() of flags, dict() exception is thrown (use has_flag() before every get_flag()).

            :param flag: String key (for example "Deterministic")
            :type flag: string
            :returns: Value of flag.
            :rtype: Type depends on the flag
        """
        return self._automaton.Flags[flag]

    def has_cycle(self):
        """
            Detects if cycle exists in automaton.

            :returns: True if nfa_data contain cycle. False otherwise.
            :rtype: boolean
        """
        if self._automaton.is_empty():
           return False

        a = self._automaton
        closure = set([a.start])
        lead_to = dict()

        for s in a.states:
            lead_to[s] = set()

        for t in a.transitions:
            #if t[0] == t[2]:
                #return True
            lead_to[t[0]].add(t[2])

        notcomputed = set([a.start])
        while len(notcomputed) > 0:
            #print closure
            nextnotcomputed = set()
            closure |= notcomputed
            for s in notcomputed:
                if lead_to[s] & closure:
                    return True
                else:
                    nextnotcomputed |= lead_to[s]
            notcomputed = nextnotcomputed

        return False

    def compute(self):
        """
            Base function for special automaton models. Inherited class should implement this method.
        """
        self._mapper = None
        self._compute = True

    def _fix_alphabet_indexes(self):
        """
            Re-sort the alphabet and make symbols id's continual. Maximum index will be len(alphabet) - 1.
        """
        # sort transitions by symbol
        tSortSym = dict()
        for symbolID in self._automaton.alphabet:
            tSortSym[symbolID] = []
        for t in self._automaton.transitions:
            tSortSym[t[1]].append(t)
        # re-sort-alphabet
        change = dict() # map old id -> new id
        newAlphabet = dict()
        # check epsilon symbol
        if -1 in self._automaton.alphabet:
#            newAlphabet[-1] = copy.deepcopy(self._automaton.alphabet[-1])
            newAlphabet[-1] = self._automaton.alphabet[-1]
            del self._automaton.alphabet[-1]
        oldSymbols = list(self._automaton.alphabet)
        for newSymbolID in range(0, len(self._automaton.alphabet), 1):
            oldSymbolID = oldSymbols.pop(0)
            change[oldSymbolID] = newSymbolID
#                newAlphabet[newSymbolID] = copy.deepcopy(self._automaton.alphabet[oldSymbolID])
            newAlphabet[newSymbolID] = self._automaton.alphabet[oldSymbolID]
            newAlphabet[newSymbolID]._id = newSymbolID
#            self._automaton.alphabet = copy.deepcopy(newAlphabet)
        self._automaton.alphabet = newAlphabet
        # recompute transitions according to changed alphabet
        for oldSymbolID in change:
            newSymbolID = change[oldSymbolID]
            for t in tSortSym[oldSymbolID]:
                self._automaton.transitions.remove(t)
                self._automaton.transitions.add( (t[0], newSymbolID, t[2]) )

    def resolve_alphabet(self):
        """
            Alphabet collision free.
            Example: Alphabet {1:["a", "b", "c"], 2: ["a", "d"]}.
                 After resolve_alphabet() will be
                 Alphabet {1:["b", "c"], 2:["d"], 3:["a]}.
            This method sets _compute to False, and get_compute() will return False until compute() is called.
        """

        if self.has_flag("Deterministic") and self.get_flag("Deterministic") == True:
            self.set_flag("Deterministic", False)

        self._fix_alphabet_indexes()

        newSymbolAdded = True
        while newSymbolAdded:
            alpComTran = dict() # mapping between old symbols and new symbols (for creating the new transition table)
            alphabetRev = dict() # reverse mapping symbol -> id
            for id, sym in self._automaton.alphabet.iteritems():
                alphabetRev[sym] = id       # reverse mapping
                alpComTran[id] = set([id])  # every symbol maps to self (if it's not resolved later)
            newSymbolAdded = False
            toCompare = list(self._automaton.alphabet.keys())
            for symbolID in list(self._automaton.alphabet):
                toCompare.remove(symbolID)
                if symbolID == -1: # epsilon
                    continue
                if symbolID not in alpComTran[symbolID]: # already resolved
                    continue
                symbol = self._automaton.alphabet[symbolID]
                for compSymbolID in toCompare:
                    if compSymbolID == -1: # epsilon
                        continue
                    if compSymbolID not in alpComTran[compSymbolID]: # already resolved
                        continue
                    compSymbol = self._automaton.alphabet[compSymbolID]
                    if symbol.collision( [compSymbol] ):
                        ret = symbol.resolve_collision(compSymbol)
                        alpComTran[symbolID].discard(symbolID)
                        alpComTran[compSymbolID].discard(compSymbolID)
                        for i in range(3):
                            newSymbols = ret[i]
                            for newSymbol in newSymbols:
                                if newSymbol not in alphabetRev: # add new symbol
                                    newSymbolID = len(self._automaton.alphabet)
                                    self._automaton.alphabet[newSymbolID] = newSymbol
                                    self._automaton.alphabet[newSymbolID].set_id(newSymbolID)
                                    alphabetRev[newSymbol] = newSymbolID
                                else:
                                    newSymbolID = alphabetRev[newSymbol]
                                if i <= 1: # 1st and intersect symbol
                                    alpComTran.setdefault(symbolID, set()).add(newSymbolID)
                                if i >= 1: # 2nd and intersect symbol
                                    alpComTran.setdefault(compSymbolID, set()).add(newSymbolID)
                                newSymbolAdded = True
            # sort transitions by symbol
            tSortSym = dict()
            for symbolID in self._automaton.alphabet:
                tSortSym[symbolID] = []
            for t in self._automaton.transitions:
                tSortSym[t[1]].append(t)
            # create new transition table according to symbol mapping
            newTrans = set()
            for symbolID in alpComTran:
                for innerSymbolID in alpComTran[symbolID]:
                    for t in tSortSym[symbolID]:
                        newTrans.add( (t[0], innerSymbolID, t[2]) )
            self._automaton.transitions = newTrans
            # re-sort transitions by symbol
            tSortSym = dict()
            for symbolID in self._automaton.alphabet:
                tSortSym[symbolID] = []
            for t in self._automaton.transitions:
                tSortSym[t[1]].append(t)
            # remove unused symbols
            for symbolID, l in tSortSym.iteritems():
                if not l:
                   del self._automaton.alphabet[symbolID]
            # re-sort alphabet
            self._fix_alphabet_indexes()

        if len(self._automaton.alphabet) > 0:
            self.set_flag("Alphabet collision free", True)
        self._compute = False

    def resolve_char_classes(self):
        """
            Alphabet collision free.
            Example: Alphabet {1:["a", "b", "c"], 2: ["a", "d"]}.
                 After resolve_alphabet() will be
                 Alphabet {1:["b", "c"], 2:["d"], 3:["a]}.
            This method sets _compute to False, and get_compute() will return False until compute() is called.
        """

        if self.has_flag("Deterministic") and self.get_flag("Deterministic") == True:
            self.set_flag("Deterministic", False)

        self._fix_alphabet_indexes()

        newSymbolAdded = True
        while newSymbolAdded:
            alpComTran = dict() # mapping between old symbols and new symbols (for creating the new transition table)
            alphabetRev = dict() # reverse mapping symbol -> id
            for id, sym in self._automaton.alphabet.iteritems():
                alphabetRev[sym] = id       # reverse mapping
                alpComTran[id] = set([id])  # every symbol maps to self (if it's not resolved later)
            newSymbolAdded = False
            toCompare = list(self._automaton.alphabet.keys())
            for symbolID in list(self._automaton.alphabet):
                toCompare.remove(symbolID)
                if symbolID == -1: # epsilon
                    continue
                if symbolID not in alpComTran[symbolID]: # already resolved
                    continue
                if self._automaton.alphabet[symbolID].get_type() == b_symbol.io_mapper["b_Sym_char"]:
                    continue
                symbol = self._automaton.alphabet[symbolID]
                for compSymbolID in toCompare:
                    if compSymbolID == -1: # epsilon
                        continue
                    if compSymbolID not in alpComTran[compSymbolID]: # already resolved
                        continue
                    if self._automaton.alphabet[compSymbolID].get_type() == b_symbol.io_mapper["b_Sym_char"]:
                        continue
                    compSymbol = self._automaton.alphabet[compSymbolID]
                    if symbol.collision( [compSymbol] ):
                        ret = symbol.resolve_collision(compSymbol)
                        alpComTran[symbolID].discard(symbolID)
                        alpComTran[compSymbolID].discard(compSymbolID)
                        for i in range(3):
                            newSymbols = ret[i]
                            for newSymbol in newSymbols:
                                if newSymbol not in alphabetRev: # add new symbol
                                    newSymbolID = len(self._automaton.alphabet)
                                    self._automaton.alphabet[newSymbolID] = newSymbol
                                    self._automaton.alphabet[newSymbolID].set_id(newSymbolID)
                                    alphabetRev[newSymbol] = newSymbolID
                                else:
                                    newSymbolID = alphabetRev[newSymbol]
                                if i <= 1: # 1st and intersect symbol
                                    alpComTran.setdefault(symbolID, set()).add(newSymbolID)
                                if i >= 1: # 2nd and intersect symbol
                                    alpComTran.setdefault(compSymbolID, set()).add(newSymbolID)
                                newSymbolAdded = True
            # sort transitions by symbol
            tSortSym = dict()
            for symbolID in self._automaton.alphabet:
                tSortSym[symbolID] = []
            for t in self._automaton.transitions:
                tSortSym[t[1]].append(t)
            # create new transition table according to symbol mapping
            newTrans = set()
            for symbolID in alpComTran:
                for innerSymbolID in alpComTran[symbolID]:
                    for t in tSortSym[symbolID]:
                        newTrans.add( (t[0], innerSymbolID, t[2]) )
            self._automaton.transitions = newTrans
            # re-sort transitions by symbol
            tSortSym = dict()
            for symbolID in self._automaton.alphabet:
                tSortSym[symbolID] = []
            for t in self._automaton.transitions:
                tSortSym[t[1]].append(t)
            # remove unused symbols
            for symbolID, l in tSortSym.iteritems():
                if not l:
                   del self._automaton.alphabet[symbolID]
            # re-sort alphabet
            self._fix_alphabet_indexes()

        if len(self._automaton.alphabet) > 0:
            self.set_flag("Alphabet collision free", True)
        self._compute = False

    def get_compute(self):
        """
            Return value of variable _compute. Which mean flag call to compute()
        """

        return self._compute

    def report_memory_optimal(self):
        """
            Report consumed memory in bytes. Optimal mapping algorithm is used \
            (with oracle).

            :returns: Returns number of bytes.
            :rtype: int
        """

    def report_memory_naive(self):
        """
            Report consumed memory in bytes. Naive mapping algorithm is used \
            (2D array).

            :returns: Returns number of bytes.
            :rtype: int
        """

    def _remove_self_epsilon_loops(self):
        """
            Removes self epsilon loop.
        """
        removeable_transitions = set()
        for transition in self._automaton.transitions:
            if transition[0] == transition[2] and transition[1] == -1:
                removeable_transitions.add(transition)
        for transition in removeable_transitions:
            self._automaton.transitions.discard(transition)

    def thompson2glushkov(self):
        """
            Transforms Thompson automaton to Glushkov automaton.
            Steps:
                1) Input automaton with eps transitions
                2) Convert thompson eps-NFA to glushkov NFA
        """
        # Create empty automaton
        fsm_n = b_Automaton()
        fsm_n.create_from_nfa_data(self.get_automaton(True),False)

        # Number of epsilon transitions in automaton
        eps_count = 0

        # Create forward and backward mapping of transitions
        mapper = dict()
        reverse_mapper = dict()
        for state in fsm_n._automaton.states:
            mapper[state] = dict()
            reverse_mapper[state] = dict()
        for transition in fsm_n._automaton.transitions:
            if mapper[transition[0]].has_key(transition[1]) == False:
                mapper[transition[0]][transition[1]] = set()
            if reverse_mapper[transition[2]].has_key(transition[1]) == False:
                reverse_mapper[transition[2]][transition[1]] = set()
            mapper[transition[0]][transition[1]].add(transition[2])
            reverse_mapper[transition[2]][transition[1]].add(transition[0])
            if transition[1] == -1:
                eps_count += 1
        old_eps_count = 0
        fsm_n._remove_self_epsilon_loops()

        # Main loop oparate on automaton until no epsilon transition is pressent
        while eps_count != old_eps_count:
            queue = deque()
            print "old: " + str(old_eps_count) + " new: " + str(eps_count)
            old_eps_count = eps_count
            visited = set()
            if isinstance(fsm_n._automaton.start, set):
                queue.extend(fsm_n._automaton.start)
            else:
                queue.append(fsm_n._automaton.start)
            while len(queue) > 0:
                state = queue.popleft()
                new_transitions = set()
                removeable_transitions = set()
                if state not in visited:
                    visited.add(state)
                    for symbol in reverse_mapper[state]:
                        if symbol == -1:
                            for sstate in reverse_mapper[state][symbol]:
                                for tsymbol in mapper[state]:
                                    for tstate in mapper[state][tsymbol]:
                                        new_transitions.add((sstate, tsymbol, tstate))
                                        if reverse_mapper[state] == 1:
                                            removeable_transitions.add((state, tsymbol, tstate))
                                removeable_transitions.add((sstate, symbol, state))
                                if state in fsm_n._automaton.final:
                                    fsm_n._automaton.final.add(sstate)
                                    fsm_n._automaton.states[state].set_regexp_number(fsm_n._automaton.states[state].get_regexp_number().copy())
                    for symbol in mapper[state]:
                        for tstate in mapper[state][symbol]:
                            if tstate not in visited and tstate not in queue:
                                queue.append(tstate)
                    fsm_n._automaton.transitions -= removeable_transitions
                    fsm_n._automaton.transitions |= new_transitions
                    for transition in removeable_transitions:
                        mapper[transition[0]][transition[1]].discard(transition[2])
                        reverse_mapper[transition[2]][transition[1]].discard(transition[0])
                        if len(mapper[transition[0]][transition[1]]) == 0:
                            del mapper[transition[0]][transition[1]]
                        if len(reverse_mapper[transition[2]][transition[1]]) == 0:
                            del reverse_mapper[transition[2]][transition[1]]
                        if transition[1] == -1:
                            eps_count -= 1
                    for transition in new_transitions:
                        if mapper[transition[0]].has_key(transition[1]) == False:
                            mapper[transition[0]][transition[1]] = set()
                        if reverse_mapper[transition[2]].has_key(transition[1]) == False:
                            reverse_mapper[transition[2]][transition[1]] = set()
                        mapper[transition[0]][transition[1]].add(transition[2])
                        reverse_mapper[transition[2]][transition[1]].add(transition[0])
                        if transition[1] == -1:
                            eps_count += 1
                        if state in fsm_n._automaton.final:
                            fsm_n._automaton.final.add(transition[2])
                            fsm_n._automaton.states[transition[2]].set_regexp_number(fsm_n._automaton.states[state].get_regexp_number().copy())
                    if len(mapper[state]) == 0 and len(reverse_mapper[state]) == 0:
                        del mapper[state]
                        del reverse_mapper[state]
                        del fsm_n._automaton.states[state]
                        if state in fsm_n._automaton.final:
                            fsm_n._automaton.final.discard(state)
            fsm_n._remove_self_epsilon_loops()
            print "old: " + str(old_eps_count) + " new: " + str(eps_count)
        # remove eps char from alphabet
        #if fsm_n._automaton.alphabet.has_key(-1):
            #del fsm_n._automaton.alphabet[-1]
        removeable = set()
        for transition in fsm_n._automaton.transitions:
            if transition[1] == -1:
                print transition
                removeable.add(transition)
        fsm_n._automaton.transitions -= removeable
        syn = dict()
        #ret = fsm_n._automaton.is_consistent(syn)
        #if ret == True:
            #print "Failure: \n" + str(syn)
        fsm_n.remove_unreachable()
        self.create_from_nfa_data(fsm_n.get_automaton(False),False)

    def _trg_reverse(self):
        """
            Reverse automaton. Full reverse is performed. This method is vital for thompson2reverse_glushkov().
        """
        new_transitions = set()
        for transition in self._automaton.transitions:
            new_transitions.add((transition[2], transition[1], transition[0]))
        self._automaton.transitions = new_transitions
        new_final = set()
        if isinstance(self._automaton.start, set):
            new_final |= self._automaton.start
        else:
            new_final.add(self._automaton.start)
        self._automaton.start = set()
        for fstate in self._automaton.final:
            self._automaton.start.add(fstate)
        self._automaton.final = new_final

    def _replace_input_self_loop(self):
        """
            Replaces input self loop generated by pcre_parser by self loop with epsilons. This method is vital for thompson2reverse_glushkov().
        """
        max_index = max(self._automaton.states.keys()) + 1
        new_transitions = set()
        removeable_transitions = set()
        for transition in self._automaton.transitions:
            if transition[0] == transition[2]:
                removeable_transitions.add(transition)
                del self._automaton.states[transition[0]]
                if isinstance(self._automaton.start, set):
                    if transition[0] in self._automaton.start:
                        self._automaton.start.discard(transition[0])
                        self._automaton.start.add(max_index + 0)
                else:
                    if transition[0] == self._automaton.start:
                        self._automaton.start = max_index + 0
                self._automaton.states[max_index + 0] = b_state.b_State(max_index + 0, set())
                self._automaton.states[max_index + 1] = b_state.b_State(max_index + 1, set())
                self._automaton.states[max_index + 2] = b_state.b_State(max_index + 2, set())
                self._automaton.states[max_index + 3] = b_state.b_State(max_index + 3, set())
                new_transitions.add((max_index + 0, -1, max_index + 1))
                new_transitions.add((max_index + 0, -1, max_index + 3))
                new_transitions.add((max_index + 1, transition[1], max_index + 2))
                new_transitions.add((max_index + 2, -1, max_index + 1))
                new_transitions.add((max_index + 2, -1, max_index + 3))
                for transition2 in self._automaton.transitions:
                    if transition2[0] == transition[0] and transition2[2] != transition[0]:
                        new_transitions.add((max_index + 3, transition2[1], transition2[2]))
                        removeable_transitions.add(transition2)
                    elif transition2[2] == transition[0] and transition2[0] != transition[0]:
                        new_transitions.add((transition2[0], transition2[1], max_index + 0))
                        removeable_transitions.add(transition2)
                max_index += 4
        self._automaton.transitions -= removeable_transitions
        self._automaton.transitions |= new_transitions

    def thompson2reverse_glushkov(self):
        """
            Transform Thompson automaton to Reverse Glushkov automaton.
        """
        self._replace_input_self_loop()
        #self.show("epsr.dot", " ")
        self._trg_reverse()
        #self.show("trg.dot", " ")
        self.thompson2glushkov()
        self._trg_reverse()

    def is_glushkov(self, reverse = False):
        """
            Check if automaton is glushkov (position) automaton.

            :param reverse: If True, check if automaton is reverse glushkov (position) automaton. Otherwise check if automaton is glushkov (position) automaton.
            :type reverse: boolean
            :returns: Returns status of the check.
            :rtype: boolean
        """
        if reverse == False:
            reverse_mapper = dict()
            for transition in self._automaton.transitions:
                if reverse_mapper.has_key(transition[2]) == True:
                    reverse_mapper[transition[2]].add(transition[1])
                    if len(reverse_mapper[transition[2]]) > 1:
                        print "PA: Offending transition: " + str(transition)
                        print "Symbol: " + str(self._automaton.alphabet[transition[1]])
                        return False
                else:
                    reverse_mapper[transition[2]] = set()
                    reverse_mapper[transition[2]].add(transition[1])
            return True
        else:
            mapper = dict()
            for transition in self._automaton.transitions:
                if mapper.has_key(transition[0]) == True:
                    mapper[transition[0]].add(transition[1])
                    if len(mapper[transition[0]]) > 1:
                        print "RPA: Offending transition: " + str(transition)
                        print "Symbol: " + str(self._automaton.alphabet[transition[1]])
                        return False
                else:
                    mapper[transition[0]] = set()
                    mapper[transition[0]].add(transition[1])
            return True

    def _fix_redundant_alphabet(self):
        """
            Fix situation when there are two same symbols in alphabet (eg. two     \
            symbols representing 'a').
        """
        print "Size of alphabet before " + str(len(self._automaton.alphabet))
        equal = dict()
        for symbol in self._automaton.alphabet:
            equal[symbol] = set()
        ignore = set()
        for symbol in self._automaton.alphabet:
            if symbol not in ignore:
                for asymbol in self._automaton.alphabet:
                    if symbol != asymbol:
                        if self._automaton.alphabet[symbol] == self._automaton.alphabet[asymbol]:
                            equal[symbol].add(asymbol)
                            ignore.add(asymbol)
        translation = range(max(self._automaton.alphabet) + 1)
        for (key, value) in equal.items():
            if len(value) > 0:
                for akey in value:
                    translation[akey] = key
                    del self._automaton.alphabet[akey]
        new_transitions = set()
        for transition in self._automaton.transitions:
            new_transitions.add((transition[0], translation[transition[1]], transition[2]))
        self._automaton.transitions = new_transitions
        print "Size of alphabet after " + str(len(self._automaton.alphabet))

    def _remove_unused_symbols(self):
        """
            Remove unused symbols from alphabet.
        """
        print "Before: " + str(len(self._automaton.alphabet))
        used_symbols = set()
        for transition in self._automaton.transitions:
            used_symbols.add(transition[1])
        all_symbols = set(self._automaton.alphabet.keys())
        removeable_symbols = all_symbols - used_symbols
        for symbol in removeable_symbols:
            del self._automaton.alphabet[symbol]
        print "After: " + str(len(self._automaton.alphabet))

    def remove_counting_constraints(self, limit = 18):
        """
            Remove counting constraints from automaton. Transitions with counting
            constraint are replaced by subautomaton with same function.
        """
        for transition in self._automaton.alphabet:
            pass
        cnt_symbols = set()
        keep_symbols = set()
        replace_symbols = dict()
        removeable_transitions = set()
        new_transitions = set()
        new_symbols = dict()

        index = max(self._automaton.alphabet) + 1
        for symbol in self._automaton.alphabet:
            if self._automaton.alphabet[symbol].ctype == b_symbol.io_mapper["b_Sym_cnt_constr"]:
                cnt_symbols.add(symbol)
                text = self._automaton.alphabet[symbol].get_text()
                text = text.split("{")
                text = text[0]
                if isinstance(self._automaton.alphabet[symbol].symbol, set) or isinstance(self._automaton.alphabet[symbol].symbol, frozenset):
                    new_symbol = sym_char_class.b_Sym_char_class(text, self._automaton.alphabet[symbol].symbol, index)
                else:
                    new_symbol = sym_char.b_Sym_char(text, self._automaton.alphabet[symbol].symbol, index)
                new_symbols[index] = new_symbol
                replace_symbols[symbol] = index
                index += 1
        index = max(self._automaton.states) + 1

        clean = False
        while clean == False:
            clean = True
            #self.normalise_by_depth()
            trn = list(self._automaton.transitions)
            trn.sort()
            for transition in trn:
                if transition[1] in cnt_symbols:
                    symbol = self._automaton.alphabet[transition[1]]
                    if symbol.m == symbol.n:
                        # {m}
                        if symbol.m >= limit:
                            keep_symbols.add(symbol)
                            continue
                        if symbol.m > 1:
                            self._automaton.states[index] =  b_state.b_State(index)
                            self._automaton.transitions.add((transition[0], replace_symbols[transition[1]], index))
                            index += 1
                            for i in xrange(1, symbol.m - 1):
                                self._automaton.states[index] =  b_state.b_State(index)
                                self._automaton.transitions.add((index - 1, replace_symbols[transition[1]], index))
                                index += 1
                            self._automaton.transitions.add((index - 1, replace_symbols[transition[1]], transition[2]))
                        else:
                            self._automaton.transitions.add((transition[0], replace_symbols[transition[1]], transition[2]))
                    elif symbol.n == float("inf"):
                        # {m,}
                        if symbol.m >= limit:
                            keep_symbols.add(symbol)
                            continue
                        if symbol.m > 1:
                            self._automaton.states[index] =  b_state.b_State(index)
                            self._automaton.transitions.add((transition[0], replace_symbols[transition[1]], index))
                            index += 1
                            for i in xrange(1, symbol.m - 1):
                                self._automaton.states[index] =  b_state.b_State(index)
                                self._automaton.transitions.add((index - 1, replace_symbols[transition[1]], index))
                                index += 1
                            self._automaton.transitions.add((index - 1, replace_symbols[transition[1]], index - 1))
                            self._automaton.transitions.add((index - 1, replace_symbols[transition[1]], transition[2]))
                        else:
                            self._automaton.transitions.add((transition[0], replace_symbols[transition[1]], transition[2]))
                            self._automaton.transitions.add((transition[0], replace_symbols[transition[1]], transition[0]))
                    else:
                        # {m, n}
                        if symbol.n >= limit:
                            keep_symbols.add(symbol)
                            continue
                        if symbol.m > 1:
                            self._automaton.states[index] =  b_state.b_State(index)
                            self._automaton.transitions.add((transition[0], replace_symbols[transition[1]], index))
                            index += 1
                            for i in xrange(1, symbol.m - 1):
                                self._automaton.states[index] =  b_state.b_State(index)
                                self._automaton.transitions.add((index - 1, replace_symbols[transition[1]], index))
                                index += 1
                            self._automaton.transitions.add((index - 1, replace_symbols[transition[1]], transition[2]))
                            last = index - 1
                        elif symbol.m == 1:
                            self._automaton.transitions.add((transition[0], replace_symbols[transition[1]], transition[2]))
                            last = transition[0]
                        else:
                            # m == 0
                            itttr = set(self._automaton.transitions)
                            for itrn in itttr:
                                if itrn[2] == transition[0] and itrn[0] != transition[0]:
                                    if itrn[1] in cnt_symbols:
                                        self._automaton.transitions.add((itrn[0], replace_symbols[itrn[1]], transition[2]))
                                        print "Warning: Fix it."
                                        print itrn
                                        print transition
                                        print self._automaton.alphabet[itrn[1]]
                                    else:
                                        self._automaton.transitions.add((itrn[0], itrn[1], transition[2]))
                            self._automaton.transitions.add((transition[0], replace_symbols[transition[1]], transition[2]))
                            last = transition[0]
                        cnt = symbol.n - symbol.m
                        for i in xrange(cnt):
                            self._automaton.states[index] =  b_state.b_State(index)
                            self._automaton.transitions.add((last, replace_symbols[transition[1]], index))
                            if i > 0:
                                self._automaton.transitions.add((index - 1, replace_symbols[transition[1]], index))
                            index += 1
                        self._automaton.transitions.add((index - 1, replace_symbols[transition[1]], transition[2]))
                    self._automaton.transitions.remove(transition)
                    #clean = False
            print len(removeable_transitions), " x", len(new_transitions)
            #self._automaton.transitions -= removeable_transitions
            #self._automaton.transitions |= new_transitions
        #for sym in cnt_symbols:
            #del self._automaton.alphabet[sym]
        for sym in new_symbols:
            self._automaton.alphabet[sym] = new_symbols[sym]

    def save_to_FA_format(self, file_name):
        fw = open(file_name, 'w')

        if isinstance(self._automaton.start, set):
            raise pattern_exceptions.general_unsupported_type(self.save_to_timbuk.__name__, self._automaton.alphabet[symbol].__class__.__name__, self._automaton.alphabet[symbol], "Method supports only instances of automaton with single start state.")
        else:
            fw.write(self._automaton.states[self._automaton.start].get_text() +"\n")

        line = ":"
        symbols = []
        for symbol in self._automaton.alphabet.keys():
            if self._automaton.alphabet[symbol].get_type() == b_symbol.io_mapper["b_Sym_char"]:
                symbols.append(ord(self._automaton.alphabet[symbol].char))
                line += " {0}".format(hex(ord(self._automaton.alphabet[symbol].char)))
            else:
                raise pattern_exceptions.general_unsupported_type(self.save_to_timbuk.__name__, self._automaton.alphabet[symbol].__class__.__name__, self._automaton.alphabet[symbol], "Method supports only instances of class b_Sym_char in simple mode.")



        symbols.sort()
        # print "Symbols count: ", len(symbols)
        # for i in range(0,256):
        #     if i < len(symbols) and symbols[i] != i:
        #         print "Warning: missing symbols "
        #         break
        # print "Adding symbols ..."
        for i in range(0,256):
            if i not in symbols:
                line += " {0}".format(hex(i))

        fw.write(line + "\n")


        for (fr, sym, to) in self._automaton.transitions:
            fw.write("{0} {1} {2}\n".format(str(fr), str(to), hex(ord(self._automaton.alphabet[sym].char))))
        for state in self._automaton.final:
            fw.write(self._automaton.states[state].get_text() + "\n")

        fw.close()



    def save_to_timbuk(self, file_name, simple = True):
        """
            Save automaton in timbuk style.

            <file>            : 'Ops' <label_list> <automaton> <automaton> ...

            <label_list>      : <label_decl> <label_decl> ... // a list of label declarations

            <label_decl>      : string ':' int // a symbol declaration (the name and the arity)

            <automaton>       : 'Automaton' string 'States' <state_list> 'Final States' <state_list> 'Transitions' <transition_list>

            <state_list>      : <state> <state> ... // a list of states

            <state>           : string // the name of a state

            <transition_list> : <transition> <transition> ... // a list of transitions

            <transition>      : <label> '(' <state> ',' <state> ',' ... ')' '->' <state> // a transition

            <label>           : string // the name of a label

            :param file_name: File name
            :type file_name: string

            :param simple: Use simple mode. In simple mode only automata with  \
                           character symbols are supported and the symbols are \
                           encoded as trasition labels in format 'sXX', where  \
                           XX is hexadecimal value of input symbol. If simple  \
                           mode is disabled, the any supported automata symbol \
                           can be used and its label is created by its function\
                           export_symbol().
            :type simple: boolean
        """
        fw = open(file_name, 'w')

        line = "Ops"
        if simple == True:
            for symbol in self._automaton.alphabet.keys():
                if self._automaton.alphabet[symbol].get_type() == b_symbol.io_mapper["b_Sym_char"]:
                    line += " s%(ord)02X:1" % {"ord":ord(self._automaton.alphabet[symbol].char)}
                else:
                    raise pattern_exceptions.general_unsupported_type(self.save_to_timbuk.__name__, self._automaton.alphabet[symbol].__class__.__name__, self._automaton.alphabet[symbol], "Method supports only instances of class b_Sym_char in simple mode.")
        else:
            for symbol in self._automaton.alphabet.keys():
                line += " " + str(self._automaton.alphabet[symbol].export_symbol()) + ":1"
        line += " start:0\n\n"
        fw.write(line)
        fw.write("Automaton A\n")
        line = "States"
        states = dict()
        for state in self._automaton.states.keys():
            line += " q" + str(state)# + ":0"
            states[state] = set()
        line += "\n"
        fw.write(line)
        line = "Final States"
        for state in self._automaton.final:
            line += " q" + str(state)
        line += "\n"
        fw.write(line)
        fw.write("Transitions\n")
        if isinstance(self._automaton.start, set):
            for sstate in self._automaton.start:
                fw.write("start() -> q" + str(sstate) +"\n")
        else:
            fw.write("start() -> q" + str(self._automaton.start) +"\n")
        for transition in self._automaton.transitions:
            #fw.write(str(self._automaton.alphabet[transition[1]].export_symbol()) + "(" + str(transition[0]) + ") -> " + str(transition[0]) + "\n")
            #fw.write("s" + str(transition[1]) + "(q" + str(transition[0]) + ") -> q" + str(transition[2]) + "\n")
            states[transition[0]].add(transition)
        k = states.keys()
        k.sort()
        for state in k:
            for transition in states[state]:
                # fw.write("s" + str(transition[1]) + "(q" + str(transition[0]) + ") -> q" + str(transition[2]) + "\n")
                fw.write("s" + str(self._automaton.alphabet[transition[1]].export_symbol()) + "(q" + str(transition[0]) + ") -> q" + str(transition[2]) + "\n")

        fw.close()

    ###########################################################################
    # Deprecated methods                                                      #
    ###########################################################################
    def _epsilon_closure(self, state, StateOutSymbols):
        """ Compute epsilon closure for selected state.

            :param state: State from which epsilon closure is computed.
            :type state: int
            :param StateOutSymbols: Mapping between states and their transitions.
            :type StateOutSymbols: dict(int, tuple(int, int, int))
            :returns: Set containing epsilon closure for state.
            :rtype: set(int)

            NOTE: This method is deprecated. Use epsilon_closure().
        """
        aux_func.deprecation_warning("method", "_epsilon_closure()", "epsilon_closure()")
        return self.epsilon_closure(state, StateOutSymbols)

    def removeCharClasses(self):
        """
            Remove char classes from automaton. Removed char classes are substituted with equivalent chars and coresponding transitions are added.

            NOTE: This method is deprecated. Use remove_char_classes().
        """
        aux_func.deprecation_warning("method", "removeCharClasses()", "remove_char_classes()")
        self.remove_char_classes()

    def _removeCharClasses(self):
        """
            Remove char classes from automaton. Removed char classes are substituted with equivalent chars and coresponding transitions are added.

            This method sets _compute to False, and get_compute() will return False until compute() is called.

            NOTE: This method is deprecated. Use remove_char_classes().
        """
        aux_func.deprecation_warning("method", "_removeCharClasses()", "remove_char_classes()")
        self.remove_char_classes()

    def _createCharClasses(self):
        """
            Creates char classes, if they can be created. Replaced transitions are removed. Unused symbols are removed after creation of char classes.

            NOTE: This method is deprecated. Use create_char_classes().
        """
        aux_func.deprecation_warning("method", "_createCharClasses()", "create_char_classes()")
        self.create_char_classes()
###############################################################################
# End of File b_automaton.py                                                  #
###############################################################################
