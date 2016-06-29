############################################################################
#  hybrid_fa.py: Module for PATTERN MATCH algorithm Hybrid Finite Automat
#  Copyright (C) 2012 Brno University of Technology, ANT @ FIT
#  Author(s): Milan Pala, <xpalam00@stud.fit.vutbr.cz>
############################################################################
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
#  This software or firmware is provided ``as is'', and any express or
#  implied warranties, including, but not limited to, the implied warranties
#  of merchantability and fitness for a particular purpose are disclaimed.
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

"""Module for pattern match: algorithm for Hybrid Finite Automat."""

from netbench.pattern_match import sym_char
from netbench.pattern_match.pcre_parser import pcre_parser
from netbench.pattern_match.b_dfa import b_dfa
from netbench.pattern_match.b_nfa import b_nfa
from netbench.pattern_match.nfa_data import nfa_data
from netbench.pattern_match.b_state import b_State
from netbench.pattern_match.sym_char import b_Sym_char
from netbench.pattern_match.sym_char_class import b_Sym_char_class
from netbench.pattern_match.b_automaton import b_Automaton
from netbench.pattern_match.pattern_exceptions import empty_automaton_exception
import os
import re
import tempfile
import math
import sys

class hybrid_fa(b_Automaton):
    """
        Class for Hybrid Finite Automat.

        Hybrid automaton is saved in:
         - self.dfa            - Head DFA part of Hybrid FA
         - self.nfas           - Tails NFA parts of Hybrid FA
         - self.tran_aut       - List of border states
                
        Indexes in self.tran_aut reffer to
        self.nfas list for particular NFA tails.
        
        Based on:
            "A hybrid finite automaton for practical deep packetinspection
            ISBN: 978-1-59593-770-4
            URL: http://portal.acm.org/citation.cfm?id=1364656
            
        Borders states are recognized in self._is_special(state) method
        based on implementation of this approach in regex tool from M. Becchi.
        Arguments for this method are saved in self._SPECIAL_MIN_DEPTH,
        self._MAX_TX and self._MAX_HEAD_SIZE and have setters like
        self.set_max_head_state() etc.
        Every option could by turn off by set -1 as value.
    """

    def __init__(self):
        """
            Constructor - inits object atributes:
            dfa            - Head DFA part of Hybrid FA
            nfas           - Tails NFA parts of Hybrid FA
            tran_aut       - List of border states
            
            Index in self.tran_aut reffer to
            self.nfas list for particular NFA tails.
            
            _compute       - Flag call to compute()
            _depthOfStates - Depth for each state from initial state
            _stateTrans    - 
            _maper         - Used to map state to (symbol, target) list
            _sort          - Sorted transitions
            _head_size     - Size of head DFA part
        """
        b_Automaton.__init__(self)
        self._compute = False
        self._depthOfStates = dict()
        self._stateTrans = dict()
        self._mapper = None
        self.dfa = b_dfa()
        self.nfas = dict()
        self.tran_aut = dict()
        self._sort = {}
        self._head_size = 0
        self._nfaEpsFree = b_nfa()
        
        self._SPECIAL_MIN_DEPTH = 5   # minimum NFA depth of a special state
        self._MAX_TX = 250            # maximum number of outgoing transitions allowed in a expanded NFA state 
        self._MAX_HEAD_SIZE = 1000    # maximum number of states in the head automaton before starting to create tails

    def set_special_min_depth(self, special_min_depth):
        """
            Set argument for _is_special() predicate.
            
            :param special_min_depth: New value. Has to be greater than 0, -1 for off.
            :type special_min_depth: int
            
            :raises: ValueError
        """
        if special_min_depth > 0 or special_min_depth == -1:
            self._SPECIAL_MIN_DEPTH = special_min_depth
        else:
            raise ValueError

    def set_max_tx(self, max_tx):
        """
            Set argument for _is_special() predicate.
            
            :param max_tx: New value. Has to be greater or equal than 0, -1 for off.
            :type max_tx: int
            
            :raises: ValueError
        """
        if max_tx >= 0 or max_tx == -1:
            self._MAX_TX = max_tx
        else:
            raise ValueError

    def set_max_head_size(self, max_head_size):
        """
            Set argument for _is_special() predicate.
            
            :param max_head_size: New value. Has to be greater or equal than 0, -1 for off.
            :type max_head_size: int
            
            :raises: ValueError
        """
        if max_head_size >= 0 or max_head_size == -1:
            self._MAX_HEAD_SIZE = max_head_size
        else:
            raise ValueError

    def compute(self):
        """
            Computes Hybrid automaton.
        """
        b_Automaton.compute(self)
        self._compute = False

        # Automaton doesn't have any state = automaton is empty
        if self._automaton.is_empty() or self._automaton.start < 0:
            return

        # Make epsilon free automaton
        self.remove_epsilons()

        # save input NFA for tails NFA parts
        self._nfaEpsFree = b_nfa()
        self._nfaEpsFree.create_from_nfa_data(self._automaton, True)

        counter = 0
        stack = list()
        newStates = dict()
        newStatesRev = dict()
        tmp = set()
        tmp.add(self._automaton.start)
        newStates[counter] = tmp
        newStatesRev[frozenset(tmp)] = counter
        stack.append(counter)
        counter += 1
        final = set()
        transitions = set()
        alphCounter = 0
        alphabet = dict()
        alphabetRev = dict()
        states = dict()
        states[0] = b_State(0, self._automaton.states[self._automaton.start].get_regexp_number())

        borders = dict()
        noSpecials = set()

        # transtions from each state
        for transition in self._automaton.transitions:
            self._stateTrans.setdefault(transition[0], set()).add((transition[1], transition[2]))
        
        # Set depth for each state
        self._setDepth()

        # copy alphabet, ID's 0,1,...
        mapId = dict() # maps old id -> new id
        for id, sym in self._automaton.alphabet.iteritems():
            sym.set_id(alphCounter)
            alphabet[alphCounter] = sym
            alphabetRev[sym] = alphCounter
            mapId[id] = alphCounter
            alphCounter += 1

        while stack:
            actState = stack.pop()
            if newStates[actState].intersection(self._automaton.final):
                final.add(actState)

            for fromState in newStates[actState]:
                if self._is_special(fromState):
                    # marked current DFA state as special and set
                    borders.setdefault(actState, set()).add(fromState)
                else:
                    noSpecials.add(fromState)

            # transitions from actual state for each symbol
            outSymbols = dict() # (symbol id, set of states id)
            for state in newStates[actState]:
                if state not in self._stateTrans:
                    continue
                if actState in borders and state in borders[actState]:
                    continue
                for t in self._stateTrans[state]:
                    outSymbols.setdefault(mapId[t[0]], set()).add(t[1])

            # resolve symbol collisions
            symbolAdded = True
            while symbolAdded:
                symbolAdded = False
                for sym1 in list(outSymbols.keys()):
                    toCompare = list(outSymbols.keys())
                    toCompare.remove(sym1)
                    for sym2 in toCompare:
                        if not (outSymbols[sym1] and outSymbols[sym2]):
                            continue # no next state for one of the symbols
                        if not alphabet[sym1].collision([alphabet[sym2]]):
                            continue
                        #print "COLLISION DETECTED"

                        symStates = list([[]] * 3)
                        symStates[0] = outSymbols[sym1]
                        symStates[2] = outSymbols[sym2]
                        symStates[1] = symStates[0] | symStates[2]
                        outSymbols[sym1] = set()
                        outSymbols[sym2] = set()
                        ret = alphabet[sym1].resolve_collision(alphabet[sym2])

                        for i in range(3):
                            if not ret[i]: # no symbol returned
                                continue

                            for new in ret[i]:
                                symbolAdded = True
                                if new not in alphabetRev.keys():
                                    # add new symbol
                                    new.set_id(alphCounter)
                                    alphabet[alphCounter] = new
                                    alphabetRev[new] = alphCounter
                                    id = alphCounter
                                    alphCounter += 1
                                else:
                                    id = alphabetRev[new]
                                # update next states for symbol
                                tmp = outSymbols.setdefault(id, set())
                                outSymbols[id] = tmp | symStates[i]

            self._head_size += len(outSymbols)

            # create new transitions
            for symbol, nextState in outSymbols.iteritems():
                if not nextState:
                    continue # no next states -> ignore symbol

                if frozenset(nextState) not in newStatesRev:
                    # create a new state
                    newStatesRev[frozenset(nextState)] = counter
                    newStates[counter] = nextState
                    stack.append(counter)

                    endVal = set() # set of regular expression numbres
                    for state in nextState:

                        if self._automaton.states[state].is_final() == True:
                            endVal |= self._automaton.states[state].get_regexp_number()

                    states[counter] = b_State(counter, endVal)

                    counter = counter + 1

                transitions.add((actState, symbol, newStatesRev[frozenset(nextState)]))

        # remove unused symbols
        toRemove = alphabet.keys()
        for trans in transitions:
            if trans[1] in toRemove:
                toRemove.remove(trans[1])
        self._automaton.alphabet = alphabet
        self._automaton.remove_symbols(toRemove)

        # set new symbol ID's
        mapId = dict() # maps old id -> new id
        alphCounter = 0
        alphabet = dict()
        for id, sym in self._automaton.alphabet.iteritems():
            sym.set_id(alphCounter)
            alphabet[alphCounter] = sym
            mapId[id] = alphCounter
            alphCounter += 1

        # correct symbol ID's in transitions
        newTrans = set()
        for trans in transitions:
            newTrans.add((trans[0], mapId[trans[1]], trans[2]))

        # create head DFA
        self.dfa.set_multilanguage(self.get_multilanguage())
        self.dfa._automaton.start = 0
        self.dfa._automaton.alphabet = alphabet
        self.dfa._automaton.states = states
        self.dfa._automaton.transitions = newTrans
        self.dfa._automaton.final = final
        self.dfa._automaton.Flags["Hybrid FA - DFA part"] = True
        self.dfa._automaton.Flags["Deterministic"] = True
        self.dfa._automaton.Flags["Epsilon free"] = True
        self.dfa._automaton.Flags["Alphabet collision free"] = True

        nfaPosition = 0
        for dfaState, nfaStates in borders.iteritems():
            for nfaState in nfaStates:
                self.nfas[nfaPosition] = b_nfa()
                self.nfas[nfaPosition].create_from_nfa_data(self._nfaEpsFree.get_automaton(False), True)
                self.nfas[nfaPosition]._automaton.start = nfaState
                self.nfas[nfaPosition]._automaton.Flags["Hybrid FA - one NFA part"] = True
                self.nfas[nfaPosition].remove_unreachable()
                self.tran_aut[nfaPosition] = dfaState
                nfaPosition += 1
        
        self._automaton = b_nfa()
        
        a = self.dfa.get_automaton(False) # shortcut
        cur_state = a.start
        # sort transitions
        for s in range(0, len(a.states)):
            self._sort[s] = []
        for t in a.transitions:
            self._sort[t[0]].append(t[1:])

        self._compute = True

    def _is_special(self, state):
        """
            Realize if state is special - has to be a border state
            
            :param state: ID of NFA state
            :type state: int
            
            :returns: Boolean if state has to be a border state
            :rtype: bool
        """
        if self._MAX_TX != -1 and self._stateTrans.has_key(state) and len(self._stateTrans[state]) < self._MAX_TX:
            return False
            
        if self._SPECIAL_MIN_DEPTH != -1 and self._depthOfStates[state] < self._SPECIAL_MIN_DEPTH:
            return False

        if self._MAX_HEAD_SIZE != -1 and self._head_size < self._MAX_HEAD_SIZE:
            return False

        return True

    def _setDepth(self):
        """
            Set depth for each state. Initial state has depth 0.
        """

        stack = list()
        stack.append(self._automaton.start)

        self._depthOfStates[self._automaton.start] = 0

        while stack:
            actState = stack.pop()

            for transition in self._stateTrans[actState]:
                toState = transition[1]
                if self._depthOfStates.has_key(toState): # depth was already set
                    continue
                self._depthOfStates[toState] = self._depthOfStates[actState]+1
                if self._stateTrans.has_key(toState): # toState has another transitions
                    stack.append(toState)

    def search(self, input_string):
        """
            Function will find patterns in the given string.

            :param input_string: Input string.
            :param input_string: string
            :returns: Bitmap of matched regular expressions.
            :rtype: list(int)
        """
        # Create mapping between reg. exp. number and coresponding final states.
        sameFinal = dict()
        for fstate in self._nfaEpsFree._automaton.final:
            rnums = self._nfaEpsFree._automaton.states[fstate].get_regexp_number()
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
        self._bitmap = [0] * rules

        self._search(self.dfa, input_string)
        
        return self._bitmap

    def _search(self, nfa, input_string):
        """
            Function will find patterns in the given string in given automaton.
        """
        # Stack of states. State is list (tupple) consisting of state and unprocessed part of input string.
        Stack = list()
        # Set of actual states.
        ActState = set()

        # Create start state.
        ActState.add((nfa._automaton.start, input_string))
        # Add start state to stack.0
        Stack.append(ActState)

        borders = dict()
        for i in range(0, len(self.tran_aut)):
            borders.setdefault(self.tran_aut[i], set()).add(i)

        # If needed create mapping between states and outgoing transitions.
        _mapper = dict()
        for transition in nfa._automaton.transitions:
            if _mapper.has_key(transition[0]) == True:
                _mapper[transition[0]].add((transition[1], transition[2]))
            else:
                _mapper[transition[0]] = set()
                _mapper[transition[0]].add((transition[1], transition[2]))

        # Until stack is empty, search
        while len(Stack) != 0:
            # Pop state from stack.
            ActState = Stack.pop()
            newActState = set()
            # Create new state. Accept char if possible and add state to new state.
            for state in ActState:
                if _mapper.has_key(state[0]):
                    for transition in _mapper[state[0]]:
                        try:
                            res = nfa._automaton.alphabet[transition[0]].accept(state[1])
                        except:
                            pass
                        else:
                            newActState.add((transition[1],res))
                # If in final state, set coresponding bitmap field to 1.
                if nfa._automaton.states[state[0]].is_final() == True:
                    for rnum in nfa._automaton.states[state[0]].get_regexp_number():
                        self._bitmap[rnum] = 1
                # Try to find in NFA tail if current state is a border one
                if borders.has_key(state[0]):
                    for nfaIndex in borders[state[0]]:
                        self._search(self.nfas[nfaIndex], state[1])
            # If possible add new state to stack.
            if len(newActState) > 0:
                Stack.append(newActState)

    def report_memory_naive(self):
        """
            Report consumed memory in bytes. Read documentaion in b_dfa
            and b_nfa methods for more information.
            
            :returns: Returns number of bytes.
            :rtype: int
        """
        size = self.dfa.report_memory_naive()
        for i in range(0, len(self.nfas)):
            size += self.nfas[i].report_memory_naive()
        size += len(self.nfas)*math.ceil(math.log(sys.maxint)/8)
        return int(size)
        
    def report_memory_optimal(self):
        """
            Report consumed memory in bytes. Read documentaion in b_dfa
            and b_nfa methods for more information.
            
            :returns: Returns number of bytes.
            :rtype: int
        """
        size = self.dfa.report_memory_optimal()
        for i in range(0, len(self.nfas)):
            size += self.nfas[i].report_memory_optimal()
        size += len(self.nfas)*math.ceil(math.log(sys.maxint)/8)
        return int(size)

    def get_automaton(self):
        """
            DFA head of automaton is save in self.dfa, NFA tails are in self.nfas.
            Read instruction in __init__ method.
            
            :raises: empty_automaton_exception()
        """
        raise empty_automaton_exception()

    def show(self, file_name):
        """
            Print states, alphabet, start, transitions, final, Flags of DFA
            part and NFA parts. And save graphviz dot file, representing
            graphical structure of nfa_data.

            :param file_name: Name of output DOT file
            :type file_name: string
        """

    # Display DFA part.
        print '*' * 80
        print "*** HYBRID FA - DFA part ***"
        print "STATES:", self.dfa.get_automaton(False).states, '\n'
        print "ALPHABET:", self.dfa.get_automaton(False).alphabet, '\n'
        print "START STATE:", self.dfa.get_automaton(False).start, '\n'
        print "TRANSITIONS:", self.dfa.get_automaton(False).transitions, '\n'
        print "FINAL STATES:", self.dfa.get_automaton(False).final, '\n'
        print "FLAGS OF AUTOMAT:", self.dfa.get_automaton(False).Flags
        print '*' * 80, '\n'
        self.dfa._automaton.show(os.path.splitext(file_name)[0] + "_DFA" + os.path.splitext(file_name)[1])
    # Display NFA parts.
        for i in range(0, len(self.nfas)):
            print '*' * 80
            print "*** HYBRID FA - NFA part which joining to",
            print "STATES:", self.nfas[i].get_automaton(False).states, '\n'
            print "ALPHABET:", self.nfas[i].get_automaton(False).alphabet, '\n'
            print "START STATE:", self.nfas[i].get_automaton(False).start, '\n'
            print "TRANSITIONS:", self.nfas[i].get_automaton(False).transitions, '\n'
            print "FINAL STATES:", self.nfas[i].get_automaton(False).final, '\n'
            print "FLAGS OF AUTOMAT:", self.nfas[i].get_automaton(False).Flags
            print '*' * 80, '\n'
            self.nfas[i]._automaton.show(os.path.splitext(file_name)[0] + "_NFA_" + str(i) + os.path.splitext(file_name)[1])

    def save_to_file(self, file_name):
        """
            DFA head of automaton is save in self.dfa, NFA tails are in self.nfas.
            Read instruction in __init__ method.
            
            :raises: empty_automaton_exception()
        """
        raise empty_automaton_exception()

    def get_state_num(self):
        """
            Return number of states in Hybrid automaton.

            :returns: Number of states in Hybrid automaton
            :rtype: int
        """

        number_states = 0
        for i in range(0, len(self.nfas)):
            number_states += len(self.nfas[i].get_automaton(False).states)
        number_states += len(self.dfa.get_automaton(False).states)
        return number_states

    def get_trans_num(self):
        """
            Return number of transitions in Hybrid automaton.

            :returns: Number of transitions in Hybrid automaton
            :rtype: int
        """

        number_tran = 0
        for i in range(0, len(self.nfas)):
            number_tran += len(self.nfas[i].get_automaton(False).transitions)
        number_tran += len(self.dfa.get_automaton(False).transitions)
        return number_tran
