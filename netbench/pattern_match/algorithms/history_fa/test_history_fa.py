###############################################################################
#  test_history_fa.py: Test module for class HistoryFA
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

from netbench.pattern_match.algorithms.history_fa.history_fa import HistoryFA
from netbench.pattern_match.parser import parser
from netbench.pattern_match.nfa_data import nfa_data
from netbench.pattern_match.b_state import b_State
from netbench.pattern_match.sym_char import b_Sym_char
from netbench.pattern_match.sym_char_class import b_Sym_char_class
from netbench.pattern_match import aux_func
import unittest, copy

class test_HistoryFA(unittest.TestCase):
    """
        Test module for class HistoryFA.
    """

    def test__discover_closure_states(self):
        """_discover_closure_states(NFA)"""
        act = nfa_data()
        act.states[0] = b_State(0,set())
        act.states[1] = b_State(1,set())
        act.states[2] = b_State(2,set())
        act.states[3] = b_State(3,set([0]))
        act.states[4] = b_State(4,set())
        act.states[5] = b_State(5,set())
        act.states[6] = b_State(6,set([1]))
        act.alphabet[0] = b_Sym_char("a", "a", 0)
        act.alphabet[1] = b_Sym_char("b", "b", 1)
        act.alphabet[2] = b_Sym_char("c", "c", 2)
        act.alphabet[3] = b_Sym_char("d", "d", 3)
        act.alphabet[4] = b_Sym_char("e", "e", 4)
        act.alphabet[5] = b_Sym_char("f", "f", 5)
        star = set()
        for ord_char in range(0, 256):
            star.add(chr(ord_char))
        act.alphabet[6] = b_Sym_char_class("*", star, 6)
        mimo_a = set()
        for ord_char in range(0, 256):
            mimo_a.add(chr(ord_char))
        mimo_a.remove('a')
        act.alphabet[7] = b_Sym_char_class("^a", mimo_a, 7)
        act.start = 0
        act.final.add(3)
        act.final.add(6)
        act.transitions.add( (0, 6, 0) )
        act.transitions.add( (0, 0, 1) )
        act.transitions.add( (1, 1, 2) )
        act.transitions.add( (2, 7, 2) )
        act.transitions.add( (2, 2, 3) )
        act.transitions.add( (0, 3, 4) )
        act.transitions.add( (4, 4, 5) )
        act.transitions.add( (5, 5, 6) )
        history = HistoryFA()
        history._automaton = act
        history.remove_epsilons()
        NFA = history.get_automaton(True)
        self.assertTrue(history._discover_closure_states(NFA) == [2])

    def test__identify_fading_states(self):
        """_identify_fading_states(nfa_closure_states)"""
        history = HistoryFA()
        history._state_representation = [ set([0]),
                                          set([0,1]),
                                          set([0,2]),
                                          set([0,3]),
                                          set([0,4]),
                                          set([0,5]),
                                          set([0,6]),
                                          set([0,2,4]),
                                          set([0,2,5]),
                                          set([0,2,6])
        ]
        self.assertTrue(history._identify_fading_states([2]) == [2, 7, 8, 9])

        act = nfa_data()
        act.states[0] = b_State(0,set())
        act.states[1] = b_State(1,set())
        act.states[2] = b_State(2,set())
        act.states[3] = b_State(3,set([0]))
        act.states[4] = b_State(4,set())
        act.states[5] = b_State(5,set())
        act.states[6] = b_State(6,set([1]))
        act.alphabet[0] = b_Sym_char("a", "a", 0)
        act.alphabet[1] = b_Sym_char("b", "b", 1)
        act.alphabet[2] = b_Sym_char("c", "c", 2)
        act.alphabet[3] = b_Sym_char("d", "d", 3)
        act.alphabet[4] = b_Sym_char("e", "e", 4)
        act.alphabet[5] = b_Sym_char("f", "f", 5)
        star = set()
        for ord_char in range(0, 256):
            star.add(chr(ord_char))
        act.alphabet[6] = b_Sym_char_class("*", star, 6)
        mimo_a = set()
        for ord_char in range(0, 256):
            mimo_a.add(chr(ord_char))
        mimo_a.remove('a')
        act.alphabet[7] = b_Sym_char_class("^a", mimo_a, 7)
        act.start = 0
        act.final.add(3)
        act.final.add(6)
        act.transitions.add( (0, 6, 0) )
        act.transitions.add( (0, 0, 1) )
        act.transitions.add( (1, 1, 2) )
        act.transitions.add( (2, 7, 2) )
        act.transitions.add( (2, 2, 3) )
        act.transitions.add( (0, 3, 4) )
        act.transitions.add( (4, 4, 5) )
        act.transitions.add( (5, 5, 6) )
        history = HistoryFA()
        history._automaton = act
        history.remove_epsilons()
        NFA = history.get_automaton(True)
        history.determinise(create_table = True)
        nfa_closure_states = history._discover_closure_states(NFA)
        self.assertTrue(history._identify_fading_states(nfa_closure_states) ==
            [5, 7, 8, 9])

    def test__remove_fading_dfa_states(self):
        """_remove_fading_dfa_states(dfa_fading_states)"""
        act = nfa_data()
        act.states[0] = b_State(0,set())
        act.states[1] = b_State(1,set())
        act.states[2] = b_State(2,set())
        act.states[3] = b_State(3,set([0]))
        act.states[4] = b_State(4,set())
        act.states[5] = b_State(5,set())
        act.states[6] = b_State(6,set([1]))
        act.alphabet[0] = b_Sym_char("a", "a", 0)
        act.alphabet[1] = b_Sym_char("b", "b", 1)
        act.alphabet[2] = b_Sym_char("c", "c", 2)
        act.alphabet[3] = b_Sym_char("d", "d", 3)
        act.alphabet[4] = b_Sym_char("e", "e", 4)
        act.alphabet[5] = b_Sym_char("f", "f", 5)
        star = set()
        for ord_char in range(0, 256):
            star.add(chr(ord_char))
        act.alphabet[6] = b_Sym_char_class("*", star, 6)
        mimo_a = set()
        for ord_char in range(0, 256):
            mimo_a.add(chr(ord_char))
        mimo_a.remove('a')
        act.alphabet[7] = b_Sym_char_class("^a", mimo_a, 7)
        act.start = 0
        act.final.add(3)
        act.final.add(6)
        act.transitions.add( (0, 6, 0) )
        act.transitions.add( (0, 0, 1) )
        act.transitions.add( (1, 1, 2) )
        act.transitions.add( (2, 7, 2) )
        act.transitions.add( (2, 2, 3) )
        act.transitions.add( (0, 3, 4) )
        act.transitions.add( (4, 4, 5) )
        act.transitions.add( (5, 5, 6) )

        history = HistoryFA()
        history._automaton = act
        history.remove_epsilons()
        NFA = history.get_automaton(True)
        history.determinise(create_table = True)
        nfa_closure_states = history._discover_closure_states(NFA)
        dfa_fading_states = history._identify_fading_states(nfa_closure_states)

        history._remove_fading_dfa_states(dfa_fading_states)
        self.assertTrue(sorted(history._automaton.states) == [0, 1, 2, 3, 4, 6])

    def test__pruning_process(self):
        """_pruning_process()"""
        act = nfa_data()
        act.states[0] = b_State(0,set())
        act.states[1] = b_State(1,set())
        act.states[2] = b_State(2,set())
        act.states[3] = b_State(3,set([0]))
        act.states[4] = b_State(4,set())
        act.states[5] = b_State(5,set())
        act.states[6] = b_State(6,set([1]))
        act.alphabet[0] = b_Sym_char("a", "a", 0)
        act.alphabet[1] = b_Sym_char("b", "b", 1)
        act.alphabet[2] = b_Sym_char("c", "c", 2)
        act.alphabet[3] = b_Sym_char("d", "d", 3)
        act.alphabet[4] = b_Sym_char("e", "e", 4)
        act.alphabet[5] = b_Sym_char("f", "f", 5)
        star = set()
        for ord_char in range(0, 256):
            star.add(chr(ord_char))
        act.alphabet[6] = b_Sym_char_class("*", star, 6)
        mimo_a = set()
        for ord_char in range(0, 256):
            mimo_a.add(chr(ord_char))
        mimo_a.remove('a')
        act.alphabet[7] = b_Sym_char_class("^a", mimo_a, 7)
        act.start = 0
        act.final.add(3)
        act.final.add(6)
        act.transitions.add( (0, 6, 0) )
        act.transitions.add( (0, 0, 1) )
        act.transitions.add( (1, 1, 2) )
        act.transitions.add( (2, 7, 2) )
        act.transitions.add( (2, 2, 3) )
        act.transitions.add( (0, 3, 4) )
        act.transitions.add( (4, 4, 5) )
        act.transitions.add( (5, 5, 6) )

        history = HistoryFA()
        history._automaton = act
        history.remove_epsilons()
        NFA = history.get_automaton(True)
        history.determinise(create_table = True)
        nfa_closure_states = history._discover_closure_states(NFA)
        dfa_fading_states = history._identify_fading_states(nfa_closure_states)
        history._remove_fading_dfa_states(dfa_fading_states)

        self.assertTrue(len(history._automaton.transitions) == 40)
        history._pruning_process()
        self.assertTrue(len(history._automaton.transitions) == 34)

    def test_compute(self):
        """compute()"""
        # Check the correctness of the logical machine output over
        # self.assertTrue on individual items + focus on the properties
        # of HistoryFA (transitions, flags, counters)

        # /abcd/; test with an expression that does not use properties
        # of HistoryFA
        par = parser("pcre_parser")
        par.set_text("/abcd/")
        history = HistoryFA()
        history.create_by_parser(par)
        history.remove_epsilons()
        NFA = history.get_automaton(True)
        history.determinise(create_table = True)
        history.compute(NFA)

        copy = history.get_automaton()
        result = nfa_data().load_from_file(aux_func.getPatternMatchDir() + "/algorithms/history_fa/test_data/test_data_1.nfa_data")

        self.assertTrue(sorted(copy.states.keys()) ==
            sorted(result.states.keys()))
        self.assertTrue(copy.alphabet == result.alphabet)
        self.assertTrue(copy.start == result.start)
        self.assertTrue(copy.final == result.final)
        self.assertTrue(copy.transitions == result.transitions)

        # /ab.*cd /; test with an expression that contains .*
        par = parser("pcre_parser")
        par.set_text("/ab.*cd/")
        history = HistoryFA()
        history.create_by_parser(par)
        history.remove_epsilons()
        NFA = history.get_automaton(True)
        history.determinise(create_table = True)
        history.compute(NFA)

        copy = history.get_automaton()
        result = nfa_data().load_from_file(aux_func.getPatternMatchDir() + "/algorithms/history_fa/test_data/test_data_2.nfa_data")

        self.assertTrue(sorted(copy.states.keys()) ==
            sorted(result.states.keys()))
        self.assertTrue(copy.alphabet == result.alphabet)
        self.assertTrue(copy.start == result.start)
        self.assertTrue(copy.final == result.final)
        self.assertTrue(copy.transitions == result.transitions)
        self.assertTrue(copy.Flags == result.Flags)

        # /ab[^1234]*cd|efg/; test with an expression containing one
        # alternation [^1234]*, the second is not
        par = parser("pcre_parser")
        par.set_text("/ab[^1234]*cd|efg/")
        history = HistoryFA()
        history.create_by_parser(par)
        history.remove_epsilons()
        NFA = history.get_automaton(True)
        history.determinise(create_table = True)
        history.compute(NFA)

        copy = history.get_automaton()
        result = nfa_data().load_from_file(aux_func.getPatternMatchDir() + "/algorithms/history_fa/test_data/test_data_3.nfa_data")

        self.assertTrue(sorted(copy.states.keys()) ==
            sorted(result.states.keys()))
        self.assertTrue(copy.alphabet == result.alphabet)
        self.assertTrue(copy.start == result.start)
        self.assertTrue(copy.final == result.final)
        self.assertTrue(copy.transitions == result.transitions)
        self.assertTrue(copy.Flags == result.Flags)

    def test_search(self):
        """search()"""
        # For RE upstairs do tests for this method.

        # /abcd/; test with an expression that does not use properties
        # of HistoryFA
        par = parser("pcre_parser")
        par.set_text("/abcd/")
        history = HistoryFA()
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
 
        # /ab.*cd /; test with an expression that contains .*
        par = parser("pcre_parser")
        par.set_text("/ab.*cd/")
        history = HistoryFA()
        history.create_by_parser(par)
        history.remove_epsilons()
        NFA = history.get_automaton(True)
        history.determinise(create_table = True)
        history.compute(NFA)

        self.assertTrue(history.search("efg") == [0])
        self.assertTrue(history.search("abnecoefg") == [0])
        self.assertTrue(history.search("abnecocx") == [0])
        self.assertTrue(history.search("necoabnecocdneco") == [1])
        self.assertTrue(history.search("abcd") == [1])
        self.assertTrue(history.search("123abcd456") == [1])
        self.assertTrue(history.search("123ab0cd456") == [1])
 
        # /ab[^1234]*cd|efg/; test with an expression containing one
        # alternation [^1234]*, the second is not
        par = parser("pcre_parser")
        par.set_text("/ab[^1234]*cd|efg/")
        history = HistoryFA()
        history.create_by_parser(par)
        history.remove_epsilons()
        NFA = history.get_automaton(True)
        history.determinise(create_table = True)
        history.compute(NFA)

        self.assertTrue(history.search("exfg") == [0])
        self.assertTrue(history.search("abnecocx") == [0])

        self.assertTrue(history.search("efg") == [1])
        self.assertTrue(history.search("textefgtext") == [1])
        self.assertTrue(history.search("abnecoefg") == [1])

        self.assertTrue(history.search("necoabnecocdneco") == [1])
        self.assertTrue(history.search("abcd") == [1])
        self.assertTrue(history.search("123abcd456") == [1])
        self.assertTrue(history.search("123ab0cd456") == [1])
 
        self.assertTrue(history.search("ab1cd") == [0])
        self.assertTrue(history.search("ab4cd") == [0])
        self.assertTrue(history.search("abcefg") == [1])
        self.assertTrue(history.search("123abblekekcd456") == [1])
        self.assertTrue(history.search("123ab0cd456") == [1])

    def test_report_memory_optimal(self):
        """report_memory_optimal()"""

        # /ab[^1234]*cd|efg/; test with an expression containing one
        # alternation [^1234]*, the second is not
        par = parser("pcre_parser")
        par.set_text("/ab[^1234]*cd|efg/")
        history = HistoryFA()
        history.create_by_parser(par)
        history.remove_epsilons()
        NFA = history.get_automaton(True)
        history.determinise(create_table = True)
        history.compute(NFA)

        self.assertTrue(history.report_memory_optimal() == 74)

    def test_report_memory_naive(self):
        """report_memory_naive()"""

        # /ab[^1234]*cd|efg/; test with an expression containing one
        # alternation [^1234]*, the second is not
        par = parser("pcre_parser")
        par.set_text("/ab[^1234]*cd|efg/")
        history = HistoryFA()
        history.create_by_parser(par)
        history.remove_epsilons()
        NFA = history.get_automaton(True)
        history.determinise(create_table = True)
        history.compute(NFA)

        self.assertTrue(history.report_memory_naive() == 187)
 
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_HistoryFA)
    unittest.TextTestRunner(verbosity=2).run(suite)
