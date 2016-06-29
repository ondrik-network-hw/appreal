###############################################################################
#  test_phf_dfa.py: Test module for class PHF_DFA.
#  Copyright (C) 2010 Brno University of Technology, ANT @ FIT
#  Author(s): Jan Kastil <ikastil@fit.vutbr.cz>
#             Milan Dvorak <xdvora66@stud.fit.vutbr.cz>
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

import unittest
import copy
import sys
import os
from netbench.pattern_match.algorithms.phf_dfa.phf_dfa import PHF_DFA
from netbench.pattern_match.bin.library.bdz import bdz
from netbench.pattern_match.bin.library.jenkins import jenkins_compress
from netbench.pattern_match.pcre_parser import pcre_parser
from netbench.pattern_match.nfa_data import nfa_data
from netbench.pattern_match.b_state import b_State
from netbench.pattern_match.sym_char import b_Sym_char
from netbench.pattern_match.sym_char_class import b_Sym_char_class
from netbench.pattern_match.sym_kchar import b_Sym_kchar


class test_PHF_DFA(unittest.TestCase):
    """This class tests implementation of the algorithm PHF_DFA."""
    def test___init__(self):
        """__init__()"""
        # Create PHF_DFA and check the values of internal variables.
        aut = PHF_DFA()
        self.assertFalse(aut.get_compute())
        self.assertEqual(aut._automaton, aut._automaton1)
        self.assertEqual(aut.state_bits, 10)
        self.assertEqual(aut.symbol_bits, 12)
        self.assertEqual(aut.hash_function, None)
        self.assertEqual(aut.trans_table, None)
        self.assertEqual(aut.ran, 0)
        self.assertFalse(aut.fallback)
        self.assertEqual(aut.fallback_state, -1)
        self.assertFalse(aut.faulty)
        self.assertEqual(aut.compress_hash, None)
        self.assertEqual(aut.compress_bits, 0)
        self.assertEqual(aut.bad_transitions, 0)
        self.assertEqual(aut.collisions, dict())

    def test_get_table_parameters(self):
        """get_table_parameters"""
        # Manually set state_bits and symbol_bits, then check if
        # if get_table_parameters returns same values
        aut = PHF_DFA()
        aut.state_bits = 24
        aut.symbol_bits = 20
        tmp = aut.get_table_parameters()
        self.assertEqual(tmp[0], 24)
        self.assertEqual(tmp[1], 20)

    def test_set_table_parameters(self):
        """set_table_parameters()"""
        # Set parameters using method set_table_parameters, then check if
        # internal variables have the same values
        aut = PHF_DFA()
        aut._compute = True
        tmp = (24, 20)
        aut.set_table_parameters(tmp)
        self.assertEqual(aut.state_bits, 24)
        self.assertEqual(aut.symbol_bits, 20)
        self.assertFalse(aut.get_compute())

    def test_set_PHF_class(self):
        """set_PHF_class()"""
        # Create phf class and assing it to PHF_DFA using method set_PHF_class.
        # Check if the variable hash_function was set and _compute is false.
        aut = PHF_DFA()
        aut._compute = True
        a = bdz()
        a.set_limit(1024)
        a.set_iteration_limit(8)
        aut.set_PHF_class(a)
        self.assertEqual(aut.hash_function, a)
        self.assertFalse(aut.get_compute())

    def test_enable_faulty_transitions(self):
        """enable_faulty_transitions()"""
        # Check if variables compress_bits, compress_hash, faulty and _compute
        # were set appropriately after calling enable_faulty_transitions.
        aut = PHF_DFA()
        aut._compute = True
        aut.enable_faulty_transitions(13)
        self.assertEqual(aut.compress_bits, 13)
        self.assertNotEqual(aut.compress_hash, None)
        self.assertFalse(aut.get_compute())
        self.assertTrue(aut.faulty)

        # Check if user created compress_hash was used
        aut = PHF_DFA()
        a = jenkins_compress(4)
        a.generate_seed()
        aut.enable_faulty_transitions(4, compress_hash = a)
        self.assertEqual(aut.compress_bits, 4)
        self.assertEqual(aut.compress_hash, a)
        self.assertFalse(aut.get_compute())
        self.assertTrue(aut.faulty)

        # Check if the hash output size is really 4 bits for few inputs
        for i in range(0, 255):
            val = aut.compress_hash.hash(([chr(i)],[chr(0)]))
            self.assertTrue(val < 16 and val >= 0)

    def test_disable_faulty_transitions(self):
        """disable_faulty_transitions()"""
        # Check if variables compress_bits, compress_hash, faulty and _compute
        # were set to their default values after calling method
        # disable_faulty_transitions
        aut = PHF_DFA()
        aut.enable_faulty_transitions(13)
        aut._compute = True
        aut.disable_faulty_transitions()
        self.assertEqual(aut.compress_bits, 13)
        self.assertNotEqual(aut.compress_hash, None)
        self.assertFalse(aut.get_compute())
        self.assertFalse(aut.faulty)
        

    def test_decode_symbol(self):
        """decode_symbol()"""
        # Test if different types of symbols are decoded correctly and
        # the symbol was removed from the beginning of input string.
        aut = PHF_DFA()
        aut._automaton.alphabet[0] = b_Sym_char_class("ch0", set(['a', 'b']), 0)
        aut._automaton.alphabet[1] = b_Sym_char_class("ch1", set(['c', 'd']), 1)
        aut._automaton.alphabet[2] = b_Sym_char_class("ch2", set(['e', 'f']), 2)
        aut._automaton.alphabet[3] = b_Sym_char("ch3", "g", 3)
        aut._automaton.alphabet[4] = b_Sym_kchar("ch4", (frozenset(['1', '2']), frozenset(['1', '2'])), 4)
        self.assertEqual(aut.decode_symbol("abeg112"), ("beg112", 0))
        self.assertEqual(aut.decode_symbol("beg112"), ("eg112", 0))
        self.assertEqual(aut.decode_symbol("eg112"), ("g112", 2))
        self.assertEqual(aut.decode_symbol("g112"), ("112", 3))
        self.assertEqual(aut.decode_symbol("112"), ("2", 4))
        # Nonexistent symbol is removed from the string and -1 is returned
        self.assertEqual(aut.decode_symbol("2"), ("", -1))

    def test_compute(self):
        """compute()"""
        # 1. /^abc/ - automaton does not change, PHF table is created
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (2,2,3) )
        nfaData.final.add(3)

        result = copy.deepcopy(nfaData)

        aut = PHF_DFA()
        a = bdz()
        a.set_limit(128)
        aut.set_PHF_class(a)
        aut.create_from_nfa_data(nfaData)
        aut.compute()
        cp = aut._automaton1

        self.assertEqual(len(cp.states), len(result.states))
        self.assertEqual(len(cp.alphabet), len(result.alphabet))
        self.assertEqual(len(cp.transitions), len(result.transitions))
        self.assertEqual(len(cp.final), len(result.final))
        self.assertNotEqual(aut.trans_table, None)
        self.assertTrue(aut.get_compute())

        # 2. determinization of /^ab|ac/, PHF table is created
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set([0]))
        nfaData.states[3] = b_State(3,set())
        nfaData.states[4] = b_State(4,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (0,0,3) )
        nfaData.transitions.add( (3,2,4) )
        nfaData.final.add(2)
        nfaData.final.add(4)

        aut = PHF_DFA()
        a = bdz()
        a.set_limit(128)
        aut.set_PHF_class(a)
        aut.create_from_nfa_data(nfaData)
        aut.compute()
        cp = aut._automaton1

        self.assertEqual(len(cp.states), 3)
        self.assertEqual(len(cp.alphabet), 3)
        self.assertEqual(len(cp.transitions), 3)
        self.assertEqual(len(cp.final), 1)
        self.assertNotEqual(aut.trans_table, None)
        self.assertTrue(aut.get_compute())
        
        # 3. resolve alphabet - /^[a-c][b-d]/, PHF table is created
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set([0]))
        nfaData.alphabet[0] = b_Sym_char_class("ch0", set(['a', 'b', 'c']), 0)
        nfaData.alphabet[1] = b_Sym_char_class("ch1", set(['b', 'c', 'd']), 1)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.final.add(2)

        aut = PHF_DFA()
        a = bdz()
        a.set_limit(128)
        aut.set_PHF_class(a)
        aut.create_from_nfa_data(nfaData)
        aut.compute()
        cp = aut._automaton1
        
        self.assertEqual(len(cp.states), 3)
        self.assertEqual(len(cp.alphabet), 3)
        self.assertEqual(len(cp.transitions), 4)
        self.assertEqual(len(cp.final), 1)
        self.assertNotEqual(aut.trans_table, None)
        self.assertTrue(aut.get_compute())

        # 4. /abc/ and enable_fallback_state - some transitions are removed
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (0,1,0) )
        nfaData.transitions.add( (0,2,0) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (1,0,1) )
        nfaData.transitions.add( (1,2,0) )
        nfaData.transitions.add( (2,2,3) )
        nfaData.transitions.add( (2,0,1) )
        nfaData.transitions.add( (2,1,0) )
        nfaData.transitions.add( (3,0,3) )
        nfaData.transitions.add( (3,1,3) )
        nfaData.transitions.add( (3,2,3) )
        nfaData.final.add(3)

        result = copy.deepcopy(nfaData)

        aut = PHF_DFA()
        a = bdz()
        a.set_limit(128)
        aut.set_PHF_class(a)
        aut.create_from_nfa_data(nfaData)
        aut.enable_fallback_state(warning=False)
        aut.compute()
        cp = aut._automaton1

        self.assertEqual(len(cp.states), len(result.states))
        self.assertEqual(len(cp.alphabet), len(result.alphabet))
        self.assertTrue(len(cp.transitions) < len(result.transitions))
        self.assertEqual(len(cp.final), len(result.final))
        self.assertNotEqual(aut.trans_table, None)
        self.assertTrue(aut.get_compute())

    def test_report_memory_real(self):
        """report_memory_real()"""
        # Few simple regression tests for different sizes of PHF table, state
        # and symbol representations and faulty transitions.
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (2,2,3) )
        nfaData.final.add(3)

        aut = PHF_DFA()
        a = bdz()
        a.set_limit(8)
        aut.set_PHF_class(a)
        aut.create_from_nfa_data(nfaData)
        aut.compute()
        self.assertEqual(aut.report_memory_real(), 120)

        aut.set_table_parameters((4,6))        
        self.assertEqual(aut.report_memory_real(), 48)

        aut.set_table_parameters((4,7))
        self.assertEqual(aut.report_memory_real(), 72)

        a.set_limit(5)
        aut.set_PHF_class(a)
        aut.compute()
        self.assertEqual(aut.report_memory_real(), 45)

        aut.enable_faulty_transitions(10)
        self.assertEqual(aut.report_memory_real(), 30)
        
        aut.enable_faulty_transitions(19)
        self.assertEqual(aut.report_memory_real(), 60)
        
    def test_report_memory_optimal(self):
        """report_memory_optimal()"""
        # Simple regression test for small automaton.
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (2,2,3) )
        nfaData.final.add(3)

        aut = PHF_DFA()
        a = bdz()
        a.set_limit(128)
        aut.set_PHF_class(a)
        aut.create_from_nfa_data(nfaData)
        aut.compute()
        self.assertEqual(aut.report_memory_optimal(), 3)

        # Test after removing fallback transitions
        aut.enable_fallback_state(1, warning=False)
        aut.remove_fallback_transitions()
        self.assertEqual(aut.report_memory_optimal(), 2)
        
    def test_report_memory_naive(self):
        """report_memory_naive()"""
        # Simple regression test for small automaton.
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (2,2,3) )
        nfaData.final.add(3)

        aut = PHF_DFA()
        a = bdz()
        a.set_limit(128)
        aut.set_PHF_class(a)
        aut.create_from_nfa_data(nfaData)
        aut.compute()
        self.assertEqual(aut.report_memory_naive(), 12)
        
        # Test after removing fallback transitions. report_memory_naive depends
        # on number of states and symbols, not transitions, so nothing changes
        aut.enable_fallback_state(1, warning=False)
        aut.remove_fallback_transitions()
        self.assertEqual(aut.report_memory_naive(), 12)

        # Manually remove symbol and state from _automaton1
        del aut._automaton1.states[2]
        del aut._automaton1.alphabet[2]
        self.assertEqual(aut.report_memory_naive(), 6)

    def test_get_state_num(self):
        """get_state_num()"""
        # Simple regression test for small automaton.
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (2,2,3) )
        nfaData.final.add(3)

        aut = PHF_DFA()
        a = bdz()
        a.set_limit(128)
        aut.set_PHF_class(a)
        aut.create_from_nfa_data(nfaData)
        aut.compute()
        self.assertEqual(aut.get_state_num(), 4)
       
        # Manually remove one state from _automaton1
        del aut._automaton1.states[2]
        self.assertEqual(aut.get_state_num(), 3)

    def test_get_trans_num(self):
        """get_trans_num()"""
        # Simple regression test for small automaton.
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (2,2,3) )
        nfaData.final.add(3)

        aut = PHF_DFA()
        a = bdz()
        a.set_limit(128)
        aut.set_PHF_class(a)
        aut.create_from_nfa_data(nfaData)
        aut.compute()
        self.assertEqual(aut.get_trans_num(), 3)
        
        # Test after removing fallback transitions
        aut.enable_fallback_state(1, warning=False)
        aut.remove_fallback_transitions() 
        self.assertEqual(aut.get_trans_num(), 2)

    def test_get_alpha_num(self):
        """get_alpha_num()"""
        # Simple regression test for small automaton.
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (2,2,3) )
        nfaData.final.add(3)

        aut = PHF_DFA()
        a = bdz()
        a.set_limit(128)
        aut.set_PHF_class(a)
        aut.create_from_nfa_data(nfaData)
        aut.compute()
        self.assertEqual(aut.get_alpha_num(), 3)
        
        # Manually remove symbol from _automaton1
        del aut._automaton1.alphabet[2]
        self.assertEqual(aut.get_alpha_num(), 2)

    def test_enable_fallback_state(self):
        """enable_fallback_state()"""
        # Test if fallback and fallback_state is set accordingly, _compute is
        # set to False and warning is/is not printed on stdout depending on
        # value of parameter warning.
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (2,2,3) )
        nfaData.final.add(3)

        aut = PHF_DFA()
        a = bdz()
        a.set_limit(128)
        aut.set_PHF_class(a)
        aut.create_from_nfa_data(nfaData)
        aut.compute()

        # redirect stdout to file
        tmp = sys.stdout
        f = open("stdout.output", 'w')
        sys.stdout = f
        
        aut.enable_fallback_state(2, warning=False)
        f.close()
        e = open("stdout.output", 'r')
        line = e.readline()
        # warning was set to False, stdout should be empty
        self.assertFalse(line)
        # check if the fallback_state was set
        self.assertEqual(aut.fallback_state, 2)
        self.assertFalse(aut.get_compute())
        self.assertTrue(aut.fallback)

        f = open("stdout.output", 'w')
        sys.stdout = f
        aut.enable_fallback_state()
        f.close()
        e = open("stdout.output", 'r')
        line = e.readline()
        # warning should be printed by default
        self.assertTrue(line)
        # check if the fallback_state was chosen correctly
        self.assertEqual(aut.fallback_state, 1)
        self.assertFalse(aut.get_compute())
        self.assertTrue(aut.fallback)
        # restore sys.stdout
        sys.stdout = tmp
        os.remove("stdout.output")

    def test_disable_fallback_state(self):
        """disable_fallback_state()"""
        # Test if the variables _compute, fallback and fallback_state were set
        # to the default values.
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (2,2,3) )
        nfaData.final.add(3)

        aut = PHF_DFA()
        a = bdz()
        a.set_limit(128)
        aut.set_PHF_class(a)
        aut.create_from_nfa_data(nfaData)
        aut.enable_fallback_state(warning=False)
        aut.compute()

        aut.disable_fallback_state()
        self.assertFalse(aut.get_compute())
        self.assertFalse(aut.fallback)
        self.assertEqual(aut.fallback_state, -1)

    def test_remove_fallback_transitions(self):
        """remove_fallback_transitions()"""
        # 1. /abc/, state -1 (automatically chosen 0) - 4 transitions removed
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (0,1,0) )
        nfaData.transitions.add( (0,2,0) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (1,0,1) )
        nfaData.transitions.add( (1,2,0) )
        nfaData.transitions.add( (2,2,3) )
        nfaData.transitions.add( (2,0,1) )
        nfaData.transitions.add( (2,1,0) )
        nfaData.transitions.add( (3,0,3) )
        nfaData.transitions.add( (3,1,3) )
        nfaData.transitions.add( (3,2,3) )
        nfaData.final.add(3)

        result = copy.deepcopy(nfaData)

        aut = PHF_DFA()
        a = bdz()
        a.set_limit(128)
        aut.set_PHF_class(a)
        aut.create_from_nfa_data(nfaData)
        aut.enable_fallback_state(warning=False)
        aut.compute()
        cp = aut._automaton1

        self.assertEqual(len(cp.states), len(result.states))
        self.assertEqual(len(cp.alphabet), len(result.alphabet))
        self.assertEqual(len(cp.transitions), 8) # 4 removed transitions
        for i in cp.transitions: # no transitions to fallback_state
            self.assertNotEqual(i[2], aut.fallback_state)
        self.assertEqual(len(cp.final), len(result.final))

        # 2. /abc/, state 1 - 3 transitions removed
        aut._automaton1 = aut._automaton
        aut.enable_fallback_state(1, False)
        aut.compute()
        cp = aut._automaton1

        self.assertEqual(len(cp.states), len(result.states))
        self.assertEqual(len(cp.alphabet), len(result.alphabet))
        self.assertEqual(len(cp.transitions), 9) # 3 removed transitions
        for i in cp.transitions: # no transitions to fallback_state
            self.assertNotEqual(i[2], aut.fallback_state)
        self.assertEqual(len(cp.final), len(result.final))
        
        # 3. /^abc/, state 0 - automaton does not change
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (2,2,3) )
        nfaData.final.add(3)

        result = copy.deepcopy(nfaData)

        aut = PHF_DFA()
        a = bdz()
        a.set_limit(128)
        aut.set_PHF_class(a)
        aut.create_from_nfa_data(nfaData)
        aut.enable_fallback_state(0, warning=False)
        aut.compute()
        cp = aut._automaton1

        self.assertEqual(len(cp.states), len(result.states))
        self.assertEqual(len(cp.alphabet), len(result.alphabet))
        self.assertEqual(len(cp.transitions), len(result.transitions))
        for i in cp.transitions: # no transitions to fallback_state
            self.assertNotEqual(i[2], aut.fallback_state)
        self.assertEqual(len(cp.final), len(result.final))

    def test_validate_transition(self):
        """validate_transition()"""
        # Test correct transition validation for both faulty and non-faulty
        # transition table.
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (2,2,3) )
        nfaData.final.add(3)

        aut = PHF_DFA()
        a = bdz()
        a.set_limit(128)
        aut.set_PHF_class(a)
        aut.create_from_nfa_data(nfaData)
        aut.compute()

        for t in aut._automaton1.transitions: # all transitions must be valid
            self.assertTrue(aut.validate_transition(aut._transition_rep(t)))
        # some nonexistent transitions -> invalid
        t = (0,2,0)
        self.assertFalse(aut.validate_transition(aut._transition_rep(t)))
        t = (1,0,2)
        self.assertFalse(aut.validate_transition(aut._transition_rep(t)))
        t = (len(aut._automaton1.states), len(aut._automaton1.alphabet), 0)
        self.assertFalse(aut.validate_transition(aut._transition_rep(t)))
        t = (0, len(aut._automaton1.alphabet), 0)
        self.assertFalse(aut.validate_transition(aut._transition_rep(t)))
        t = (len(aut._automaton1.states), 0, 0)
        self.assertFalse(aut.validate_transition(aut._transition_rep(t)))
        # faulty transitions
        aut.enable_faulty_transitions(32)
        aut.compute()
        for t in aut._automaton1.transitions: # all transitions must be valid
            self.assertTrue(aut.validate_transition(aut._transition_rep(t)))
        # some nonexistent transitions -> invalid, collisions are improbable
        t = (0,2,0)
        self.assertFalse(aut.validate_transition(aut._transition_rep(t)))
        t = (1,0,2)
        self.assertFalse(aut.validate_transition(aut._transition_rep(t)))
        t = (10,10,1)
        self.assertFalse(aut.validate_transition(aut._transition_rep(t)))
        t = (11,11,1)
        self.assertFalse(aut.validate_transition(aut._transition_rep(t)))
        t = (12,12,1)
        self.assertFalse(aut.validate_transition(aut._transition_rep(t)))

    def test_generate_PHF_table(self):
        """generate_PHF_table()"""
        # Test of PHF table generation - the right size of tabel, every
        # transition is exactly once in the table and on the right index.
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (0,1,0) )
        nfaData.transitions.add( (0,2,0) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (1,0,1) )
        nfaData.transitions.add( (1,2,0) )
        nfaData.transitions.add( (2,2,3) )
        nfaData.transitions.add( (2,0,1) )
        nfaData.transitions.add( (2,1,0) )
        nfaData.transitions.add( (3,0,3) )
        nfaData.transitions.add( (3,1,3) )
        nfaData.transitions.add( (3,2,3) )
        nfaData.final.add(3)

        aut = PHF_DFA()
        a = bdz()
        a.set_limit(128)
        aut.set_PHF_class(a)
        aut._automaton1 =  nfaData
        aut.generate_PHF_table()
        # transition table size
        self.assertEqual(aut.ran, len(aut.trans_table))
        self.assertEqual(aut.ran, 384)
        # count number of unique lines in transition table
        tranCount = dict()
        for l in aut.trans_table:
            tranCount.setdefault(l[1], 0)
            tranCount[l[1]] += 1
        # test if every automaton transition is just once in the table
        for t in aut._automaton1.transitions:
            self.assertEqual(tranCount[aut._transition_rep(t)], 1)
        t = ([2 ** aut.state_bits - 1, 2 ** aut.symbol_bits - 1, 0])
        # rest of trans are the nonexistent transitions
        self.assertEqual(tranCount[aut._transition_rep(t)], aut.ran - len(aut._automaton1.transitions))
        # check if each transition is on its index returned by hash function
        for t in aut._automaton1.transitions:
            rep = aut._transition_rep(t)
            self.assertEqual(rep, aut.trans_table[aut.hash_function.hash(rep)][1])
        # test the representation in faulty table
        aut.enable_faulty_transitions(8)
        aut.generate_PHF_table()
        for t in aut._automaton1.transitions:
            rep = aut._transition_rep(t)
            self.assertEqual(aut.compress_hash.hash(rep), aut.trans_table[aut.hash_function.hash(rep)][3])

        # change the size of PHF table and repeat tests
        aut = PHF_DFA()
        a = bdz()
        a.set_ratio(6.0)
        a.set_iteration_limit(10)
        aut.set_PHF_class(a)
        aut._automaton1 = nfaData
        aut.generate_PHF_table()
        # transition table size
        self.assertEqual(aut.ran, len(aut.trans_table))
        self.assertEqual(aut.ran, 72)
        # count number of unique lines in transition table
        tranCount = dict()
        for l in aut.trans_table:
            tranCount.setdefault(l[1], 0)
            tranCount[l[1]] += 1
        # test if every automaton transition is just once in the table
        for t in aut._automaton1.transitions:
            self.assertEqual(tranCount[aut._transition_rep(t)], 1)
        t = ([2 ** aut.state_bits - 1, 2 ** aut.symbol_bits - 1, 0])
        # rest of trans are the nonexistent transitions
        self.assertEqual(tranCount[aut._transition_rep(t)], aut.ran - len(aut._automaton1.transitions))
        # check if each transition is on its index returned by hash function
        for t in aut._automaton1.transitions:
            rep = aut._transition_rep(t)
            self.assertEqual(rep, aut.trans_table[aut.hash_function.hash(rep)][1])
        # test the representation in faulty table
        aut.enable_faulty_transitions(8)
        aut.generate_PHF_table()
        for t in aut._automaton1.transitions:
            rep = aut._transition_rep(t)
            self.assertEqual(aut.compress_hash.hash(rep), aut.trans_table[aut.hash_function.hash(rep)][3])

        # RE /#include.*>/ and enable fallback_state
        par = pcre_parser()
        par.set_text("/#include.*>/s")
        aut = PHF_DFA()
        a = bdz()
        a.set_ratio(2.5)
        a.set_iteration_limit(10)
        aut.set_PHF_class(a)
        aut.create_by_parser(par)
        aut.enable_fallback_state(warning=False)
        aut.compute()
        # transition table size
        self.assertEqual(aut.ran, len(aut.trans_table))
        self.assertEqual(aut.ran, 90)
        # count number of unique lines in transition table
        tranCount = dict()
        for l in aut.trans_table:
            tranCount.setdefault(l[1], 0)
            tranCount[l[1]] += 1
        # test if every automaton transition is just once in the table
        for t in aut._automaton1.transitions:
            self.assertEqual(tranCount[aut._transition_rep(t)], 1)
        t = ([2 ** aut.state_bits - 1, 2 ** aut.symbol_bits - 1, 0])
        # rest of trans are the nonexistent transitions
        self.assertEqual(tranCount[aut._transition_rep(t)], aut.ran - len(aut._automaton1.transitions))
        # check if each transition is on its index returned by hash function
        for t in aut._automaton1.transitions:
            rep = aut._transition_rep(t)
            self.assertEqual(rep, aut.trans_table[aut.hash_function.hash(rep)][1])
        # test the representation in faulty table
        aut.enable_faulty_transitions(8)
        aut.generate_PHF_table()
        for t in aut._automaton1.transitions:
            rep = aut._transition_rep(t)
            self.assertEqual(aut.compress_hash.hash(rep), aut.trans_table[aut.hash_function.hash(rep)][3])
        # disable fallback_state
        aut.disable_fallback_state()
        aut.compute()
        self.assertEqual(aut.ran, len(aut.trans_table))
        self.assertEqual(aut.ran, 252)
        # count number of unique lines in transition table
        tranCount = dict()
        for l in aut.trans_table:
            tranCount.setdefault(l[1], 0)
            tranCount[l[1]] += 1
        # test if every automaton transition is just once in the table
        for t in aut._automaton1.transitions:
            self.assertEqual(tranCount[aut._transition_rep(t)], 1)
        t = ([2 ** aut.state_bits - 1, 2 ** aut.symbol_bits - 1, 0])
        # rest of trans are the nonexistent transitions
        self.assertEqual(tranCount[aut._transition_rep(t)], aut.ran - len(aut._automaton1.transitions))
        # check if each transition is on its index returned by hash function
        for t in aut._automaton1.transitions:
            rep = aut._transition_rep(t)
            self.assertEqual(rep, aut.trans_table[aut.hash_function.hash(rep)][1])
        # test the representation in faulty table
        aut.enable_faulty_transitions(8)
        aut.generate_PHF_table()
        for t in aut._automaton1.transitions:
            rep = aut._transition_rep(t)
            self.assertEqual(aut.compress_hash.hash(rep), aut.trans_table[aut.hash_function.hash(rep)][3])

    def test_search(self):
        """search()"""
        # 1. RE /^abc/
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (2,2,3) )
        nfaData.final.add(3)

        aut = PHF_DFA()
        a = bdz()
        a.set_limit(128)
        aut.set_PHF_class(a)
        aut.create_from_nfa_data(nfaData)
        aut.compute()

        self.assertEqual(aut.search("abc"), [1])
        self.assertEqual(aut.search("aaaaaaaaaaaaaabc"), [0])
        self.assertEqual(aut.search("ccccbbbabc"), [0])
        self.assertEqual(aut.search("ababc"), [0])
        self.assertEqual(aut.search("d"), [0])
        self.assertEqual(aut.search("cbabbacba"), [0])

        # 2. RE /abc/
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (0,1,0) )
        nfaData.transitions.add( (0,2,0) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (1,0,1) )
        nfaData.transitions.add( (1,2,0) )
        nfaData.transitions.add( (2,2,3) )
        nfaData.transitions.add( (2,0,1) )
        nfaData.transitions.add( (2,1,0) )
        nfaData.transitions.add( (3,0,3) )
        nfaData.transitions.add( (3,1,3) )
        nfaData.transitions.add( (3,2,3) )
        nfaData.final.add(3)

        aut = PHF_DFA()
        a = bdz()
        a.set_limit(128)
        aut.set_PHF_class(a)
        aut.create_from_nfa_data(nfaData)
        aut.compute()

        self.assertEqual(aut.search("abc"), [1])
        self.assertEqual(aut.search("aaaaaaaaaaaaaabc"), [1])
        self.assertEqual(aut.search("ccccbbbabc"), [1])
        self.assertEqual(aut.search("ababc"), [1])
        self.assertEqual(aut.search("d"), [0])
        self.assertEqual(aut.search("cbabbacba"), [0])

        # 2a. same test with faulty transitions
        aut.enable_faulty_transitions(32)
        aut.compute()
        self.assertEqual(aut.search("abc"), [1])
        self.assertEqual(aut.search("aaaaaaaaaaaaaabc"), [1])
        self.assertEqual(aut.search("ccccbbbabc"), [1])
        self.assertEqual(aut.search("ababc"), [1])
        self.assertEqual(aut.search("d"), [0])
        self.assertEqual(aut.search("cbabbacba"), [0])

        # 3. RE /#include.*>/ with enable_fallback_state
        par = pcre_parser()
        par.set_text("/#include.*>/")
        aut = PHF_DFA()
        a = bdz()
        a.set_ratio(2.5)
        a.set_iteration_limit(10)
        aut.set_PHF_class(a)
        aut.create_by_parser(par)
        aut.enable_fallback_state(warning=False)
        aut.compute()
        self.assertEqual(aut.search("#include <stdio.h>"), [1])
        self.assertEqual(aut.search("#include <stdlib.h>"), [1])
        self.assertEqual(aut.search("#include <stdio.h>bba"), [1])
        self.assertEqual(aut.search('#include "pcre.h"'), [0])
        self.assertEqual(aut.search('asdf#include <stdio.h>'), [1])

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_PHF_DFA)
    unittest.TextTestRunner(verbosity=2).run(suite)
