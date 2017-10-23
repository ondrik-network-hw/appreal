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
import wfa.core_wfa as core_wfa
import wfa.aux_functions as aux
import wfa.wfa_exceptions as wfa_exceptions

from collections import deque
#from profilehooks import profile

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
        """Get the deterministic version of the finite automaton. Implemented
        using the powerset construction.

        Return: NFA (but deterministic)
        Note: States of the returned NFA are frozenset([State])
        """
        initial = frozenset(super(NFA, self).get_starts().keys())
        remaining = deque([initial])
        completed = set()
        finals = frozenset(super(NFA, self).get_finals().keys())
        tr_dict = super(NFA, self).get_dictionary_transitions()

        new_transitions = []
        new_finals = dict()

        state_dict_orig = dict()
        for symbol in super(NFA, self).get_alphabet():
            state_dict_orig[symbol] = set()

        while remaining:
            act = remaining.popleft()
            completed.add(act)

            if (act & finals) != frozenset():
                new_finals[act] = 1.0

            state_dict = copy.deepcopy(state_dict_orig)
            for state in act:
                for transition in tr_dict[state]:
                    state_dict[transition.symbol].add(transition.dest)

            for symbol, state in state_dict.iteritems():
                state = frozenset(state)
                if state == frozenset():
                    continue

                new_transitions.append(core_wfa.Transition(act, state, symbol, 1.0))
                if (state not in completed) and (state not in remaining):
                    remaining.append(state)

        return NFA(new_transitions, new_finals, {initial: 1.0}, super(NFA, self).get_alphabet())

    @staticmethod
    def _get_pred_states_symbol(states, predecessors, symbol):
        """Get predecessors of the given states (denoted as X) s.t.
        from X there is a transition to states labeled by symbol.

        Return: Set([State])
        Keyword arguments:
        states -- frozenset([State]) (or set)
        predecessors -- Dictionary: State -> [Transtion] (predecessors transitions)
        symbol -- Int (label of transitions)
        """
        pred = set([])
        for state in iter(states):
            for trans in predecessors[state]:
                if trans.symbol == symbol:
                    pred.add(trans.src)
        return pred


    def get_minimal_dfa_hopcroft(self):
        """Get minimal DFA using the Hopcroft's algorithm. Assumes that the
        input NFA is deterministic and the trimming is performed first.

        Return: NFA (minimal equivalent DFA).
        """
        states = frozenset(self.get_states())
        finals = frozenset(self.get_finals())
        partition = set([finals, states - finals])
        alphabet = self.get_alphabet()
        #queue = deque([finals])
        queue = set([finals])

        predecessors = self.get_predecessors_transitions()

        while queue:
            act = iter(queue).next()
            queue.remove(act)

            for symbol in alphabet:
                pred = frozenset(NFA._get_pred_states_symbol(act, predecessors, symbol))
                if pred == frozenset([]):
                    continue
                part_list = copy.copy(partition)

                for part in iter(part_list):
                    prod_set = part & pred
                    minus_set = part - pred
                    if (prod_set == set([])) or (minus_set == set([])):
                        continue

                    partition.remove(part)
                    partition.add(prod_set)
                    partition.add(minus_set)

                    if part in queue:
                        queue.remove(part)
                        queue.add(prod_set)
                        queue.add(minus_set)
                    else:
                        if len(prod_set) <= len(minus_set):
                            queue.add(prod_set)
                        else:
                            queue.add(minus_set)
                #partition = part_list
        return self._merge_states(partition)


    def _merge_states(self, partition):
        """Merge states according to a partition on a set of states and
        create a new automaton.

        Return: NFA (with merged states and modified transitions according
        to a partitioning).
        Keyword arguments:
        partition -- Set([Frozenset([State])]) partitioning on a set of states.
        """
        new_transitions = set([])

        state_map = {}
        for part in iter(partition):
            for st in iter(part):
                state_map[st] = part

        for trans in self.get_transitions():
            add_trans = core_wfa.Transition(state_map[trans.src], state_map[trans.dest], trans.symbol, trans.weight)
            new_transitions.add(add_trans)

        new_finals = {}
        for key, _ in self.get_finals().iteritems():
            new_finals[state_map[key]] = 1.0

        new_initial = {}
        ini = self.get_starts().keys()[0]
        new_initial[state_map[ini]] = 1.0
        return NFA(list(new_transitions), new_finals, new_initial, self.get_alphabet())

    def get_minimal_dfa_brzozowski(self):
        """Get minimal DFA using the Brzozowski's algorithm. Assumes that the
        input NFA is deterministic and the trimming is performed first.

        Return: NFA (minimal equivalent DFA).
        """
        rev_aut = self.get_reversed_aut()
        rev_aut.__class__ = NFA
        dfa = rev_aut.get_dfa()
        dfa.rename_states()

        rev_aut = dfa.get_reversed_aut()
        rev_aut.__class__ = NFA

        return rev_aut.get_dfa()

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
        #queue = set([])
        q_prime = set()

        finals = super(NFA, self).get_finals().keys()

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
        relation_dict = {}
        relation_dict[initial] = set([initial])

        new_transitions = set()
        tr_dict = super(NFA, self).get_dictionary_transitions()
        new_tr_dic = {}

        while queue:
            p, s = queue.popleft()

            if p in finals:
                is_final = True
                for item in iter(relation_dict.get((p,s), [])): #aux.get_related(relation, (p, s)):
                    if item in finals_set:
                        is_final = False
                        break
                if is_final:
                    finals_set.add((p, s))

            for transition in tr_dict[p]:

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
                for item in iter(relation_dict.get((p,s), [])): #aux.get_related(relation, (p, s)):
                    if (item, transition.symbol, (transition.dest, t_set)) in new_transitions:
                        cont = False
                        break

                if cont:
                    if (transition.dest, t_set) not in q_prime:
                        q_prime.add((transition.dest, t_set))
                        queue.append((transition.dest, t_set))
                        num_states += 1
                        if (max_states is not None) and (num_states > max_states):
                            return None

                    trans_item = ((p, s), transition.symbol, (transition.dest, t_set))
                    new_transitions.add(trans_item)
                    if trans_item[0] not in new_tr_dic:
                        new_tr_dic[trans_item[0]] = []
                    new_tr_dic[trans_item[0]].append(trans_item)

                    tmp = list(relation_dict.get((p,s), []))
                    for item in tmp: #aux.get_related(relation, (p, s)):
                        for tr_prime in new_tr_dic.get(item, []): #iter(new_transitions):
                            if (tr_prime[0] == item) and (tr_prime[1] == transition.symbol):
                                relation.add(((transition.dest, t_set), tr_prime[2]))
                                relation.add((tr_prime[2], (transition.dest, t_set)))
                                try:
                                    relation_dict[tr_prime[2]].add((transition.dest, t_set))
                                except KeyError:
                                    relation_dict[tr_prime[2]] = set([(transition.dest, t_set)])

                                try:
                                    relation_dict[(transition.dest, t_set)].add(tr_prime[2])
                                except KeyError:
                                    relation_dict[(transition.dest, t_set)] = set([tr_prime[2]])



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

    def get_concat_nfa(self, state):
        """Get NFA corresponding to language L^{-1}(state).L(state)

        Return: NFA corresponding to above specified language.
        Keyword arguments:
        state -- State of the original NFA.
        """
        visited = set([])
        tr_dict = self.get_dictionary_transitions()
        back = self.get_backward_nfa(state)
        self.breadth_first_search(state, visited, tr_dict)
        forward = super(NFA, self).get_automata_restriction(visited)

        for_trans = set(forward.get_transitions())
        back_trans = set(back.get_transitions())
        cat_trans = for_trans.union(back_trans)

        return NFA(list(cat_trans), forward.get_finals(), back.get_starts(), self.get_alphabet())

    def accept_word(self, word, read_all=True, tr_dict=None):
        """Simulate run of automata on an input word.

        Return Bool (True NFA accept word, otherwise False)
        Keyword arguments:
        word -- input word (string)
        read_all -- If True automaton must read the whole input and reach the
            final state. If False automaton might not read the whole input
            (just reach a final state during reading input word)
        """
        prev_states = set(super(NFA, self).get_starts().keys())
        new_states = set()
        final_states = set(super(NFA, self).get_finals().keys())
        if tr_dict is None:
            tr_dict = super(NFA, self).get_dictionary_transitions()

        for char in word:
            if not prev_states: #len(prev_states) == 0:
                return False
            ord_char = ord(char)
            for prev in list(prev_states):
                for transition in tr_dict[prev]:
                    if transition.symbol == ord_char:
                        new_states.add(transition.dest)
            #Assumes simple states (i.e., not objects)
            prev_states = copy.copy(new_states)

            if (not read_all) and (final_states & prev_states):
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

    def remove_selfloop(self, states):
        """Remove Self-loops from states from the list states.

        Return: Modified NFA
        Keyword arguments:
        states -- [State]
        """
        transitions = super(NFA, self).get_transitions()
        new_transitions = []
        for transition in transitions:
            if (transition.src not in states) or (transition.dest not in states):
                new_transitions.append(transition)

        super(NFA, self).set_transitions(new_transitions)

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


    def prefix_acceptance_prepare(self):
        """Prepare automaton for a prefix acceptance, i.e., add self-loop on
        every symbol to each final state.
        """
        aut = copy.deepcopy(self)
        for state, _ in self.get_finals().iteritems():
            aut.add_selfloop(set([state]))
        return aut.get_trim_automaton()

    def _contain_selfloop(self, tr_dict, state):
        """Check whether a given state constains self-loop on every symbol.

        Return: Bool (state contans self-loop on every symbol)
        Keyword arguments:
        tr_dict -- Dict: State -> [Transition], Transition dictionary
        state -- State of the NFA
        """
        alphabet = self.get_alphabet()
        for symbol in alphabet:
            found = False
            for transition in tr_dict[state]:
                if (transition.dest == state) and (transition.symbol == symbol):
                    found = True
                    break
            if not found:
                return False
        return True

    def remove_final_selfloops(self):
        """Remove self-loops from states which contain self-loop on
        every symbol.
        """
        tr_dict = self.get_dictionary_transitions()
        for state, _ in self.get_finals().iteritems():
            if self._contain_selfloop(tr_dict, state):
                self.remove_selfloop(set([state]))
