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
import core_wfa
import aux_functions as aux
import wfa_exceptions

from collections import deque

class NFAOperationException(wfa_exceptions.WFAOperationException):
    """Exception used when an error during parsing is occured.
    """
    def __init__(self, msg):
        super(NFAOperationException, self).__init__()
        self.msg = msg

    def __str__(self):
        return self.msg

"""Class representing an NFA.
"""
class NFA(core_wfa.CoreWFA):

    def __init__(self, transitions=None, finals=None, start=None, alphabet=None):
        super(NFA, self).__init__(transitions, finals, start, alphabet)

    def is_unambiguous(self):
        """Determine whether automaton is UFA (unambiguous).

        Return Bool, True -- is UFA, otherwise False.
        """
        prod_aut = super(NFA, self).product(self)
        restricted = prod_aut.get_trim_automaton()
        for (st1, st2) in restricted.get_states():
            if st1 != st2:
                return False
        return True

    def get_dfa(self):
        # TODO: implement on-the-fly determinization
        pass

    def get_unambiguous_nfa(self, max_states=None):
        """Convert general NFA into UFA. Algorithm from article
        Mohri: A Disambiguation Algorithm for Finite Automata and Functional
        Transducers. The resulting UFA can be exponentialy more succinct than
        input NFA.

        Return instance of NFA.
        """
        #TODO: Add support for multiple initial states
        if len(super(NFA, self).get_starts()) != 1:
            raise NFAOperationException("Only NFA with a single initial state can be converted unambiguous automaton.")

        queue = deque([])
        q_prime = set()

        b = super(NFA, self).product(self)
        b = b.get_trim_automaton()
        b_states = b.get_states()
        initial_state = super(NFA, self).get_starts().keys()[0]
        s = frozenset([initial_state])
        initial = (initial_state, s)
        queue.append(initial)
        q_prime.add(initial)
        num_states = 1

        finals_set = set([])
        relation = set([(initial, initial)])
        new_transitions = set()

        tr_dict = super(NFA, self).get_dictionary_transitions()

        while len(queue) > 0:
            p, s = queue.popleft()

            if p in super(NFA, self).get_finals().keys():
                is_final = True
                for item in aux.get_related(relation, (p, s)):
                    if item in finals_set:
                        is_final = False
                if is_final:
                    finals_set.add((p, s))

            for transition in super(NFA, self).get_transitions():
                if transition.src != p:
                    continue

                delta = []
                for state in list(s):
                    for state_tr in tr_dict[state]:
                        if state_tr.symbol == transition.symbol:
                            delta.append(state_tr.dest)

                t_set = set()
                for r in delta:
                    if (transition.dest, r) in b_states:
                        t_set.add(r)

                t_set = frozenset(t_set)

                cont = True
                for item in aux.get_related(relation, (p, s)):
                    if (item, transition.symbol, (transition.dest, t_set)) in new_transitions:
                        cont = False

                if cont:
                    if (transition.dest, t_set) not in q_prime:
                        q_prime.add((transition.dest, t_set))
                        queue.append((transition.dest, t_set))
                        num_states += 1
                        if (max_states is not None) and (num_states > max_states):
                            return None
                    new_transitions.add(((p, s), transition.symbol, (transition.dest, t_set)))

                    for item in aux.get_related(relation, (p, s)):
                        for tr_prime in list(new_transitions):
                            if (tr_prime[0] == item) and (tr_prime[1] == transition.symbol):
                                relation.add(((transition.dest, t_set), tr_prime[2]))
                                relation.add((tr_prime[2], (transition.dest, t_set)))

        transitions = []
        finals = dict()
        for item in list(new_transitions):
            transitions.append(core_wfa.Transition(item[0], item[2], item[1], 1.0))

        for fin in list(finals_set):
            finals[fin] = 1.0

        alphabet = self.get_alphabet()
        return NFA(transitions, finals, {initial: 1.0}, alphabet)

    def get_backward_nfa(self, state):
        """Backward subautomaton (automaton with only final state -- state).

        Return NFA corresponding to backward subautomaton.
        Keyword arguments:
        state -- state for creating his backward subautomaton
        """
        visited = set([])
        reverse_aut = super(NFA, self).get_rev_transitions_aut()
        tr_dict = reverse_aut.get_dictionary_transitions()
        reverse_aut.breadth_first_search(state, visited, tr_dict)
        restriction = super(NFA, self).get_automata_restriction(visited)
        restriction.set_finals({state: 1.0})
        return restriction


    def accept_word(self, word, read_all=True, tr_dict=None):
        """Simulate run of automata on an input word.

        Return Bool (True NFA accept word, otherwise False)
        Keyword arguments:
        word -- input word (string)
        read_all -- If True automaton must read the whole input and reach the
            final state. If False automaton might not read the whole input
            (just reach a final state during reading input word)
        """
        prev_states = set([super(NFA, self).get_starts().keys()])
        new_states = set()
        final_states = set(super(NFA, self).get_finals())
        if tr_dict is None:
            tr_dict = super(NFA, self).get_dictionary_transitions()

        for char in word:
            if len(prev_states) == 0:
                return False
            for prev in list(prev_states):
                for transition in tr_dict[prev]:
                    if transition.symbol == ord(char):
                        new_states.add(transition.dest)
            prev_states = copy.deepcopy(new_states)
            if (not read_all) and ((final_states & prev_states) != set()):
                return True
            new_states = set([])

        if (final_states & prev_states) != set():
            return True
        else:
            return False

    def get_branch_subautomata(self):
        """Find all so called branch subautomata (subautomata contains the NFA
        start state and the remaining states from outside of this subautomaton
        cannot reach subatomaton states).

        Return: List: [NFA]
        """

        if len(super(NFA, self).get_starts()) != 1:
            raise NFAOperationException("Only NFA with a single initial state can be divided into subautomata.")

        ret = []
        candidates = set([])
        reach = {}
        equivalence_class = set([])
        tr_dict = super(NFA, self).get_dictionary_transitions()
        initial_state = super(NFA, self).get_starts().keys()[0]

        for transition in tr_dict[initial_state]:
            candidates.add(transition.dest)
        if candidates == set([]):
            return []

        for state in list(candidates):
            visited = set([])
            super(NFA, self).breadth_first_search(state, visited, tr_dict)
            reach[state] = copy.deepcopy(visited)
            equivalence_class.add(frozenset([state]))

        candidates_list = list(candidates)
        for state1 in candidates_list:
            for state2 in candidates_list:
                if reach[state1].intersection(reach[state2]) != set([]):
                    equivalence_class = aux.merge_equivalence_classes(equivalence_class, state1, state2)

        for partition in list(equivalence_class):
            for state in list(partition):
                partition = partition.union(reach[state])
            partition = partition.union(frozenset([initial_state]))
            aut = super(NFA, self).get_automata_restriction(partition)
            aut.__class__ = NFA
            ret.append(aut)

        return ret

    def make_all_finals(self):
        """Mark all states as final states.
        """
        states = super(NFA, self).get_states()
        finals = dict()
        for state in states:
            finals[state] = 1.0
        super(NFA, self).set_finals(finals)


    def add_selfloop(self, states):
        """Add self-loops containing all symbols from an alphabet to states
        in states.

        Keyword arguments:
        states -- Set of states where the self-loops are added.
        """

        alphabet = super(NFA, self).get_alphabet()
        transitions = super(NFA, self).get_transitions()
        finals = super(NFA, self).get_finals()
        new_transitions = []
        for transition in transitions:
            if transition.src not in states:
                new_transitions.append(transition)

        for state in list(states):
            for symbol in alphabet:
                new_transitions.append(core_wfa.Transition(state, state, symbol, 1.0))
            finals[state] = 1.0

        super(NFA, self).set_transitions(new_transitions)
        super(NFA, self).set_finals(finals)


    def sladd(self, states):
        """Operation sladd. Add self-loops to states in states and trim
        this automaton.

        Return: NFA
        Keyword arguments:
        states -- list of states where the self-loops are added.
        """

        if len(super(NFA, self).get_starts()) != 1:
            raise NFAOperationException("Only to an NFA with a single initial state can be added self-loops.")

        aut = copy.deepcopy(self)
        aut.add_selfloop(states)
        tr_aut = aut.get_trim_automaton()
        tr_aut.__class__ = NFA
        return tr_aut

    def get_predecessors(self, state):
        """Operation that finds predessors of the state state.

        Return: List: [State]
        Keyword arguments:
        state -- The state whose predessors are found.
        """
        ret = set([])
        transitions = self.get_transitions()
        for tr in transitions:
            if tr.dest == state:
                ret.add(tr.src)
        return ret


    def to_dot(self, replace_alphabet=True, state_label=None):
        """Convert NFA to dot format (for graphical visualization). Use
        aggregation of transitions between same states.

        Return: String
        Keyword arguments:
        replace_alphabet -- if true the aggregated transition labeled by the
            whole alphabel is replaced with ^[]
        state_label -- label of each state (shown inside of the state)
        """
        dot = str()
        dot += "digraph \" Automat \" {\n    rankdir=LR;\n"
        dot += "node [shape = doublecircle];\n"

        if len(super(NFA, self).get_finals()) > 0:
            for state, _ in super(NFA, self).get_finals().iteritems():
                if state_label == None:
                    dot += "\"" + str(state) + "\"" + " [label=\"" \
                        + str(state) + "\"]"
                else:
                    dot += "\"" + str(state) + "\"" + " [label=\"" \
                        + str(state) + ", " \
                        + "{:.2e}".format(state_label[state]) + "\"]"
                dot += ";\n"

        dot += "node [shape = circle];\n"
        if state_label != None:
            for state in super(NFA, self).get_states():
                if state not in super(NFA, self).get_finals():
                    dot += "\"" + str(state) + "\"" + " [label=\"" \
                        + str(state) + ", " \
                        + "{:.2e}".format(state_label[state]) + "\"]"
                    dot += ";\n"
        else:
            for state in self.get_states():
                if state not in super(NFA, self).get_finals():
                    dot += "\"" + str(state) + "\"" + " [label=\"" \
                        + str(state) + "\"]"
                    dot += ";\n"

        dot += "node [shape = circle];\n"
        for (src, dest), res in super(NFA, self).get_aggregated_transitions().items():
            dot += "\"" + str(src) + "\""
            dot += " -> "
            dot += "\"" + str(dest) + "\""
            dot += " [ label = \"" + self.format_label(res[0], replace_alphabet)
            dot += "\" ];\n"

        dot += "}"
        return dot

    def to_fa_format(self, alphabet=False):
        """Converts automaton to FA format.

        Return: String (NFA in FA format)
        Keyword arguments:
        alphabet -- whether show explicitly symbols from alphabet.
        """

        if len(super(NFA, self).get_starts()) != 1:
            raise NFAOperationException("Only to an NFA with a single initial state can be converted to the FA format.")

        fa = str()
        fa += str(super(NFA, self).get_starts().keys()[0])+"\n"
        if alphabet:
            fa += ":"
            for sym in self.get_alphabet():
                fa += hex(sym) + " "
            fa += "\n"
        for transition in self._transitions:
            fa += "{0} {1} {2}\n".format(transition.src, transition.dest,\
                hex(transition.symbol))
        for final, _ in self._finals.iteritems():
            fa += "{0}\n".format(final)

        return fa

    def format_label(self, sym, replace_alphabet=True):
        """Format label for dot converting (btw. this method perform
        aggregation of transitions for better clarity).

        Return: String (formatted label)
        Keyword arguments:
        sym -- list of symbols
        replace_alphabet -- replace transition labeled with the whole
            alphabel with ^[]
        """
        max_symbols = core_wfa.SYMBOLS
        sym_str = str()
        if (set(sym) == set(self.get_alphabet())) and replace_alphabet:
            return "^[]"
        for char in sorted(sym):
            if max_symbols > 0:
                sym_str += aux.convert_to_pritable(chr(char), True)
                max_symbols = max_symbols - 1
            else:
                sym_str += "... {0}".format(len(sym))
                break
        return "[" + sym_str + "]"

    def to_timbuk(self):
        """Convert NFA to Timbuk format (only NFA with single initial state
        can be converted to the Timbuk format).

        Return: String (NFA in Timbuk format)
        """
        if len(super(NFA, self).get_starts()) != 1:
            raise NFAOperationException("Only NFA with a single initial state can be converted to the Timbuk format.")

        timbuk = str()
        timbuk += "Ops "
        for sym in super(NFA, self).get_alphabet():
            timbuk += "a{0}:1 ".format(sym)
        timbuk += "x:0\n\n"
        timbuk += "Automaton A1\nStates "
        for state in super(NFA, self).get_states():
            timbuk += "q{0} ".format(state)
        timbuk += "\nFinal States "

        for final, _ in super(NFA, self).get_finals().iteritems():
            timbuk += "q{0} ".format(final)
        timbuk += "\nTransitions\n"

        timbuk += "x -> q{0}\n".format(super(NFA, self).get_starts().keys()[0])
        for transition in super(NFA, self).get_transitions():
            timbuk += "a{0}(q{1}) -> q{2}\n".format(transition.symbol, transition.src, transition.dest)

        return timbuk
