###############################################################################
#  test_JHybridFA.py: Test module for class JHybridFA
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

from netbench.pattern_match.algorithms.j_hybrid_fa.j_hybrid_fa import JHybridFA
from netbench.pattern_match.pcre_parser import pcre_parser
from netbench.pattern_match.nfa_data import nfa_data
from netbench.pattern_match.b_dfa import b_dfa
from netbench.pattern_match.b_nfa import b_nfa
from netbench.pattern_match.b_state import b_State
from netbench.pattern_match.sym_char import b_Sym_char
from netbench.pattern_match.sym_char_class import b_Sym_char_class
from netbench.pattern_match.pattern_exceptions import empty_automaton_exception, general_not_implemented, unknown_parser
from netbench.pattern_match import aux_func
import unittest, copy

class test_JHybridFA(unittest.TestCase):
    """
        Test module for class JHybridFA.
    """

    def test___init__(self):
        """__init__()"""
        """
            self.get_compute() has to be False after init
        """
        hyfa = JHybridFA()
        self.assertFalse(hyfa.get_compute())

    def test_set_parser(self):
        """set_parser()"""
        """
            Tests if set_parser() method works properly.
        """
        hyfa = JHybridFA()

        # test with regular parser
        parser = pcre_parser()
        hyfa.set_parser(parser)
        self.assertEqual(parser, hyfa._parser)

        # test with another class
        self.assertRaises(unknown_parser, hyfa.set_parser, "not_parser")

    def test__find_first_occurence_of_blowup(self):
        """_find_first_occurence_of_blowup()"""
        hyfa = JHybridFA()
        
        # test without blow up patterns
        i = hyfa._find_first_occurence_of_blowup("/abcd/")
        self.assertEqual(None, i)
        
        # test with dot star
        i = hyfa._find_first_occurence_of_blowup("/ab.*cd/")
        self.assertEqual(3, i)
        
        # test with char class star
        i = hyfa._find_first_occurence_of_blowup("/ab[a-z]*cd/")
        self.assertEqual(3, i)

        # test with char class counting constrains
        i = hyfa._find_first_occurence_of_blowup("/ab[a-z]{1,2}cd/")
        self.assertEqual(3, i)

        # test with char class counting constrains
        i = hyfa._find_first_occurence_of_blowup("/ab[0-9]{1}cd/")
        self.assertEqual(3, i)
        
        # test with char class counting constrains
        i = hyfa._find_first_occurence_of_blowup("/ab[a-z0-9]{1,}cd/")
        self.assertEqual(3, i)
        
        # test with fake char class
        i = hyfa._find_first_occurence_of_blowup("/ab\[a-z]{1,2}cd/")
        self.assertEqual(None, i)

        # test with blow up on start of RE
        i = hyfa._find_first_occurence_of_blowup("/[a-z]{1,2}cd/")
        self.assertEqual(1, i)

        # test with more blow up patterns
        i = hyfa._find_first_occurence_of_blowup("/ab[a-z]{1,2}cd.*/")
        self.assertEqual(3, i)

    def test__split_expresion(self):
        """_split_expresion()"""
        """
            Tests if _split_expresion() works properly
        """
        hyfa = JHybridFA()
        
        # try to split RE without blow up pattern
        (a, b) = hyfa._split_expresion("/abcd/")
        self.assertEqual("/abcd/", a)
        self.assertEqual("", b)
        
        # try to split RE without blow up pattern with option in RE
        (a, b) = hyfa._split_expresion("/abcd/i")
        self.assertEqual("/abcd/i", a)
        self.assertEqual("", b)

        # try to split RE with dot star
        (a, b) = hyfa._split_expresion("/ab.*cd/")
        self.assertEqual("/ab/", a)
        self.assertEqual("/.*cd/", b)

        # try to split RE with dot star
        (a, b) = hyfa._split_expresion("/ab.*cd/i")
        self.assertEqual("/ab/i", a)
        self.assertEqual("/.*cd/i", b)
        
        # try to split RE with char class star
        (a, b) = hyfa._split_expresion("/ab[a-z]*cd/iUm")
        self.assertEqual("/ab/iUm", a)
        self.assertEqual("/[a-z]*cd/iUm", b)

        # try to split RE with char class CC
        (a, b) = hyfa._split_expresion("/ab[a-z]{1,2}cd/iUm")
        self.assertEqual("/ab/iUm", a)
        self.assertEqual("/[a-z]{1,2}cd/iUm", b)

        # try to split RE with char class CC
        (a, b) = hyfa._split_expresion("/ab[0-9]{1}cd/iUm")
        self.assertEqual("/ab/iUm", a)
        self.assertEqual("/[0-9]{1}cd/iUm", b)

        # try to split RE with char class CC
        (a, b) = hyfa._split_expresion("/ab[a-z0-9]{1,}cd/")
        self.assertEqual("/ab/", a)
        self.assertEqual("/[a-z0-9]{1,}cd/", b)

        # try to split RE with fake char class CC
        (a, b) = hyfa._split_expresion("/ab\[a-z]{1,2}cd/")
        self.assertEqual("/ab\[a-z]{1,2}cd/", a)
        self.assertEqual("", b)

        # try to split RE with char class CC on start of RE
        (a, b) = hyfa._split_expresion("/[a-z]{1,2}cd/iUm")
        self.assertEqual("", a)
        self.assertEqual("/[a-z]{1,2}cd/iUm", b)

        # try to split RE with more blow up patterns
        (a, b) = hyfa._split_expresion("/ab[a-z]{1,2}cd.*/")
        self.assertEqual("/ab/", a)
        self.assertEqual("/[a-z]{1,2}cd.*/", b)

    def test_compute(self):
        """compute()"""
        # test without blow up patterns
        # test with more patterns and one blow up pattern on 1st position
        # test with more patterns and one blow up pattern on 2nd position
        # test with more patterns and one with blow up on start on RE
        # test with more patterns where some are blow up
        self._test_compute_1()
        self._test_compute_2()
        self._test_compute_3()
        self._test_compute_4()
        self._test_compute_5()
    
    def _test_compute_1(self):
        """compute()"""
        """
            Test without blow up patterns
        """
        hyfa = JHybridFA()
        
        parser = pcre_parser()
        hyfa.set_parser(parser)
        hyfa.load_file(aux_func.getPatternMatchDir() + "/algorithms/j_hybrid_fa/tests_data/test_compute_1.re")
        
        hyfa.compute()
        
        # self.get_compute() has to be True
        self.assertTrue(hyfa.get_compute())

        parser = pcre_parser()
        parser.load_file(aux_func.getPatternMatchDir() + "/algorithms/j_hybrid_fa/tests_data/test_compute_1.re")
        dfa = b_dfa()
        dfa.create_by_parser(parser)
        dfa.compute()
        
        a = hyfa.dfa.get_automaton(False)
        b = dfa.get_automaton(False)
        
        # Test without blow up patterns
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
            Test with more patterns and one blow up pattern on 1st position
        """
        hyfa = JHybridFA()
        
        parser = pcre_parser()
        hyfa.set_parser(parser)
        hyfa.load_file(aux_func.getPatternMatchDir() + "/algorithms/j_hybrid_fa/tests_data/test_compute_2.re")
        
        hyfa.compute()
        
        # self.get_compute() has to be True
        self.assertTrue(hyfa.get_compute())

        # self.get_compute() has to be True
        self.assertTrue(hyfa.get_compute())

        hd = hyfa.dfa.get_automaton(False)
        hn0 = hyfa.nfas[0].get_automaton(False)
        d = nfa_data().load_from_file(aux_func.getPatternMatchDir() + "/algorithms/j_hybrid_fa/tests_data/test_compute_2_dfa.nfa_data")
        n = nfa_data().load_from_file(aux_func.getPatternMatchDir() + "/algorithms/j_hybrid_fa/tests_data/test_compute_2_nfa0.nfa_data")

        # Test with more patterns and one blow up pattern on 2nd position
        # test of DFA part
        self.assertEqual(hd.states.keys(), d.states.keys())
        self.assertEqual(hd.alphabet, d.alphabet)
        self.assertEqual(hd.start, d.start)
        self.assertEqual(len(hd.final), 3)
        self.assertEqual(hd.transitions, d.transitions)
        self.assertTrue(hd.Flags['Hybrid FA - DFA part'])
        self.assertTrue(hd.Flags['Deterministic'])
        
        self.assertEqual(len(hyfa.nfas), 1)
        self.assertEqual(hyfa.tran_aut, {0: 9})
        
        # test of NFA part #0
        self.assertEqual(hn0.states.keys().sort(), n.states.keys().sort())
        self.assertEqual(hn0.alphabet, n.alphabet)
        self.assertEqual(hn0.start, n.start)
        self.assertEqual(hn0.final, n.final)
        self.assertEqual(hn0.transitions, n.transitions)
        self.assertTrue(hn0.Flags['Hybrid FA - one NFA part'])

    def _test_compute_3(self):
        """compute()"""
        """
            Test with more patterns and one with blow up on start on RE
        """
        hyfa = JHybridFA()
        
        parser = pcre_parser()
        hyfa.set_parser(parser)
        hyfa.load_file(aux_func.getPatternMatchDir() + "/algorithms/j_hybrid_fa/tests_data/test_compute_3.re")
        
        hyfa.compute()
        
        # self.get_compute() has to be True
        self.assertTrue(hyfa.get_compute())

        # self.get_compute() has to be True
        self.assertTrue(hyfa.get_compute())

        hd = hyfa.dfa.get_automaton(False)
        hn0 = hyfa.nfas[0].get_automaton(False)
        d = nfa_data().load_from_file(aux_func.getPatternMatchDir() + "/algorithms/j_hybrid_fa/tests_data/test_compute_3_dfa.nfa_data")
        n = nfa_data().load_from_file(aux_func.getPatternMatchDir() + "/algorithms/j_hybrid_fa/tests_data/test_compute_3_nfa0.nfa_data")

        # Test with more patterns and one with blow up on start on RE
        # test of DFA part
        self.assertEqual(hd.states.keys().sort(), d.states.keys().sort())
        self.assertEqual(hd.alphabet, d.alphabet)
        self.assertEqual(hd.start, d.start)
        self.assertEqual(len(hd.final), 3)
        self.assertEqual(hd.transitions, d.transitions)
        self.assertTrue(hd.Flags['Hybrid FA - DFA part'])
        self.assertTrue(hd.Flags['Deterministic'])
        
        self.assertEqual(len(hyfa.nfas), 1)
        self.assertEqual(hyfa.tran_aut, {0: 8})
        
        # test of NFA part #0
        self.assertEqual(hn0.states.keys().sort(), n.states.keys().sort())
        self.assertEqual(hn0.alphabet, n.alphabet)
        self.assertEqual(hn0.start, n.start)
        self.assertEqual(hn0.final, n.final)
        self.assertEqual(hn0.transitions, n.transitions)
        self.assertTrue(hn0.Flags['Hybrid FA - one NFA part'])

    def _test_compute_4(self):
        """compute()"""
        """
            Test with more patterns where some are blow up
        """
        hyfa = JHybridFA()
        
        parser = pcre_parser()
        hyfa.set_parser(parser)
        hyfa.load_file(aux_func.getPatternMatchDir() + "/algorithms/j_hybrid_fa/tests_data/test_compute_4.re")
        
        hyfa.compute()
        
        # self.get_compute() has to be True
        self.assertTrue(hyfa.get_compute())

        # self.get_compute() has to be True
        self.assertTrue(hyfa.get_compute())

        hd = hyfa.dfa.get_automaton(False)
        hn0 = hyfa.nfas[0].get_automaton(False)
        d = nfa_data().load_from_file(aux_func.getPatternMatchDir() + "/algorithms/j_hybrid_fa/tests_data/test_compute_4_dfa.nfa_data")
        n = nfa_data().load_from_file(aux_func.getPatternMatchDir() + "/algorithms/j_hybrid_fa/tests_data/test_compute_4_nfa0.nfa_data")

        # Test with more patterns where some are blow up
        # test of DFA part
        self.assertEqual(hd.states.keys(), d.states.keys())
        self.assertEqual(hd.alphabet, d.alphabet)
        self.assertEqual(hd.start, d.start)
        self.assertEqual(len(hd.final), 2)
        self.assertEqual(hd.transitions, d.transitions)
        self.assertTrue(hd.Flags['Hybrid FA - DFA part'])
        self.assertTrue(hd.Flags['Deterministic'])
        
        self.assertEqual(len(hyfa.nfas), 1)
        self.assertEqual({0: 0}, hyfa.tran_aut)
        
        # test of NFA part #0
        self.assertEqual(hn0.states.keys(), n.states.keys())
        self.assertEqual(hn0.alphabet, n.alphabet)
        self.assertEqual(hn0.start, n.start)
        self.assertEqual(hn0.final, n.final)
        self.assertEqual(hn0.transitions, n.transitions)
        self.assertTrue(hn0.Flags['Hybrid FA - one NFA part'])

    def _test_compute_5(self):
        """compute()"""
        """
            Test where are more blow up REs
        """
        hyfa = JHybridFA()
        
        parser = pcre_parser()
        hyfa.set_parser(parser)
        hyfa.load_file(aux_func.getPatternMatchDir() + "/algorithms/j_hybrid_fa/tests_data/test_compute_5.re")
        
        hyfa.compute()
        
        # self.get_compute() has to be True
        self.assertTrue(hyfa.get_compute())

        # self.get_compute() has to be True
        self.assertTrue(hyfa.get_compute())

        hd = hyfa.dfa.get_automaton(False)
        hn0 = hyfa.nfas[0].get_automaton(False)
        hn1 = hyfa.nfas[1].get_automaton(False)
        d = nfa_data().load_from_file(aux_func.getPatternMatchDir() + "/algorithms/j_hybrid_fa/tests_data/test_compute_5_dfa.nfa_data")
        n0 = nfa_data().load_from_file(aux_func.getPatternMatchDir() + "/algorithms/j_hybrid_fa/tests_data/test_compute_5_nfa0.nfa_data")
        n1 = nfa_data().load_from_file(aux_func.getPatternMatchDir() + "/algorithms/j_hybrid_fa/tests_data/test_compute_5_nfa1.nfa_data")

        # test where are more blow up REs
        # test of DFA part
        self.assertEqual(hd.states.keys(), d.states.keys())
        self.assertEqual(hd.alphabet, d.alphabet)
        self.assertEqual(hd.start, d.start)
        self.assertEqual(len(hd.final), 3)
        self.assertEqual(hd.transitions, d.transitions)
        self.assertTrue(hd.Flags['Hybrid FA - DFA part'])
        self.assertTrue(hd.Flags['Deterministic'])
        
        self.assertEqual(len(hyfa.nfas), 2)
        self.assertEqual({0:0, 1: 10}, hyfa.tran_aut)
        
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
        #self._test_search_4()

    def _test_search_1(self):
        """search()"""
        """
            Test with more regular expression where computed automaton
            has some NFA parts.
        """
        
        parser = pcre_parser()
        
        hyfa = JHybridFA()
        hyfa.load_file(aux_func.getPatternMatchDir() + "/algorithms/j_hybrid_fa/tests_data/test_search_1.re")
        hyfa.set_parser(parser)
      
        hyfa.compute()
        
        self.assertTrue(hyfa.get_compute())
        
        ret = hyfa.search("0123 uvwx")
        self.assertEqual(ret, [1,0,1,0])
        
        ret = hyfa.search("abcd abgggcd")
        self.assertEqual(ret, [0,1,0,1])
        
        ret = hyfa.search("aaaaa")
        self.assertEqual(ret, [0,0,0,0])

    def _test_search_2(self):
        """search()"""
        """
            Test with more regular expression where are not blow up REs.
        """
        
        parser = pcre_parser()
        
        hyfa = JHybridFA()
        hyfa.load_file(aux_func.getPatternMatchDir() + "/algorithms/j_hybrid_fa/tests_data/test_search_2.re")
        hyfa.set_parser(parser)

        hyfa.compute()
        
        self.assertTrue(hyfa.get_compute())
        
        ret = hyfa.search("0123")
        self.assertEqual(ret, [1,0,0,0])
        
        ret = hyfa.search("uvwx")
        self.assertEqual(ret, [0,0,1,0])

        ret = hyfa.search("abcd uvwx")
        self.assertEqual(ret, [0,1,1,0])
        
        ret = hyfa.search("cdefgh")
        self.assertEqual(ret, [0,0,0,0])

    def _test_search_3(self):
        """search()"""
        """
            Test with more REs where some have blow up patterns on his starts.
        """
        
        parser = pcre_parser()
        
        hyfa = JHybridFA()
        hyfa.load_file(aux_func.getPatternMatchDir() + "/algorithms/j_hybrid_fa/tests_data/test_search_3.re")
        hyfa.set_parser(parser)

        hyfa.compute()
        
        self.assertTrue(hyfa.get_compute())
        
        ret = hyfa.search("0123")
        self.assertEqual(ret, [1,0,0,0])
        
        ret = hyfa.search("uvwx")
        self.assertEqual(ret, [0,0,1,0])

        ret = hyfa.search("abcd uvwx")
        self.assertEqual(ret, [0,1,1,1])
        
        ret = hyfa.search("abcd agcd")
        self.assertEqual(ret, [0,1,0,1])
        
        ret = hyfa.search("cdefgh")
        self.assertEqual(ret, [0,0,0,0])
        
    def _test_search_4(self):
        """search()"""
        """
            Test with many regular expression where computed automaton
            has many NFA parts.
            Compares results of searching in computed Hybrid FA with
            regular NFA automaton searching.
        """
        parser = pcre_parser()
        parser.load_file(aux_func.getPatternMatchDir() + "/rules/Moduly/web-cgi.rules.pcre")

        nfa_aut = b_nfa()
        nfa_aut.create_by_parser(parser)
        nfa_aut.compute()
        
        parser = pcre_parser()
        
        hyfa = JHybridFA()
        hyfa.set_parser(parser)
        hyfa.load_file(aux_func.getPatternMatchDir() + "/rules/Moduly/web-cgi.rules.pcre")
        
        hyfa.compute()

        input_data = "/awstats.pl?---configdir=| /calendar-admin.pl /db4web_c.exe/aaaa:  /itemid=123f  /ShellExample.cgi?*"
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
        hyfa = JHybridFA()
        
        parser = pcre_parser()
        hyfa.set_parser(parser)
        hyfa.load_file(aux_func.getPatternMatchDir() + "/algorithms/j_hybrid_fa/tests_data/test_get_xxx_num_1.re")
        
        hyfa.compute()
        
        self.assertEqual(hyfa.get_state_num(), 21)

    def _test_get_state_num_2(self):
        """get_state_num()"""
        """
            Test with more regular expression where computed automaton
            has some NFA parts.
        """
        hyfa = JHybridFA()
        
        parser = pcre_parser()
        hyfa.set_parser(parser)
        hyfa.load_file(aux_func.getPatternMatchDir() + "/algorithms/j_hybrid_fa/tests_data/test_get_xxx_num_2.re")
        
        hyfa.compute()
        
        self.assertEqual(hyfa.get_state_num(), 23)

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
        hyfa = JHybridFA()
        
        parser = pcre_parser()
        hyfa.set_parser(parser)
        hyfa.load_file(aux_func.getPatternMatchDir() + "/algorithms/j_hybrid_fa/tests_data/test_get_xxx_num_1.re")
        
        hyfa.compute()
        
        self.assertEqual(hyfa.get_trans_num(), 102)

    def _test_get_trans_num_2(self):
        """get_trans_num()"""
        """
            Test with more regular expression where computed automaton
            has some NFA parts.
        """        
        hyfa = JHybridFA()
        
        parser = pcre_parser()
        hyfa.set_parser(parser)
        hyfa.load_file(aux_func.getPatternMatchDir() + "/algorithms/j_hybrid_fa/tests_data/test_get_xxx_num_2.re")
        
        hyfa.compute()

        self.assertEqual(hyfa.get_trans_num(), 67)

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
        hyfa = JHybridFA()
        
        parser = pcre_parser()
        hyfa.set_parser(parser)
        hyfa.load_file(aux_func.getPatternMatchDir() + "/algorithms/j_hybrid_fa/tests_data/test_get_xxx_num_1.re")
        
        hyfa.compute()
        
        self.assertEqual(hyfa.report_memory_optimal(), 102)

    def _test_report_memory_optimal_2(self):
        """report_memory_optimal()"""
        """
            Test with more regular expression where computed automaton
            has some NFA parts.
        """
        hyfa = JHybridFA()
        
        hyfa = JHybridFA()
        
        parser = pcre_parser()
        hyfa.set_parser(parser)
        hyfa.load_file(aux_func.getPatternMatchDir() + "/algorithms/j_hybrid_fa/tests_data/test_get_xxx_num_2.re")
        
        hyfa.compute()
        self.assertEqual(hyfa.report_memory_optimal(), 111)

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
        hyfa = JHybridFA()
        
        parser = pcre_parser()
        hyfa.set_parser(parser)
        hyfa.load_file(aux_func.getPatternMatchDir() + "/algorithms/j_hybrid_fa/tests_data/test_get_xxx_num_1.re")
        
        hyfa.compute()
        
        self.assertEqual(hyfa.report_memory_naive(), 630)

    def _test_report_memory_naive_2(self):
        """report_memory_naive()"""
        """
            Test with more regular expression where computed automaton
            has some NFA parts.
        """
        hyfa = JHybridFA()
        
        parser = pcre_parser()
        hyfa.set_parser(parser)
        hyfa.load_file(aux_func.getPatternMatchDir() + "/algorithms/j_hybrid_fa/tests_data/test_get_xxx_num_2.re")
        
        hyfa.compute()

        self.assertEqual(hyfa.report_memory_naive(), 390)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_JHybridFA)
    unittest.TextTestRunner(verbosity=2).run(suite)
