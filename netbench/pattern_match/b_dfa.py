###############################################################################
#  b_dfa.py: Module for PATTERN MATCH - base DFA implementation.
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

import sym_char
import sym_char_class
from b_state import b_State
from b_automaton import b_Automaton
from nfa_data import nfa_data
import random
import b_state
import b_symbol
import gc
import copy
from pattern_exceptions import ALPHABET_COLLISION_FREE_ERROR
from pattern_exceptions import DETERMINISTIC_ERROR
import math

class b_dfa(b_Automaton):
    """
        A base class for DFA automata.
    """
    def __init__(self):
        b_Automaton.__init__(self)
        self._state_representation = list() # List of states in DFA.
                                            # Every state is represented
                                            # by set of states in NFA
        self._compute = False

    def determinise(self, create_table = False, states_limit = 0):
        """
            Determinisation of automaton.

            :param create_table: If create_table = false than state representation table is not created and less memory is consumed.
            :type create_table: boolean

            :param states_limit: If num of states exceeds this limit, during determinization, then flag "Deterministic" is set to False and determinize stops; if nfa exceeds limit and is already deterministic, then nothing happens (this is because speed, not because logic); safe use is only if you want to stop algorithm if it exceeds limit; zero means no limit.
            :type states_limit: int

            :flags: Set Deterministic, Epsilon Free and Alphabet collision free.

            This method sets _compute to False, and get_compute() will return False until compute() is called.
        """

#        if not self.has_flag("Alphabet collision free") \
#           or self.get_flag("Alphabet collision free") == False:
#            raise ALPHABET_COLLISION_FREE_ERROR
        
        # Automaton doesn't have any state = automaton is empty
        if self._automaton.is_empty() or self._automaton.start < 0:
            return

        self.remove_epsilons() # check the Epsilon free flag ?

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
        stateTrans = dict()

        # transtions from each state
        for transition in self._automaton.transitions:
            stateTrans.setdefault(transition[0], set()).add((transition[1], transition[2]))

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
            
            # transitions from actual state for each symbol
            outSymbols = dict() # (symbol id, set of states id) 
            for state in newStates[actState]:
                if state not in stateTrans.keys():
                    continue
                for t in stateTrans[state]:
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
#                        print "COLLISION DETECTED"

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
                                if new not in alphabetRev:
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

            # create new transitions
            for symbol, nextState in outSymbols.iteritems(): 
                if not nextState:
                    continue # no next states -> ignore symbol

                if frozenset(nextState) not in newStatesRev.keys():
                    # create a new state
                    newStatesRev[frozenset(nextState)] = counter
                    newStates[counter] = nextState
                    stack.append(counter)

                    endVal = set() # set of regular expression numbres 
                    for state in nextState:
                        if self._automaton.states[state].is_final() == True:
                            endVal |= self._automaton.states[state].get_regexp_number()

                    states[counter] = b_State(counter, endVal)

                    if states_limit != 0 and counter > states_limit:
                        self.set_flag("Deterministic", False)
                        return

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
            
        # update automaton
        self._automaton.start = 0
        self._automaton.alphabet = alphabet
        self._automaton.states = states
        self._automaton.transitions = newTrans
        self._automaton.final = final

        self.set_flag("Deterministic", True)
        self.set_flag("Epsilon Free", True)
        if len(self._automaton.alphabet) > 0:
            self.set_flag("Alphabet collision free", True)

        self._compute = False

        if create_table == True:
            for i in range(0, counter):
                self._state_representation.append(newStates[i])


    def _determinise(self, create_table = False, states_limit = 0):
        """
            Determinisation of automaton.

            :param create_table: If create_table = false than state representation table is not created and less memory is consumed.
            :type create_table: boolean

            :param states_limit: If num of states exceeds this limit, during determinization, then flag "Deterministic" is set to False and determinize stops; if nfa exceeds limit and is already deterministic, then nothing happens (this is because speed, not because logic); safe use is only if you want to stop algorithm if it exceeds limit; zero means no limit.
            :type states_limit: int

            :raises: ALPHABET_COLLISION_FREE_ERROR() if alphabet is not collision free.
            :flags: Set Deterministic and Epsilon Free.

            This method sets _compute to False, and get_compute() will return False until compute() is called.
        """
        if self.has_flag("Deterministic") and self.get_flag("Deterministic") == True:
            return
        if self.has_flag("Epsilon Free") == False or self.get_flag("Epsilon Free") == False:
            self.remove_epsilons()

        if not self.has_flag("Alphabet collision free") \
           or self.get_flag("Alphabet collision free") == False:
            raise ALPHABET_COLLISION_FREE_ERROR
        
        # Automatom doesn't have any state = automaton is empty
        if self._automaton.is_empty() or self._automaton.start < 0:
            return
            
        Stack = list()
        Citac = 0
        newStates = dict()
        newStatesBack = dict()
        tmp = set()
        tmp.add(self._automaton.start)
        newStates[Citac] = tmp
        newStatesBack[frozenset(tmp)] = Citac
        Citac = Citac+1
        Stack.append(0)
        EndStates = set()
        Transitions = set()
        alphabetCounter = 0;
        alphabet = dict()
        alphabetBack = dict()
        states = dict()
        states[0] = b_State(0, self._automaton.states[self._automaton.start].get_regexp_number())
        StateOutSymbols = dict()

        for transition in self._automaton.transitions:
            if StateOutSymbols.has_key(transition[0]) == True:
                StateOutSymbols[transition[0]].add((transition[1], transition[2]))
            else:
                StateOutSymbols[transition[0]] = set()
                StateOutSymbols[transition[0]].add((transition[1], transition[2]))

        while len(Stack) != 0:
            ActState = Stack.pop();
            TransitionLine = dict();
            if len(newStates[ActState].intersection(self._automaton.final)) != 0 :
                EndStates.add(ActState)
            Symbols = set();

            SymbolSetList = list()
            translationTable = list()

            for States in newStates[ActState]:
                if States in StateOutSymbols.keys():
                    for sym in StateOutSymbols[States]:
                        if self._automaton.alphabet[sym[0]].get_type() == b_symbol.io_mapper["b_Sym_char"]:
                            SymbolSetList.append(set(self._automaton.alphabet[sym[0]].char))
                            translationTable.append(sym[1])
                        elif self._automaton.alphabet[sym[0]].get_type() == b_symbol.io_mapper["b_Sym_char_class"]:
                            SymbolSetList.append(self._automaton.alphabet[sym[0]].charClass)
                            translationTable.append(sym[1])
                        else:
                            raise Exception()

            res = self.__allIntersections(SymbolSetList)

            translatedUsedList = list()

            for used in res[0]:
                newSet = set()
                for target in used:
                    newSet.add(translationTable[target])
                translatedUsedList.append(newSet)

            for i in range(0, len(translatedUsedList)):
                if frozenset(translatedUsedList[i]) not in newStatesBack.keys():
                    newStatesBack[frozenset(translatedUsedList[i])] = Citac;
                    newStates[Citac] = translatedUsedList[i];
                    Stack.append(Citac);

                    endVal = set()
                    for state in translatedUsedList[i]:
                        if self._automaton.states[state].is_final() == True:
                            endVal |= self._automaton.states[state].get_regexp_number()

                    states[Citac] = b_State(Citac, endVal)

                    if states_limit != 0 and Citac > states_limit:
                        self.set_flag("Deterministic", False)
                        return

                    Citac = Citac + 1

                if frozenset(res[1][i]) not in alphabetBack.keys():
                    alphabetBack[frozenset(res[1][i])] = alphabetCounter;
                    if len(res[1][i]) > 1:
                        strSymSetMod = str()
                        for sym in res[1][i]:
                            strSymSetMod += sym
                        strSymSetMod = "[" + strSymSetMod + "]"
                        Tmp = sym_char_class.b_Sym_char_class(strSymSetMod, res[1][i], alphabetCounter)
                        alphabet[Tmp.get_id()] = Tmp
                    else:
                        for sym in res[1][i]:
                            char = sym
                        Symbol = sym_char.b_Sym_char(char, char, alphabetCounter)
                        alphabet[Symbol.get_id()] = Symbol
                    alphabetCounter += 1

                Transitions.add((ActState, alphabetBack[frozenset(res[1][i])], newStatesBack[frozenset(translatedUsedList[i])]))

        self._automaton.start = 0
        self._automaton.alphabet = alphabet
        self._automaton.states = states
        self._automaton.transitions = Transitions
        self._automaton.final = EndStates

        if create_table == True:
            for i in range(0, Citac):
                self._state_representation.append(newStates[i])

        self.set_flag("Deterministic", True)
        self.set_flag("Epsilon Free", True)
        self._compute = False

    def minimise(self):
        """
            Minimalization of DFA automaton.

            :raises: ALPHABET_COLLISION_ERROR() if alphabet is not collision free.
            :raises: DETERMINISTIC_ERROR() if automaton is not deterministic.
            :flags: Sets Minimal flag to true.

            This method sets _compute to False, and get_compute() will return False until compute() is called.
        """

        if not self.has_flag("Alphabet collision free") \
        or self.get_flag("Alphabet collision free") == False:
            raise ALPHABET_COLLISION_FREE_ERROR
        if not self.has_flag("Deterministic") \
        or self.get_flag("Deterministic") != True:
            raise DETERMINISTIC_ERROR

        # variables
        a = self._automaton    # shortcut
        newClasses = dict()    # new indistinguishable states
        actualClasses = dict() # actual indistinguishable states
        table = dict()  # table of "transitions", key is state, value is class

        # 1) *** Eliminate not available states. ***
        self.remove_unreachable()

        # 2) *** Compute not indistinguishable states. ***
        # set default table
        for state in a.states.keys():
          table[state] = dict()
        for t in a.transitions:
          table[t[0]] [t[1]] = t[2]
        defaultTable = copy.deepcopy(table)
        # zero iteration:
        # set first class other then final states
        newClasses[0] = a.states.keys()
        for finalState in a.final:
            if finalState in newClasses[0]:
                newClasses[0].remove(finalState)

        if self.get_multilanguage() is True:
            # set final states into next classes
            # each final state will be set in class according 
            # get_regexp_number()
            newClassIdOffset = len(newClasses)
            newClassIdMapper = dict()
            for finalStateKey in a.final:
                frozen_regexp = frozenset(a.states[finalStateKey].get_regexp_number())
                if not newClassIdMapper.has_key(frozen_regexp):
                    newClassIdMapper[frozen_regexp] = newClassIdOffset
                    newClasses[newClassIdOffset] = list()
                    newClassIdOffset += 1
                newClasses[newClassIdMapper[frozen_regexp]].append(finalStateKey)
        else:
            # all final states are in one class
            newClasses[1] = list(a.final)
        
        # indistinguishable iterations
        while newClasses != actualClasses:
            actualClasses = copy.deepcopy(newClasses)
            # recompute table for next iteration
            table = copy.deepcopy(defaultTable)
            for state in table.keys():
                for symbol in table[state].keys():
                    for ClassID in range(0, len(actualClasses), 1):
                        if table[state] [symbol] in actualClasses[ClassID]:
                            table[state] [symbol] = ClassID
                            break
            newClasses = dict()
            for ClassID in sorted(actualClasses.keys()):
                states_in_class = copy.deepcopy(actualClasses[ClassID])
                while states_in_class != []:
                    state = states_in_class[0]
                    states_in_class.remove(state)
                    states_in_new_class = []
                    states_in_new_class.append(state)
                    for other_state in list(states_in_class):
                        if table[state] == table[other_state]:
                            states_in_class.remove(other_state)
                            states_in_new_class.append(other_state)
                    newClassID = len(newClasses.keys())
                    newClasses[newClassID] = states_in_new_class
        # *** Change to Reduced DFA. ***
        # change STATES
        back = a.states
        a.states = dict()
        for ClassID in range(0, len(actualClasses), 1):
            finalIndication = set() # indication of final states
            for state in actualClasses[ClassID]:
                if state in a.final:
                    finalIndication |= back[state].get_regexp_number()
            a.states[ClassID] = b_State(mid = ClassID, rnum = finalIndication)
        # change ALPHABET - nothing to change
        # change START STATE
        for ClassID in range(0, len(actualClasses), 1):
            if a.start in actualClasses[ClassID]:
                a.start = ClassID
                break
        # change TRANSITIONS
        newTran = set() # re-computed transitions
        for t in a.transitions:
            sourceState = -1
            destinationState = -1
            # discover source state
            for ClassID in range(0, len(actualClasses), 1):
                if t[0] in actualClasses[ClassID]:
                    sourceState = ClassID
                    break
            # discover destination state
            for ClassID in range(0, len(actualClasses), 1):
                if t[2] in actualClasses[ClassID]:
                    destinationState = ClassID
                    break
            # add new transitions
            newTran.add((sourceState, t[1], destinationState))
        a.transitions = newTran
        # change FINAL STATES
        newFinal = set()
        for finalState in a.final:
            for ClassID in range(0, len(actualClasses), 1):
                if finalState in actualClasses[ClassID]:
                    newFinal.add(ClassID)
                    break
        a.final = newFinal

        # 3) *** Removal of surplus state that do not affect the adoption
        # of a string. ***
        self.set_flag("Minimal", True)
        self._compute = False

    def compute(self):
        """
            Determinise and minimise object. Implentation of inherited method from b_automaton.
        """
        b_Automaton.compute(self)
        self.determinise()
        self.minimise()
        self._compute = True

    def __allIntersections(self, sets):
        """
            Compute all posible(in determinisation way, not in mathematic way - when char from set is used in intersection it's removed) intersections of list of char sets

            :param sets: List of char sets.
            :type sets: list(set(char))
            :returns: Intersections of list of char sets.
            :rtype: tupple(set(int), list(set(char)))
        """

        intersections = list()
        usedSetsList = list()

        usedSets = set()

        stop = False

        while stop == False:
            intersection = set()
            usedSets = set()

            j = 0
            while j < len(sets):
                if (len(sets[j]) > 0):
                    intersection = sets[j]
                    usedSets.add(j)
                    stop = False
                    break
                else:
                    j += 1
            else:
                stop = True

            if stop == False:
                for i in range(j, len(sets)):
                    #if intersection.isdisjoint(sets[i]) == False:
                    if len(intersection.intersection(sets[i])) > 0:
                        intersection = intersection.intersection(sets[i])
                        usedSets.add(i)

                intersections.insert(len(intersections), intersection)
                usedSetsList.insert(len(usedSetsList), usedSets)

                for k in usedSets:
                    sets[k] = sets[k].difference(intersection)


        return (usedSetsList, intersections)

    def isomorphic(self, nfa_data):
        """
            Check isomorfism of automaton with another nfa_data object.
            Both automatons must be deterministic and without unreachable states.

            :param nfa_data: nfa_data object containing second automaton.
            :type nfa_data: nfa_data
            :returns: True if automata are isomorphic, else otherwise.
            :rtype: boolean
        """

        try:
            if self._automaton.Flags["Deterministic"] == False:
                raise DETERMINISTIC_ERROR

            if nfa_data.Flags["Deterministic"] == False:
                raise DETERMINISTIC_ERROR
        except:
            raise DETERMINISTIC_ERROR

        # rename automatons, dfa means nfa_data of dfa
        dfa1 = self._automaton
        dfa2 = nfa_data

        #print dfa1
        #print dfa2

        # compute translator from alphabet of dfa1 to alphabet of dfa2
        a1 = dfa1.alphabet
        a2 = dfa2.alphabet
        symbols_used_in1 = set()
        for t in dfa1.transitions:
            symbols_used_in1.add(t[1])
        a2_to_a1 = dict() # translator from dfa1 alphapet to dfa2 alphabet
        for symbol1 in symbols_used_in1:
            found = False
            for symbol2 in a2.keys():
                if a1[symbol1] == a2[symbol2]:
                    found = True
                    a2_to_a1[symbol2] = symbol1
            if not found:
                return False
        #print a2_to_a1

        # compute dictionaries lead_to (state to list of states), lead_with (state,state by symbol) and lead_to_by(state, symbol to state)
        lead_to1 = dict()
        lead_with1 = dict()
        lead_to_by1 = dict()
        for s in dfa1.states:
            lead_to1[s] = list()
        for t in dfa1.transitions:
            lead_with1[ ( t[0],t[2] ) ] = t[1]
            lead_to_by1[ ( t[0],t[1] ) ] = t[2]
            lead_to1[t[0]].append(t[2])

        lead_to2 = dict()
        lead_with2 = dict()
        lead_to_by2 = dict()
        for s in dfa2.states:
            lead_to2[s] = list()
        for t in dfa2.transitions:
            #print t[1]
            lead_with2[ ( t[0],t[2] ) ] = a2_to_a1[t[1]]
            lead_to_by2[ ( t[0], a2_to_a1[t[1]] ) ] = t[2]
            lead_to2[t[0]].append(t[2])

        # add start states as first double to Stack
        Stack = [(dfa1.start,dfa2.start)]
        # mark start states as used before
        was = [(dfa1.start,dfa2.start)]
        was1 = [dfa1.start]
        was2 = [dfa2.start]
        while Stack:
            (s1,s2) = Stack.pop()
            #print "States from stack", (s1,s2)
            # check number of transitions
            if len(lead_to1[s1]) != len(lead_to2[s2]):
                #print "not number of transitions"
                return False
            # check if both are final or both are not final
            #if dfa1.states[s1].is_final() != dfa2.states[s2].is_final():
            #    return False
            if (s1 in dfa1.final) != (s2 in dfa2.final):
                #print "not finals"
                return False
            # find for all transitions in dfa1 corresponding transitions in dfa2
            for s1_to in lead_to1[s1]:
                symbol = lead_with1[(s1,s1_to)]
                # find corresponding state s2_to for (s1,symbol) -> s1_to in dfa2
                # transition with symbol from s2 does not exist
                if (s2,symbol) not in lead_to_by2.keys():
                    #print "not symbol", (s2, symbol), "in", lead_to_by2.keys()
                    return False
                s2_to = lead_to_by2[(s2,symbol)]
                # not in computed
                if (s1_to,s2_to) not in was:
                    if s1_to in was1 or s2_to in was2:
                        #print "not integrity:", s1_to, "in", was1, " ", s2_to, "in", was2, "\n", (s1_to,s2_to), "not in", was
                        return False
                    #print "adding to stack", (s1_to,s2_to)
                    Stack.insert(0,(s1_to,s2_to))
                    was1.append(s1_to)
                    was2.append(s2_to)
                    was.append((s1_to,s2_to))
                    #print "stack", Stack
                    #print "was", was

        #print "returning True"
        return True

    def report_memory_optimal(self):
        """
            Report consumed memory in bytes. Optimal mapping algorithm is used \
            (with oracle). Basic algorithm for this variant of mapping is:     \
            M = \|transitions\| * ceil(log(\|states\|, 2) / 8)
            
            :returns: Returns number of bytes.
            :rtype: int
        """
        tr_len = len(self._automaton.transitions)
        st_len = len(self._automaton.states)
        return int(tr_len * math.ceil(math.log(st_len, 2) / 8));
    
    def report_memory_naive(self):
        """
            Report consumed memory in bytes. Naive mapping algorithm is used \
            (2D array). Basic algorithm for this variant of mapping is:      \
            M = \|states\| * \|alphabet\| * ceil(log(\|states\| + 1, 2) / 8)
            
            :returns: Returns number of bytes.
            :rtype: int
        """
        st_len = len(self._automaton.states)
        al_len = len(self._automaton.alphabet)
        return int(st_len * al_len * math.ceil(math.log(st_len + 1, 2) / 8));

###############################################################################
# End of File b_dfa.py                                                        #
###############################################################################
