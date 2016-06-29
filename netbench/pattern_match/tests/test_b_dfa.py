###############################################################################
#  test_b_dfa.py: Module for PATTERN MATCH - test base DFA implementation
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

from netbench.pattern_match.nfa_data import nfa_data
from netbench.pattern_match.b_state import b_State
from netbench.pattern_match.sym_char import b_Sym_char
from netbench.pattern_match.sym_char_class import b_Sym_char_class
from netbench.pattern_match.b_dfa import b_dfa
from netbench.pattern_match.pattern_exceptions import \
    ALPHABET_COLLISION_FREE_ERROR
from netbench.pattern_match.pattern_exceptions import DETERMINISTIC_ERROR
from netbench.pattern_match.parser import parser
import unittest

class test_b_dfa(unittest.TestCase):
    """A base test class for DFA automata."""

    def test_determinise(self):
        """determinise()"""
        # Test the function of the five machines, to test the function of
        # leaders of correct results for these machines.
        # Vending machines should include:
        #   iterate (*),
        #   character classes,
        #   branched (/ (abcd | abce) /),
        #   etc.

        # 0) should not raise aplhabet collision free exception
        # will use some non empty automaton
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (1,2,2) )
        nfaData.final.add(2)
        dfa = b_dfa()
        dfa.create_from_nfa_data(nfaData)
        try :
            dfa.determinise()
            self.assertTrue(True)
        except ALPHABET_COLLISION_FREE_ERROR:
            self.assertTrue(False)

        # 1) concatenation
        # 0 -a-> 1 -b-> 2 -c-> 3  =>  0 -a-> 1 -b-> 2 -c-> 3 (nothing happen)
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

        dfa = b_dfa()
        dfa.create_from_nfa_data(nfaData)
        dfa.determinise()
        cp = dfa.get_automaton()
        result = nfa_data().load_from_file("test_data/(1)determinise.nfa_data")

        self.assertTrue(sorted(cp.states.keys()) == sorted(result.states.keys()))
        self.assertTrue(cp.alphabet == result.alphabet)
        self.assertTrue(cp.start == result.start)
        self.assertTrue(cp.final == result.final)
        self.assertTrue(cp.transitions == result.transitions)
        self.assertTrue(cp.Flags == result.Flags)

        # 2) branch
        #     |-a--> 1 --c--\--> 5
        # 0 --|-a--> 2 --d-----> 4
        #     |-b--> 3 --d----/
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set())
        nfaData.states[4] = b_State(4,set([0]))
        nfaData.states[5] = b_State(5,set([1]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.alphabet[3] = b_Sym_char("d", "d", 3)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (0,0,2) )
        nfaData.transitions.add( (0,1,3) )
        nfaData.transitions.add( (1,2,4) )
        nfaData.transitions.add( (1,2,5) )
        nfaData.transitions.add( (2,3,4) )
        nfaData.transitions.add( (3,3,4) )
        nfaData.final.add(4)
        nfaData.final.add(5)

        dfa = b_dfa()
        dfa.create_from_nfa_data(nfaData)
        dfa.determinise()
        cp = dfa.get_automaton()
        result = nfa_data().load_from_file("test_data/(2)determinise.nfa_data")

        self.assertTrue(sorted(cp.states.keys()) == sorted(result.states.keys()))
        #self.assertTrue(cp.alphabet == result.alphabet)
        self.assertTrue(cp.start == result.start)
        self.assertTrue(cp.final == result.final)
        self.assertTrue(cp.transitions == result.transitions)
        self.assertTrue(cp.Flags == result.Flags)

        # 3) loop back to the same state
        #          b
        #         / \
        #         \ /
        # 0 --a--> 1 --c--> 2
        #           \--b--/
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (1,2,2) )
        nfaData.final.add(2)

        dfa = b_dfa()
        dfa.create_from_nfa_data(nfaData)
        dfa.determinise()
        cp = dfa.get_automaton()
        result = nfa_data().load_from_file("test_data/(3)determinise.nfa_data")

        self.assertTrue(sorted(cp.states.keys()) == sorted(result.states.keys()))
        self.assertTrue(cp.alphabet == result.alphabet)
        self.assertTrue(cp.start == result.start)
        self.assertTrue(cp.final == result.final)
        self.assertTrue(cp.transitions == result.transitions)
        self.assertTrue(cp.Flags == result.Flags)

        # 4) transition back / transition back to the initial state
        #    0 <----
        #    |     |
        #    a     |
        #    |     |
        #    1 <-  c
        #    |  |  |
        #    b  c  |
        #    |  |  |
        #    2 -----
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (2,2,1) )
        nfaData.transitions.add( (2,2,0) )
        nfaData.final.add(2)

        dfa = b_dfa()
        dfa.create_from_nfa_data(nfaData)
        dfa.determinise()
        cp = dfa.get_automaton()
        result = nfa_data().load_from_file("test_data/(4)determinise.nfa_data")

        self.assertTrue(sorted(cp.states.keys()) == sorted(result.states.keys()))
        self.assertTrue(cp.alphabet == result.alphabet)
        self.assertTrue(cp.start == result.start)
        self.assertTrue(cp.final == result.final)
        self.assertTrue(cp.transitions == result.transitions)
        self.assertTrue(cp.Flags == result.Flags)

        # 5) double loop back to the same state
        #        --b--
        #       /  c  \
        #       \ / \ /
        #        \\ //
        # 0 --a--> 1 --c--> 2
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,1) )
        nfaData.transitions.add( (1,2,1) )
        nfaData.transitions.add( (1,2,2) )
        nfaData.final.add(2)

        dfa = b_dfa()
        dfa.create_from_nfa_data(nfaData)
        dfa.determinise()
        cp = dfa.get_automaton()
        result = nfa_data().load_from_file("test_data/(5)determinise.nfa_data")

        self.assertTrue(sorted(cp.states.keys()) == sorted(result.states.keys()))
        self.assertTrue(cp.alphabet == result.alphabet)
        self.assertTrue(cp.start == result.start)
        self.assertTrue(cp.final == result.final)
        self.assertTrue(cp.transitions == result.transitions)
        self.assertTrue(cp.Flags == result.Flags)

        # 6) character classes
        #            [e,f]
        #             / \
        #             \ /
        # 0 --[a,b]--> 1 --[e,f]--> 3
        #   \-[b,c]--> 2  \---g---> 4
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set([0]))
        nfaData.states[4] = b_State(4,set([1]))
        nfaData.alphabet[0] = b_Sym_char_class("ch0", set(['a', 'b']), 0)
        nfaData.alphabet[1] = b_Sym_char_class("ch1", set(['b', 'c']), 1)
        nfaData.alphabet[2] = b_Sym_char_class("ch2", set(['e', 'f']), 2)
        nfaData.alphabet[3] = b_Sym_char("g", "g", 3)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (0,1,2) )
        nfaData.transitions.add( (1,2,1) )
        nfaData.transitions.add( (1,2,3) )
        nfaData.transitions.add( (1,3,4) )
        nfaData.final.add(3)
        nfaData.final.add(4)
        dfa = b_dfa()
        dfa.create_from_nfa_data(nfaData)
        dfa.determinise()
        cp = dfa.get_automaton()
        result = nfa_data().load_from_file("test_data/(6)determinise.nfa_data")
        res = b_dfa()
        res.create_from_nfa_data(result)
        self.assertTrue(sorted(cp.states.keys()) == sorted(result.states.keys()))
        self.assertTrue(cp.alphabet == result.alphabet)
        self.assertTrue(cp.start == result.start)
        self.assertTrue(cp.final == result.final)
        self.assertTrue(cp.transitions == result.transitions)
        self.assertTrue(cp.Flags == result.Flags)

        # 7) test with symbol collisions
        par = parser("pcre_parser")
        par.set_text("/^T(a|[a-c]|[c-e])E(1|1)S([e-m]|[j-l]|[x-z])T/")
        dfa = b_dfa()
        dfa.create_by_parser(par)
        dfa.determinise()
        cp = dfa.get_automaton()
        result = nfa_data().load_from_file("test_data/(7)determinise.nfa_data")
        res = b_dfa()
        res.create_from_nfa_data(result)
        self.assertTrue(sorted(cp.states.keys()) == sorted(result.states.keys()))
        self.assertTrue(cp.alphabet == result.alphabet)
        self.assertTrue(cp.start == result.start)
        self.assertTrue(cp.final == result.final)
        self.assertTrue(cp.transitions == result.transitions)
        self.assertTrue(cp.Flags == result.Flags)

        # 8) will use some non empty automaton
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (1,2,2) )
        nfaData.final.add(2)

        dfa = b_dfa()
        dfa.create_from_nfa_data(nfaData)
        dfa.determinise(create_table = False)
        self.assertTrue(len(dfa._state_representation) == 0)

        other_dfa = b_dfa()
        other_dfa.create_from_nfa_data(nfaData)
        other_dfa.determinise(create_table = True)
        self.assertTrue(len(other_dfa._state_representation) != 0)

        # Verify parameter states_limit (in the previous paragraphs are
        # presumed zero):
        # - Set the value on small number and try to determinizovat machine,
        #   which is in this size definitely does not fit -> Deterministic flag
        #   must be False.
        # - To test whether it is performed properly determinization fits to the
        #   size of the DFA to states_limit.

        # 9) will use some non empty automaton
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (1,2,2) )
        nfaData.final.add(2)

        dfa = b_dfa()
        dfa.create_from_nfa_data(nfaData)
        dfa.determinise(states_limit = 2)
        self.assertTrue(dfa._automaton.Flags["Deterministic"] == False)

        other_dfa = b_dfa()
        other_dfa.create_from_nfa_data(nfaData)
        other_dfa.determinise(states_limit = 10)
        self.assertTrue(other_dfa._automaton.Flags["Deterministic"] == True)

    def test_minimise(self):
        """minimise()"""
        # To test whether the exception is thrown if the machine is not
        # deterministic. To test the function of the five machines, to test the
        # function of leaders of correct results for these machines.
        # Vending machines should include:
        #   - iterate (*),
        #   - character classes,
        #   - branched (/ (abcd | ABCE) /),
        #   - etc.

        # 0) try error if is not deterministic
        # will use some non empty automaton
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (1,2,2) )
        nfaData.final.add(2)
        dfa = b_dfa()
        dfa.create_from_nfa_data(nfaData)
        dfa.set_multilanguage(False)
        try :
            dfa.set_flag("Alphabet collision free", True)
            dfa.minimise()
            self.assertTrue(False)
        except DETERMINISTIC_ERROR:
            self.assertTrue(True)

        # 1) concatenation
        # 0 -a-> 1 -b-> 2 -c-> 3  =>  0 -a-> 1 -b-> 2 -c-> 3 (nothing happen)
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

        dfa = b_dfa()
        dfa.create_from_nfa_data(nfaData)
        dfa.set_multilanguage(False)
        dfa.determinise()
        dfa.minimise()
        cp = dfa.get_automaton()
        result = nfa_data().load_from_file("test_data/(1)minimise.nfa_data")

        self.assertTrue(sorted(cp.states.keys()) == sorted(result.states.keys()))
        self.assertTrue(cp.alphabet == result.alphabet)
        self.assertTrue(cp.start == result.start)
        self.assertTrue(cp.final == result.final)
        self.assertTrue(cp.transitions == result.transitions)
        self.assertTrue(cp.Flags == result.Flags)

        # 2) branch
        #     |-a--> 1 --c--\--> 5
        # 0 --|-a--> 2 --d-----> 4
        #     |-b--> 3 --d----/
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set())
        nfaData.states[4] = b_State(4,set([0]))
        nfaData.states[5] = b_State(5,set([1]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.alphabet[3] = b_Sym_char("d", "d", 3)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (0,0,2) )
        nfaData.transitions.add( (0,1,3) )
        nfaData.transitions.add( (1,2,4) )
        nfaData.transitions.add( (1,2,5) )
        nfaData.transitions.add( (2,3,4) )
        nfaData.transitions.add( (3,3,4) )
        nfaData.final.add(4)
        nfaData.final.add(5)

        dfa = b_dfa()
        dfa.create_from_nfa_data(nfaData)
        dfa.set_multilanguage(False)
        dfa.determinise()
        dfa.minimise()
        cp = dfa.get_automaton()
        result = nfa_data().load_from_file("test_data/(2)minimise.nfa_data")
        self.assertTrue(sorted(cp.states.keys()) == sorted(result.states.keys()))
        self.assertTrue(cp.alphabet == result.alphabet)
        self.assertTrue(cp.start == result.start)
        self.assertTrue(cp.final == result.final)
        self.assertTrue(cp.transitions == result.transitions)
        self.assertTrue(cp.Flags == result.Flags)

        # 3) loop back to the same state
        #          b
        #         / \
        #         \ /
        # 0 --a--> 1 --c--> 2
        #           \--b--/
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (1,2,2) )
        nfaData.final.add(2)

        dfa = b_dfa()
        dfa.create_from_nfa_data(nfaData)
        dfa.set_multilanguage(False)
        dfa.determinise()
        dfa.minimise()
        cp = dfa.get_automaton()
        result = nfa_data().load_from_file("test_data/(3)minimise.nfa_data")

        self.assertTrue(sorted(cp.states.keys()) == sorted(result.states.keys()))
        self.assertTrue(cp.alphabet == result.alphabet)
        self.assertTrue(cp.start == result.start)
        self.assertTrue(cp.final == result.final)
        self.assertTrue(cp.transitions == result.transitions)
        self.assertTrue(cp.Flags == result.Flags)

        # 4) transition back / transition back to the initial state
        #    0 <----
        #    |     |
        #    a     |
        #    |     |
        #    1 <-  c
        #    |  |  |
        #    b  c  |
        #    |  |  |
        #    2 -----
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (2,2,1) )
        nfaData.transitions.add( (2,2,0) )
        nfaData.final.add(2)

        dfa = b_dfa()
        dfa.create_from_nfa_data(nfaData)
        dfa.set_multilanguage(False)
        dfa.determinise()
        dfa.minimise()
        cp = dfa.get_automaton()
        result = nfa_data().load_from_file("test_data/(4)minimise.nfa_data")

        self.assertTrue(sorted(cp.states.keys()) == sorted(result.states.keys()))
        self.assertTrue(cp.alphabet == result.alphabet)
        self.assertTrue(cp.start == result.start)
        self.assertTrue(cp.final == result.final)
        self.assertTrue(cp.transitions == result.transitions)
        self.assertTrue(cp.Flags == result.Flags)

        # 5) double loop back to the same state
        #        --b--
        #       /  c  \
        #       \ / \ /
        #        \\ //
        # 0 --a--> 1 --c--> 2
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,1) )
        nfaData.transitions.add( (1,2,1) )
        nfaData.transitions.add( (1,2,2) )
        nfaData.final.add(2)

        dfa = b_dfa()
        dfa.create_from_nfa_data(nfaData)
        dfa.set_multilanguage(False)
        dfa.determinise()
        dfa.minimise()
        cp = dfa.get_automaton()
        result = nfa_data().load_from_file("test_data/(5)minimise.nfa_data")

        self.assertTrue(sorted(cp.states.keys()) == sorted(result.states.keys()))
        self.assertTrue(cp.alphabet == result.alphabet)
        self.assertTrue(cp.start == result.start)
        self.assertTrue(cp.final == result.final)
        self.assertTrue(cp.transitions == result.transitions)
        self.assertTrue(cp.Flags == result.Flags)

        # 6) character classes
        #            [e,f]
        #             / \
        #             \ /
        # 0 --[a,b]--> 1 --[e,f]--> 3
        #   \-[b,c]--> 2  \---g---> 4
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set([0]))
        nfaData.states[4] = b_State(4,set([1]))
        nfaData.alphabet[0] = b_Sym_char_class("ch0", set(['a', 'b']), 0)
        nfaData.alphabet[1] = b_Sym_char_class("ch1", set(['b', 'c']), 1)
        nfaData.alphabet[2] = b_Sym_char_class("ch2", set(['e', 'f']), 2)
        nfaData.alphabet[3] = b_Sym_char("ch3", "g", 3)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (0,1,2) )
        nfaData.transitions.add( (1,2,1) )
        nfaData.transitions.add( (1,2,3) )
        nfaData.transitions.add( (1,3,4) )
        nfaData.final.add(3)
        nfaData.final.add(4)

        dfa = b_dfa()
        dfa.create_from_nfa_data(nfaData)
        dfa.set_multilanguage(False)
        dfa.determinise()
        dfa.minimise()
        cp = dfa.get_automaton()
        result = nfa_data().load_from_file("test_data/(6)minimise.nfa_data")

        self.assertTrue(sorted(cp.states.keys()) == sorted(result.states.keys()))
        self.assertTrue(cp.alphabet == result.alphabet)
        self.assertTrue(cp.start == result.start)
        self.assertTrue(cp.final == result.final)
        self.assertTrue(cp.transitions == result.transitions)
        self.assertTrue(cp.Flags == result.Flags)
        
        # 7) branch - multilanguage
        #     |-a--> 1 --c--\--> 5
        # 0 --|-a--> 2 --d-----> 4
        #     |-b--> 3 --d----/
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set())
        nfaData.states[4] = b_State(4,set([0]))
        nfaData.states[5] = b_State(5,set([1]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.alphabet[3] = b_Sym_char("d", "d", 3)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (0,0,2) )
        nfaData.transitions.add( (0,1,3) )
        nfaData.transitions.add( (1,2,4) )
        nfaData.transitions.add( (1,2,5) )
        nfaData.transitions.add( (2,3,4) )
        nfaData.transitions.add( (3,3,4) )
        nfaData.final.add(4)
        nfaData.final.add(5)

        dfa = b_dfa()
        dfa.create_from_nfa_data(nfaData)
        dfa.set_multilanguage(True)
        dfa.determinise()
        dfa.minimise()
        cp = dfa.get_automaton()
        result = nfa_data().load_from_file("test_data/(7)minimise.nfa_data")
        self.assertTrue(sorted(cp.states.keys()) == sorted(result.states.keys()))
        self.assertTrue(cp.alphabet == result.alphabet)
        self.assertTrue(cp.start == result.start)
        self.assertTrue(cp.final == result.final)
        self.assertTrue(cp.transitions == result.transitions)
        self.assertTrue(cp.Flags == result.Flags)


    def test_compute(self):
        """compute()"""
        # Test execution of determinise and minimise and
        # settings self._compute = True.

        # will use some non empty automaton
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (1,2,2) )
        nfaData.final.add(2)
        dfa = b_dfa()
        dfa.create_from_nfa_data(nfaData)
        dfa.compute()
        self.assertTrue(dfa._automaton.Flags["Deterministic"] == True)
        self.assertTrue(dfa._automaton.Flags["Minimal"] == True)
        self.assertTrue(dfa._compute == True)

    def test_isomorphic(self):
        """isomorphic()"""
        # To test the function of the five machines, to test the function of
        # leaders of correct results for these machines.
        # Test the function in case of machine is not isomorphic. Vending
        # machines should include:
        #   - iterate (*),
        #   - character classes,
        #   - branched (/ (abcd | ABCE) /),
        #   - etc.

        # 0) try error if is not deterministic
        # will use some non empty automaton
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (1,2,2) )
        nfaData.final.add(2)
        dfa = b_dfa()
        dfa.create_from_nfa_data(nfaData)
        try :
            dfa.isomorphic(nfaData)
            self.assertTrue(False)
        except DETERMINISTIC_ERROR:
            self.assertTrue(True)

        # 1) concatenation
        # 1.1) right compare (just reversed states number)
        # 0 -a-> 1 -b-> 2 -c-> 3
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
        dfa = b_dfa()
        dfa.create_from_nfa_data(nfaData)
        dfa.determinise()

        nfaData_compare = nfa_data()
        nfaData_compare.states[3] = b_State(0,set())
        nfaData_compare.states[2] = b_State(1,set())
        nfaData_compare.states[1] = b_State(2,set())
        nfaData_compare.states[0] = b_State(3,set([0]))
        nfaData_compare.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData_compare.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData_compare.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData_compare.start = 3
        nfaData_compare.transitions.add( (3,0,2) )
        nfaData_compare.transitions.add( (2,1,1) )
        nfaData_compare.transitions.add( (1,2,0) )
        nfaData_compare.final.add(0)
        dfa_compare = b_dfa()
        dfa_compare.create_from_nfa_data(nfaData_compare)
        dfa_compare.determinise()

        self.assertTrue(dfa.isomorphic(dfa_compare._automaton) == True)

        # 1.2) wrong compare (different automaton)
        # 0 -a-> 1 -b-> 2 -c-> 3
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
        dfa = b_dfa()
        dfa.create_from_nfa_data(nfaData)
        dfa.determinise()

        nfaData_compare = nfa_data()
        nfaData_compare.states[0] = b_State(0,set())
        nfaData_compare.states[1] = b_State(1,set())
        nfaData_compare.states[2] = b_State(2,set())
        nfaData_compare.states[3] = b_State(3,set())
        nfaData_compare.states[4] = b_State(4,set([0]))
        nfaData_compare.states[5] = b_State(5,set([1]))
        nfaData_compare.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData_compare.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData_compare.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData_compare.alphabet[3] = b_Sym_char("d", "d", 3)
        nfaData_compare.start = 0
        nfaData_compare.transitions.add( (0,0,1) )
        nfaData_compare.transitions.add( (0,0,2) )
        nfaData_compare.transitions.add( (0,1,2) )
        nfaData_compare.transitions.add( (1,2,4) )
        nfaData_compare.transitions.add( (1,2,5) )
        nfaData_compare.transitions.add( (2,3,4) )
        nfaData_compare.transitions.add( (3,3,4) )
        nfaData_compare.final.add(4)
        nfaData_compare.final.add(5)
        dfa_compare = b_dfa()
        dfa_compare.create_from_nfa_data(nfaData_compare)
        dfa_compare.determinise()

        #self.assertTrue(dfa.isomorphic(dfa_compare._automaton) == False)

        # 2) branch
        # 2.1) right compare (throw states 1 and 4)
        #     |-a--> 1 --c--\--> 5
        # 0 --|-a--> 2 --d-----> 4
        #     |-b--> 3 --d----/
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set())
        nfaData.states[4] = b_State(4,set([0]))
        nfaData.states[5] = b_State(5,set([1]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.alphabet[3] = b_Sym_char("d", "d", 3)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (0,0,2) )
        nfaData.transitions.add( (0,1,3) )
        nfaData.transitions.add( (1,2,4) )
        nfaData.transitions.add( (1,2,5) )
        nfaData.transitions.add( (2,3,4) )
        nfaData.transitions.add( (3,3,4) )
        nfaData.final.add(4)
        nfaData.final.add(5)
        dfa = b_dfa()
        dfa.create_from_nfa_data(nfaData)
        dfa.determinise()

        nfaData_compare = nfa_data()
        nfaData_compare.states[0] = b_State(0,set())
        nfaData_compare.states[1] = b_State(1,set([0]))
        nfaData_compare.states[2] = b_State(2,set())
        nfaData_compare.states[3] = b_State(3,set())
        nfaData_compare.states[4] = b_State(4,set())
        nfaData_compare.states[5] = b_State(5,set([1]))
        nfaData_compare.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData_compare.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData_compare.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData_compare.alphabet[3] = b_Sym_char("d", "d", 3)
        nfaData_compare.start = 0
        nfaData_compare.transitions.add( (0,0,4) )
        nfaData_compare.transitions.add( (0,0,2) )
        nfaData_compare.transitions.add( (0,1,3) )
        nfaData_compare.transitions.add( (4,2,1) )
        nfaData_compare.transitions.add( (4,2,5) )
        nfaData_compare.transitions.add( (2,3,1) )
        nfaData_compare.transitions.add( (3,3,1) )
        nfaData_compare.final.add(1)
        nfaData_compare.final.add(5)
        dfa_compare = b_dfa()
        dfa_compare.create_from_nfa_data(nfaData_compare)
        dfa_compare.determinise()

        self.assertTrue(dfa.isomorphic(dfa_compare._automaton) == True)

        # 2.2) wrong compare (different automaton)
        #     |-a--> 1 --c--\--> 5
        # 0 --|-a--> 2 --d-----> 4
        #     |-b--> 3 --d----/
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set())
        nfaData.states[4] = b_State(4,set([0]))
        nfaData.states[5] = b_State(5,set([1]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.alphabet[3] = b_Sym_char("d", "d", 3)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (0,0,2) )
        nfaData.transitions.add( (0,1,3) )
        nfaData.transitions.add( (1,2,4) )
        nfaData.transitions.add( (1,2,5) )
        nfaData.transitions.add( (2,3,4) )
        nfaData.transitions.add( (3,3,4) )
        nfaData.final.add(4)
        nfaData.final.add(5)
        dfa = b_dfa()
        dfa.create_from_nfa_data(nfaData)
        dfa.determinise()

        nfaData_compare = nfa_data()
        nfaData_compare.states[0] = b_State(0,set())
        nfaData_compare.states[1] = b_State(1,set())
        nfaData_compare.states[2] = b_State(2,set([0]))
        nfaData_compare.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData_compare.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData_compare.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData_compare.start = 0
        nfaData_compare.transitions.add( (0,0,1) )
        nfaData_compare.transitions.add( (1,1,1) )
        nfaData_compare.transitions.add( (1,1,2) )
        nfaData_compare.transitions.add( (1,2,2) )
        nfaData_compare.final.add(2)
        dfa_compare = b_dfa()
        dfa_compare.create_from_nfa_data(nfaData_compare)
        dfa_compare.determinise()

        self.assertTrue(dfa.isomorphic(dfa_compare._automaton) == False)

        # 3) loop back to the same state
        # 3.1) right compare (turn alphabet)
        #          b
        #         / \
        #         \ /
        # 0 --a--> 1 --c--> 2
        #           \--b--/
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (1,2,2) )
        nfaData.final.add(2)
        dfa = b_dfa()
        dfa.create_from_nfa_data(nfaData)
        dfa.determinise()

        nfaData_compare = nfa_data()
        nfaData_compare.states[0] = b_State(0,set())
        nfaData_compare.states[1] = b_State(1,set())
        nfaData_compare.states[2] = b_State(2,set([0]))
        nfaData_compare.alphabet[2] = b_Sym_char("a", "a", 2)
        nfaData_compare.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData_compare.alphabet[0] = b_Sym_char("c", "c", 0)
        nfaData_compare.start = 0
        nfaData_compare.transitions.add( (0,2,1) )
        nfaData_compare.transitions.add( (1,1,1) )
        nfaData_compare.transitions.add( (1,1,2) )
        nfaData_compare.transitions.add( (1,0,2) )
        nfaData_compare.final.add(2)
        dfa_compare = b_dfa()
        dfa_compare.create_from_nfa_data(nfaData_compare)
        dfa_compare.determinise()

        self.assertTrue(dfa.isomorphic(dfa_compare._automaton) == True)

        # 3.2) wrong compare (different transitions)
        #          b
        #         / \
        #         \ /
        # 0 --a--> 1 --c--> 2
        #           \--b--/
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (1,2,2) )
        nfaData.final.add(2)
        dfa = b_dfa()
        dfa.create_from_nfa_data(nfaData)
        dfa.determinise()

        nfaData_compare = nfa_data()
        nfaData_compare.states[0] = b_State(0,set())
        nfaData_compare.states[1] = b_State(1,set())
        nfaData_compare.states[2] = b_State(2,set([0]))
        nfaData_compare.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData_compare.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData_compare.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData_compare.start = 0
        nfaData_compare.transitions.add( (0,1,1) )
        nfaData_compare.transitions.add( (1,1,1) )
        nfaData_compare.transitions.add( (1,1,2) )
        nfaData_compare.transitions.add( (1,2,2) )
        nfaData_compare.final.add(2)
        dfa_compare = b_dfa()
        dfa_compare.create_from_nfa_data(nfaData_compare)
        dfa_compare.determinise()

        self.assertTrue(dfa.isomorphic(dfa_compare._automaton) == False)

        # 4) transition back / transition back to the initial state
        # 4.1) right compare (same automaton)
        #    0 <----
        #    |     |
        #    a     |
        #    |     |
        #    1 <-  c
        #    |  |  |
        #    b  c  |
        #    |  |  |
        #    2 -----
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (2,2,1) )
        nfaData.transitions.add( (2,2,0) )
        nfaData.final.add(2)
        dfa = b_dfa()
        dfa.create_from_nfa_data(nfaData)
        dfa.determinise()

        nfaData_compare = nfa_data()
        nfaData_compare.states[0] = b_State(0,set())
        nfaData_compare.states[1] = b_State(1,set())
        nfaData_compare.states[2] = b_State(2,set([0]))
        nfaData_compare.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData_compare.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData_compare.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData_compare.start = 0
        nfaData_compare.transitions.add( (0,0,1) )
        nfaData_compare.transitions.add( (1,1,2) )
        nfaData_compare.transitions.add( (2,2,1) )
        nfaData_compare.transitions.add( (2,2,0) )
        nfaData_compare.final.add(2)
        dfa_compare = b_dfa()
        dfa_compare.create_from_nfa_data(nfaData_compare)
        dfa_compare.determinise()

        self.assertTrue(dfa.isomorphic(dfa_compare._automaton) == True)

        # 4.2) wrong compare (different final state)
        #    0 <----
        #    |     |
        #    a     |
        #    |     |
        #    1 <-  c
        #    |  |  |
        #    b  c  |
        #    |  |  |
        #    2 -----
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (2,2,1) )
        nfaData.transitions.add( (2,2,0) )
        nfaData.final.add(2)
        dfa = b_dfa()
        dfa.create_from_nfa_data(nfaData)
        dfa.determinise()

        nfaData_compare = nfa_data()
        nfaData_compare.states[0] = b_State(0,set())
        nfaData_compare.states[1] = b_State(1,set())
        nfaData_compare.states[2] = b_State(2,set([0]))
        nfaData_compare.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData_compare.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData_compare.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData_compare.start = 0
        nfaData_compare.transitions.add( (0,0,1) )
        nfaData_compare.transitions.add( (1,1,2) )
        nfaData_compare.transitions.add( (2,2,1) )
        nfaData_compare.transitions.add( (2,2,0) )
        nfaData_compare.final.add(1)
        dfa_compare = b_dfa()
        dfa_compare.create_from_nfa_data(nfaData_compare)
        dfa_compare.determinise()

        self.assertTrue(dfa.isomorphic(dfa_compare._automaton) == False)

        # 5) double loop back to the same state
        # 5.1) right compare (change number of initial state)
        #        --b--
        #       /  c  \
        #       \ / \ /
        #        \\ //
        # 0 --a--> 1 --c--> 2
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,1) )
        nfaData.transitions.add( (1,2,1) )
        nfaData.transitions.add( (1,2,2) )
        nfaData.final.add(2)
        dfa = b_dfa()
        dfa.create_from_nfa_data(nfaData)
        dfa.determinise()

        nfaData_compare = nfa_data()
        nfaData_compare.states[1] = b_State(1,set())
        nfaData_compare.states[0] = b_State(0,set())
        nfaData_compare.states[2] = b_State(2,set([0]))
        nfaData_compare.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData_compare.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData_compare.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData_compare.start = 1
        nfaData_compare.transitions.add( (1,0,0) )
        nfaData_compare.transitions.add( (0,1,0) )
        nfaData_compare.transitions.add( (0,2,0) )
        nfaData_compare.transitions.add( (0,2,2) )
        nfaData_compare.final.add(2)
        dfa_compare = b_dfa()
        dfa_compare.create_from_nfa_data(nfaData_compare)
        dfa_compare.determinise()

        self.assertTrue(dfa.isomorphic(dfa_compare._automaton) == True)

        # 5.2) wrong compare (change number of initial state)
        #        --b--
        #       /  c  \
        #       \ / \ /
        #        \\ //
        # 0 --a--> 1 --c--> 2
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,1) )
        nfaData.transitions.add( (1,2,1) )
        nfaData.transitions.add( (1,2,2) )
        nfaData.final.add(2)
        dfa = b_dfa()
        dfa.create_from_nfa_data(nfaData)
        dfa.determinise()

        nfaData_compare = nfa_data()
        nfaData_compare.states[1] = b_State(1,set())
        nfaData_compare.states[0] = b_State(0,set())
        nfaData_compare.states[2] = b_State(2,set([0]))
        nfaData_compare.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData_compare.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData_compare.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData_compare.start = 2
        nfaData_compare.transitions.add( (1,0,0) )
        nfaData_compare.transitions.add( (0,1,0) )
        nfaData_compare.transitions.add( (0,2,0) )
        nfaData_compare.transitions.add( (0,2,2) )
        nfaData_compare.final.add(2)
        dfa_compare = b_dfa()
        dfa_compare.create_from_nfa_data(nfaData_compare)
        dfa_compare.determinise()

        self.assertTrue(dfa.isomorphic(dfa_compare._automaton) == False)

        # 6) character classes
        # 6.1) right compare (new numbers for final states)
        #            [e,f]
        #             / \
        #             \ /
        # 0 --[a,b]--> 1 --[e,f]--> 3
        #   \-[b,c]--> 2  \---g---> 4
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set([0]))
        nfaData.states[4] = b_State(4,set([1]))
        nfaData.alphabet[0] = b_Sym_char_class("ch0", set(['a', 'b']), 0)
        nfaData.alphabet[1] = b_Sym_char_class("ch1", set(['b', 'c']), 1)
        nfaData.alphabet[2] = b_Sym_char_class("ch2", set(['e', 'f']), 2)
        nfaData.alphabet[3] = b_Sym_char("ch3", "g", 3)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (0,1,2) )
        nfaData.transitions.add( (1,2,1) )
        nfaData.transitions.add( (1,2,3) )
        nfaData.transitions.add( (1,3,4) )
        nfaData.final.add(3)
        nfaData.final.add(4)
        dfa = b_dfa()
        dfa.create_from_nfa_data(nfaData)
        dfa.determinise()

        nfaData_compare = nfa_data()
        nfaData_compare.states[0] = b_State(0,set())
        nfaData_compare.states[1] = b_State(1,set())
        nfaData_compare.states[2] = b_State(2,set())
        nfaData_compare.states[5] = b_State(5,set([0]))
        nfaData_compare.states[10] = b_State(10,set([1]))
        nfaData_compare.alphabet[0] = b_Sym_char_class("ch0", set(['a', 'b']), 0)
        nfaData_compare.alphabet[1] = b_Sym_char_class("ch1", set(['b', 'c']), 1)
        nfaData_compare.alphabet[2] = b_Sym_char_class("ch2", set(['e', 'f']), 2)
        nfaData_compare.alphabet[3] = b_Sym_char("ch3", "g", 3)
        nfaData_compare.start = 0
        nfaData_compare.transitions.add( (0,0,1) )
        nfaData_compare.transitions.add( (0,1,2) )
        nfaData_compare.transitions.add( (1,2,1) )
        nfaData_compare.transitions.add( (1,2,5) )
        nfaData_compare.transitions.add( (1,3,10) )
        nfaData_compare.final.add(5)
        nfaData_compare.final.add(10)
        dfa_compare = b_dfa()
        dfa_compare.create_from_nfa_data(nfaData_compare)
        dfa_compare.determinise()

        self.assertTrue(dfa.isomorphic(dfa_compare._automaton) == True)

        # 6.2) wrong compare (wrong number of final state)
        #            [e,f]
        #             / \
        #             \ /
        # 0 --[a,b]--> 1 --[e,f]--> 3
        #   \-[b,c]--> 2  \---g---> 4
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set([0]))
        nfaData.states[4] = b_State(4,set([1]))
        nfaData.alphabet[0] = b_Sym_char_class("ch0", set(['a', 'b']), 0)
        nfaData.alphabet[1] = b_Sym_char_class("ch1", set(['b', 'c']), 1)
        nfaData.alphabet[2] = b_Sym_char_class("ch2", set(['e', 'f']), 2)
        nfaData.alphabet[3] = b_Sym_char("ch3", "g", 3)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (0,1,2) )
        nfaData.transitions.add( (1,2,1) )
        nfaData.transitions.add( (1,2,3) )
        nfaData.transitions.add( (1,3,4) )
        nfaData.final.add(3)
        nfaData.final.add(4)
        dfa = b_dfa()
        dfa.create_from_nfa_data(nfaData)
        dfa.determinise()

        nfaData_compare = nfa_data()
        nfaData_compare.states[0] = b_State(0,set())
        nfaData_compare.states[1] = b_State(1,set())
        nfaData_compare.states[2] = b_State(2,set())
        nfaData_compare.states[3] = b_State(3,set([0]))
        nfaData_compare.states[4] = b_State(4,set([1]))
        nfaData_compare.alphabet[0] = b_Sym_char_class("ch0", set(['a', 'b']), 0)
        nfaData_compare.alphabet[1] = b_Sym_char_class("ch1", set(['b', 'c']), 1)
        nfaData_compare.alphabet[2] = b_Sym_char_class("ch2", set(['e', 'f']), 2)
        nfaData_compare.alphabet[3] = b_Sym_char("ch3", "g", 3)
        nfaData_compare.start = 0
        nfaData_compare.transitions.add( (0,0,1) )
        nfaData_compare.transitions.add( (0,1,2) )
        nfaData_compare.transitions.add( (1,2,1) )
        nfaData_compare.transitions.add( (1,2,3) )
        nfaData_compare.transitions.add( (1,3,2) )
        nfaData_compare.final.add(3)
        nfaData_compare.final.add(4)
        dfa_compare = b_dfa()
        dfa_compare.create_from_nfa_data(nfaData_compare)
        dfa_compare.determinise()

        self.assertTrue(dfa.isomorphic(dfa_compare._automaton) == False)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_b_dfa)
    unittest.TextTestRunner(verbosity=2).run(suite)
