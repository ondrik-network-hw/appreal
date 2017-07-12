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

import core_reduction
import operator
import FAdo.common

class SelfLoopReduction(core_reduction.CoreReduction):
    """Class for the self-loops reductions.
    """
    def __init__(self, pa, nfa_aut):
        super(SelfLoopReduction, self).__init__(pa, nfa_aut)
        self._selfloop_states = None

    def get_selfloop_states(self):
        """Get states where the self-loops are added.

        Return: List(State).
        """
        return self._selfloop_states

    def is_pa_valid(self):
        """Check whether an input PA is valid for the reduction.

        Return: Bool (True=valid)
        """
        pa = super(SelfLoopReduction, self).get_pa()
        try:
            fado_aut = pa.supp_to_fado(True)
        except FAdo.common.DFAnotNFA:
            return False

        assert len(fado_aut.States) == len(pa.get_states()), "Fail FAdo conversion"
        assert fado_aut.countTransitions() == len(pa.get_transitions()), "Fail FAdo conversion"

        fado_minimal = fado_aut.minimal()
        if fado_minimal == fado_minimal.star():
            return True
        return False

    def compute_error(self, weight, aut, states):
        """Compute error when add self-loops to states.

        Return: Float (error of sladd operation).
        Keyword arguments:
        weight -- The weights of all states.
        aut -- The original NFA.
        states -- Set of states where the self-loops are added.
        """
        aut_prime = aut.sladd(states)
        new_states = set(aut_prime.get_states())
        valid = new_states.intersection(states)

        err = 0.0
        for state in list(valid):
            err += weight[state]

        return err

    def eps_reduction(self, weight, eps):
        """Eps self-loop reduction. The restriction parameter is a maximal error.

        Return: NFA (reduced automaton).
        Keyword arguments:
        weight -- Dictionary of all states weights: State -> weight.
        eps -- The restriction parameter.
        """
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
            e = self.compute_error(weight, aut, v_set.union(item_set))
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

    def k_reduction(self, weight, k):
        """k self-loop reduction. The restriction parameter is a ratio
        between the original and the reduced automaton.

        Return: NFA (reduced automaton).
        Keyword arguments:
        weight -- Dictionary of all states weights: State -> weight.
        k -- The restriction parameter.
        """
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

    def k_reduction_modif(self, weight, k):
        """The modified k-self-loop reduction of the input NFA (with respect to ratio
        of #states of the reduced NFA and #states of the input NFA).

        Return: NFA (reduced input NFA)
        Keyword arguments:
        weight -- Dictionary of all states weights: State -> weight.
        k -- The ratio of number of states.
        """
        sorted_weight = sorted(weight.items(), key=operator.itemgetter(1))
        sum_all = 0.0
        for item in sorted_weight:
            sum_all += item[1]

        aut = super(SelfLoopReduction, self).get_nfa()
        states = set(aut.get_states())
        lim = k*len(states)
        count_states = len(states)
        v_set = set()
        index = 0
        self._selfloop_states = set()
        err = 0.0
        best_err = 2*sum_all

        while index < len(sorted_weight):
            item = sorted_weight[index]
            index += 1

            item_set = set([item[0]])
            aut_prime = aut.sladd(v_set.union(item_set))
            e = len(aut_prime.get_states())
            err = self.compute_error(weight, aut, v_set.union(item_set))

            if e <= lim and err <= best_err:
                v_set = v_set.union(item_set)
                best_err = err

            if e >= lim and e < count_states:
                v_set = v_set.union(item_set)
                count_states = e

        aut_prime = aut.sladd(v_set)
        if aut_prime.get_states() == aut.get_states():
            return aut

        new_states = set(aut_prime.get_states())
        self._selfloop_states = new_states.intersection(v_set)
        return aut.sladd(v_set)
