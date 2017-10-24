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

import operator
import copy
import appred.core_reduction as core_reduction
import wfa.nfa as nfa
import wfa.nfa_export as nfa_export
import label.states_weights as states_weights

class SelfLoopReduction(core_reduction.CoreReduction):
    """Class for the self-loops reductions.
    """
    def __init__(self, pa, nfa_aut, label_type):
        super(SelfLoopReduction, self).__init__(pa, nfa_aut)
        self._selfloop_states = None
        self._label_type = label_type
        #State labels handler for computing the weights.
        self.state_labels = states_weights.StatesWeights(pa, nfa_aut, label_type)

    def get_selfloop_states(self):
        """Get states where the self-loops are added.

        Return: List(State).
        """
        return self._selfloop_states

    def prepare(self):
        """Prepare the reduction (initialize also the weights computation).
        """
        super(SelfLoopReduction, self).prepare()
        self.state_labels = states_weights.StatesWeights(super(SelfLoopReduction, self).get_pa(), copy.copy(super(SelfLoopReduction, self).get_nfa()), self._label_type)
        self.state_labels.prepare()

    def compute_labels(self, approx, sparse=False):
        """Compute the state labels (weights).

        Keyword arguments:
        approx -- Use approximate computation (Bool).
        """
        self.state_labels.compute_weights(approx, sparse)

    def compute_error(self, aut, states):
        """Compute error when add self-loops to states.

        Return: Float (error of sladd operation).
        Keyword arguments:
        weight -- The weights of all states.
        aut -- The original NFA.
        states -- Set of states where the self-loops are added.
        """
        weight = self.state_labels.get_labels()
        aut_prime = aut.sladd(states)
        new_states = set(aut_prime.get_states())
        valid = new_states.intersection(states)

        err = 0.0
        for state in list(valid):
            err += weight[state]

        return err

    def eps_reduction(self, eps):
        """Eps self-loop reduction. The restriction parameter is a maximal error.

        Return: NFA (reduced automaton).
        Keyword arguments:
        weight -- Dictionary of all states weights: State -> weight.
        eps -- The restriction parameter.
        """
        weight = self.state_labels.get_labels()
        sorted_weight = sorted(weight.items(), key=operator.itemgetter(1))
        aut = super(SelfLoopReduction, self).get_nfa()
        states = set(aut.get_states())
        count_states = len(states)
        v_set = set()
        #err = 0
        index = 0
        self._selfloop_states = set()

        while index < len(sorted_weight):
            item = sorted_weight[index]
            index += 1

            item_set = set([item[0]])


            e = self.compute_error(aut, v_set.union(item_set))
            aut_prime = aut.sladd(v_set.union(item_set))
            red_count = len(aut_prime.get_states())
            if e <= eps and red_count < count_states:
                #err = e
                v_set = v_set.union(item_set)
                count_states = red_count

        aut_prime = aut.sladd(v_set)
        if aut_prime.get_states() == aut.get_states():
            return aut

        new_states = set(aut_prime.get_states())
        self._selfloop_states = new_states.intersection(v_set)
        return aut.sladd(v_set)

    def k_reduction(self, k):
        """k self-loop reduction. The restriction parameter is a ratio
        between the original and the reduced automaton.

        Return: NFA (reduced automaton).
        Keyword arguments:
        weight -- Dictionary of all states weights: State -> weight.
        k -- The restriction parameter.
        """
        weight = self.state_labels.get_labels()
        sorted_weight = sorted(weight.items(), key=operator.itemgetter(1))
        aut = super(SelfLoopReduction, self).get_nfa()
        states = set(aut.get_states())
        lim = k*len(states)
        count_states = len(states)
        v_set = set()
        index = 0
        self._selfloop_states = set()

        while index < len(sorted_weight):
            item = sorted_weight[index]
            index += 1

            print index

            item_set = set([item[0]])
            aut_prime = aut.sladd(v_set.union(item_set))
            e = len(aut_prime.get_states())
            if e >= lim and e < count_states:
                v_set = v_set.union(item_set)
                count_states = e

        aut_prime = aut.sladd(v_set)
        if aut_prime.get_states() == aut.get_states():
            return aut

        new_states = set(aut_prime.get_states())
        self._selfloop_states = new_states.intersection(v_set)
        return aut.sladd(v_set)

    @staticmethod
    def _self_loop_red_states_count(graph, sl_states):
        """Optimized procedure counting the states after adding self-loops.

        Return: Int (number of states after adding self-loops).
        Keyword arguments:
        sl_states -- set(state), states where self-loops are added.
        """
        # aut = super(SelfLoopReduction, self).get_nfa()
        initials = set(graph.get_starts().keys())
        graph_prime = graph.sladd(sl_states)
        sts = graph_prime.get_coaccessible_states() & graph_prime.get_accessible_states()

        if sts & initials == set([]):
            return len(sts) + 1, sts
        else:
            return len(sts), sts


    def k_reduction_modif(self, k):
        """The modified k-self-loop reduction of the input NFA (with respect to ratio
        of #states of the reduced NFA and #states of the input NFA).

        Return: NFA (reduced input NFA)
        Keyword arguments:
        weight -- Dictionary of all states weights: State -> weight.
        k -- The ratio of number of states.
        """
        weight = self.state_labels.get_labels()
        sorted_weight = sorted(weight.items(), key=operator.itemgetter(1))

        aut = super(SelfLoopReduction, self).get_nfa()
        states = set(aut.get_states())
        lim = k*len(states)
        v_set = set()
        index = 0
        self._selfloop_states = set()

        graph = aut.get_oriented_graph()
        graph.__class__ = nfa.NFA
        index = len(sorted_weight) - 1

        while index >= 0:
            item = sorted_weight[index]
            index -= 1
            item_set = set([item[0]])

            e_prime, ret = SelfLoopReduction._self_loop_red_states_count(graph, states - v_set.union(item_set))
            e = e_prime

            if e <= lim:
                v_set = v_set.union(item_set)

        aut_prime = aut.sladd(states - v_set)
        if aut_prime.get_states() == aut.get_states():
            return aut

        new_states = set(aut_prime.get_states())
        self._selfloop_states = new_states.intersection(states - v_set)
        return aut.sladd(states - v_set)
