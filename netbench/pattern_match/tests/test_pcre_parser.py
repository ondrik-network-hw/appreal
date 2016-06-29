###############################################################################
#  test_pcre_parser.py: Module for PATTERN MATCH tests
#  Copyright (C) 2011 Brno University of Technology, ANT @ FIT
#  Author(s): Jaroslav Suchodol <xsucho04@stud.fit.vutbr.cz>
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
#  This software or firmware is provided ``as is'', and any express or implied
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

from netbench.pattern_match.b_automaton import b_Automaton
from netbench.pattern_match.pcre_parser import pcre_parser
from netbench.pattern_match.nfa_data import nfa_data
import unittest

class test_pcre_parser(unittest.TestCase):
    """Test class for parsing RE using new C pcre parser."""

    def test_get_nfa(self):
        """get_nfa()"""
        # If attribute _position < 0, check returning None.
        parser = pcre_parser()
        self.assertTrue(parser._position < 0)
        self.assertTrue(parser.get_nfa() == None)
            
        # Try method on a few regular expressions.
        # The results obtained compare with the manually completed machines.
        # (Recommend to compare after the elimination of epsilon transition)
        # 1) concatenation
        parser = pcre_parser()
        parser.set_text("/first/")
        automat = b_Automaton()
        automat._automaton = parser.get_nfa()
        automat.remove_epsilons()
        cp = automat.get_automaton()
        result = nfa_data().load_from_file("test_data/(1)pcre_get_nfa.nfa_data")

        self.assertTrue(sorted(cp.states.keys()) == sorted(result.states.keys()))
        self.assertTrue(cp.alphabet == result.alphabet)
        self.assertTrue(cp.start == result.start)
        self.assertTrue(cp.final == result.final)
        self.assertTrue(cp.transitions == result.transitions)
        self.assertTrue(cp.Flags == result.Flags)

        # 2) branch (automat create char class), iteration *
        parser = pcre_parser()
        parser.set_text("/[ab]cd*/")
        automat = b_Automaton()
        automat._automaton = parser.get_nfa()
        automat.remove_epsilons()
        cp = automat.get_automaton()
        result = nfa_data().load_from_file("test_data/(2)pcre_get_nfa.nfa_data")

        self.assertTrue(sorted(cp.states.keys()) == sorted(result.states.keys()))
        self.assertTrue(cp.alphabet == result.alphabet)
        self.assertTrue(cp.start == result.start)
        self.assertTrue(cp.final == result.final)
        self.assertTrue(cp.transitions == result.transitions)
        self.assertTrue(cp.Flags == result.Flags)

        # 3) try second RE (move to next line)
        parser = pcre_parser()
        parser.set_text("/abc/\n/ABC/\n")
        parser.next_line()
        automat = b_Automaton()
        automat._automaton = parser.get_nfa()
        automat.remove_epsilons()
        cp = automat.get_automaton()
        result = nfa_data().load_from_file("test_data/(3)pcre_get_nfa.nfa_data")

        self.assertTrue(sorted(cp.states.keys()) == sorted(result.states.keys()))
        self.assertTrue(cp.alphabet == result.alphabet)
        self.assertTrue(cp.start == result.start)
        self.assertTrue(cp.final == result.final)
        self.assertTrue(cp.transitions == result.transitions)
        self.assertTrue(cp.Flags == result.Flags)

        # 4) basic counting constratin
        parser = pcre_parser()
        parser.set_text("/ab{5}c/")
        automat = b_Automaton()
        automat._automaton = parser.get_nfa()
        automat.remove_epsilons()
        cp = automat.get_automaton()
        result = nfa_data().load_from_file("test_data/(4)pcre_get_nfa.nfa_data")

        self.assertTrue(sorted(cp.states.keys()) == sorted(result.states.keys()))
        self.assertTrue(cp.alphabet == result.alphabet)
        self.assertTrue(cp.start == result.start)
        self.assertTrue(cp.final == result.final)
        self.assertTrue(cp.transitions == result.transitions)
        self.assertTrue(cp.Flags == result.Flags)

        # 5) branch, iteration +, harder counting constraint
        parser = pcre_parser()
        parser.set_text("/a[bc]+d{2,3}/")
        automat = b_Automaton()
        automat._automaton = parser.get_nfa()
        automat.remove_epsilons()
        cp = automat.get_automaton()
        result = nfa_data().load_from_file("test_data/(5)pcre_get_nfa.nfa_data")

        self.assertTrue(sorted(cp.states.keys()) == sorted(result.states.keys()))
        self.assertTrue(cp.alphabet == result.alphabet)
        self.assertTrue(cp.start == result.start)
        self.assertTrue(cp.final == result.final)
        self.assertTrue(cp.transitions == result.transitions)
        self.assertTrue(cp.Flags == result.Flags)
        
        # 6) basic counting constratin, use param create_cnt_constr = True
        parser = pcre_parser(create_cnt_constr = True)
        parser.set_text("/ab{5}c/")
        automat = b_Automaton()
        automat._automaton = parser.get_nfa()
        automat.remove_epsilons()
        cp = automat.get_automaton()
        result = nfa_data().load_from_file("test_data/(6)pcre_get_nfa.nfa_data")
        
        self.assertTrue(sorted(cp.states.keys()) == sorted(result.states.keys()))
        self.assertTrue(cp.alphabet == result.alphabet)
        self.assertTrue(cp.start == result.start)
        self.assertTrue(cp.final == result.final)
        self.assertTrue(cp.transitions == result.transitions)
        self.assertTrue(cp.Flags == result.Flags)

        # 7) branch, iteration +, harder counting constraint, 
        #    use param create_cnt_constr = True
        parser = pcre_parser(create_cnt_constr = True)
        parser.set_text("/a[bc]+d{2,3}/")
        automat = b_Automaton()
        automat._automaton = parser.get_nfa()
        automat.remove_epsilons()
        cp = automat.get_automaton()
        result = nfa_data().load_from_file("test_data/(7)pcre_get_nfa.nfa_data")
        
        self.assertTrue(sorted(cp.states.keys()) == sorted(result.states.keys()))
        self.assertTrue(cp.alphabet == result.alphabet)
        self.assertTrue(cp.start == result.start)
        self.assertTrue(cp.final == result.final)
        self.assertTrue(cp.transitions == result.transitions)
        self.assertTrue(cp.Flags == result.Flags)
        
        # 8) concatenation, with create_eof_symbols = True, no $
        parser = pcre_parser(create_eof_symbols = True)
        parser.set_text("/first/")
        automat = b_Automaton()
        automat._automaton = parser.get_nfa()
        automat.remove_epsilons()
        cp = automat.get_automaton()
        result = nfa_data().load_from_file("test_data/(1)pcre_get_nfa.nfa_data")

        self.assertTrue(sorted(cp.states.keys()) == sorted(result.states.keys()))
        self.assertTrue(cp.alphabet == result.alphabet)
        self.assertTrue(cp.start == result.start)
        self.assertTrue(cp.final == result.final)
        self.assertTrue(cp.transitions == result.transitions)
        self.assertTrue(cp.Flags == result.Flags)
        
        # 9) concatenation, with create_eof_symbols = True, $
        parser = pcre_parser(create_eof_symbols = True)
        parser.set_text("/first$/")
        automat = b_Automaton()
        automat._automaton = parser.get_nfa()
        automat.remove_epsilons()
        cp = automat.get_automaton()
        result = nfa_data().load_from_file("test_data/(9)pcre_get_nfa.nfa_data")

        self.assertTrue(sorted(cp.states.keys()) == sorted(result.states.keys()))
        self.assertTrue(cp.alphabet == result.alphabet)
        self.assertTrue(cp.start == result.start)
        self.assertTrue(cp.final == result.final)
        self.assertTrue(cp.transitions == result.transitions)
        self.assertTrue(cp.Flags == result.Flags)
        
        # 10) branch, iteration +, harder counting constraint
        # create_eof_symbols = True, create_cnt_constr = True
        parser = pcre_parser(create_eof_symbols = True, create_cnt_constr = True)
        parser.set_text("/a[bc]+d{2,3}$/")
        automat = b_Automaton()
        automat._automaton = parser.get_nfa()
        automat.remove_epsilons()
        cp = automat.get_automaton()
        result = nfa_data().load_from_file("test_data/(10)pcre_get_nfa.nfa_data")

        self.assertTrue(sorted(cp.states.keys()) == sorted(result.states.keys()))
        self.assertTrue(cp.alphabet == result.alphabet)
        self.assertTrue(cp.start == result.start)
        self.assertTrue(cp.final == result.final)
        self.assertTrue(cp.transitions == result.transitions)
        self.assertTrue(cp.Flags == result.Flags)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_pcre_parser)
    unittest.TextTestRunner(verbosity=2).run(suite)
