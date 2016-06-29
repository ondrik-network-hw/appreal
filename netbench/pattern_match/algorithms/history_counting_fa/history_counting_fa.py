############################################################################
#  HistoryCountingFA.py: Module for class HistoryCountingFA
#  Copyright (C) 2011 Brno University of Technology, ANT @ FIT
#  Author(s): Jaroslav Suchodol, <xsucho04@stud.fit.vutbr.cz>
############################################################################
#
#  LICENSE TERMS
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions
#  are met:
#  1. Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#  2. Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in
#     the documentation and/or other materials provided with the
#     distribution.
#  3. All advertising materials mentioning features or use of this software
#     or firmware must display the following acknowledgement:
#
#       This product includes software developed by the University of
#       Technology, Faculty of Information Technology, Brno and its
#       contributors.
#
#  4. Neither the name of the Company nor the names of its contributors
#     may be used to endorse or promote products derived from this
#     software without specific prior written permission.
#
#  This software or firmware is provided ``as is'', and any express or
#  implied warranties, including, but not limited to, the implied warranties
#  of merchantability and fitness for a particular purpose are disclaimed.
#  In no event shall the company or contributors be liable for any
#  direct, indirect, incidental, special, exemplary, or consequential
#  damages (including, but not limited to, procurement of substitute
#  goods or services; loss of use, data, or profits; or business
#  interruption) however caused and on any theory of liability, whether
#  in contract, strict liability, or tort (including negligence or
#  otherwise) arising in any way out of the use of this software, even
#  if advised of the possibility of such damage.
#
#  $Id$

from netbench.pattern_match.b_dfa import b_dfa
from netbench.pattern_match.b_symbol import io_mapper
from netbench.pattern_match.sym_char import b_Sym_char
from netbench.pattern_match.sym_char_class import b_Sym_char_class
from netbench.pattern_match.b_automaton import b_Automaton
from netbench.pattern_match.pattern_exceptions import DETERMINISTIC_ERROR
from netbench.pattern_match.pattern_exceptions import \
    not_epsilon_free_automaton_exception
import copy, string, math

class HistoryCountingFA(b_dfa):
    """
        Class for HistoryCountingFA.

        Based on
            - "Curing Regular Expressions Matching Algorithms from Insomnia,
              Amnesia, and Acalculia"
            - ISBN: 978-1-59593-945-6
            - URL: http://portal.acm.org/citation.cfm?id=1323574&dl=GUIDE,

        For how to use this class see 'example_of_use.py' or look inside tests
        correctly method compute().
    """

    def __init__(self):
        """
            Construct basic items.
        """
        b_dfa.__init__(self)

        self._dfa_fading_state_to_flag = dict()
        self._deleted_dfa_fading_state_to_new_dfa_state = dict()

        # for search method
        self.flags = dict()
        self.flags_cnt = dict()

    def compute(self, NFA):
        """
            Fuction for make HistoryCountingFA.

            :param NFA: NFA
            :type NFA: nfa_data
            :rises DETERMINISTIC_ERROR: Automat must be Deterministic before \
                calling compute()
        """
        if not self.has_flag("Deterministic") \
        or self.get_flag("Deterministic") != True:
            raise DETERMINISTIC_ERROR

        NFA_without_cnt = self._replace_length_restriction_with_a_closure(NFA)
        nfa_closure_states = self._discover_closure_states(NFA_without_cnt)
        dfa_fading_states = self._identify_fading_states(nfa_closure_states)
        self._remove_fading_dfa_states(dfa_fading_states)
        self._pruning_process()

        self._automaton.Flags["History counting FA"] = True
        self._compute = True

    def _replace_length_restriction_with_a_closure(self, NFA):
        """
            The first step in this construction replaces the length
            restriction with a closure, and constructs the H-FA, with
            the closure represented by a flag in the history buffer.

            :param NFA: NFA
            :type NFA: nfa_data
            :returns: NFA without counting constraint
            :rtype: nfa_data
        """
        # identify counting transitions with exactly X counting
        cnt_transitions = list()
        for t in NFA.transitions:
            if NFA.alphabet[t[1]].ctype == io_mapper["b_Sym_cnt_constr"]:
                if NFA.alphabet[t[1]].m == NFA.alphabet[t[1]].n:
                    cnt_transitions.append(t)

        # remove founded counting transtions
        #   and replace them with loop transitions
        #   and add epsilon tran. to next state
        for t in cnt_transitions:
            NFA.transitions.remove(t)
            
            cnt_symbol = NFA.alphabet[t[1]]
            self.flags_cnt[t[0]] = str(cnt_symbol.m)

            NFA.transitions.add(
                (t[0],
                t[1],
                t[0])
            )
            NFA.transitions.add(
                (t[0],
                -1,
                t[2])
            )

        # replace cnt symbol at char or char class
        # and add epsilon symbol into alphabet if does not exist
        for t in cnt_transitions:
            symbolID = t[1]
            cnt_symbol = copy.deepcopy(NFA.alphabet[symbolID])
            if cnt_symbol.ctype == io_mapper["b_Sym_cnt_constr"]:
                if isinstance(cnt_symbol.symbol, str):
                    NFA.alphabet[symbolID] = b_Sym_char_class(
                        new_text = cnt_symbol._text,
                        charClass = set([cnt_symbol.symbol]),
                        new_id = cnt_symbol._id)
                else :
                    NFA.alphabet[symbolID] = b_Sym_char_class(
                        new_text = cnt_symbol._text,
                        charClass = cnt_symbol.symbol,
                        new_id = cnt_symbol._id)

            epsilonID = -1
            if not epsilonID in NFA.alphabet:
                NFA.alphabet[epsilonID] = b_Sym_char("Epsilon", "", -1)

        # remove epsilons
        aut = b_Automaton()
        aut._automaton = NFA
        aut.remove_epsilons()

        return aut._automaton

    def _discover_closure_states(self, NFA_without_cnt):
        """
            Discover closure states.

            :param NFA_without_cnt: NFA without counting constraint
            :type NFA: nfa_data
            :returns: list of closure states
            :rtype: list(int)
            :rises not_epsilon_free_automaton_exception: Automat must be \
                without epsilons before calling this method
        """
        NFA = NFA_without_cnt
        if not self.has_flag("Epsilon Free") \
        or self.get_flag("Epsilon Free") != True:
            raise not_epsilon_free_automaton_exception

        closure_states = list()
        for t in NFA.transitions:
            if t[0] == t[2] and t[0] != NFA.start:
                closure_states.append(t[0])
                # for search method
                self.flags[str(t[0])] = False
        return sorted(closure_states)

    def _identify_fading_states(self, nfa_closure_states):
        """
            Identify those DFA states, which comprise of these closure
            NFA states.

            :param nfa_closure_states: NFA closure states
            :type nfa_closure_states: list(int)
            :returns: list of DFA fading states
            :rtype: list(int)
        """
        dfa_fading_states = list()
        for closure_state in nfa_closure_states:
            for set_nfa_states in copy.deepcopy(self._state_representation):
                new_dfa_state = copy.deepcopy(set_nfa_states)
                new_dfa_state.discard(closure_state)
                # and new_dfa_state in self._state_representation:
                #   adjustment because of self._state_representation is other
                #   than in scientific article
                if closure_state in set_nfa_states \
                and new_dfa_state in self._state_representation:

                    fading_state = self._state_representation. \
                        index(set_nfa_states)

                    dfa_fading_states.append(fading_state)

                    self._dfa_fading_state_to_flag[fading_state] = closure_state

                    self._deleted_dfa_fading_state_to_new_dfa_state[
                        fading_state] = self._state_representation.index(
                        new_dfa_state)
        return dfa_fading_states

    def _remove_fading_dfa_states(self, dfa_fading_states):
        """
            In the next step, we attempt to remove fading DFA states.

            Transitions which originated from a non-fading state and led to
            a fading state and vice-versa will now set and reset the history
            flag, respectively. Futhermore, all transitions that remain
            in the fading regin will have an associated condition that
            the flag is set.

            :param dfa_fading_states: DFA fading states
            :type dfa_fading_states: list(int)
        """
        for t in copy.deepcopy(self._automaton.transitions):
            conditions = frozenset()
            actions = frozenset()
            self._automaton.transitions.remove(t)
            t = (t[0], t[1], t[2], conditions, actions)
            self._automaton.transitions.add(t)

        for fading_state in dfa_fading_states:
            fading_state_is_counting = False
            cnt_flag = False
            del self._automaton.states[fading_state]
            if fading_state in self._automaton.final:
                self._automaton.final.remove(fading_state)

            # change numbering in transitions
            deleted_state = fading_state
            flag_in_string = str(self._dfa_fading_state_to_flag[fading_state])
            new_state = self._deleted_dfa_fading_state_to_new_dfa_state[
                deleted_state]

            for cnt_nfa_state in self.flags_cnt:
                if cnt_nfa_state in self._state_representation[fading_state]:
                    fading_state_is_counting = True
                    cnt_flag = cnt_nfa_state

            for t in copy.deepcopy(self._automaton.transitions):

                if t[0] not in dfa_fading_states \
                and t[2] == fading_state:
                    new_actions = []
                    for old_action in t[4]:
                        new_actions.append(old_action)
                    new_actions.append("+" + flag_in_string)
                    if fading_state_is_counting:
                        new_actions.append("ctr" + str(cnt_flag) +":" \
                            + self.flags_cnt[cnt_flag])
                    self._automaton.transitions.remove(t)
                    new_t = (
                        t[0],
                        t[1],
                        new_state,
                        t[3],
                        frozenset(new_actions))
                    self._automaton.transitions.add(new_t)

                elif t[0] == fading_state \
                and t[2] not in dfa_fading_states:
                    new_conditions = []
                    for old_condition in t[3]:
                        new_conditions.append(old_condition)
                    new_conditions.append("|" + flag_in_string)
                    if fading_state_is_counting:
                        new_conditions.append("ctr" + str(cnt_flag) +":" + "0")
                    new_actions = []
                    for old_action in t[4]:
                        new_actions.append(old_action)
                    new_actions.append("-" + flag_in_string)
                    if fading_state_is_counting:
                        new_actions.append("ctr" + str(cnt_flag) +":" + "-1")
                    self._automaton.transitions.remove(t)
                    new_t = (
                            new_state,
                            t[1],
                            t[2],
                            frozenset(new_conditions),
                            frozenset(new_actions))
                    self._automaton.transitions.add(new_t)
                elif t[0] == fading_state \
                and t[2] in dfa_fading_states:
                    new_conditions = []
                    for old_condition in t[3]:
                        new_conditions.append(old_condition)
                    new_conditions.append("|" + flag_in_string)
                    if fading_state_is_counting:
                        new_conditions.append("ctr" + str(cnt_flag) +":" + "0")
                    self._automaton.transitions.remove(t)
                    new_t = (
                        new_state,
                        t[1],
                        self._deleted_dfa_fading_state_to_new_dfa_state[t[2]],
                        frozenset(new_conditions),
                        t[4])
                    self._automaton.transitions.add(new_t)

    def _pruning_process(self):
        """
            Notice that several transitions in machine can be pruned.
            The representation of conditions as vectors eases out the
            pruning process, which is carried out immediately after the

            construction. The pruning process eliminates any transition
            with condition C1, if another transition on condition C2 exists
            between the same pair of states, over the same character such 
            that the condition C1 is a subset of the condition C2 (i.e. C2
            is true whether C1 is true) and the actions associated with
            both the transitions are the same. In general, pruning process

            eliminates a large number of transitions, and it is essential
            in reducing the memory requirements of H-FAs.
        """
        # discover Hfa transitions
        hfa_transitions = []
        for t in self._automaton.transitions:
            if len(t) == 5 and (t[3] != frozenset() or t[4] != frozenset()):
                hfa_transitions.append(t)
        transitions_to_delete = []
        for hfa_t in hfa_transitions:
            self._automaton.transitions.remove(hfa_t)
            conditions_hfa_t = hfa_t[3]
            actions_hfa_t = hfa_t[4]
            for other_t in self._automaton.transitions:
                conditions_other_t = other_t[3]
                actions_other_t = other_t[4]
                if hfa_t[0] == other_t[0] \
                and hfa_t[1] == other_t[1] \
                and hfa_t[2] == other_t[2] \
                and actions_hfa_t == actions_other_t:
                    if conditions_hfa_t.issubset(conditions_other_t):
                        transitions_to_delete.append(other_t)
                    elif conditions_other_t.issubset(conditions_hfa_t):
                        transitions_to_delete.append(hfa_t)
            self._automaton.transitions.add(hfa_t)
        for t in transitions_to_delete:
            self._automaton.transitions.discard(t)

    def search(self, input_string):
        """
            This function will find patterns in the given string
            by the approach.

            :param input_string: Input string.
            :param input_string: string
            :returns: Bitmap of matched regular expressions.
            :rtype: list(int)
        """
        for flag in self.flags:
            self.flags[flag] = False

        cnt = copy.deepcopy(self.flags_cnt)
        for flag in cnt:
            cnt[flag] = -1

        # Stack of states. State is list (tupple) consisting of state and unprocessed part of input string.
        Stack = list()
        # Set of actual states.
        ActState = set()

        # Create start state.
        ActState.add((self._automaton.start, input_string))
        # Add start state to stack.0
        Stack.append(ActState)

        # Create mapping between reg. exp. number and coresponding final states.
        sameFinal = dict()
        for fstate in self._automaton.final:
            rnums = self._automaton.states[fstate].get_regexp_number()
            for rnum in rnums:
                if sameFinal.has_key(rnum) == True:
                    sameFinal[rnum].add(fstate)
                else:
                    sameFinal[rnum] = set()
                    sameFinal[rnum].add(fstate)

        # Compute number of reg. exp.
        rules = len(sameFinal)
        # dictionary is no longer needed.
        sameFinal = None

        # Init bitmap to zeros.
        bitmap = [0] * rules

        # If needed create mapping between states and outgoing transitions.
        if self._mapper == None:
            self._mapper = dict()
            for transition in self._automaton.transitions:
                if self._mapper.has_key(transition[0]) == True:
                    self._mapper[transition[0]].add((transition[1], transition[2], transition[3], transition[4]))
                else:
                    self._mapper[transition[0]] = set()
                    self._mapper[transition[0]].add((transition[1], transition[2], transition[3], transition[4]))

        # Until stack is empty, search
        while len(Stack) != 0:
            # Pop state from stack.
            ActState = Stack.pop()
            newActState = set()
            # Create new state. Accept char if possible and add state to new state.
            for state in ActState:
                if self._mapper.has_key(state[0]):
                    for transition in self._mapper[state[0]]:
                        conditions = transition[2]
                        actions = transition[3]
                        try:
                            # Handle strided automaton, add padding characters if needed
                            # (when size of string is smaller than size of stride)
                            astr = ""
                            if self._automaton.states[transition[1]].is_final():
                                if self._automaton.Flags.has_key("Stride") and len(state[1]) < self._automaton.Flags["Stride"]:
                                    mod = len(state[1]) % self._automaton.Flags["Stride"]
                                    if mod != 0:
                                        for i in xrange(0, self._automaton.Flags["Stride"] - mod):
                                            astr += chr(0)
                                                  
                            res = self._automaton.alphabet[transition[0]].accept(state[1] + astr)
                        except:
                            pass
                        else:
                            if conditions == frozenset():
                                for cnt_flag in cnt:
                                    cnt[cnt_flag] -= 1
                                for action in actions:
                                    if action[0] == "-":
                                        self.flags[action[1:]] = False
                                    elif action[0] == "+":
                                        self.flags[action[1:]] = True
                                    elif action[:3] == "ctr":
                                        cnt_flag = string.atoi(action.split(":")[0][3:])
                                        cnt_value = string.atoi(action.split(":")[1])
                                        cnt[cnt_flag] = cnt_value
                                newActState.add((transition[1],res))
                            else :
                                execute_transition = True
                                for condition in conditions:
                                    if condition[0] == "|":
                                        if self.flags[condition[1:]] != True:
                                            execute_transition = False
                                            break
                                    elif condition[:3] == "ctr":
                                        cnt_flag = string.atoi(condition.split(":")[0][3:])
                                        if cnt[cnt_flag] != 0:
                                            execute_transition = False
                                            break
                                if execute_transition:
                                    for cnt_flag in cnt:
                                        cnt[cnt_flag] -= 1
                                    for action in actions:
                                        if action[0] == "-":
                                            self.flags[action[1:]] = False
                                        elif action[0] == "+":
                                            self.flags[action[1:]] = True
                                        elif action[:3] == "ctr":
                                            cnt_flag = string.atoi(action.split(":")[0][3:])
                                            cnt_value = string.atoi(action.split(":")[1])
                                            cnt[cnt_flag] = cnt_value
                                    newActState.add((transition[1],res))
                # If in final state, set coresponding bitmap field to 1.
                if self._automaton.states[state[0]].is_final() == True:
                    for rnum in self._automaton.states[state[0]].get_regexp_number():
                        bitmap[rnum] = 1
            # If possible add new state to stack.
            if len(newActState) > 0:
                Stack.append(newActState)

        # Return bitmap.
        return bitmap

    def _show(self, FileName, sizeStr=" size=\"10\"\n"):
        """
            Save graphviz dot file, representing graphical structure of nfa_data.

            :param FileName: Name of file into which nfa_data graphical representation will be saved.
            :type FileName: string
            :param sizeStr: Size of resulting image. Set to " " to set unbounded dimensions. Format of                  this parameter is / size="x,y"\\n/ to set width to x inches and height to y inches.
            :type sizeStr: string
            :returns: True if success, False otherwise.
            :rtype: boolean
        """
        # If object does not contain automaton, stop.
        if len(self._automaton.states) == 0:
            return False
        else:
            # Otherwise open file and save the representation.
            f = open(FileName,"w")

            #Print header of the dot file
            f.write("digraph \" Automat \" {\n    rankdir=LR;\n "+sizeStr);
            f.write("node [shape = doublecircle];\n");

            #Print end states as double circles
            for EndSt in self._automaton.final:
                f.write(self._automaton.states[EndSt].get_text())
                f.write(";\n");

            f.write("node [shape=circle];\n");

            #print all transitions. States are print as a circle
            for Source in self._automaton.transitions:
                f.write(self._automaton.states[Source[0]].get_text())
                f.write(" -> ")
                f.write(self._automaton.states[Source[2]].get_text())
                f.write(" [ label = \"")

                s = self._automaton.alphabet[Source[1]].get_text()
                i = 0
                modStr = str()

               # unprintable characters save in hexa
                while i < len(s):
                       if (ord(s[i]) > 127 or ord(s[i]) < 30):
                           modStr = modStr + "\\" + hex(ord(s[i]))
                       elif s[i] == '"':
                           modStr = modStr + "\\" + hex(ord(s[i]))
                       elif s[i] == '\'':
                           modStr = modStr + "\\" + hex(ord(s[i]))
                       else:
                           modStr = modStr + s[i]
                       i = i + 1

                t = Source
                if len(t) == 5 and (t[3] != frozenset() or t[4] != frozenset()):
                    for condition in t[3]:
                        modStr += "," + condition
                    for action in t[4]:
                        modStr += "," + action

                f.write(modStr)
                f.write("\" ];\n")
            f.write("}")
            f.close();
            return True

    def report_memory_optimal(self):
        """
            Report consumed memory in bytes. Optimal mapping algorithm is used \
            (with oracle). Basic algorithm for this variant of mapping is:     \
            M = \|transitions\| * ceil(log(\|states\|, 2) / 8).
            For History is: basic + Mem(Flags) + (Tran*Flags*2).
            
            :returns: Returns number of bytes.
            :rtype: int
        """
        tr_len = len(self._automaton.transitions)
        st_len = len(self._automaton.states)
        return int(tr_len * math.ceil(math.log(st_len, 2) / 8)) + \
            (len(self.flags) / 8) + (tr_len*(len(self.flags))*6/8);
    
    def report_memory_naive(self):
        """
            Report consumed memory in bytes. Naive mapping algorithm is used \
            (2D array). Basic algorithm for this variant of mapping is:      \
            M = \|states\| * \|alphabet\| * ceil(log(\|states\| + 1, 2) / 8)
            For History is: basic + Mem(Flags) + (State * Sym * Flags * 2)
            
            :returns: Returns number of bytes.
            :rtype: int
        """
        st_len = len(self._automaton.states)
        al_len = len(self._automaton.alphabet)
        return int(st_len * al_len * math.ceil(math.log(st_len + 1, 2) / 8)) +\
            (len(self.flags) / 8) + (st_len*al_len*len(self.flags)*6/8);

