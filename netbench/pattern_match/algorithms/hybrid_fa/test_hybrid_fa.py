###############################################################################
#  test_hybrid_fa.py: Test module for class hybrid_fa
#  Copyright (C) 2012 Brno University of Technology, ANT @ FIT
#  Author(s): Milan Pala, <xpalam00@stud.fit.vutbr.cz>
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

from netbench.pattern_match.algorithms.hybrid_fa.hybrid_fa import hybrid_fa
from netbench.pattern_match.pcre_parser import pcre_parser
from netbench.pattern_match.nfa_data import nfa_data
from netbench.pattern_match.b_dfa import b_dfa
from netbench.pattern_match.b_nfa import b_nfa
from netbench.pattern_match.b_state import b_State
from netbench.pattern_match.sym_char import b_Sym_char
from netbench.pattern_match.sym_char_class import b_Sym_char_class
from netbench.pattern_match import aux_func
import unittest, copy

class test_hybrid_fa(unittest.TestCase):
    """
        Test module for class hybrid_fa.
    """

    def test___init__(self):
        """__init__()"""
        """
            self.get_compute() has to be False after init
        """
        hyfa = hybrid_fa()
        self.assertFalse(hyfa.get_compute())

    def test_set_special_min_depth(self):
        """set_special_min_depth()"""
        """
            Tests if set_special_min_depth() method works properly.
        """
        hyfa = hybrid_fa()
        
        # test for regular value: above zero
        hyfa.set_special_min_depth(10)
        self.assertEqual(hyfa._SPECIAL_MIN_DEPTH, 10)
        
        # test for off this option
        hyfa.set_special_min_depth(-1)
        self.assertEqual(hyfa._SPECIAL_MIN_DEPTH, -1)
        
        # test for iregular value: zero
        self.assertRaises(ValueError, hyfa.set_special_min_depth, 0)

        # test for iregular value: below zero
        self.assertRaises(ValueError, hyfa.set_special_min_depth, -2)

    def test_set_max_head_size(self):
        """set_max_head_size()"""
        """
            Tests if set_max_head_size() method works properly.
        """
        hyfa = hybrid_fa()
        
        # test for regular value: above zero
        hyfa.set_max_head_size(10)
        self.assertEqual(hyfa._MAX_HEAD_SIZE, 10)
        
        # test for regular value: zero
        hyfa.set_max_head_size(0)
        self.assertEqual(hyfa._MAX_HEAD_SIZE, 0)

        # test for off this option
        hyfa.set_max_head_size(-1)
        self.assertEqual(hyfa._MAX_HEAD_SIZE, -1)

        # test for iregular value: below zero
        self.assertRaises(ValueError, hyfa.set_max_head_size, -2)


    def test_set_max_tx(self):
        """set_max_tx()"""
        """
            Tests if set_max_tx() method works properly.
        """        
        hyfa = hybrid_fa()
        
        # test for regular value: above zero
        hyfa.set_max_tx(10)
        self.assertEqual(hyfa._MAX_TX, 10)
        
        # test for off this option
        hyfa.set_max_tx(-1)
        self.assertEqual(hyfa._MAX_TX, -1)

        # test for regular value: zero
        hyfa.set_max_tx(0)
        self.assertEqual(hyfa._MAX_TX, 0)
        
        # test for iregular value: below zero
        self.assertRaises(ValueError, hyfa.set_max_tx, -2)

    def test_compute(self):
        """compute()"""
        self._test_compute_1()
        self._test_compute_2()
        self._test_compute_3()
        self._test_compute_4()
    
    def _test_compute_1(self):
        """compute()"""
        """
            Test with one regular expression, where computed automaton
            has only DFA part without any NFA tails.
        """
        hyfa = hybrid_fa()
        
        parser = pcre_parser()
        parser.set_text("/abcd/")
        hyfa.create_by_parser(parser)
        
        hyfa.set_special_min_depth(10)
        hyfa.set_max_head_size(10)
        hyfa.set_max_tx(10)
        
        hyfa.compute()
        
        # self.get_compute() has to be True
        self.assertTrue(hyfa.get_compute())

        dfa = b_dfa()
        dfa.create_by_parser(parser)
        dfa.determinise()
        
        a = hyfa.dfa.get_automaton()
        b = dfa.get_automaton()
        
        # test on automaton where is only DFA part without NFA tails
        self.assertEqual(a.states.keys(), b.states.keys())
        self.assertEqual(a.alphabet, b.alphabet)
        self.assertEqual(a.start, b.start)
        self.assertEqual(a.final, b.final)
        self.assertEqual(a.transitions, b.transitions)
        self.assertTrue(a.Flags['Hybrid FA - DFA part'])
        self.assertTrue(a.Flags['Deterministic'])
        self.assertEqual(len(hyfa.nfas), 0)
        self.assertEqual(hyfa.tran_aut, {})

    def _test_compute_2(self):
        """compute()"""
        """
            Test with one regular expression, where computed automaton
            has one NFA tail
        """
        
        hyfa = hybrid_fa()
        
        parser = pcre_parser()
        parser.set_text("/abcd/")
        hyfa.create_by_parser(parser)
        
        hyfa.set_special_min_depth(2)
        hyfa.set_max_head_size(-1)
        hyfa.set_max_tx(-1)
        
        hyfa.compute()

        # self.get_compute() has to be True
        self.assertTrue(hyfa.get_compute())

        parser_dfa = pcre_parser()
        parser_dfa.set_text("/ab/")
        dfa = b_dfa()
        dfa.create_by_parser(parser_dfa)
        dfa.determinise()

        hd = hyfa.dfa.get_automaton()
        hn0 = hyfa.nfas[0].get_automaton()
        d = dfa.get_automaton()
        n = nfa_data().load_from_file(aux_func.getPatternMatchDir() + "/algorithms/hybrid_fa/tests_data/test_compute_2_nfa0.nfa_data")

        # test on automaton where is one NFA tail
        # test of DFA part
        self.assertEqual(hd.states.keys(), d.states.keys())
        self.assertEqual(hd.alphabet, d.alphabet)
        self.assertEqual(hd.start, d.start)
        self.assertEqual(len(hd.final), 0)
        self.assertEqual(hd.transitions, d.transitions)
        self.assertTrue(hd.Flags['Hybrid FA - DFA part'])
        self.assertTrue(hd.Flags['Deterministic'])
        
        self.assertEqual(len(hyfa.nfas), 1)
        self.assertEqual(hyfa.tran_aut, {0: 2})
        
        # test of NFA part #0
        self.assertEqual(hn0.states.keys(), n.states.keys())
        self.assertEqual(hn0.alphabet, n.alphabet)
        self.assertEqual(hn0.start, n.start)
        self.assertEqual(hn0.final, n.final)
        self.assertEqual(hn0.transitions, n.transitions)
        self.assertTrue(hn0.Flags['Hybrid FA - one NFA part'])

    def _test_compute_3(self):
        """compute()"""
        """
            Test with more regular expressions, where computed automaton
            has only DFA part without any NFA tails
        """

        parser = pcre_parser()
        parser.load_file(aux_func.getPatternMatchDir() + "/algorithms/hybrid_fa/tests_data/test_compute_3_pattern.re")

        hyfa = hybrid_fa()
        hyfa.create_by_parser(parser)
        
        hyfa.set_special_min_depth(10)
        hyfa.set_max_head_size(-1)
        hyfa.set_max_tx(-1)
        hyfa.compute()

        # self.get_compute() has to be True
        self.assertTrue(hyfa.get_compute())

        parser = pcre_parser()
        parser.load_file(aux_func.getPatternMatchDir() + "/algorithms/hybrid_fa/tests_data/test_compute_3_pattern.re")
        
        dfa = b_dfa()
        dfa.create_by_parser(parser)
        dfa.determinise()

        hd = hyfa.dfa.get_automaton()
        d = dfa.get_automaton()

        # test of DFA part
        self.assertEqual(hd.states.keys(), d.states.keys())
        self.assertEqual(hd.alphabet, d.alphabet)
        self.assertEqual(hd.start, d.start)
        self.assertEqual(hd.final, d.final)
        self.assertEqual(hd.transitions, d.transitions)
        self.assertTrue(hd.Flags['Hybrid FA - DFA part'])
        self.assertTrue(hd.Flags['Deterministic'])

        # without NFA tails
        self.assertEqual(len(hyfa.nfas), 0)
        self.assertEqual(hyfa.tran_aut, {})

    def _test_compute_4(self):
        """compute()"""
        """
            Test with more regular expressions, where computed automaton
            has has some NFA tails
        """

        hyfa = hybrid_fa()
        
        parser = pcre_parser()
        parser.load_file(aux_func.getPatternMatchDir() + "/algorithms/hybrid_fa/tests_data/test_compute_4_pattern.re")
        hyfa.create_by_parser(parser)
        
        hyfa.set_special_min_depth(2)
        hyfa.set_max_head_size(-1)
        hyfa.set_max_tx(-1)

        hyfa.compute()

        # self.get_compute() has to be True
        self.assertTrue(hyfa.get_compute())

        hd = hyfa.dfa.get_automaton()
        hn0 = hyfa.nfas[0].get_automaton()
        hn1 = hyfa.nfas[1].get_automaton()
        d = nfa_data().load_from_file(aux_func.getPatternMatchDir() + "/algorithms/hybrid_fa/tests_data/test_compute_4_dfa.nfa_data")
        n0 = nfa_data().load_from_file(aux_func.getPatternMatchDir() + "/algorithms/hybrid_fa/tests_data/test_compute_4_nfa0.nfa_data")
        n1 = nfa_data().load_from_file(aux_func.getPatternMatchDir() + "/algorithms/hybrid_fa/tests_data/test_compute_4_nfa1.nfa_data")

        # test of DFA part
        self.assertEqual(hd.states.keys(), d.states.keys())
        self.assertEqual(hd.alphabet, d.alphabet)
        self.assertEqual(hd.start, d.start)
        self.assertTrue(len(hd.final) == 0)
        self.assertEqual(hd.transitions, d.transitions)
        self.assertTrue(hd.Flags['Hybrid FA - DFA part'])
        self.assertTrue(hd.Flags['Deterministic'])
        
        # two NFA tails
        self.assertEqual(len(hyfa.nfas), 2)
        self.assertEqual(hyfa.tran_aut, {0:4, 1:5})
        
        # test of NFA part #0
        self.assertEqual(hn0.states.keys(), n0.states.keys())
        self.assertEqual(hn0.alphabet, n0.alphabet)
        self.assertEqual(hn0.start, n0.start)
        self.assertEqual(hn0.final, n0.final)
        self.assertEqual(hn0.transitions, n0.transitions)
        self.assertTrue(hn0.Flags['Hybrid FA - one NFA part'])

        # test of NFA part #1
        self.assertEqual(hn1.states.keys(), n1.states.keys())
        self.assertEqual(hn1.alphabet, n1.alphabet)
        self.assertEqual(hn1.start, n1.start)
        self.assertEqual(hn1.final, n1.final)
        self.assertEqual(hn1.transitions, n1.transitions)
        self.assertTrue(hn1.Flags['Hybrid FA - one NFA part'])

    def test_search(self):
        """search()"""
        self._test_search_1()
        self._test_search_2()
        self._test_search_3()

    def _test_search_1(self):
        """search()"""
        """
            Test with more regular expression where computed automaton
            has only DFA part.
        """
        
        parser = pcre_parser()
        parser.load_file(aux_func.getPatternMatchDir() + "/algorithms/hybrid_fa/tests_data/test_search_1_pattern.re")
        
        hyfa = hybrid_fa()
        hyfa.create_by_parser(parser)
        
        hyfa.set_special_min_depth(10)
        hyfa.set_max_head_size(-1)
        hyfa.set_max_tx(-1)
        
        hyfa.compute()
        
        self.assertTrue(hyfa.get_compute())
        
        ret = hyfa.search("abcd")
        self.assertEqual(ret, [1,0])
        
        ret = hyfa.search("bce")
        self.assertEqual(ret, [0,1])
        
        ret = hyfa.search("cdefgh")
        self.assertEqual(ret, [0,0])

    def _test_search_2(self):
        """search()"""
        """
            Test with more regular expression where computed automaton
            has some NFA parts.
        """
        
        parser = pcre_parser()
        parser.load_file(aux_func.getPatternMatchDir() + "/algorithms/hybrid_fa/tests_data/test_search_1_pattern.re")
        
        hyfa = hybrid_fa()
        hyfa.create_by_parser(parser)
        
        hyfa.set_special_min_depth(2)
        hyfa.set_max_head_size(-1)
        hyfa.set_max_tx(-1)
        
        hyfa.compute()
        
        self.assertTrue(hyfa.get_compute())
        
        ret = hyfa.search("abcd")
        self.assertEqual(ret, [1,0])
        
        ret = hyfa.search("bce")
        self.assertEqual(ret, [0,1])
        
        ret = hyfa.search("cdefgh")
        self.assertEqual(ret, [0,0])

    def _test_search_3(self):
        """search()"""
        """
            Test with many regular expression where computed automaton
            has many NFA parts.
            Compares results of searching in computed Hybrid FA with
            regular NFA automaton searching.
        """
        parser = pcre_parser()
        parser.load_file(aux_func.getPatternMatchDir() + "/rules/Snort/web-cgi.rules.pcre")

        nfa_aut = b_nfa()
        nfa_aut.create_by_parser(parser)
        nfa_aut.compute()
        
        parser = pcre_parser()
        parser.load_file(aux_func.getPatternMatchDir() + "/rules/Snort/web-cgi.rules.pcre")
        
        hyfa = hybrid_fa()
        hyfa.create_by_parser(parser)
        
        hyfa.set_special_min_depth(2)
        hyfa.set_max_head_size(0)
        hyfa.set_max_tx(0)
       
        hyfa.compute()

        input_data = "/awstats.pl?---configdir=| /calendar-admin.pl /db4web_c.exe/aaaa:  /itemid=123f  /ShellExample.cgi?aaaaa*"
        self.assertEqual(nfa_aut.search(input_data), hyfa.search(input_data))

    def test_get_state_num(self):
        """get_state_num()"""
        self._test_get_state_num_1()
        self._test_get_state_num_2()
        
    def _test_get_state_num_1(self):
        """get_state_num()"""
        """
            Test with more regular expression where computed automaton
            has only DFA part.
        """
        hyfa = hybrid_fa()
        
        parser = pcre_parser()
        parser.set_text("/abcd/")
        hyfa.create_by_parser(parser)
        
        hyfa.set_special_min_depth(10)
        hyfa.set_max_head_size(10)
        hyfa.set_max_tx(10)
        
        hyfa.compute()
        
        self.assertEqual(hyfa.get_state_num(), 5)

    def _test_get_state_num_2(self):
        """get_state_num()"""
        """
            Test with more regular expression where computed automaton
            has some NFA parts.
        """
        hyfa = hybrid_fa()
        
        parser = pcre_parser()
        parser.load_file(aux_func.getPatternMatchDir() + "/algorithms/hybrid_fa/tests_data/test_get_state_num_2.re")
        hyfa.create_by_parser(parser)
        
        hyfa.set_special_min_depth(2)
        hyfa.set_max_head_size(-1)
        hyfa.set_max_tx(-1)

        hyfa.compute()

        self.assertEqual(hyfa.get_state_num(), 11)

    def test_get_trans_num(self):
        """get_state_num()"""
        self._test_get_trans_num_1()
        self._test_get_trans_num_2()
        
    def _test_get_trans_num_1(self):
        """get_state_num()"""
        """
            Test with more regular expression where computed automaton
            has only DFA part.
        """
        hyfa = hybrid_fa()
        
        parser = pcre_parser()
        parser.set_text("/abcd/")
        hyfa.create_by_parser(parser)
        
        hyfa.set_special_min_depth(10)
        hyfa.set_max_head_size(10)
        hyfa.set_max_tx(10)
        
        hyfa.compute()
        
        self.assertEqual(hyfa.get_trans_num(), 13)

    def _test_get_trans_num_2(self):
        """get_trans_num()"""
        """
            Test with more regular expression where computed automaton
            has some NFA parts.
        """        
        hyfa = hybrid_fa()
        
        parser = pcre_parser()
        parser.load_file(aux_func.getPatternMatchDir() + "/algorithms/hybrid_fa/tests_data/test_get_trans_num_2.re")
        hyfa.create_by_parser(parser)
        
        hyfa.set_special_min_depth(2)
        hyfa.set_max_head_size(-1)
        hyfa.set_max_tx(-1)

        hyfa.compute()

        self.assertEqual(hyfa.get_trans_num(), 23)

    def test__is_special(self):
        """_is_special()"""
        """
            Tests whether _is_special() method works properly.
        """
        parser = pcre_parser()
        parser.set_text("/abcd/")
        
        hyfa = hybrid_fa()
        hyfa.create_by_parser(parser)

        hyfa.set_special_min_depth(2)
        hyfa.set_max_head_size(-1)
        hyfa.set_max_tx(-1)

        hyfa.compute()

        # tests with depth of states
        
        # test when same states are borders
        self.assertFalse(hyfa._is_special(0))
        self.assertFalse(hyfa._is_special(2))
        self.assertTrue(hyfa._is_special(4))
        self.assertTrue(hyfa._is_special(6))
        self.assertTrue(hyfa._is_special(8))

        # test when all states are not borders
        hyfa.set_special_min_depth(6)
        hyfa.set_max_head_size(-1)
        hyfa.set_max_tx(-1)

        self.assertFalse(hyfa._is_special(0))
        self.assertFalse(hyfa._is_special(2))
        self.assertFalse(hyfa._is_special(4))
        self.assertFalse(hyfa._is_special(6))
        self.assertFalse(hyfa._is_special(8))

        # tests with head size

        hyfa.set_special_min_depth(-1)
        hyfa.set_max_head_size(3)
        hyfa.set_max_tx(-1)
        
        # state is not border
        hyfa._head_size = 2
        self.assertFalse(hyfa._is_special(0))
        
        # head is full, all states are borders
        hyfa._head_size = 4
        self.assertTrue(hyfa._is_special(0))

        # tests with outgoing transitions

        # test ...
        hyfa.set_max_tx(1)
        hyfa.set_max_head_size(-1)
        hyfa.set_special_min_depth(-1)
        self.assertTrue(hyfa._is_special(0))
        self.assertTrue(hyfa._is_special(2))

    def test_report_memory_optimal(self):
        """report_memory_optimal()"""
        self._test_report_memory_optimal_1()
        self._test_report_memory_optimal_2()

    def _test_report_memory_optimal_1(self):
        """report_memory_optimal()"""
        """
            Test with more regular expression where computed automaton
            has only DFA part.
        """
        hyfa = hybrid_fa()
        
        parser = pcre_parser()
        parser.set_text("/abcd/")
        hyfa.create_by_parser(parser)
        
        hyfa.set_special_min_depth(10)
        hyfa.set_max_head_size(10)
        hyfa.set_max_tx(10)
        
        hyfa.compute()
        
        self.assertEqual(hyfa.report_memory_optimal(), 13)

    def _test_report_memory_optimal_2(self):
        """report_memory_optimal()"""
        """
            Test with more regular expression where computed automaton
            has some NFA parts.
        """
        hyfa = hybrid_fa()
        
        parser = pcre_parser()
        parser.load_file(aux_func.getPatternMatchDir() + "/algorithms/hybrid_fa/tests_data/test_get_state_num_2.re")
        hyfa.create_by_parser(parser)
        
        hyfa.set_special_min_depth(2)
        hyfa.set_max_head_size(-1)
        hyfa.set_max_tx(-1)

        hyfa.compute()

        self.assertEqual(hyfa.report_memory_optimal(), 37)

    def test_report_memory_naive(self):
        """report_memory_naive()"""
        self._test_report_memory_naive_1()
        self._test_report_memory_naive_2()

    def _test_report_memory_naive_1(self):
        """report_memory_naive()"""
        """
            Test with more regular expression where computed automaton
            has only DFA part.
        """
        hyfa = hybrid_fa()
        
        parser = pcre_parser()
        parser.set_text("/abcd/")
        hyfa.create_by_parser(parser)
        
        hyfa.set_special_min_depth(10)
        hyfa.set_max_head_size(10)
        hyfa.set_max_tx(10)
        
        hyfa.compute()
        
        self.assertEqual(hyfa.report_memory_naive(), 40)

    def _test_report_memory_naive_2(self):
        """report_memory_naive()"""
        """
            Test with more regular expression where computed automaton
            has some NFA parts.
        """
        hyfa = hybrid_fa()
        
        parser = pcre_parser()
        parser.load_file(aux_func.getPatternMatchDir() + "/algorithms/hybrid_fa/tests_data/test_get_state_num_2.re")
        hyfa.create_by_parser(parser)
        
        hyfa.set_special_min_depth(2)
        hyfa.set_max_head_size(-1)
        hyfa.set_max_tx(-1)

        hyfa.compute()

        self.assertEqual(hyfa.report_memory_naive(), 58)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_hybrid_fa)
    unittest.TextTestRunner(verbosity=2).run(suite)
