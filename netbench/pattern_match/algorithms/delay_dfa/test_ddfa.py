###############################################################################
#  test_ddfa.py: Test module for Delay DFA
#  Copyright (C) 2011 Brno University of Technology, ANT @ FIT
#  Author(s): Martin Soka <xsokam00@stud.fit.vutbr.cz>
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

from netbench.pattern_match.algorithms.delay_dfa.ddfa import DELAY_DFA
from netbench.pattern_match.pcre_parser import pcre_parser
from netbench.pattern_match.nfa_data import nfa_data
from netbench.pattern_match.b_dfa import b_dfa
from netbench.pattern_match.b_nfa import b_nfa
from netbench.pattern_match.b_symbol import b_Symbol, DEF_SYMBOLS
from netbench.pattern_match.sym_char import b_Sym_char
from netbench.pattern_match.b_state import b_State
from netbench.pattern_match.b_automaton import b_Automaton
from netbench.pattern_match import aux_func
import unittest

class test_ddfa(unittest.TestCase):
    """
        Test module for Delay DFA
    """
    def test_compute(self):
        """compute()"""
        
        #Test with simple expression - Delay DFA have no default 
        #transitions. For example regular expression /^abcd/.
        self._test_compute1()
        
        #Test with simple expression - Delay DFA have one default 
        #transitions. For example regular expression /^(a|b)+/.
        self._test_compute2()
        
        #Test with automaton from paper.
        self._test_compute3()
        
    def _test_compute1(self):
        
        delay_dfa = DELAY_DFA()
        
        parser = pcre_parser()
        parser.set_text("/^abcd/")
        delay_dfa.create_by_parser(parser)
        
        delay_dfa.compute()
        self.assertTrue(delay_dfa.get_compute())
        
        dfa = b_dfa()
        dfa.create_by_parser(parser)
        dfa.compute()
        
        a = delay_dfa.get_automaton()
        b = dfa.get_automaton()
        
        l = len(b.alphabet.keys())
        b.add_symbols(DEF_SYMBOLS("default", l))
        
        self.assertEqual(a.states.keys(), b.states.keys())
        self.assertEqual(a.start, b.start)
        self.assertEqual(a.final, b.final)
        self.assertEqual(a.alphabet, b.alphabet)
        self.assertEqual(a.transitions, b.transitions)
        self.assertTrue(a.Flags["Delay DFA"])
        
    def _test_compute2(self):
        
        delay_dfa = DELAY_DFA()
        
        parser = pcre_parser()
        parser.set_text("/^(a|b)+/")
        delay_dfa.create_by_parser(parser)
        
        delay_dfa.compute()
        self.assertTrue(delay_dfa.get_compute())
        
        a = delay_dfa.get_automaton()
        b = nfa_data()
        
        b.add_symbols(b_Sym_char("a","a",0))
        b.add_symbols(b_Sym_char("b","b",1))
        b.add_symbols(DEF_SYMBOLS("default", 2))
        
        b.add_states(b_State(0,set()))
        b.add_states(b_State(1,set([0])))
        b.start = 0
        b.final = set([1])
        
        b.add_transitions( (0,0,1) )
        b.add_transitions( (0,1,1) )
        b.add_transitions( (1,2,0) )
        
        self.assertEqual(a.states.keys(), b.states.keys())
        self.assertEqual(a.start, b.start)
        self.assertEqual(a.final, b.final)
        self.assertEqual(a.alphabet, b.alphabet)
        self.assertEqual(a.transitions, b.transitions)
        self.assertTrue(a.Flags["Delay DFA"])
        
    def _test_compute3(self):
        # Get test directory 
        tdir = aux_func.getPatternMatchDir() + "/algorithms/delay_dfa/"
        
        delay_dfa = DELAY_DFA()
        
        nfaData = nfa_data().load_from_file(tdir + "test_data/text_ddfa.nfa_data")
        
        delay_dfa.create_from_nfa_data(nfaData)
        delay_dfa.determinise()
        delay_dfa.compute(False)
        self.assertTrue(delay_dfa.get_compute())
        
        a = delay_dfa.get_automaton()
        b = nfa_data()
        
        b.add_symbols(b_Sym_char("a","a",0))
        b.add_symbols(b_Sym_char("b","b",1))
        b.add_symbols(b_Sym_char("c","c",2))
        b.add_symbols(b_Sym_char("d","d",3))
        b.add_symbols(DEF_SYMBOLS("default", 4))
        
        b.add_states(b_State(0,set()))
        b.add_states(b_State(1,set([0])))
        b.add_states(b_State(2,set()))
        b.add_states(b_State(3,set([0])))
        b.add_states(b_State(4,set([0])))
        b.start = 0
        b.final = set([1,3,4])
        
        b.add_transitions( (0,2,0) )
        b.add_transitions( (0,0,1) )
        b.add_transitions( (0,1,2) )
        b.add_transitions( (0,3,3) )
        b.add_transitions( (1,4,0) )
        b.add_transitions( (2,2,4) )
        b.add_transitions( (2,4,0) )
        b.add_transitions( (3,4,0) )
        b.add_transitions( (4,4,0) )
        
        self.assertEqual(a.states.keys(), b.states.keys())
        self.assertEqual(a.start, b.start)
        self.assertEqual(a.final, b.final)
        self.assertEqual(a.alphabet, b.alphabet)
        self.assertEqual(a.transitions, b.transitions)
        self.assertTrue(a.Flags["Delay DFA"])
        
    def test_search(self):
        """search()"""
        
        #Tests a set of regular expressions and compares the results with
        #results form NFA.
        self._test_search1()
        self._test_search2()
        self._test_search3()
        
    def _test_search1(self):
        
        re = "/a+b*c.*a|bc+/"
            
        delay_dfa = DELAY_DFA()
    
        parser = pcre_parser()
        parser.set_text(re)
        delay_dfa.create_by_parser(parser)
    
        delay_dfa.compute()
        self.assertTrue(delay_dfa.get_compute())
    
        aut = b_dfa()
    
        parser = pcre_parser()
        parser.set_text(re)
        aut.create_by_parser(parser)
    
        self.assertEqual(delay_dfa.search("ac123ac"), aut.search("ac123ac"))
        self.assertEqual(delay_dfa.search("aacac"), aut.search("aacac"))
        self.assertEqual(delay_dfa.search("abbb"), aut.search("abbb"))
        
    def _test_search2(self):
        
        re = "/a+b*c+d/\n/abc/"
            
        delay_dfa = DELAY_DFA()
    
        parser = pcre_parser()
        parser.set_text(re)
        delay_dfa.create_by_parser(parser)
    
        delay_dfa.compute()
        self.assertTrue(delay_dfa.get_compute())
    
        aut = b_dfa()
    
        parser = pcre_parser()
        parser.set_text(re)
        aut.create_by_parser(parser)
        aut.compute()
    
        self.assertEqual(delay_dfa.search("abcd"), aut.search("abcd"))
        self.assertEqual(delay_dfa.search("abcd abc"), aut.search("abcd abc"))
        self.assertEqual(delay_dfa.search("abc"), aut.search("abc"))
        self.assertEqual(delay_dfa.search("acd"), aut.search("acd"))
        self.assertEqual(delay_dfa.search("abd"), aut.search("abd"))
        
    def _test_search3(self):
        
        re = "/a+b*c+/\n/b+c*d+/\n/c+d*e/"
            
        delay_dfa = DELAY_DFA()
    
        parser = pcre_parser()
        parser.set_text(re)
        delay_dfa.create_by_parser(parser)
    
        delay_dfa.compute()
        self.assertTrue(delay_dfa.get_compute())
    
        aut = b_dfa()
    
        parser = pcre_parser()
        parser.set_text(re)
        aut.create_by_parser(parser)
        aut.compute()
    
        self.assertEqual(delay_dfa.search("abcd"), aut.search("abcd"))
        self.assertEqual(delay_dfa.search("abcd abc"), aut.search("abcd abc"))
        self.assertEqual(delay_dfa.search("gabc"), aut.search("gabc"))
        self.assertEqual(delay_dfa.search("ac bd ce"), aut.search("ac bd ce"))
        self.assertEqual(delay_dfa.search("ab123a bcd cde"), aut.search("ab123a bcd cde"))
        self.assertEqual(delay_dfa.search("bce"), aut.search("bce"))
        self.assertEqual(delay_dfa.search("abe"), aut.search("abe"))
    
    def test_set_bound(self):
        """set_bound()"""
        
        #Tests manual control of the number of consecutive default 
        #transitions in larger automaton
        
        re = "/a+b*c+/\n/b+c*d+/\n/c+d*e/"
            
        delay_dfa = DELAY_DFA()
    
        parser = pcre_parser()
        parser.set_text(re)
        delay_dfa.create_by_parser(parser)
    
        delay_dfa.set_bound(0)
        delay_dfa.compute()
        self.assertTrue(delay_dfa.get_compute())
        
        a = delay_dfa.get_automaton()
        lenght1 = self._get_length_default_path(a)
        
        delay_dfa = DELAY_DFA()
    
        parser = pcre_parser()
        parser.set_text(re)
        delay_dfa.create_by_parser(parser)
    
        delay_dfa.set_bound(1)
        delay_dfa.compute()
        self.assertTrue(delay_dfa.get_compute())
        
        a = delay_dfa.get_automaton()
        lenght2 = self._get_length_default_path(a)
        
        delay_dfa = DELAY_DFA()
    
        parser = pcre_parser()
        parser.set_text(re)
        delay_dfa.create_by_parser(parser)
    
        delay_dfa.set_bound(2)
        delay_dfa.compute()
        self.assertTrue(delay_dfa.get_compute())
        
        a = delay_dfa.get_automaton()
        lenght3 = self._get_length_default_path(a)
        
        delay_dfa = DELAY_DFA()
    
        parser = pcre_parser()
        parser.set_text(re)
        delay_dfa.create_by_parser(parser)
    
        delay_dfa.set_bound(3)
        delay_dfa.compute()
        self.assertTrue(delay_dfa.get_compute())
        
        a = delay_dfa.get_automaton()
        lenght4 = self._get_length_default_path(a)
        
        self.assertEqual(lenght1, 3)
        self.assertEqual(lenght2, 1)
        self.assertEqual(lenght3, 2)
        self.assertEqual(lenght4, 3)
        
    def _get_length_default_path(self, aut):
        
        defaultSymbolID = -1
        def_trans = {}

        for symbolID in aut.alphabet:
            if isinstance(aut.alphabet[symbolID], DEF_SYMBOLS):
                defaultSymbolID = symbolID
        if defaultSymbolID != -1:
            for t in aut.transitions:
                if t[1] == defaultSymbolID:
                    def_trans[t[0]] = t[2]
        
        lenght = 0
        for t in def_trans.keys():
            nxt = t
            l = 0
            while nxt in def_trans.keys():
                l += 1
                if l > lenght:
                    lenght = l
                nxt = def_trans[nxt]
        return lenght
    
    def test_get_default_trans_num(self):
        """get_default_trans_num"""
        
        #Tests with regular expressions from test_compute
        
        delay_dfa1 = DELAY_DFA()
        
        parser = pcre_parser()
        parser.set_text("/^abcd/")
        delay_dfa1.create_by_parser(parser)
        
        delay_dfa1.compute()
        self.assertTrue(delay_dfa1.get_compute())
        
        delay_dfa2 = DELAY_DFA()
        
        parser = pcre_parser()
        parser.set_text("/^(a|b)+/")
        delay_dfa2.create_by_parser(parser)
        
        delay_dfa2.compute()
        self.assertTrue(delay_dfa2.get_compute())
        
        delay_dfa3 = DELAY_DFA()
        
        # Get test directory 
        tdir = aux_func.getPatternMatchDir() + "/algorithms/delay_dfa/"
        
        nfaData = nfa_data().load_from_file(tdir + "test_data/text_ddfa.nfa_data")
        
        delay_dfa3.create_from_nfa_data(nfaData)
        delay_dfa3.determinise()
        delay_dfa3.compute(False)
        self.assertTrue(delay_dfa3.get_compute())
        
        self.assertEqual(delay_dfa1.get_default_trans_num(),0)
        self.assertEqual(delay_dfa2.get_default_trans_num(),1)
        self.assertEqual(delay_dfa3.get_default_trans_num(),4)
    
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_ddfa)
    unittest.TextTestRunner(verbosity=2).run(suite)
