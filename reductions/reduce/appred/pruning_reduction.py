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
import operator
import wfa.nfa as nfa
import wfa.aux_functions as aux
import pulp
import appred.core_reduction as core_reduction
import label.states_probabilities as states_probabilities

class PruningReduction(core_reduction.CoreReduction):
    """Class for the pruning reduction.
    """
    def __init__(self, pa, nfa_aut):
        super(PruningReduction, self).__init__(pa, nfa_aut)
        self._removed_finals = []
        self.state_labels = states_probabilities.StatesProbabilities(pa, nfa_aut)

    def get_removed_finals(self):
        """All removed finals are saved. This method gets all removed finals.

        Return: List(State)
        """
        return self._removed_finals

    def prepare(self):
        self.state_labels = states_probabilities.StatesProbabilities(super(PruningReduction, self).get_pa(), super(PruningReduction, self).get_nfa())
        super(PruningReduction, self).prepare()

    def get_states_label(self):
        """For each state q compute the set of final states reached by q.
        Corresponds to the function \alpha in work.

        Return: Dictionary: State -> set([State])
        """
        nfa_aut = super(PruningReduction, self).get_nfa()
        nfa_finals = nfa_aut.get_finals().keys()

        visited = set([])
        reverse_aut = nfa_aut.get_rev_transitions_aut()
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


    def compute_labels(self, approx, sparse=False):
        """Compute state labels (backward probabilities).

        Keyword arguments:
        approx -- Compute the state labels approximately (Bool).
        """
        self.state_labels.compute_probs(sparse)

    @staticmethod
    def _weight_function(states_label, states):
        """Weight function (the number of states labeled by the subset of states).

        Return: Int
        Keyword arguments:
        states_label -- alpha label of each state (Dictionary: State -> set([State]))
        states -- the set of states as input of weight function
        """
        return len(PruningReduction._get_labeled_states(states_label, states))

    @staticmethod
    def _get_labeled_states(states_label, states):
        """Get the set of states labeled with subset of the set states.

        Return: Set([States])
        Keyword arguments:
        states_label -- alpha label of each state (Dictionary: State -> set([State]))
        states -- input set of states
        """
        ret = set()
        for state, label in states_label.iteritems():
            if label.issubset(states):
                ret.add(state)
        return ret

    def _value_function(self, states_label, states):
        """Value function (the backward probabilities sum of states in the set states).

        Return: Float
        Keyword arguments:
        back_prob -- Backward probability of each state (Dictionary: State -> Float)
        states -- The set of states (input of value function c)
        """
        ret = 0.0
        back_prob = self.state_labels.get_labels()
        total_set = set([])
        for state in list(states):
            total_set = total_set.union(states_label[state])
        for state in list(total_set):
            ret += back_prob[state]
        return ret

    def _compare_sets(self, set1, set2, states_label):
        """Comparison of final states subsets set1 >= set2 (first according to
        weight function, then according to value function).

        Return: Bool (True -- set1 >= set2, otherwise False)
        Keyword arguments:
        set1 -- First operand (subset of final states)
        set2 -- Second operand (subset of final states)
        states_label -- alpha label of each state (Dictionary: State -> set([State]))
        """
        weight1 = PruningReduction._weight_function(states_label, set1)
        weight2 = PruningReduction._weight_function(states_label, set2)
        if weight1 > weight2:
            return True
        elif (weight1 == weight2) and (self._value_function(states_label, set1)\
            <= self._value_function(states_label, set2)):
            return True
        else:
            return False

    def _compare_sets_error(self, set1, set2, states_label):
        """Comparison of final states subsets with respect to error.

        Return: Bool (True -- set1 >= set2, otherwise False)
        Keyword arguments:
        set1 -- First operand (subset of final states)
        set2 -- Second operand (subset of final states)
        states_label -- alpha label of each state (Dictionary: State -> set([State]))
        """
        val1 = self._value_function(states_label, set1)
        val2 = self._value_function(states_label, set2)
        if val1 < val2:
            return True
        elif (val1 == val2) and PruningReduction._weight_function(states_label, set1) \
            >= PruningReduction._weight_function(states_label, set2):
            return True
        else:
            return False

    def k_reduction(self, k):
        """k-reduction of input NFA (with respect to ration of #states of the
        reduced NFA and #states of the input NFA).

        Return: NFA (reduced input NFA)
        Keyword arguments:
        back_prob -- Backward probability of each state (Dictionary: State -> Float)
        k -- reduction ratio (Float in range 0,1). Ratio of reduced NFA states
            and input NFA states
        """
        V = set([])
        automaton = super(PruningReduction, self).get_nfa()
        nfa_states = automaton.get_states()
        nfa_finals = automaton.get_finals().keys()
        W = (1-k)*len(nfa_states)
        final_subsets = aux.list_powerset(nfa_finals)
        states_label = self.get_states_label()

        for M in final_subsets:
            if (PruningReduction._weight_function(states_label, M) <= W) \
                and (self._compare_sets(M, V, states_label)):
                V = copy.deepcopy(M)

        state_set = set(nfa_states)
        self._removed_finals = list(V)
        new_states = state_set.difference(PruningReduction._get_labeled_states(states_label, V))
        new_automaton = automaton.get_automata_restriction(new_states)
        new_automaton.__class__ = nfa.NFA
        return new_automaton

    def k_reduction_modif(self, k):
        """k-reduction of input NFA (with respect to ration of #states of the
        reduced NFA and #states of the input NFA).

        Return: NFA (reduced input NFA)
        Keyword arguments:
        back_prob -- Backward probability of each state (Dictionary: State -> Float)
        k -- reduction ratio (Float in range 0,1). Ratio of reduced NFA states
            and input NFA states
        """

        automaton = super(PruningReduction, self).get_nfa()
        nfa_states = automaton.get_states()
        nfa_finals = automaton.get_finals().keys()
        V = set(nfa_finals)
        W = (1-k)*len(nfa_states)
        final_subsets = aux.list_powerset(nfa_finals)
        states_label = self.get_states_label()

        for M in final_subsets:
            if (PruningReduction._weight_function(states_label, M) >= W) \
                and (self._compare_sets_error(M, V, states_label)):
                V = copy.deepcopy(M)

        state_set = set(nfa_states)
        self._removed_finals = list(V)
        new_states = state_set.difference(PruningReduction._get_labeled_states(states_label, V))
        new_automaton = automaton.get_automata_restriction(new_states)
        new_automaton.__class__ = nfa.NFA
        return new_automaton

    def eps_reduction(self, eps):
        """eps-reduction of input NFA. The maximal error (probabilistic distance
        of input and reduced NFA) must be less or equal to eps.

        Return: NFA (reduced input NFA)
        Keyword arguments:
        back_prob -- Backward probability of each state (Dictionary: State -> Float)
        eps -- Maximal error (Float)
        """
        V = set([])
        automaton = super(PruningReduction, self).get_nfa()
        nfa_states = automaton.get_states()
        nfa_finals = automaton.get_finals().keys()
        W = eps
        final_subsets = aux.list_powerset(nfa_finals)
        states_label = self.get_states_label()

        for M in final_subsets:
            if (self._value_function(states_label, M) <= W) \
                and (self._compare_sets(M, V, states_label)):
                V = copy.deepcopy(M)

        state_set = set(nfa_states)
        self._removed_finals = list(V)
        new_states = state_set.difference(PruningReduction._get_labeled_states(states_label, V))
        new_automaton = automaton.get_automata_restriction(new_states)
        new_automaton.__class__ = nfa.NFA
        return new_automaton

    def eps_reduction_lp(self, sub_automata, eps):
        """The relaxed eps-reduction of the input NFA. The maximal error
        (probabilistic distance of input and reduced NFA) must be less or
        equal to eps. For computing integer linear programming is used.

        Return: NFA (reduced input NFA)
        Keyword arguments:
        back_prob -- Backward probability of each state (Dictionary: State -> Float)
        sub_automata -- All subautomata.
        eps -- Maximal error (Float)
        """
        states_label = self.get_states_label()
        automaton = super(PruningReduction, self).get_nfa()
        val = []
        constraint = []
        for aut in sub_automata:
            sub_finals = set(aut.get_finals())
            val.append(PruningReduction._weight_function(states_label, sub_finals))
            constraint.append(self._value_function(states_label, sub_finals))

        sub_vars = range(0,len(sub_automata))
        variables = pulp.LpVariable.dicts('sub', sub_vars, lowBound = 0, upBound = 1,\
            cat = pulp.LpInteger)
        reduction_model = pulp.LpProblem("Reduction Problem", pulp.LpMaximize)
        #Objective function
        reduction_model += pulp.lpSum([val[sub] * variables[sub] for sub in sub_vars])
        #Constraints
        reduction_model += sum([constraint[sub] * variables[sub] for sub in sub_vars]) <= eps,\
            "Maximal_error"

        reduction_model.solve()

        remove_states = set()
        for sub in sub_vars:
            if variables[sub].value() == 1.0:
                remove_states = remove_states.union(set(sub_automata[sub].get_finals()))

        self._removed_finals = list(remove_states)
        state_set = set(automaton.get_states())
        new_states = state_set.difference(PruningReduction._get_labeled_states(states_label, remove_states))
        new_automaton = automaton.get_automata_restriction(new_states)
        new_automaton.__class__ = nfa.NFA
        return new_automaton


    def k_reduction_lp(self, sub_automata, k, max_iter=100):
        """The relaxed k-reduction of the input NFA (with respect to ratio
        of #states of the reduced NFA and #states of the input NFA) For
        computing integer linear programming is used.

        Return: NFA (reduced input NFA)
        Keyword arguments:
        back_prob -- Backward probability of each state (Dictionary: State -> Float)
        sub_automata -- All subautomata.
        k -- The ratio of number of states.
        max_iter -- Maximum number of iterations (improvements).
        """

        states_label = self.get_states_label()
        automaton = super(PruningReduction, self).get_nfa()
        #aut_states = automaton.get_states()

        #W = (1-k)*len(automaton.get_states())
        val = []
        constraint = []
        for aut in sub_automata:
            #sub_finals = set(aut.get_finals())
            val.append(PruningReduction._weight_function(states_label, set(aut.get_finals())))
            constraint.append(self._value_function(states_label, set(aut.get_finals())))

        sub_vars = range(0,len(sub_automata))
        variables = pulp.LpVariable.dicts('sub', sub_vars, lowBound = 0, upBound = 1,\
            cat = pulp.LpInteger)
        reduction_model = pulp.LpProblem("Reduction Problem", pulp.LpMaximize)
        #Objective function
        reduction_model += pulp.lpSum([val[sub] * variables[sub] for sub in sub_vars])
        #Constraints
        reduction_model += pulp.lpSum([val[sub] * variables[sub] for sub in sub_vars]) <= (1-k)*len(automaton.get_states()),\
            "Maximal_states_removing"

        feasible = []
        counter = 0
        while counter < max_iter:

            reduction_model.solve()
            counter += 1
            if pulp.LpStatus[reduction_model.status] == "Optimal":
                total_err = 0.0
                total_weight = 0.0
                feasible = []
                for sub in sub_vars:
                    if variables[sub].value() == 1.0:
                        total_err += constraint[sub]
                        total_weight += val[sub]
                        feasible.append(sub)

                reduction_model += pulp.lpSum([1*variables[sub] for sub in feasible]) <= len(feasible) - 1
                reduction_model += pulp.lpSum([val[sub] * variables[sub] for sub in sub_vars]) >= total_weight
                reduction_model += pulp.lpSum([constraint[sub] * variables[sub] for sub in sub_vars]) <= total_err
            else:
                break

        remove_states = set()
        for sub in feasible:
            remove_states = remove_states.union(set(sub_automata[sub].get_finals()))

        self._removed_finals = list(remove_states)
        state_set = set(automaton.get_states())
        new_automaton = automaton.get_automata_restriction(state_set.difference(PruningReduction._get_labeled_states(states_label, remove_states)))
        new_automaton.__class__ = nfa.NFA
        return new_automaton

    def k_reduction_lp_modif(self, sub_automata, k):
        """The modified relaxed k-reduction of the input NFA (with respect to ratio
        of #states of the reduced NFA and #states of the input NFA) For
        computing integer linear programming is used.

        Return: NFA (reduced input NFA)
        Keyword arguments:
        back_prob -- Backward probability of each state (Dictionary: State -> Float)
        sub_automata -- All subautomata.
        k -- The ratio of number of states.
        max_iter -- Maximum number of iterations (improvements).
        """
        states_label = self.get_states_label()
        automaton = super(PruningReduction, self).get_nfa()
        val = []
        constraint = []
        W = (1-k)*len(automaton.get_states())

        for aut in sub_automata:
            sub_finals = set(aut.get_finals())
            constraint.append(PruningReduction._weight_function(states_label, sub_finals))
            val.append(self._value_function(states_label, sub_finals))

        sub_vars = range(0,len(sub_automata))
        variables = pulp.LpVariable.dicts('sub', sub_vars, lowBound = 0, upBound = 1,\
            cat = pulp.LpInteger)
        reduction_model = pulp.LpProblem("Reduction Problem", pulp.LpMinimize)
        #Objective function
        reduction_model += pulp.lpSum([val[sub] * variables[sub] for sub in sub_vars])
        #Constraints
        reduction_model += sum([constraint[sub] * variables[sub] for sub in sub_vars]) >= W,\
            "Maximal_error"

        reduction_model.solve()

        remove_states = set()
        for sub in sub_vars:
            if variables[sub].value() == 1.0:
                remove_states = remove_states.union(set(sub_automata[sub].get_finals()))

        self._removed_finals = list(remove_states)
        state_set = set(automaton.get_states())
        new_states = state_set.difference(PruningReduction._get_labeled_states(states_label, remove_states))
        new_automaton = automaton.get_automata_restriction(new_states)
        new_automaton.__class__ = nfa.NFA
        return new_automaton

    def k_reduction_greedy(self, k):
        weight = self.state_labels.get_labels()
        sorted_weight = sorted(weight.items(), key=operator.itemgetter(1))

        aut = super(PruningReduction, self).get_nfa()
        states = set(aut.get_states())
        lim = k*len(states)
        v_set = set()
        index = 0

        graph = aut.get_oriented_graph()
        graph.__class__ = nfa.NFA
        index = len(sorted_weight) - 1

        while index >= 0:
            item = sorted_weight[index]
            index -= 1

            item_set = set([item[0]])

            e_prime, ret = PruningReduction._pruning_red_states(graph, states - v_set.union(item_set), states)
            e = e_prime

            if e <= lim:
                v_set = v_set.union(item_set)

        _, new_states = self._compute_error(aut, states, states - v_set)
        self._removed_finals = new_states
        return aut.get_automata_restriction(v_set).get_trim_automaton()

    def eps_reduction_greedy(self, eps):
        prob = self.state_labels.get_labels()
        sorted_prob = sorted(prob.items(), key=operator.itemgetter(1))
        aut = super(PruningReduction, self).get_nfa()
        states = set(aut.get_states())
        #count_states = len(states)
        v_set = set()
        #err = 0
        index = 0
        self._removed_finals = set()

        graph = aut.get_oriented_graph()
        graph.__class__ = nfa.NFA

        while index < len(sorted_prob):
            item = sorted_prob[index]
            index += 1

            item_set = set([item[0]])

            e, sts = self._compute_error(graph, states, v_set.union(item_set))
            if e <= eps:
                v_set = sts

        _, new_states = self._compute_error(aut, states, v_set)
        self._removed_finals = new_states
        return aut.get_automata_restriction(states - v_set).get_trim_automaton()

    def _compute_error(self, aut, all_states,  pr_states):
        change = True
        sts = pr_states
        prob = self.state_labels.get_labels()
        err = 0.0

        while change:
            change = False
            for item in iter(sts):
                _, new_states = PruningReduction._pruning_red_states(aut, sts - set([item]), all_states)
                if item not in new_states:
                    sts = sts - set([item])
                    change = True
                    break

        for s in iter(sts):
            err += prob[s]
        print err
        return err, sts

    @staticmethod
    def _pruning_red_states(graph, pr_states, all_states):
        """Optimized procedure counting the states after adding self-loops.

        Return: Int (number of states after adding self-loops).
        Keyword arguments:
        sl_states -- set(state), states where self-loops are added.
        """
        # aut = super(SelfLoopReduction, self).get_nfa()
        initials = set(graph.get_starts().keys())
        graph_prime = graph.get_automata_restriction(all_states - pr_states)
        sts = graph_prime.get_coaccessible_states() & graph_prime.get_accessible_states()

        if sts & initials == set([]):
            return len(sts) + 1, sts
        else:
            return len(sts), sts
