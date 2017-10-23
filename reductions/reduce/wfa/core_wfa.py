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
import bitarray
import wfa.wfa_exceptions as wfa_exceptions

from collections import deque

#Profiling directive
#from profilehooks import profile

class Transition(object):
    """Class for represention of the WFA transition.
    """
    def __init__(self, src, dest, sym, weight):
        self.src = src
        self.dest = dest
        self.symbol = sym
        self.weight = weight

    def __str__(self):
        return "({0}, {1}, {2}, {3})".format(self.src, self.dest, self.symbol, self.weight)

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other):
        return (self.src == other.src) and (self.dest == other.dest) and (self.symbol == other.symbol) and (self.weight == other.weight)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash((self.src, self.dest, self.symbol, self.weight))


class CoreWFA(object):
    """Basic class for representation of WFA
    """
    def __init__(self, transitions=None, finals=None, start=None, alphabet=None):
        self._transitions = transitions
        if self._transitions == None:
            self._transitions = []
        self._finals = finals
        if self._finals == None:
            self._finals = dict()
        self._start = start
        if self._start is None:
            self._start = {0: 1.0}
        self._states_dict = None
        self._alphabet = alphabet
        self._states = None
        self._modif = True

    def get_transitions(self):
        """Get all transitions of the WFA.

        Return: List of transitions.
        """
        return self._transitions

    def set_all_finals(self):
        for st in self.get_states():
            self._finals[st] = 1.0

    def set_transitions(self, transitions):
        """Set transitions of the WFA.

        Keyword arguments:
        transition -- The list of transitions.
        """
        self._modif = True
        self._transitions = transitions

    def get_finals(self):
        """Get all final states of the WFA.

        Return: Dictionary: Final state -> float (weight)
        """
        return self._finals

    def all_states_final(self):
        """Check whether all states are finals (nonzero probability of
        accepting).

        Return: Bool
        """
        fin = set(self._finals.keys())
        states = set(self.get_states())
        return (fin == states)

    def set_finals(self, finals):
        """Set final states of the WFA.

        Keyword arguments:
        finals -- Dictionary of final states and their probability of accepting.
        """
        self._modif = True
        self._finals = finals

    def get_starts(self):
        """Get the start state (only one start state is allowed).

        Return: Start state.
        """
        return self._start

    def set_starts(self, start):
        """Get all initial states of the WFA.

        Return: Dictionary: Initial state -> float (weight)
        """
        self._modif = True
        self._start = start

    def get_alphabet(self):
        """Get alphabet used by the WFA. If the alphabet is not explicitly
        given (in constructor), the alphabet is computed from the transitions.

        Return: List (of symbols).
        """
        alph = []
        if self._alphabet != None:
            return self._alphabet
        for transition in self._transitions:
            if transition.symbol not in alph:
                alph.append(transition.symbol)
        return alph

    def get_states(self):
        """Get all states of the WFA (the list of states is computed
        from the transitions).

        Return: List of states.
        """
        if not self._modif:
            return self._states

        states = set([])
        for start, _ in self._start.iteritems():
            if start not in states:
                states.add(start)
        for final, _ in self._finals.iteritems():
            if final not in states:
                states.add(final)
        for transition in self._transitions:
            if transition.src not in states:
                states.add(transition.src)
            if transition.dest not in states:
                states.add(transition.dest)

        self._states = list(states)
        self._modif = False
        return list(states)

    def get_rename_dict(self):
        """Get the dictionary containing original state labels and renamed
        state labels. The dictionary is created after method rename_states
        is invoked.

        Return: Dictionary: State (original) -> State (renamed).
        """
        return self._states_dict

    def get_single_dictionary_transitions(self):
        """Get the transitions (ommiting transitions that differ only on the
        symbol) in the form of dictinary (for each state there
        is a list of transitions leading from this state).

        Return: Dictionary: State -> List(Transitions)
        """
        tr_dict = dict()
        destinations = dict()

        states = self.get_states()
        for st in states:
            tr_dict[st] = []
            destinations[st] = set([])

        for transition in self._transitions:
            if transition.dest not in destinations[transition.src]:
                tr_dict[transition.src].append(transition)
                destinations[transition.src].add(transition.dest)
        return tr_dict

    def get_dictionary_transitions(self):
        """Get transitions in the form of dictionary (for each state there
        is a list of transitions leading from this state).

        Return: Dictionary: State -> List(Transitions)
        """
        tr_dict = dict()

        states = self.get_states()
        for st in states:
            tr_dict[st] = []

        for transition in self._transitions:
            tr_dict[transition.src].append(transition)
        return tr_dict

    def get_reversed_aut(self):
        """Get reversed automaton. The transitions are reversed and the
        initial and final states are swapped.

        Return: NFA
        """
        rev = self.get_rev_transitions_aut()
        ini = rev.get_finals()
        rev.set_finals(rev.get_starts())
        rev.set_starts(ini)
        return rev

    def get_rev_transitions_aut(self):
        """Get automaton with reversed directions of transitios.

        Return: WFA with reversed transitions.
        """
        rev_transitions = []
        for transition in self.get_transitions():
            rev_transitions.append(Transition(transition.dest, transition.src, \
                transition.symbol, transition.weight))

        return CoreWFA(rev_transitions, copy.copy(self._finals), copy.copy(self._start), copy.copy(self.get_alphabet()))

    def rename_states(self):
        """Rename states of the WFA. Assign to the states numbers
        from 0 to n-1 (n is the number of states). The start state has number 0.
        The renamed and original states are stored in the states_dict dictionary.
        """
        self._states_dict = dict()
        new_transitions = []
        new_finals = dict()
        new_starts = dict()
        count = 0

        for st, weight in self._start.iteritems():
            self._states_dict[st] = count
            new_starts[count] = weight
            count += 1

        for state in self.get_states():
            if state not in self._states_dict:
                self._states_dict[state] = count
                count += 1

        for (state, prob) in self._finals.iteritems():
            dest = self._states_dict[state]
            new_finals[dest] = prob

        for transition in self._transitions:
            new_transitions.append(Transition( \
                self._states_dict[transition.src], \
                self._states_dict[transition.dest], \
                transition.symbol, transition.weight))

        self._transitions = new_transitions
        self._finals = new_finals
        self._start = new_starts
        self._modif = True


    def product(self, aut):
        """Perform the product of two WFAs.

        Return: WFA representing the product of WFAs
        Keyword arguments:
        aut -- Second automaton for the product.
        """
        #queue = deque([])
        queue = set([])
        ret_finals = dict()
        ret_start = dict()
        ret_transitions = []

        self_finals = set(self._finals.keys())
        aut_finals = set(aut.get_finals().keys())

        for st1, weight1 in self._start.iteritems():
            for st2, weight2 in aut.get_starts().iteritems():
                queue.add((st1, st2))
                ret_start[(st1, st2)] = weight1 * weight2

        finished = set([])
        tr_dict1 = self.get_dictionary_transitions()
        tr_dict2 = aut.get_dictionary_transitions()

        while queue:
            act = iter(queue).next()
            queue.remove(act)
            finished.add(act)

            if (act[0] in self_finals) \
                and (act[1] in aut_finals):
                ret_finals[act] = self._finals[act[0]] \
                    * aut.get_finals()[act[1]]

            for tr1 in tr_dict1[act[0]]:
                for tr2 in tr_dict2[act[1]]:
                    if tr2.symbol != tr1.symbol:
                        continue

                    dest_state = (tr1.dest, tr2.dest)
                    ret_transitions.append(Transition(act, dest_state, \
                        tr1.symbol, tr1.weight * tr2.weight))

                    if (dest_state not in finished): #and (dest_state not in queue):
                        queue.add(dest_state)

        alphabet = set(self.get_alphabet()) & set(aut.get_alphabet())
        return CoreWFA(ret_transitions, ret_finals, ret_start, alphabet)

    def breadth_first_search(self, state, visited, tr_dict):
        """BFS in the automaton graph.

        Return: Out parameter visited (the list of visited states).
        Keyword arguments:
        state -- The start state of the BFS.
        visited -- The list of visited states (out parameter).
        tr_dict -- Transition dictionary.
        """
        queue = deque([state])
        if tr_dict is None:
            tr_dict = self.get_single_dictionary_transitions()
        while queue:
            head = queue.popleft()
            visited.add(head)
            for transition in tr_dict[head]:
                if (transition.dest not in visited) \
                    and (transition.dest not in queue):
                    queue.append(transition.dest)


    def get_coaccessible_states(self, tr_dict=None):
        """Get coaccessible states of the WFA.

        Return: The list of coaccessible states.
        """
        visited = set([])
        reverse_aut = self.get_rev_transitions_aut()
        if tr_dict is None:
            tr_dict = reverse_aut.get_single_dictionary_transitions()
        for state, _ in reverse_aut.get_finals().iteritems():
            reverse_aut.breadth_first_search(state, visited, tr_dict)
        return visited

    def get_accessible_states(self, tr_dict=None):
        """Get accessible states of the WFA.

        Return: The list of accessible states.
        """
        visited = set([])
        if tr_dict is None:
            tr_dict = self.get_single_dictionary_transitions()
        for state, _ in self.get_starts().iteritems():
            self.breadth_first_search(state, visited, tr_dict)
        return visited

    def get_automata_restriction(self, states):
        """Get WFA restriction to only states in states.

        Return: WFA (restriction to states in the list states)
        Keyword arguments:
        states -- The list of states of the new WFA.
        """
        rest_transitions = []
        rest_finals = dict()
        rest_initials = dict()
        alphabet = self.get_alphabet()
        for transition in self._transitions:
            if (transition.src in states) and (transition.dest in states):
                rest_transitions.append(Transition(transition.src, transition.dest,\
                    transition.symbol, transition.weight))

        for state, weight in self._finals.iteritems():
            if state in states:
                rest_finals[state] = weight

        #Since some NFA formalisms do not allow an NFA without an initial state,
        #if the list states do not contain any initial state, we add new initial
        #state (but only if the original NFA contains at least one intial state).
        for state, weight in self._start.iteritems():
            if state in states:
                rest_initials[state] = weight
        if len(rest_initials) == 0 and len(self._start) > 0:
            single_ini = self._start.keys()[0]
            rest_initials[single_ini] = self._start[single_ini]

        return CoreWFA(rest_transitions, rest_finals,\
            rest_initials, alphabet)

    def get_coaccessible_automaton(self):
        """Get automaton having only coaccessible states.

        Return: WFA having only coaccessible states.
        """
        costates = self.get_coaccessible_states()
        return self.get_automata_restriction(costates)

    def get_accessible_automaton(self):
        """Get automaton having only accessible states.

        Return: WFA having only accessible states.
        """
        access_states = self.get_accessible_states()
        return self.get_automata_restriction(access_states)

    #@profile
    def get_trim_automaton(self):
        """Get trimed WFA.

        Return: Trimmed WFA.
        Keyword arguments:
        """
        sts = self.get_coaccessible_states() & self.get_accessible_states()
        return self.get_automata_restriction(sts)

    def topological_sort_states(self, tr_dict=None):
        """Topological sort of states of the automaton.
        Colors: WHITE(0), GRAY(1), BLACK(2)

        Return: list of sorted states (list(State))
        Keyword arguments:
        tr_dict -- Transition dictionary, Dictionary: State -> list(Transition)

        Raises:
        WFAOperationException (WFAErrorType.not_DAG)
        """
        if tr_dict is None:
            tr_dict = self.get_dictionary_transitions()
        states = self.get_states()
        colors = {}
        sort_list = []
        for st in states:
            colors[st] = 0

        for st in states:
            if colors[st] == 0:
                self._dfs_visit(st, colors, sort_list, tr_dict)
        return sort_list

    def _dfs_visit(self, state, colors, sort_list, tr_dict):
        """Depth first search in the automaton graph G(A).

        Keyword arguments:
        state -- Actual searched state
        colors -- Dictionary of actual colour for each state
        sort_list -- List where are placed already finished states (contains topologically sorted states)
        tr_dict -- Transition dictionary, Dictionary: State -> list(Transition)

        Raises:
        WFAOperationException (WFAErrorType.not_DAG)
        """
        colors[state] = 1
        for transition in tr_dict[state]:
            if transition.dest == state:
                continue
            if colors[transition.dest] == 0:
                self._dfs_visit(transition.dest, colors, sort_list, tr_dict)
            elif colors[transition.dest] == 1:
                raise wfa_exceptions.WFAOperationException("Graph is not a DAG.", wfa_exceptions.WFAErrorType.not_DAG)
        colors[state] = 2
        sort_list.insert(0, state)

    def get_predecessors(self, state):
        """Operation that finds predessors of the state state.

        Return: List: [State]
        Keyword arguments:
        state -- The state whose predessors are found.
        """
        ret = set([])
        transitions = self.get_transitions()
        for tr in transitions:
            if tr.dest == state:
                ret.add(tr.src)
        return ret

    def get_predecessors_transitions(self):
        """Get predecessors of all states of the WFA.

        Return: Dict: State -> Set(State)
        """
        predecessors = {}
        for state in self.get_states():
            predecessors[state] = []

        for transition in self.get_transitions():
            predecessors[transition.dest].append(transition)

        return predecessors


    def get_oriented_graph(self):
        """Get oriented graph of the automaton. Multiple transitions that
        differ only in symbol and weight are not considered in graph.

        Return: CoreWFA (only single transitions between two states
        are considered).
        """
        dim = len(self.get_states())
        connection_matrix = [dim*bitarray.bitarray('0') for _ in range(dim)]
        new_transitions = []

        mapping = {}
        i = 0
        for state in self.get_states():
            mapping[state] = i
            i += 1

        for trans in self.get_transitions():
            if not connection_matrix[mapping[trans.src]][mapping[trans.dest]]:
                new_transitions.append(trans)
                connection_matrix[mapping[trans.src]][mapping[trans.dest]] = True

        return CoreWFA(new_transitions, copy.copy(self.get_finals()), copy.copy(self.get_starts()), [0])


    def is_pa_well_defined(self, eps=0.0):
        """Check whether PA is well defined. Specifically check whether the sum
        of outgoing transitions and the accepting probability of each state is
        at most eps from 1.0.

        Return: Bool
        Keyword arguments:
        eps -- Precision/tolerance
        """
        state_dict = {}
        for state in self.get_states():
            state_dict[state] = 0.0
        for state, weight in self.get_finals().iteritems():
            state_dict[state] = weight
        for trans in self.get_transitions():
            state_dict[trans.src] += trans.weight

        print self.get_starts()

        for state, weight in state_dict.iteritems():
            if weight != 1.0:
                print state, weight
                #return False
        return True
