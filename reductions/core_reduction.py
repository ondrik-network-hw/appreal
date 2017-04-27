#!/usr/bin/python

"""
Tool for approximate reductions of finite automata used in network traffic
monitoring.

Author: Vojtech Havlena, <xhavle03@stud.fit.vutbr.cz>
"""

import copy
import numpy
import nfa
import matrix_wfa

class CoreReduction(object):
    """Base class for operations used for NFA reductions.
    """

    def __init__(self, pa, i_nfa):
        """Set input PA and NFA.

        Keyword arguments:
        pa -- PA as an input for a reduction
        nfa -- NFA as an input for a reduction
        """
        self.pa = pa
        self.pa.__class__ = matrix_wfa.MatrixWFA
        self.nfa = i_nfa
        self.nfa.__class__ = nfa.NFA

    def get_nfa(self):
        """Get a stored NFA (input for a reduction). Return NFA.
        """
        return self.nfa

    def get_pa(self):
        """Get a stored PA (input for a reduction). Return MatrixWFA.
        """
        return self.pa

    def prepare(self):
        """Make a preparation for reduction (trimming input automata,
        rename their states). Return void.
        """
        self.pa = self.pa.get_trim_automaton()
        self.pa.rename_states()
        self.pa.__class__ = matrix_wfa.MatrixWFA

        self.nfa = self.nfa.get_trim_automaton()
        self.nfa.rename_states()
        self.nfa.__class__ = nfa.NFA

    def get_finals_prob_subautomaton(self, closure_mode, check_unambiguity, iterations=0):
        """Get backward language probabilities for each final state of NFA (f_P(L^{-1}(q))).
        Concrete probabilities are computed using subautomaton method. For each
        final state the automaton accepting L^{-1}(q) is created (using BFS as in
        the case of non-coaccessible states removing). Then if subautomaton is not UFA,
        disambiguation is performed. Finally product of PA with subautomaton is
        computed and backward language probability for curent final state
        is language probability of this product.

        Return: Dictionary: Final state -> float
        Keyword arguments:
        closure_mode -- mode how to compute transition matrix closure (inverse matrix,
                        iterative multiplication ....)
        check_unambiguity -- input NFA is surely UFA, we dont need perform unambiguity check
        iterations -- number of iterations in the case of iterative multiplication closure_mode
        """
        language_sum = {}
        #finals = self.nfa.get_finals().keys()
        for final, _  in self.nfa.get_finals().iteritems():
            language_sum[final] = 0

        for final, _  in self.nfa.get_finals().iteritems():
            back = self.nfa.get_backward_nfa(final).get_trim_automaton()
            back.__class__ = nfa.NFA
            if check_unambiguity:
                if not back.is_unambiguous():
                    back = back.get_unambiguous_nfa().get_trim_automaton()

            wfa_back = self.pa.product(back)
            wfa_back = wfa_back.get_trim_automaton()
            wfa_back.rename_states()
            wfa_back.__class__ = matrix_wfa.MatrixWFA
            language_sum[final] = wfa_back.compute_language_probability(closure_mode, iterations)
        return language_sum

    def get_finals_prob_product(self, closure_mode, iterations=0):
        """Get backward language probabilities for each final state of NFA (f_P(L^{-1}(q))).
        Concrete probabilities are computed using product method. Assumes that
        input NFA is UFA. Product PA with whole input NFA is performed.
        Then the probabilities are computed directly from transition
        matrix closure of the product automaton.

        Return: Dictionary: Final state -> float
        Keyword arguments:
        closure_mode -- mode how to compute transition matrix closure (inverse matrix,
                        iterative multiplication ....)
        iterations -- number of iterations in the case of iterative multiplication closure_mode
        """
        wfa_p1 = self.pa.product(self.nfa)
        wfa_p1 = wfa_p1.get_trim_automaton()
        wfa_p1.rename_states()
        wfa_p1.__class__ = matrix_wfa.MatrixWFA

        pa_ini = self.pa.get_initial_vector()
        pa_fin = self.pa.get_final_vector()
        closure = wfa_p1.compute_transition_closure(closure_mode, iterations)

        language_sum = {}
        finals = self.nfa.get_finals().keys()
        for final, _  in self.nfa.get_finals().iteritems():
            language_sum[final] = 0

        for old, new in wfa_p1.get_rename_dict().iteritems():
            if new != wfa_p1.get_start():
                continue
            for old1, new1 in wfa_p1.get_rename_dict().iteritems():
                if old1[1] not in finals:
                    continue
                language_sum[old1[1]] += pa_ini[0,old[0]] * closure[new, new1] * pa_fin[0,old1[0]]

        return language_sum


    def get_states_weight_subautomaton(self, closure_mode, check_unambiguity, iterations=0):
        """Get backward language weights for each final state of NFA (weight_P(L^{-1}(q))).
        Concrete weights are computed using subautomaton method. For each
        state the automaton accepting L^{-1}(q) is created (using BFS as in
        the case of non-coaccessible states removing). Then if subautomaton is not UFA,
        disambiguation is performed. Finally product of PA with subautomaton is
        computed and backward language weight for curent final state
        is language probability of this product.

        Return: Dictionary: State -> float
        Keyword arguments:
        closure_mode -- mode how to compute transition matrix closure (inverse matrix,
                        iterative multiplication ....)
        check_unambiguity -- input NFA is surely UFA, we dont need perform unambiguity check
        iterations -- number of iterations in the case of iterative multiplication closure_mode
        """
        language_sum = {}
        states = self.nfa.get_states()
        for state in states:
            language_sum[state] = 0

        for state in states:
            back = self.nfa.get_backward_nfa(state).get_trim_automaton()
            back.__class__ = nfa.NFA
            if check_unambiguity:
                if not back.is_unambiguous():
                    back = back.get_unambiguous_nfa().get_trim_automaton()

            wfa_back = self.pa.product(back)
            wfa_back = wfa_back.get_trim_automaton()
            wfa_back.rename_states()
            wfa_back.__class__ = matrix_wfa.MatrixWFA
            language_sum[state] = wfa_back.compute_language_weight(closure_mode, iterations)
        return language_sum


    def get_states_weight_product(self, closure_mode, iterations=0):
        """Get backward language weights for each state of NFA (weight_P(L^{-1}(q))).
        Concrete weights are computed using product method. Assumes that
        input NFA is UFA. Product PA with whole input NFA is performed.
        Then the weihts are computed directly from transition
        matrix closure of the product automaton.

        Return: Dictionary: Final state -> float
        Keyword arguments:
        closure_mode -- mode how to compute transition matrix closure (inverse matrix,
                        iterative multiplication ....)
        iterations -- number of iterations in the case of iterative multiplication closure_mode
        """
        aut = copy.deepcopy(self.nfa)
        #aut.make_all_finals()
        wfa_p1 = self.pa.product(aut)
        wfa_p1 = wfa_p1.get_trim_automaton()
        #print "Original:", len(self.pa.product(self.nfa).get_trim_automaton().get_states())
        #print "All finals:", len(wfa_p1.get_states())
        wfa_p1.rename_states()
        wfa_p1.__class__ = matrix_wfa.MatrixWFA

        pa_ini = self.pa.get_initial_vector()
        pa_fin = self.pa.get_final_ones()
        closure = wfa_p1.compute_transition_closure(closure_mode, iterations)

        for i in range(0, len(pa_fin)):
            if pa_fin[0, i] != 1.0:
                raise Exception("Debug error, all states must be final.")

        language_sum = {}
        #finals = aut.get_states()
        for state in aut.get_states():
            language_sum[state] = 0

        for old, new in wfa_p1.get_rename_dict().iteritems():
            if new != wfa_p1.get_start():
                continue
            for old1, new1 in wfa_p1.get_rename_dict().iteritems():
                # if old1[1] not in finals:
                #     raise Exception("Debug error, all states must be final.")
                #     continue
                language_sum[old1[1]] += pa_ini[0,old[0]] * closure[new, new1] #* pa_fin[0,old1[0]]

        return language_sum