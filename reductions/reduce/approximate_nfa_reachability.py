
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
import nfa
import matrix_wfa
import core_wfa
import collections

DIRECTORY = "subautomata"
SL_AUT_FILE = "pa_loop_aut"
SL_CLOSURE_FILE = "pa_loop_closure"
CLOSURE_MODE = matrix_wfa.ClosureMode.inverse
ITERATIONS = 100
MAX_STATES = 40

"""Wrapper for storing a WFA, initial, final vectors, and a transition closure.
"""
WFAReachabilityWrap = collections.namedtuple('WFAReachabilityWrap', ['wfa', 'ini_vec', 'fin_vec', 'closure'])

class ApproxNFAReach(object):

    # pylint: disable=too-many-instance-attributes

    def __init__(self, pa, fa):
        """Set input PA and NFA and initialize state weights.

        Keyword arguments:
        pa -- PA as an input for a reduction
        nfa -- NFA as an input for a reduction
        """
        self._pa = pa
        self._pa.__class__ = matrix_wfa.MatrixWFA
        self._nfa = fa
        self._nfa.__class__ = nfa.NFA

        self._language_sum = {}
        self._reachable_states = {}
        self._nfa_tr_dict = {}
        self._pa_tr_dict = {}
        self._sl_automata = {}
        self._sl_closure = {}

    def get_language_sum(self):
        """Get the language labels.

        Return: Dictionary: State (NFA) -> (Dictionary: State (PA) -> Float (weight))
        """
        return self._language_sum

    def prepare(self):
        """Initialize values for a new computation of the state labels.
        """
        self._language_sum = {}
        self._reachable_states = {}
        for state in self._nfa.get_states():
            self._language_sum[state] = 0
        self._nfa_tr_dict = self._nfa.get_dictionary_transitions()
        self._pa_tr_dict = self._pa.get_dictionary_transitions()

        # if load_sl_aut:
        #     with open("{0}/{1}".format(DIRECTORY, SL_AUT_FILE), 'rb') as f:
        #         self._sl_automata = pickle.load(f)
        #     with open("{0}/{1}".format(DIRECTORY, SL_CLOSURE_FILE), 'rb') as f:
        #         self._sl_closure = pickle.load(f)
        # else:
        #     self._sl_automata = {}
        #     self._sl_closure = {}
        #     for st in self._pa.get_states():
        #         aut = copy.deepcopy(self._pa)
        #         aut.set_start({st: 1.0})
        #         aut = aut.get_trim_automaton()
        #         aut.rename_states()
        #         aut.__class__ = matrix_wfa.MatrixWFA
        #         self._sl_automata[st] = aut
        #         self._sl_closure[st] = aut.compute_transition_closure(CLOSURE_MODE, ITERATIONS)
        #         #print st
        #
        #     with open("{0}/{1}".format(DIRECTORY, SL_AUT_FILE), 'wb') as f:
        #         pickle.dump(self._sl_automata, f, pickle.HIGHEST_PROTOCOL)
        #     with open("{0}/{1}".format(DIRECTORY, SL_CLOSURE_FILE), 'wb') as f:
        #         pickle.dump(self._sl_closure, f, pickle.HIGHEST_PROTOCOL)

    def _get_pa_states_reachability(self, reach_wrap, lang_aggr, lang_weight):
        """Compute new PA state labels from the transition closure, initial and
        final vectors.

        Return: (Float(Language weight), Dictinary: State(PA) -> Float(State Label, weight))
        Keyword arguments:
        reach_wrap -- Type WFAReachabilityWrap. Automata reachability information
            (an initial, final weights, and a transition closure)
        lang_aggr -- Current value of the PA state labels.
        lang_weight -- Current state label of the NFA state (beta function).
        """
        if len(lang_aggr) < len(self._pa.get_states()):
            for pa_state in self._pa.get_states():
                lang_aggr[pa_state] = 0.0

        for old, new in reach_wrap.wfa.get_rename_dict().iteritems():
            if new not in reach_wrap.wfa.get_starts():
                continue
            for old1, new1 in reach_wrap.wfa.get_rename_dict().iteritems():
                lang_aggr[old1[0]] += reach_wrap.ini_vec[0,old[0]] * reach_wrap.closure[new, new1] * reach_wrap.fin_vec[0,new1]
                lang_weight += reach_wrap.ini_vec[0,old[0]] * reach_wrap.closure[new, new1] * reach_wrap.fin_vec[0,new1]
        return (lang_weight, lang_aggr)

    def _get_back_nfa(self, state, max_states=None):
        """Get backward NFA to a given state (and perform disambiguation if
        necessary). If a size of the automaton is greater than max_states,
        None is returned.

        Return: unambiguous NFA or None (if the automaton is too big)
        Keyword arguments:
        state -- State of the NFA to obtain the backward automaton.
        max_states -- Maximum number of states of the back NFA.
        """
        nfa_back = self._nfa.get_backward_nfa(state).get_trim_automaton()
        nfa_back.__class__ = nfa.NFA
        if (max_states is not None) and (len(nfa_back.get_states()) > max_states):
            return None
        if not nfa_back.is_unambiguous():
            nfa_back = nfa_back.get_unambiguous_nfa(max_states)
            if nfa_back is not None:
                nfa_back = nfa_back.get_trim_automaton()
        return nfa_back

    def process_branch_state(self, state, predecessors):
        """Compute approximate state labels of the PA for a state state of the NFA.
        It is assumed that the state state has no self-loop (self-loops are
        ignored).

        Keyword arguments:
        state -- State of the NFA.
        predecessors -- List of predecessors of the state state.
        """
        lang_aggr = {}
        lang_weight = 0.0

        for pa_state in self._pa.get_states():
            lang_aggr[pa_state] = 0.0

        for act_pred in predecessors:
            if act_pred == state:
                continue

            #Get all transitions from actual predessors
            #rest_nfa_trans = []
            symbols = set([])
            for transition in self._nfa_tr_dict[act_pred]:
                if transition.dest == state:
                    #rest_nfa_trans.append(transition)
                    symbols.add(transition.symbol)
            # trans_nfa = nfa.NFA(rest_nfa_trans, {state: 1.0}, {act_pred: 1.0})
            #
            # pa_ini_states = self._reachable_states[act_pred] #{k:v for k, v in self._reachable_states[act_pred]}
            # pa_copy = copy.copy(self._pa)
            # pa_copy.set_starts(pa_ini_states)



            #Product of the PA and predecessors automaton
            # spa = pa_copy.product(trans_nfa)
            # spa = spa.get_trim_automaton()
            # spa.rename_states()
            # spa.__class__ = matrix_wfa.MatrixWFA

            for st, weight in self._reachable_states[act_pred].iteritems():
                tr_sum = 0.0
                for transition in self._pa_tr_dict[st]:
                    if transition.symbol in symbols:
                        tr_sum += transition.weight
                        lang_aggr[transition.dest] += weight*transition.weight
                lang_weight += tr_sum*weight

            #Get initial and final vectors and compute the transition closure
            # closure = spa.compute_transition_closure(CLOSURE_MODE, ITERATIONS)
            # wfa_wrap = WFAReachabilityWrap(spa, pa_copy.get_initial_vector(), spa.get_final_ones(), closure)
            #
            # lang_weight, lang_aggr = self._get_pa_states_reachability(wfa_wrap, lang_aggr, lang_weight)

        self._reachable_states[state] = lang_aggr
        self._language_sum[state] = lang_weight


    def process_self_loop_state_approx(self, state, lang_aggr, lang_weight):
        """Compute approximate state labels of the PA for a state state of the NFA.
        It is assumed that the state state has self-loops (transitions from
        predecessors are ignored).

        Keyword arguments:
        state -- State of the NFA.
        lang_aggr -- Current value of the PA state labels.
        lang_weight -- Current state label of the NFA state (beta function).
        """
        loop_transitions = []
        for sym in self._nfa.get_alphabet():
            loop_transitions.append(core_wfa.Transition(state, state, sym, 1.0))
        loop_nfa = nfa.NFA(loop_transitions, {state: 1.0}, {state: 1.0})
        loop_nfa.rename_states()

        pa_ini_states = self._reachable_states[state]
        pa_copy = copy.copy(self._pa)
        pa_copy.set_starts(pa_ini_states)

        spa = pa_copy.product(loop_nfa)
        spa = spa.get_trim_automaton()
        spa.rename_states()
        spa.__class__ = matrix_wfa.MatrixWFA

        #Get initial and final vectors and compute the transition closure
        closure = spa.compute_transition_closure(CLOSURE_MODE, ITERATIONS)
        wfa_wrap = WFAReachabilityWrap(spa, pa_copy.get_initial_vector(), spa.get_final_ones(), closure)
        lang_weight, lang_aggr = self._get_pa_states_reachability(wfa_wrap, lang_aggr, lang_weight)

        self._reachable_states[state] = lang_aggr
        self._language_sum[state] = lang_weight


    def process_states(self):
        """Compute the state labels of all states of the NFA.
        """
        for state in self._nfa.topological_sort_states():
            predecessors = list(self._nfa.get_predecessors(state))
            if state in predecessors:
                nfa_back = self._get_back_nfa(state, MAX_STATES)
                if nfa_back is None:
                    self.process_branch_state(state, predecessors)
                    self.process_self_loop_state_approx(state, dict(), self._language_sum[state])
                else:
                    self.process_backward_state(nfa_back, state)
            elif len(predecessors) >= 1:
                self.process_branch_state(state, predecessors)
            else:
                nfa_back = self._get_back_nfa(state, None)
                self.process_backward_state(nfa_back, state)
            #print state

    def process_backward_state(self, nfa_back, state):
        """Compute state labels of the PA for a state state of the NFA (using
        the subautomata method).

        Keyword arguments:
        nfa_back -- Backward NFA.
        state -- State of the NFA whose state labels are computed.
        """
        wfa_back = self._pa.product(nfa_back)
        wfa_back = wfa_back.get_trim_automaton()
        wfa_back.rename_states()
        wfa_back.__class__ = matrix_wfa.MatrixWFA

        closure = wfa_back.compute_transition_closure(CLOSURE_MODE, ITERATIONS)
        wfa_wrap = WFAReachabilityWrap(wfa_back, self._pa.get_initial_vector(), wfa_back.get_final_ones(), closure)

        lang_weight, lang_aggr = self._get_pa_states_reachability(wfa_wrap, dict(), 0.0)

        self._reachable_states[state] = lang_aggr
        self._language_sum[state] = lang_weight
