###############################################################################
#  test_HistoryCountingFA.py: Test module for class HistoryCountingFA
#  Copyright (C) 2011 Brno University of Technology, ANT @ FIT
#  Author(s): Jaroslav Suchodol, <xsucho04@stud.fit.vutbr.cz>
###############################################################################
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
#  This software or firmware is provided ``as is, and any express or implied
#  warranties, including, but not limited to, the implied warranties of
#  merchantability and fitness for a particular purpose are disclaimed.
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

from netbench.pattern_match.algorithms.history_counting_fa. \
    history_counting_fa import HistoryCountingFA
from netbench.pattern_match.pcre_parser import pcre_parser
from netbench.pattern_match.nfa_data import nfa_data
from netbench.pattern_match.b_state import b_State
from netbench.pattern_match.sym_char import b_Sym_char
from netbench.pattern_match.sym_char_class import b_Sym_char_class
from netbench.pattern_match import aux_func
import unittest, copy

class test_HistoryCountingFA(unittest.TestCase):
    """
        Test module for class HistoryCountingFA.
    """

    def test__replace_length_restriction_with_a_closure(self):
        """_replace_length_restriction_with_a_closure(NFA)"""
        # /ab.{4}cd /; test with an expression that contains .{4}
        par = pcre_parser(create_cnt_constr = True)
        par.set_text("/ab.{4}cd/")
        history = HistoryCountingFA()
        history.create_by_parser(par)
        history.remove_epsilons()
        NFA = history.get_automaton(True)
        NFA_without_cnt = history._replace_length_restriction_with_a_closure(NFA)
        copy = NFA_without_cnt

        result = nfa_data().load_from_file(aux_func.getPatternMatchDir() + "/algorithms/history_counting_fa/test_data/test_data_1.nfa_data")

        self.assertTrue(history.flags_cnt == {4: "4"})

        self.assertTrue(sorted(copy.states.keys()) ==
            sorted(result.states.keys()))
        self.assertTrue(copy.alphabet == result.alphabet)
        self.assertTrue(copy.start == result.start)
        self.assertTrue(copy.final == result.final)
        self.assertTrue(copy.transitions == result.transitions)
        self.assertTrue(copy.Flags == result.Flags)

    def test__discover_closure_states(self):
        """_discover_closure_states(NFA)"""
        par = pcre_parser(create_cnt_constr = True)
        par.set_text("/ab[^a]{4}c|def/")
        history = HistoryCountingFA()
        history.create_by_parser(par)
        history.remove_epsilons()
        NFA = history.get_automaton(True)

        NFA_without_cnt = \
            history._replace_length_restriction_with_a_closure(NFA)
        self.assertTrue(history._discover_closure_states(NFA_without_cnt)
            == [12])

    def test__identify_fading_states(self):
        """_identify_fading_states(nfa_closure_states)"""
        par = pcre_parser(create_cnt_constr = True)
        par.set_text("/ab[^a]{4}c|def/")
        history = HistoryCountingFA()
        history.create_by_parser(par)
        history.remove_epsilons()
        NFA = history.get_automaton(True)

        NFA_without_cnt = \
            history._replace_length_restriction_with_a_closure(NFA)

        history._automaton = copy.deepcopy(NFA_without_cnt)
        history.determinise(create_table = True)

        nfa_closure_states = history._discover_closure_states(NFA_without_cnt)
        self.assertTrue(history._identify_fading_states(nfa_closure_states)
            == [5, 7, 8, 9])

    def test__remove_fading_dfa_states(self):
        """_remove_fading_dfa_states(dfa_fading_states)"""
        par = pcre_parser(create_cnt_constr = True)
        par.set_text("/ab[^a]{4}c|def/")
        history = HistoryCountingFA()
        history.create_by_parser(par)
        history.remove_epsilons()
        NFA = history.get_automaton(True)

        NFA_without_cnt = \
            history._replace_length_restriction_with_a_closure(NFA)

        history._automaton = copy.deepcopy(NFA_without_cnt)
        history.determinise(create_table = True)

        nfa_closure_states = history._discover_closure_states(NFA_without_cnt)
        dfa_fading_states = history._identify_fading_states(nfa_closure_states)
        history._remove_fading_dfa_states(dfa_fading_states)

        self.assertTrue(sorted(history._automaton.states)
            == [0, 1, 2, 3, 4, 6])

    def test__pruning_process(self):
        """_pruning_process()"""
        par = pcre_parser(create_cnt_constr = True)
        par.set_text("/ab[^a]{4}c|def/")
        history = HistoryCountingFA()
        history.create_by_parser(par)
        history.remove_epsilons()
        NFA = history.get_automaton(True)

        NFA_without_cnt = \
            history._replace_length_restriction_with_a_closure(NFA)

        history._automaton = copy.deepcopy(NFA_without_cnt)
        history.determinise(create_table = True)

        nfa_closure_states = history._discover_closure_states(NFA_without_cnt)
        dfa_fading_states = history._identify_fading_states(nfa_closure_states)
        history._remove_fading_dfa_states(dfa_fading_states)

        self.assertTrue(len(history._automaton.transitions) == 40)
        history._pruning_process()
        self.assertTrue(len(history._automaton.transitions) == 34)

    def test_compute(self):
        """compute()"""
        # Check the correctness of the logical machine output over
        # self.assertTrue on individual items + focus on the properties
        # of HistoryCountingFA (transitions, flags, counters)

        # /abcd/; test with an expression that does not use properties
        # of HistoryCountingFA
        par = pcre_parser(create_cnt_constr = True)
        par.set_text("/abcd/")
        history = HistoryCountingFA()
        history.create_by_parser(par)
        history.remove_epsilons()
        NFA = history.get_automaton(True)

        history.determinise(create_table = True)

        history.compute(NFA)

        copy = history.get_automaton()

        result = nfa_data().load_from_file(aux_func.getPatternMatchDir() + "/algorithms/history_counting_fa/test_data/test_data_2.nfa_data")

        self.assertTrue(sorted(copy.states.keys()) ==
            sorted(result.states.keys()))
        self.assertTrue(copy.alphabet == result.alphabet)
        self.assertTrue(copy.start == result.start)
        self.assertTrue(copy.final == result.final)
        self.assertTrue(copy.transitions == result.transitions)
        
        # /ab.{3}cd /; test with an expression that contains .{X}
        par = pcre_parser(create_cnt_constr = True)
        par.set_text("/ab.{3}cd/")
        history = HistoryCountingFA()
        history.create_by_parser(par)
        history.remove_epsilons()
        NFA = history.get_automaton(True)

        NFA_without_cnt = \
            history._replace_length_restriction_with_a_closure(NFA)
        NFA = history.get_automaton(True)
        history._automaton = NFA_without_cnt
        history.determinise(create_table = True)

        history.compute(NFA)

        copy = history.get_automaton()

        result = nfa_data().load_from_file(aux_func.getPatternMatchDir() + "/algorithms/history_counting_fa/test_data/test_data_3.nfa_data")

        self.assertTrue(sorted(copy.states.keys()) ==
            sorted(result.states.keys()))
        self.assertTrue(copy.alphabet == result.alphabet)
        self.assertTrue(copy.start == result.start)
        self.assertTrue(copy.final == result.final)
        self.assertTrue(copy.transitions == result.transitions)

        # /ab[^1234]{3}cd|efg/; test with an expression containing one
        # alternation [^1234]{3}, the second is not
        par = pcre_parser(create_cnt_constr = True)
        par.set_text("/ab[^1234]{3}cd|efg/")
        history = HistoryCountingFA()
        history.create_by_parser(par)
        history.remove_epsilons()
        NFA = history.get_automaton(True)

        NFA_without_cnt = \
            history._replace_length_restriction_with_a_closure(NFA)
        NFA = history.get_automaton(True)
        history._automaton = NFA_without_cnt
        history.determinise(create_table = True)

        history.compute(NFA)

        copy = history.get_automaton()

        result = nfa_data().load_from_file(aux_func.getPatternMatchDir() + "/algorithms/history_counting_fa/test_data/test_data_4.nfa_data")

        self.assertTrue(sorted(copy.states.keys()) ==
            sorted(result.states.keys()))
        self.assertTrue(copy.alphabet == result.alphabet)
        self.assertTrue(copy.start == result.start)
        self.assertTrue(copy.final == result.final)
        self.assertTrue(copy.transitions == result.transitions)

    def test_search(self):
        """search()"""
        # For RE upstairs do tests for this method.

        # /abcd/; test with an expression that does not use properties
        # of Hfa
        par = pcre_parser(create_cnt_constr = True)
        par.set_text("/abcd/")
        history = HistoryCountingFA()
        history.create_by_parser(par)
        history.remove_epsilons()
        NFA = history.get_automaton(True)

        history.determinise(create_table = True)

        history.compute(NFA)

        self.assertTrue(history.search("efg") == [0])
        self.assertTrue(history.search("efabcg") == [0])
        self.assertTrue(history.search("efabcd") == [1])
        self.assertTrue(history.search("abcefabcdabcx") == [1])
        self.assertTrue(history.search("abcd") == [1])
        self.assertTrue(history.search("123abcd456") == [1])
        self.assertTrue(history.search("123ab0cd456") == [0])
 
        # /ab.{3}cd /; test with an expression that contains .{X}
        par = pcre_parser(create_cnt_constr = True)
        par.set_text("/ab.{3}cd/")
        history = HistoryCountingFA()
        history.create_by_parser(par)
        history.remove_epsilons()
        NFA = history.get_automaton(True)

        NFA_without_cnt = \
            history._replace_length_restriction_with_a_closure(NFA)
        NFA = history.get_automaton(True)
        history._automaton = NFA_without_cnt
        history.determinise(create_table = True)

        history.compute(NFA)

        self.assertTrue(history.search("efg") == [0])
        self.assertTrue(history.search("abnecoefg") == [0])
        self.assertTrue(history.search("abnecocx") == [0])
        self.assertTrue(history.search("necoabneccdneco") == [1])
        self.assertTrue(history.search("ab123cd") == [1])
        self.assertTrue(history.search("123abcd456") == [0])
        self.assertTrue(history.search("123abXXXcd456") == [1])
        self.assertTrue(history.search("123abXXXXcd456") == [0])

        # TODO Communist behavior (match more than 100%)
        self.assertTrue(history.search("123abXXXcccccccccd456") == [1])

        # /ab[^1234]{3}cd|efg/; test with an expression containing one
        # alternation [^1234]{3}, the second is not
        par = pcre_parser(create_cnt_constr = True)
        par.set_text("/ab[^1234]{3}cd|efg/")
        history = HistoryCountingFA()
        history.create_by_parser(par)
        history.remove_epsilons()
        NFA = history.get_automaton(True)

        NFA_without_cnt = \
            history._replace_length_restriction_with_a_closure(NFA)
        NFA = history.get_automaton(True)
        history._automaton = NFA_without_cnt
        history.determinise(create_table = True)

        history.compute(NFA)

        self.assertTrue(history.search("exfg") == [0])
        self.assertTrue(history.search("abnecocx") == [0])

        self.assertTrue(history.search("efg") == [1])
        self.assertTrue(history.search("textefgtext") == [1])
        self.assertTrue(history.search("abnecoefg") == [1])

        self.assertTrue(history.search("necoabnecXcdneco") == [0])
        self.assertTrue(history.search("necoabneccdneco") == [1])
        self.assertTrue(history.search("abxXxcd") == [1])

        self.assertTrue(history.search("abXX2cd") == [0])
        # TODO Communist behavior (match more than 100%)
        self.assertTrue(history.search("ab2XXcd") == [1])
        self.assertTrue(history.search("abX2Xcd") == [1])

        self.assertTrue(history.search("123abcd456") == [0])
        self.assertTrue(history.search("123abXXXcd456") == [1])
 
        self.assertTrue(history.search("ab123cd") == [0])
        self.assertTrue(history.search("ab4456cd") == [0])
        self.assertTrue(history.search("abcefg") == [1])
        self.assertTrue(history.search("123abblekekcd456") == [0])
        self.assertTrue(history.search("123ab000cd456") == [1])

        # TODO Communist behavior (match more than 100%)
        self.assertTrue(history.search("123abcccccccAXXXcd456") == [1])

    def test_report_memory_optimal(self):
        """report_memory_optional()"""
        # /ab[^1234]*cd|efg/; test with an expression containing one
        # alternation [^1234]*, the second is not
        par = pcre_parser(create_cnt_constr = True)
        par.set_text("/ab[^1234]{3}cd|efg/")
        history = HistoryCountingFA()
        history.create_by_parser(par)
        history.remove_epsilons()
        NFA = history.get_automaton(True)

        NFA_without_cnt = \
            history._replace_length_restriction_with_a_closure(NFA)
        NFA = history.get_automaton(True)
        history._automaton = NFA_without_cnt
        history.determinise(create_table = True)

        history.compute(NFA)

        self.assertTrue(history.report_memory_optimal() == 78)

    def test_report_memory_naive(self):
        """report_memory_naive()"""
        # /ab[^1234]*cd|efg/; test with an expression containing one
        # alternation [^1234]*, the second is not
        par = pcre_parser(create_cnt_constr = True)
        par.set_text("/ab[^1234]{3}cd|efg/")
        history = HistoryCountingFA()
        history.create_by_parser(par)
        history.remove_epsilons()
        NFA = history.get_automaton(True)

        NFA_without_cnt = \
            history._replace_length_restriction_with_a_closure(NFA)
        NFA = history.get_automaton(True)
        history._automaton = NFA_without_cnt
        history.determinise(create_table = True)

        history.compute(NFA)

        self.assertTrue(history.report_memory_naive() == 208)
 
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_HistoryCountingFA)
    unittest.TextTestRunner(verbosity=2).run(suite)
