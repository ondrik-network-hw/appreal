#!/usr/bin/python

"""
Tool for approximate reductions of finite automata used in network traffic
monitoring.

Copyright (C) 2017  Vojtech Havlena, <xhavle03@stud.fit.vutbr.cz>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License.
If not, see <http://www.gnu.org/licenses/>.
"""

import copy
import aux_functions as aux
import FAdo.fa

from collections import deque

#Precise of float numbers (for output)
PRECISE = 3
#Max number of symbols on transition (DOT format)
SYMBOLS = 25

class Transition(object):
    """Class for represention of the WFA transition.
    """
    def __init__(self, src, dest, sym, weight):
        self.src = src
        self.dest = dest
        self.symbol = sym
        self.weight = weight


class CoreWFA(object):
    """Basic class for representation of WFA
    """
    def __init__(self, transitions=None, finals=None, start=0, alphabet=None):
        self._transitions = transitions
        if self._transitions == None:
            self._transitions = []
        self._finals = finals
        if self._finals == None:
            self._finals = dict()
        self._start = start
        self._states_dict = None
        self._alphabet = alphabet

    def get_transitions(self):
        """Get all transitions of the WFA.

        Return: List of transitions.
        """
        return self._transitions

    def set_transitions(self, transitions):
        """Set transitions of the WFA.

        Keyword arguments:
        transition -- The list of transitions.
        """
        self._transitions = transitions

    def get_finals(self):
        """Get all final states of the WFA.

        Return: Dictionary: Final state -> float (weight)
        """
        return self._finals

    def all_states_final(self):
        """Check whether all states are finals (nonzero probability of
        accepting).

        Return: Bool
        """
        fin = set(self._finals.keys())
        states = set(self.get_states())
        return (fin == states)

    def set_finals(self, finals):
        """Set final states of the WFA.

        Keyword arguments:
        finals -- Dictionary of final states and their probability of accepting.
        """
        self._finals = finals

    def get_start(self):
        """Get the start state (only one start state is allowed).

        Return: Start state.
        """
        return self._start

    def get_alphabet(self):
        """Get alphabet used by the WFA. If the alphabet is not explicitly
        given (in constructor), the alphabet is computed from the transitions.

        Return: List (of symbols).
        """
        alph = []
        if self._alphabet != None:
            return self._alphabet
        for transition in self._transitions:
            if transition.symbol not in alph:
                alph.append(transition.symbol)
        return alph

    def get_states(self):
        """Get all states of the WFA (the list of states is computed
        from the transitions).

        Return: List of states.
        """
        states = [self._start]
        for final, _ in self._finals.iteritems():
            if final not in states:
                states.append(final)
        for transition in self._transitions:
            if transition.src not in states:
                states.append(transition.src)
            if transition.dest not in states:
                states.append(transition.dest)
        return states

    def get_rename_dict(self):
        """Get the dictionary containing original state labels and renamed
        state labels. The dictionary is created after method rename_states
        is invoked.

        Return: Dictionary: State (original) -> State (renamed).
        """
        return self._states_dict

    def get_dictionary_transitions(self):
        """Get transitions in the form of dictionary (for each state there
        is a list of transitions leading from this state).

        Return: Dictionary: State -> List(Transitions)
        """
        tr_dict = dict()
        for transition in self._transitions:

            try:
                tr_dict[transition.src].append(transition)
            except KeyError:
                tr_dict[transition.src] = [transition]

            # if transition.src not in tr_dict.keys():
            #     tr_dict[transition.src] = [transition]
            # else:
            #     tr_dict[transition.src].append(transition)
        return tr_dict

    def get_rev_transitions_aut(self):
        """Get automaton with reversed directions of transitios.

        Return: WFA with reversed transitions.
        """
        automaton = copy.deepcopy(self)
        for transition in automaton.get_transitions():
            tmp = transition.src
            transition.src = transition.dest
            transition.dest = tmp
        return automaton

    def get_aggregated_transitions(self):
        """Get aggregated transitions (merging transitions which differs
        only on symbol into a transition labeled with the list of symbols).

        Return: List(Transitions).
        """
        aggregate = dict()
        for transition in self._transitions:
            if (transition.src, transition.dest) not in aggregate:
                aggregate[(transition.src, transition.dest)] \
                    = [[transition.symbol], transition.weight]
            else:
                aggregate[(transition.src, transition.dest)][0]\
                    .append(transition.symbol)
                aggregate[(transition.src, transition.dest)][1] \
                    += float(transition.weight)
        return aggregate

    def to_dot(self, state_label=None):
        """Convert the WFA to dot format (for graphical visualization). Use
        aggregation of transitions between same states.

        Return: String (DOF format)
        Keyword arguments:
        state_label -- label of each state (shown inside of the state)
        """
        dot = str()
        dot += "digraph \" Automat \" {\n    rankdir=LR;\n"
        dot += "node [shape = doublecircle];\n"

        if len(self._finals) > 0:
            for state, weight in self._finals.iteritems():
                if state_label == None:
                    dot += "\"" + str(state) + "\"" + " [label=\"" \
                        + str(state) + ", " \
                        + str(round(weight, PRECISE)) + "\"]"
                else:
                    dot += "\"" + str(state) + "\"" + " [label=\"" \
                        + str(state) + ", " \
                        + "{:.2e}".format(state_label[state]) + "\"]"
                dot += ";\n"

        dot += "node [shape = circle];\n"
        if state_label != None:
            for state in self.get_states():
                if state not in self._finals:
                    dot += "\"" + str(state) + "\"" + " [label=\"" \
                        + str(state) + ", " \
                        + "{:.2e}".format(state_label[state]) + "\"]"
                    dot += ";\n"
        elif self._start not in self._finals:
            dot += "\"" + str(self._start) + "\"" + " [label=\"" \
                + str(self._start) + "\"]"
            dot += ";\n"

        dot += "node [shape = circle];\n"
        for (src, dest), res in self.get_aggregated_transitions().items():
            dot += "\"" + str(src) + "\""
            dot += " -> "
            dot += "\"" + str(dest) + "\""
            dot += " [ label = \"" + self.format_label(res[0], res[1])
            dot += "\" ];\n"

        dot += "}"
        return dot

    def to_fa_format(self, alphabet=False):
        """Converts automaton to FA format (WFA version).

        Return: String (WFA in the FA format)
        Keyword arguments:
        alphabet -- whether show explicitly symbols from alphabet.
        """
        fa = str()
        fa += str(self._start)
        if alphabet:
            fa += ":"
            for sym in self.get_alphabet():
                fa += hex(sym) + " "
            fa += "\n"
        for transition in self._transitions:
            fa += "{0} {1} {2} {3}\n".format(transition.src, transition.dest,
                transition.symbol, transition.weight)
        for final, weight in self._finals.iteritems():
            fa += "{0} {1}\n".format(final, weight)

        return fa

    def to_automata_fado_format(self):
        """Convert to FAdo format (consider only the support of the WFA).

        Return: String (The support of the WFA in the FAdo format)
        """
        fado = str()
        fado += "@DFA" #or @NFA
        for fin in self._finals.keys():
            fado += " " + str(fin)
        fado += "$"
        for sym in self.get_alphabet():
            fado += " " + str(sym)
        fado += "\r\n"
        for transition in self._transitions:
            if transition.weight > 0.0:
                fado += str(transition.src) + " " + str(transition.symbol) + " " + \
                    str(transition.dest) + "\r\n"
        return fado

    def supp_to_fado(self, dfa):
        """Convert the support of the WFA to the inner representation used in
        FAdo library.

        Return: Automaton used in FAdo library
        Keyword arguments:
        dfa -- Is the support DFA or NFA.
        """
        if dfa:
            fado_aut = FAdo.fa.DFA()
        else:
            fado_aut = FAdo.fa.NFA()
        sigma = []
        for sym in self.get_alphabet():
            sigma.append(str(sym))

        fado_aut.setSigma(sigma)
        for state in self.get_states():
            fado_aut.addState(state)

        fado_aut.setInitial(self.get_start())
        for fin in self._finals.keys():
            fado_aut.addFinal(fin)

        for transition in self._transitions:
            if transition.weight > 0.0:
                fado_aut.addTransition(transition.src, str(transition.symbol),
                    transition.dest)
        return fado_aut


    def rename_states(self):
        """Rename states of the WFA. Assign to the states numbers
        from 0 to n-1 (n is the number of states). The start state has number 0.
        The renamed and original states are stored in the states_dict dictionary.
        """
        self._states_dict = dict()
        new_transitions = []
        new_finals = dict()

        self._states_dict[self._start] = 0

        for state in self.get_states():
            if state not in self._states_dict:
                dest = len(self._states_dict)
                self._states_dict[state] = dest

        for (state, prob) in self._finals.iteritems():
            if state not in self._states_dict:
                dest = len(self._states_dict)
                self._states_dict[state] = dest
            else:
                dest = self._states_dict[state]
            new_finals[dest] = prob

        for transition in self._transitions:
            new_transitions.append(Transition( \
                self._states_dict[transition.src], \
                self._states_dict[transition.dest], \
                transition.symbol, transition.weight))

        self._start = 0
        self._transitions = copy.deepcopy(new_transitions)
        self._finals = copy.deepcopy(new_finals)


    def product(self, aut):
        """Perform the product of two WFAs.

        Return: WFA representing the product of WFAs
        Keyword arguments:
        aut -- Second automaton for the product.
        """
        queue = deque([])
        ret_finals = dict()
        ret_transitions = []

        queue.append((self._start, aut.get_start()))
        ret_start = (self._start, aut.get_start())

        if (self._start in self._finals.keys()) \
            and (aut.get_start() in aut.get_finals().keys()):
            ret_finals[ret_start] = self._finals[self._start] \
                * aut.get_finals()[aut.get_start()]

        finished = [ret_start]
        tr_dict1 = self.get_dictionary_transitions()
        tr_dict2 = aut.get_dictionary_transitions()

        while len(queue) > 0:
            act = queue.popleft()

            if (act[0] in self._finals.keys()) \
                and (act[1] in aut.get_finals().keys()):
                ret_finals[act] = self._finals[act[0]] \
                    * aut.get_finals()[act[1]]

            if (act[0] not in tr_dict1.keys()) \
                or (act[1] not in tr_dict2.keys()):
                continue

            for tr1 in tr_dict1[act[0]]:
                for tr2 in tr_dict2[act[1]]:
                    if tr2.symbol != tr1.symbol:
                        continue

                    dest_state = (tr1.dest, tr2.dest)
                    ret_transitions.append(Transition(act, dest_state, \
                        tr1.symbol, tr1.weight * tr2.weight))

                    if dest_state not in finished:
                        finished.append(dest_state)
                        queue.append(dest_state)

        alphabet = self.get_alphabet()
        return CoreWFA(ret_transitions, ret_finals, ret_start, alphabet)

    def breadth_first_search(self, state, visited, tr_dict):
        """BFS in the automaton graph.

        Return: Out parameter visited (the list of visited states).
        Keyword arguments:
        state -- The start state of the BFS.
        visited -- The list of visited states (out parameter).
        tr_dict -- Transition dictionary.
        """
        queue = deque([state])
        while len(queue) > 0:
            head = queue.popleft()
            visited.add(head)
            if head not in tr_dict.keys():
                continue
            for transition in tr_dict[head]:
                if (transition.dest not in visited) \
                    and (transition.dest not in queue):
                    queue.append(transition.dest)


    def get_coaccessible_states(self):
        """Get coaccessible states of the WFA.

        Return: The list of coaccessible states.
        """
        visited = set([])
        reverse_aut = self.get_rev_transitions_aut()
        tr_dict = reverse_aut.get_dictionary_transitions()
        for state, _ in reverse_aut.get_finals().iteritems():
            reverse_aut.breadth_first_search(state, visited, tr_dict)
        return visited

    def get_accessible_states(self):
        """Get accessible states of the WFA.

        Return: The list of accessible states.
        """
        visited = set([])
        tr_dict = self.get_dictionary_transitions()
        self.breadth_first_search(self._start, visited, tr_dict)
        return visited

    def get_automata_restriction(self, states):
        """Get WFA restriction to only states in states.

        Return: WFA (restriction to states in the list states)
        Keyword arguments:
        states -- The list of states of the new WFA.
        """
        rest_transitions = []
        rest_finals = dict()
        alphabet = self.get_alphabet()
        for transition in self._transitions:
            if (transition.src in states) and (transition.dest in states):
                rest_transitions.append(copy.deepcopy(transition))

        for state, weight in self._finals.iteritems():
            if state in states:
                rest_finals[state] = weight

        return CoreWFA(rest_transitions, rest_finals,\
            copy.deepcopy(self._start), alphabet)

    def get_coaccessible_automaton(self):
        """Get automaton having only coaccessible states.

        Return: WFA having only coaccessible states.
        """
        costates = self.get_coaccessible_states()
        return self.get_automata_restriction(costates)

    def get_accessible_automaton(self):
        """Get automaton having only accessible states.

        Return: WFA having only accessible states.
        """
        access_states = self.get_accessible_states()
        return self.get_automata_restriction(access_states)

    def get_trim_automaton(self):
        """Get trimed WFA.

        Return: Trimmed WFA.
        Keyword arguments:
        """
        return self.get_accessible_automaton().get_coaccessible_automaton()

    def format_label(self, sym, weight):
        """Format label for DOT converting.

        Return: String (formatted label)
        Keyword arguments:
        sym -- List of symbols
        weight -- Weight of the transition.
        """
        max_symbols = SYMBOLS
        sym_str = str()
        if set(sym) == set(self.get_alphabet()):
            return "^[] " + str(round(weight, PRECISE))
        for char in sorted(sym):
            if max_symbols > 0:
                sym_str += aux.convert_to_pritable(chr(char), True)
                max_symbols = max_symbols - 1
            else:
                sym_str += "... {0}".format(len(sym))
                break
        return "[" + sym_str + "] " + str(round(weight, PRECISE))
