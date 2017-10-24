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

import wfa.matrix_wfa as matrix_wfa
import label.state_labels as state_labels
import wfa.nfa as nfa
import copy

class StatesProbabilities(state_labels.StateLabels):
    """Class for computing the state probabilities.
    """

    def __init__(self, pa, nfa_i):
        super(StatesProbabilities, self).__init__(pa, nfa_i)

    def _final_reachability(self):
        """For each state q compute the set of final states reached by q.
        Corresponds to the function \alpha in work.

        Return: Dictionary: State -> set([State])
        """
        aut = super(StatesProbabilities, self).get_nfa()
        nfa_finals = aut.get_finals().keys()

        visited = set([])
        reverse_aut = aut.get_rev_transitions_aut()
        tr_dict = reverse_aut.get_dictionary_transitions()
        states_label = {}

        for final in nfa_finals:
            reverse_aut.breadth_first_search(final, visited, tr_dict)
            for state in list(visited):
                try:
                    states_label[state].add(final)
                except KeyError:
                    states_label[state] = set([final])
            visited = set([])
        return states_label

    def _compute_aut_prob(self, labels, sparse=False):
        """Compute the state labels (probabilities) for a single NFA.

        Return: State labels (probabilities), Dict: State -> Float.
        Keyword arguments:
        aut -- NFA for computing the state probabilities.
        """
        reach = self._final_reachability()

        final_probs = super(StatesProbabilities, self).get_finals_prob_subautomaton(matrix_wfa.ClosureMode.inverse, True, sparse)

        for state, finals in reach.iteritems():
            #labels[state] = 0.0
            for fin in iter(finals):
                labels[state] += final_probs[fin]

        return labels


    def _compute_states_probs_sub(self, sparse=False):
        """Compute the state probabilities via dividing to subautomata.

        Return: State labels (probabilities), Dict: State -> Float.
        """
        subautomata = super(StatesProbabilities, self).get_nfa().get_branch_subautomata()

        labels = {}
        for st in super(StatesProbabilities, self).get_nfa().get_states():
            labels[st] = 0.0

        for aut in subautomata:
            super(StatesProbabilities, self).set_nfa(aut)
            labels = self._compute_aut_prob(labels, sparse)

        return labels

    def compute_probs(self, sparse=False):
        """Compute and store the state probabilities via dividing to subautomata.
        """
        labels = self._compute_states_probs_sub(sparse)
        super(StatesProbabilities, self).set_labels(labels)
