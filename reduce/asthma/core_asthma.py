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

import asthma.tree as tree
import wfa.core_wfa as core_wfa
import wfa.core_wfa_export as core_wfa_export

#import sys

class Asthma(object):

    def __init__(self, freq_tree, predicates):
        """Constructor.

        Keyword arguments:
        freq_tree -- Frequency prefix tree acceptor of the sample
        predicates -- Predicates used for collapsing of the FPTA (type Predicates)
        """
        self._fpta = freq_tree
        self._predicates = predicates
        self._pa = None
        self._sinks = {}
        #Create a state for every predicate
        for pred in self._predicates:
            sink_state = tree.Tree(0, [])
            sink_state.data = pred
            self._sinks[pred] = sink_state

    def get_pa(self):
        """Get learned probabilistic automaton (PA).

        Return: core_wfa_export.CoreWFAExport()
        """
        return self._pa

    @staticmethod
    def _divide_language_classes(state):
        """Divide states to classes according to predicates.

        Return: Divided language classes, [frozenset(Tree)]
        Keyword arguments:
        state -- Current state whose followers are divided, Tree
        """
        dct = {}
        ret = []
        for trans in state.transitions:
            if trans.dest.data.symbols not in dct:
                dct[trans.dest.data.symbols] = set([trans.dest])
            else:
                dct[trans.dest.data.symbols].add(trans.dest)

        for key, val in dct.iteritems():
            if key is None:
                for value in list(val):
                    ret.append(frozenset([value]))
            else:
                ret.append(frozenset(val))
        return ret

    @staticmethod
    def _get_symbols(st1, st2):
        """
        """
        symbols = set()
        for trans in st1.transitions:
            if trans.dest == st2:
                symbols.add(trans.symbol)
        return symbols

    @staticmethod
    def _get_symbols_set(set1, set2):
        symbols = set()
        for st1 in list(set1):
            for st2 in list(set2):
                symbols = symbols | Asthma._get_symbols(st1, st2)
        return symbols

    def _set_predicates(self, state, merged_states, omega):
        tmp = self._predicates.get_bottom_pred()
        for st in merged_states:
            if st.freq < omega:
                tmp = self._predicates.least_predicate(st.data, tmp)

        assert tmp.symbols is not None, "SetPredicates -- Predicate Union"

        state.data = self._predicates.get_bottom_pred()
        found = False
        for st in merged_states:
            prime = self._predicates.get_bottom_pred()
            if st.freq < omega:
                st.data = tmp
                prime = st.data
            else:
                prime = self._predicates.get_top()
                found = True
            state.data = self._predicates.least_predicate(state.data, self._predicates.least_predicate_contains(prime, Asthma._get_symbols(state, st)))

        assert (found or (state.data.symbols is not None)), "SetPredicates -- Predicate Top Inconsistence"


    @staticmethod
    def _merge_states(state, classes, second):
        new_states = []

        for cl in classes:
            cl_node = tree.Tree(0, [])
            for st in list(cl):
                for trans in st.transitions:
                    assert trans.src == st, "MergeStates -- inconsistent states"
                    trans.src = cl_node
                cl_node.transitions += st.transitions
                cl_node.value += st.value
                cl_node.freq += st.freq
                cl_node.data = st.data
                cl_node.name += ";{0};".format(st.name)
                if second:
                    cl_node.max_freq = max(cl_node.max_freq, st.max_freq)
                else:
                    cl_node.max_freq = max(cl_node.max_freq, st.freq)

            new_states.append(cl_node)
            for trans in state.transitions:
                if trans.dest in cl:
                    trans.dest = cl_node

        return new_states

    def _tree_to_pa(self, node, visited, reduced):

        if node.data != self._predicates.get_top():
            return

        if node.value > 0:
            self._pa.get_finals()[node] = float(node.value) / node.freq

        assert len(node.transitions) != 0, "TreeToPA -- incomplete tree"

        for trans in node.transitions:
            trans.weight = float(trans.weight) / trans.src.freq
            if reduced and (trans.dest.data != self._predicates.get_top()):
                self._pa.get_transitions().append(core_wfa.Transition(trans.src, self._sinks[trans.dest.data], trans.symbol, trans.weight))
            else:
                self._pa.get_transitions().append(trans)
            if trans.dest not in visited:
                visited.add(trans.dest)
                self._tree_to_pa(trans.dest, visited, reduced)

    def _convert_to_pa(self, root, reduced=False):
        self._pa = core_wfa_export.CoreWFAExport()
        self._pa.set_starts({root: 1.0})
        self._tree_to_pa(root, set([root]), reduced)
        for pred, state in self._sinks.iteritems():
            un_weight = 1.0/(len(pred.symbols)+1.0)
            self._pa.get_finals()[state] = un_weight
            for symbol in list(pred.symbols):
                self._pa.get_transitions().append(core_wfa.Transition(state, state, symbol, un_weight))
        self._pa = self._pa.get_trim_automaton()
        self._pa.__class__ = core_wfa_export.CoreWFAExport


    @staticmethod
    def _add_transitions(src, dest, symbols):
        for sym in list(symbols):
            src.transitions.append(core_wfa.Transition(src, dest, sym, 0))

    @staticmethod
    def _update_weights(src, dests, count):
        total = 0
        for trans in src.transitions:
            if trans.dest in dests:
                total += trans.weight
        for trans in src.transitions:
            if trans.dest in dests:
                trans.weight = float(total) / count

    def _generalize_transitions(self, state, remaining_merge, all_states):
        rem_symbols = Asthma._get_symbols_set(set([state]), remaining_merge)
        all_symbols = Asthma._get_symbols_set(set([state]), all_states)
        all_symbols = all_symbols - rem_symbols

        pred = self._predicates.least_predicate_contains(self._predicates.get_bottom_pred(), rem_symbols)
        if (pred.symbols & all_symbols) == set():
            Asthma._add_transitions(state, list(remaining_merge)[0], pred.symbols - rem_symbols)
            Asthma._update_weights(state, remaining_merge, len(pred.symbols))



    def learn_pa(self, omega, trans_generalize=False, reduced=False):
        reverse = self._fpta.get_rev_transitions_aut()
        states = reverse.topological_sort_states()

        for state in states:
            if len(state.transitions) == 0:
                state.data = self._predicates.get_bottom_pred()

            classes = Asthma._divide_language_classes(state)
            merged = Asthma._merge_states(state, classes, False)

            self._set_predicates(state, merged, omega)
            classes = Asthma._divide_language_classes(state)

            assert ((state.data.symbols is not None) or (state.freq >= omega)), "LearnPA -- inconsistent predicate"

            merged = Asthma._merge_states(state, classes, True)
            if state.freq >= omega and trans_generalize:
                for st in merged:
                    if st.max_freq < omega:
                        self._generalize_transitions(state, set([st]), merged)

        self._convert_to_pa(self._fpta.get_starts().keys()[0], reduced)
