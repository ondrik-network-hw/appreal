#!/usr/bin/python

"""
Tool for approximate reductions of finite automata used in network traffic
monitoring.

Author: Vojtech Havlena, <xhavle03@stud.fit.vutbr.cz>
"""

import copy
import nfa
import core_reduction
import aux_functions as aux
import pulp

class PruningReduction(core_reduction.CoreReduction):
    """Class for the pruning reduction.
    """
    def __init__(self, pa, nfa_aut):
        super(PruningReduction, self).__init__(pa, nfa_aut)
        self._removed_finals = []

    def get_removed_finals(self):
        """All removed finals are saved. This method gets all removed finals.

        Return: List(State)
        """
        return self._removed_finals

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


    def weight_function(self, states_label, states):
        """Weight function (the number of states labeled by the subset of states).

        Return: Int
        Keyword arguments:
        states_label -- alpha label of each state (Dictionary: State -> set([State]))
        states -- the set of states as input of weight function
        """
        return len(self.get_labeled_states(states_label, states))

    def get_labeled_states(self, states_label, states):
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

    def value_function(self, back_prob, states_label, states):
        """Value function (the backward probabilities sum of states in the set states).

        Return: Float
        Keyword arguments:
        back_prob -- Backward probability of each state (Dictionary: State -> Float)
        states -- The set of states (input of value function c)
        """
        ret = 0.0
        total_set = set([])
        for state in list(states):
            total_set = total_set.union(states_label[state])
        for state in list(total_set):
            ret += back_prob[state]
        return ret

    def compare_sets(self, set1, set2, states_label, back_prob):
        """Comparison of final states subsets set1 >= set2 (first according to
        weight function, then according to value function).

        Return: Bool (True -- set1 >= set2, otherwise False)
        Keyword arguments:
        set1 -- First operand (subset of final states)
        set2 -- Second operand (subset of final states)
        states_label -- alpha label of each state (Dictionary: State -> set([State]))
        back_prob -- Backward probability of each state (Dictionary: State -> Float)
        """
        weight1 = self.weight_function(states_label, set1)
        weight2 = self.weight_function(states_label, set2)
        if weight1 > weight2:
            return True
        elif (weight1 == weight2) and (self.value_function(back_prob, states_label, set1)\
            <= self.value_function(back_prob, states_label, set2)):
            return True
        else:
            return False

    def compare_sets_error(self, set1, set2, states_label, back_prob):
        """Comparison of final states subsets with respect to error.

        Return: Bool (True -- set1 >= set2, otherwise False)
        Keyword arguments:
        set1 -- First operand (subset of final states)
        set2 -- Second operand (subset of final states)
        states_label -- alpha label of each state (Dictionary: State -> set([State]))
        back_prob -- Backward probability of each state (Dictionary: State -> Float)
        """
        val1 = self.value_function(back_prob, states_label, set1)
        val2 = self.value_function(back_prob, states_label, set2)
        if val1 < val2:
            return True
        elif (val1 == val2) and self.weight_function(states_label, set1) \
            >= self.weight_function(states_label, set2):
            return True
        else:
            return False

    def k_reduction(self, back_prob, k):
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

        print back_prob

        for M in final_subsets:
            if (self.weight_function(states_label, M) <= W) \
                and (self.compare_sets(M, V, states_label, back_prob)):
                V = copy.deepcopy(M)

        state_set = set(nfa_states)
        self._removed_finals = list(V)
        new_states = state_set.difference(self.get_labeled_states(states_label, V))
        new_automaton = automaton.get_automata_restriction(new_states)
        new_automaton.__class__ = nfa.NFA
        return new_automaton

    def k_reduction_modif(self, back_prob, k):
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
            if (self.weight_function(states_label, M) >= W) \
                and (self.compare_sets_error(M, V, states_label, back_prob)):
                V = copy.deepcopy(M)

        state_set = set(nfa_states)
        self._removed_finals = list(V)
        new_states = state_set.difference(self.get_labeled_states(states_label, V))
        new_automaton = automaton.get_automata_restriction(new_states)
        new_automaton.__class__ = nfa.NFA
        return new_automaton

    def eps_reduction(self, back_prob, eps):
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
            if (self.value_function(back_prob, states_label, M) <= W) \
                and (self.compare_sets(M, V, states_label, back_prob)):
                V = copy.deepcopy(M)

        state_set = set(nfa_states)
        self._removed_finals = list(V)
        new_states = state_set.difference(self.get_labeled_states(states_label, V))
        new_automaton = automaton.get_automata_restriction(new_states)
        new_automaton.__class__ = nfa.NFA
        return new_automaton

    def eps_reduction_lp(self, back_prob, sub_automata, eps):
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
            val.append(self.weight_function(states_label, sub_finals))
            constraint.append(self.value_function(back_prob, states_label, sub_finals))

        sub_vars = range(0,len(sub_automata))
        variables = pulp.LpVariable.dicts('sub', sub_vars, lowBound = 0, upBound = 1,\
            cat = pulp.LpInteger)
        reduction_model = pulp.LpProblem("Reduction Problem", pulp.LpMaximize)
        #Objective function
        reduction_model += pulp.lpSum([val[sub] * variables[sub] for sub in sub_vars])
        #Constraints
        reduction_model += sum([constraint[sub] * variables[sub] for sub in sub_vars]) <= eps,\
            "Maximal_error"

        #print reduction_model

        reduction_model.solve()

        remove_states = set()
        for sub in sub_vars:
            if variables[sub].value() == 1.0:
                remove_states = remove_states.union(set(sub_automata[sub].get_finals()))

        self._removed_finals = list(remove_states)
        state_set = set(automaton.get_states())
        new_states = state_set.difference(self.get_labeled_states(states_label, remove_states))
        new_automaton = automaton.get_automata_restriction(new_states)
        new_automaton.__class__ = nfa.NFA
        return new_automaton

    def k_reduction_lp(self, back_prob, sub_automata, k, max_iter=100):
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
        aut_states = automaton.get_states()

        W = (1-k)*len(aut_states)
        val = []
        constraint = []
        for aut in sub_automata:
            sub_finals = set(aut.get_finals())
            val.append(self.weight_function(states_label, sub_finals))
            constraint.append(self.value_function(back_prob, states_label, sub_finals))

        sub_vars = range(0,len(sub_automata))
        variables = pulp.LpVariable.dicts('sub', sub_vars, lowBound = 0, upBound = 1,\
            cat = pulp.LpInteger)
        reduction_model = pulp.LpProblem("Reduction Problem", pulp.LpMaximize)
        #Objective function
        reduction_model += pulp.lpSum([val[sub] * variables[sub] for sub in sub_vars])
        #Constraints
        reduction_model += pulp.lpSum([val[sub] * variables[sub] for sub in sub_vars]) <= W,\
            "Maximal_states_removing"

        feasible = []
        counter = 0
        while counter < max_iter:
            #print reduction_model
            #sys.stdin.readline()

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
        new_states = state_set.difference(self.get_labeled_states(states_label, remove_states))
        new_automaton = automaton.get_automata_restriction(new_states)
        new_automaton.__class__ = nfa.NFA
        return new_automaton

    def k_reduction_lp_modif(self, back_prob, sub_automata, k):
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
            constraint.append(self.weight_function(states_label, sub_finals))
            val.append(self.value_function(back_prob, states_label, sub_finals))

        sub_vars = range(0,len(sub_automata))
        variables = pulp.LpVariable.dicts('sub', sub_vars, lowBound = 0, upBound = 1,\
            cat = pulp.LpInteger)
        reduction_model = pulp.LpProblem("Reduction Problem", pulp.LpMinimize)
        #Objective function
        reduction_model += pulp.lpSum([val[sub] * variables[sub] for sub in sub_vars])
        #Constraints
        reduction_model += sum([constraint[sub] * variables[sub] for sub in sub_vars]) >= W,\
            "Maximal_error"

        #print reduction_model

        reduction_model.solve()

        remove_states = set()
        for sub in sub_vars:
            if variables[sub].value() == 1.0:
                remove_states = remove_states.union(set(sub_automata[sub].get_finals()))

        self._removed_finals = list(remove_states)
        state_set = set(automaton.get_states())
        new_states = state_set.difference(self.get_labeled_states(states_label, remove_states))
        new_automaton = automaton.get_automata_restriction(new_states)
        new_automaton.__class__ = nfa.NFA
        return new_automaton
