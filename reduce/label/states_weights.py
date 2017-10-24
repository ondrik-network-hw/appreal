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
import wfa.matrix_wfa_export as matrix_wfa_export
import label.state_labels as state_labels
import wfa.wfa_exceptions as wfa_exceptions
import wfa.nfa as nfa
import wfa.nfa_export as nfa_export
import FAdo.common

import enum

class LabelType(enum.Enum):
    weight = 0
    prob_sigma = 1
    exact = 2

class StatesWeights(state_labels.StateLabels):
    """Class for computing the state weights.
    """

    def __init__(self, pa, nfa_i, label_type):
        super(StatesWeights, self).__init__(pa, nfa_i)
        self._label_type = label_type

    def prepare(self):
        super(StatesWeights, self).prepare()
        if self._label_type == LabelType.weight:
            self.get_pa().set_all_finals()

    def is_pa_valid(self):
        """Check whether an input PA is valid for the reduction.

        Return: Bool (True=valid)
        """

        #TODO: Check correctness!!!
        #return False

        pa = super(StatesWeights, self).get_pa()
        pa.__class__ = matrix_wfa_export.MatrixWFAExport
        try:
            fado_aut = pa.supp_to_fado(True)
        except FAdo.common.DFAnotNFA:
            return False

        assert len(fado_aut.States) == len(pa.get_states()), "Fail FAdo conversion"
        assert fado_aut.countTransitions() == len(pa.get_transitions()), "Fail FAdo conversion"

        # fado_minimal = fado_aut.minimal()
        # if fado_minimal == fado_minimal.star():
        #     return True
        # return False
        return True

    def _compute_exact_weight(self, closure_mode, check_unambiguity, sparse=False, iterations=0):
        """Compute more precise state labels (L^{-1}(q).Sigma* - L^{-1}(q).L(q))

        Return: Dictionary: State -> float (weight of each state)
        Keyword arguments:
        closure_mode -- mode how to compute transition matrix closure (inverse matrix,
                        iterative multiplication ....)
        check_unambiguity -- input NFA is surely UFA, we dont need perform unambiguity check
        sparse -- Use sparse representation of the transition matrices.
        iterations -- number of iterations in the case of iterative multiplication closure_mode
        """
        language_sum = {}
        states = super(StatesWeights, self).get_nfa().get_states()
        language_sum = super(StatesWeights, self).get_states_prob_sigma(matrix_wfa.ClosureMode.inverse, sparse, True)

        for state in states:
            back = super(StatesWeights, self).get_nfa().get_concat_nfa(state)
            back.__class__ = nfa.NFA
            back = back.get_trim_automaton()
            back.__class__ = nfa.NFA

            if check_unambiguity:
                if not back.is_unambiguous():
                    back = back.get_dfa().get_trim_automaton()

            wfa_back = self.pa.product(back)
            wfa_back = wfa_back.get_trim_automaton()
            wfa_back.rename_states()
            wfa_back.__class__ = matrix_wfa.MatrixWFA
            lang_prob = wfa_back.compute_language_probability(closure_mode, sparse, iterations)
            language_sum[state] -= lang_prob

        return language_sum

    def _compute_aut_weight(self, aut, sparse=False):
        """Compute the state labels (weights) for a single NFA.

        Return: State labels (weights), Dict: State -> Float.
        Keyword arguments:
        aut -- NFA for computing the state weights.
        """
        if self._label_type == LabelType.weight:
            if aut.is_unambiguous() and self.is_pa_valid():
                return super(StatesWeights, self).get_states_weight_product(matrix_wfa.ClosureMode.inverse, True, sparse)
            else:
                return super(StatesWeights, self).get_states_weight_subautomaton(matrix_wfa.ClosureMode.inverse, True, sparse)
        elif self._label_type == LabelType.prob_sigma:
            return super(StatesWeights, self).get_states_prob_sigma(matrix_wfa.ClosureMode.inverse, True, sparse)
        elif self._label_type == LabelType.exact:
            return self._compute_exact_weight(matrix_wfa.ClosureMode.inverse, True, sparse)
        else:
            return None


    def _compute_states_weights_sub(self, approx, sparse=False):
        """Compute the state weights via dividing to subautomata.

        Return: State labels (weights), Dict: State -> Float.
        Keyword arguments:
        approx -- Compute the weights approximately (Bool).
        """
        subautomata = super(StatesWeights, self).get_nfa().get_branch_subautomata()
        back_prob = dict()

        for aut in subautomata:
            if approx:
                try:
                    ld = super(StatesWeights, self).get_states_weight_subautomaton_approximate(matrix_wfa.ClosureMode.inverse, True, sparse)
                except wfa_exceptions.WFAOperationException as e:
                    if e.err_type == wfa_exceptions.WFAErrorType.not_DAG:
                        print "G(A) is not a DAG, approximation cannot be used."
                        ld = self._compute_aut_weight(aut, sparse)
                    else:
                        raise
            else:
                self.set_nfa(aut)
                ld = self._compute_aut_weight(aut, sparse)
            back_prob.update(ld)
        return back_prob

    def compute_weights(self, approx, sparse=False):
        """Compute and store the state weights via dividing to subautomata.

        Keyword arguments:
        approx -- Compute the weights approximately (Bool).
        """
        labels = self._compute_states_weights_sub(approx, sparse)
        super(StatesWeights, self).set_labels(labels)
