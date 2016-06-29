###############################################################################
#  test_b_automaton.py: Test module for PATTERN MATCH - test automaton class
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
from netbench.pattern_match.b_state import b_State
from netbench.pattern_match.parser import parser
from netbench.pattern_match.nfa_data import nfa_data
from netbench.pattern_match.sym_char import b_Sym_char
from netbench.pattern_match.sym_eof import b_Sym_EOF
from netbench.pattern_match.sym_char_class import b_Sym_char_class
from netbench.pattern_match.sym_kchar import b_Sym_kchar
from netbench.pattern_match.b_dfa import b_dfa
import os
import unittest
import copy

class test_b_Automaton(unittest.TestCase):
    """A base test class for the pattern matching approaches based on
    finite automaton."""

    def test_show(self):
        """show()"""
        # 5 regular expressions, manual nfa_data, manual dot files.
        # If the result of the method show () different from pre-built
        # file, an error occurred. In prepared machines should occur:
        #   - the transition from one state into multiple states,
        #   - the transition from multiple states into one state,
        #   - the loop (switch) back to the same state,
        #   - the transition back to the initial condition,
        #   - multiple transitions - two transitions entering and coming to the
        #     same state.

        # 1) Transition from one state to more states
        # RE a[bcd]
        aut1 = b_Automaton()
        nfa1 = aut1._automaton

        nfa1.states[0] = b_State(0,set())
        nfa1.states[1] = b_State(1,set())
        nfa1.states[2] = b_State(2,set([0]))
        nfa1.states[3] = b_State(3,set([0]))
        nfa1.states[4] = b_State(4,set([0]))

        nfa1.alphabet[0] = b_Sym_char("a", "a", 0)
        nfa1.alphabet[1] = b_Sym_char("b", "b", 1)
        nfa1.alphabet[2] = b_Sym_char("c", "c", 2)
        nfa1.alphabet[3] = b_Sym_char("d", "d", 3)

        nfa1.start = 0

        nfa1.transitions.add( (0,0,1) )
        nfa1.transitions.add( (1,1,2) )
        nfa1.transitions.add( (1,2,3) )
        nfa1.transitions.add( (1,3,4) )

        nfa1.final.add(2)
        nfa1.final.add(3)
        nfa1.final.add(4)

        aut1.show("test_data/gen_aut1.dot")

        with open("test_data/gen_aut1.dot") as gen_dot1:
            with open("test_data/hand_aut1.dot") as hand_dot1:
                self.assertTrue(gen_dot1.readlines() == hand_dot1.readlines())
        os.unlink("test_data/gen_aut1.dot")

        # 2) Transition from many states to one state
        # RE a[bcd]e
        aut2 = b_Automaton()
        nfa2 = aut2._automaton

        nfa2.states[0] = b_State(0,set())
        nfa2.states[1] = b_State(1,set())
        nfa2.states[2] = b_State(2,set())
        nfa2.states[3] = b_State(3,set())
        nfa2.states[4] = b_State(4,set())
        nfa2.states[5] = b_State(5,set([0]))

        nfa2.alphabet[0] = b_Sym_char("a", "a", 0)
        nfa2.alphabet[1] = b_Sym_char("b", "b", 1)
        nfa2.alphabet[2] = b_Sym_char("c", "c", 2)
        nfa2.alphabet[3] = b_Sym_char("d", "d", 3)
        nfa2.alphabet[4] = b_Sym_char("e", "e", 4)

        nfa2.start = 0

        nfa2.transitions.add( (0,0,1) )
        nfa2.transitions.add( (1,1,2) )
        nfa2.transitions.add( (1,2,3) )
        nfa2.transitions.add( (1,3,4) )
        nfa2.transitions.add( (2,4,5) )
        nfa2.transitions.add( (3,4,5) )
        nfa2.transitions.add( (4,4,5) )

        nfa2.final.add(5)

        aut2.show("test_data/gen_aut2.dot")

        with open("test_data/gen_aut2.dot") as gen_dot2:
            with open("test_data/hand_aut2.dot") as hand_dot2:
                self.assertTrue(gen_dot2.readlines() == hand_dot2.readlines())
        os.unlink("test_data/gen_aut2.dot")

        # 3) Loop (transition) back to the same state
        # RE a+
        aut3 = b_Automaton()
        nfa3 = aut3._automaton

        nfa3.states[0] = b_State(0,set())
        nfa3.states[1] = b_State(1,set([0]))

        nfa3.alphabet[0] = b_Sym_char("a", "a", 0)

        nfa3.start = 0

        nfa3.transitions.add( (0,0,1) )
        nfa3.transitions.add( (1,0,1) )

        nfa3.final.add(1)

        aut3.show("test_data/gen_aut3.dot")

        with open("test_data/gen_aut3.dot") as gen_dot3:
            with open("test_data/hand_aut3.dot") as hand_dot3:
                self.assertTrue(gen_dot3.readlines() == hand_dot3.readlines())
        os.unlink("test_data/gen_aut3.dot")

        # 4) The transition back to the initial state
        # RE
        aut4 = b_Automaton()
        nfa4 = aut4._automaton

        nfa4.states[0] = b_State(0,set())
        nfa4.states[1] = b_State(1,set())
        nfa4.states[2] = b_State(2,set([0]))

        nfa4.alphabet[0] = b_Sym_char("a", "a", 0)
        nfa4.alphabet[1] = b_Sym_char("b", "b", 1)
        nfa4.alphabet[2] = b_Sym_char("c", "c", 2)

        nfa4.start = 0

        nfa4.transitions.add( (0,0,1) )
        nfa4.transitions.add( (1,1,0) )
        nfa4.transitions.add( (1,2,2) )

        nfa4.final.add(2)

        aut4.show("test_data/gen_aut4.dot")

        with open("test_data/gen_aut4.dot") as gen_dot4:
            with open("test_data/hand_aut4.dot") as hand_dot4:
                self.assertTrue(gen_dot4.readlines() == hand_dot4.readlines())
        os.unlink("test_data/gen_aut4.dot")

        # 5) two transitions entering and coming to the same state
        # RE something like a[bc]*
        aut5 = b_Automaton()
        nfa5 = aut5._automaton

        nfa5.states[0] = b_State(0,set())
        nfa5.states[1] = b_State(1,set([0]))

        nfa5.alphabet[0] = b_Sym_char("a", "a", 0)
        nfa5.alphabet[1] = b_Sym_char("b", "b", 1)
        nfa5.alphabet[2] = b_Sym_char("c", "c", 2)

        nfa5.start = 0

        nfa5.transitions.add( (0,0,1) )
        nfa5.transitions.add( (1,1,1) )
        nfa5.transitions.add( (1,2,1) )

        nfa5.final.add(1)

        aut5.show("test_data/gen_aut5.dot")

        with open("test_data/gen_aut5.dot") as gen_dot5:
            with open("test_data/hand_aut5.dot") as hand_dot5:
                self.assertTrue(gen_dot5.readlines() == hand_dot5.readlines())
        os.unlink("test_data/gen_aut5.dot")

    def test_create_from_nfa_data(self):
        """create_from_nfa_data()"""
        # Automaton returned via call get_automaton() must match the predefined
        # nfa_data structure. The test is needed for different variants of
        # automaton:
        #   an empty machine,
        #   vending machine with one state without transition,
        #   a transition state with a single, normal machine.
        # It is necessary to implement both options: safe = True / False tests
        # and possibly interfere with the object being passed nfa_data.
        # With safe = False then any changes should be reflected.
        # With safe = True then changes must not occur.

        # 1) Empty automaton - True
        nfaData = nfa_data()
        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData, safe = True)

        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.final.add(1)

        cp = aut.get_automaton()

        self.assertTrue(cp.states == dict())
        self.assertTrue(cp.alphabet == dict())
        self.assertTrue(cp.start == -1)
        self.assertTrue(cp.final == set())
        self.assertTrue(cp.transitions == set())

        # 2) Empty automaton - False
        nfaData = nfa_data()
        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData, safe = False)

        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.final.add(1)

        cp = aut.get_automaton()

        self.assertTrue(sorted(cp.states.keys()) == [0, 1])
        self.assertTrue(sorted(cp.alphabet.keys()) == [0])
        self.assertTrue(cp.start == 0)
        self.assertTrue(cp.final == set([1]))
        self.assertTrue(cp.transitions == set([(0,0,1)]))

        # 3) Automaton with one state without transitions - True
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData, safe = True)

        nfaData.states[1] = b_State(1,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.final.add(1)

        cp = aut.get_automaton()

        self.assertTrue(sorted(cp.states.keys()) == [0])
        self.assertTrue(cp.alphabet == dict())
        self.assertTrue(cp.start == -1)
        self.assertTrue(cp.final == set())
        self.assertTrue(cp.transitions == set())

        # 4) Automaton with one state without transitions - False
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData, safe = False)

        nfaData.states[1] = b_State(1,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.final.add(1)

        cp = aut.get_automaton()

        self.assertTrue(sorted(cp.states.keys()) == [0, 1])
        self.assertTrue(sorted(cp.alphabet.keys()) == [0])
        self.assertTrue(cp.start == 0)
        self.assertTrue(cp.final == set([1]))
        self.assertTrue(cp.transitions == set([(0,0,1)]))

        # 5) One state with one transition - True
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.transitions.add( (0,0,1) )
        nfaData.start = 0
        nfaData.final.add(1)
        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData, safe = True)

        nfaData.states[2] = b_State(2,set([1]))
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.start = 1
        nfaData.transitions.add( (1,1,2) )
        nfaData.final.add(2)

        cp = aut.get_automaton()

        self.assertTrue(sorted(cp.states.keys()) == [0, 1])
        self.assertTrue(sorted(cp.alphabet.keys()) == [0])
        self.assertTrue(cp.start == 0)
        self.assertTrue(cp.final == set([1]))
        self.assertTrue(cp.transitions == set([(0,0,1)]))

        # 6) One state with one transition - False
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.transitions.add( (0,0,1) )
        nfaData.start = 0
        nfaData.final.add(1)
        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData, safe = False)

        nfaData.states[2] = b_State(2,set([1]))
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.start = 1
        nfaData.transitions.add( (1,1,2) )
        nfaData.final.add(2)

        cp = aut.get_automaton()

        self.assertTrue(sorted(cp.states.keys()) == [0, 1, 2])
        self.assertTrue(sorted(cp.alphabet.keys()) == [0, 1])
        self.assertTrue(cp.start == 1)
        self.assertTrue(cp.final == set([1, 2]))
        self.assertTrue(cp.transitions == set([(0,0,1), (1,1,2)]))

        # 7) Normal automaton - True
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set())
        nfaData.states[4] = b_State(4,set())
        nfaData.states[5] = b_State(5,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.alphabet[3] = b_Sym_char("d", "d", 3)
        nfaData.alphabet[4] = b_Sym_char("e", "e", 4)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (1,2,3) )
        nfaData.transitions.add( (1,3,4) )
        nfaData.transitions.add( (2,4,5) )
        nfaData.transitions.add( (3,4,5) )
        nfaData.transitions.add( (4,4,5) )
        nfaData.final.add(5)
        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData, safe = True)

        nfaData.states[6] = b_State(6,set([1]))
        nfaData.alphabet[5] = b_Sym_char("f", "f", 5)
        nfaData.start = 1
        nfaData.transitions.add( (4,5,6) )
        nfaData.final.add(6)

        cp = aut.get_automaton()

        self.assertTrue(sorted(cp.states.keys()) == [0, 1, 2, 3, 4, 5])
        self.assertTrue(sorted(cp.alphabet.keys()) == [0, 1, 2, 3, 4])
        self.assertTrue(cp.start == 0)
        self.assertTrue(cp.final == set([5]))
        self.assertTrue(cp.transitions == set([(0,0,1), (1,1,2), (1,2,3),
        (1,3,4), (2,4,5), (3,4,5), (4,4,5)]))

        # 8) Normal automaton - False
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set())
        nfaData.states[4] = b_State(4,set())
        nfaData.states[5] = b_State(5,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.alphabet[3] = b_Sym_char("d", "d", 3)
        nfaData.alphabet[4] = b_Sym_char("e", "e", 4)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (1,2,3) )
        nfaData.transitions.add( (1,3,4) )
        nfaData.transitions.add( (2,4,5) )
        nfaData.transitions.add( (3,4,5) )
        nfaData.transitions.add( (4,4,5) )
        nfaData.final.add(5)
        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData, safe = False)

        nfaData.states[6] = b_State(6,set([1]))
        nfaData.alphabet[5] = b_Sym_char("f", "f", 5)
        nfaData.start = 1
        nfaData.transitions.add( (4,5,6) )
        nfaData.final.add(6)

        cp = aut.get_automaton()

        self.assertTrue(sorted(cp.states.keys()) == [0, 1, 2, 3, 4, 5, 6])
        self.assertTrue(sorted(cp.alphabet.keys()) == [0, 1, 2, 3, 4, 5])
        self.assertTrue(cp.start == 1)
        self.assertTrue(cp.final == set([5, 6]))
        self.assertTrue(cp.transitions == set([(0,0,1), (1,1,2), (1,2,3),
        (1,3,4), (2,4,5), (3,4,5), (4,4,5), (4, 5, 6)]))

    def test_create_by_parser(self):
        """create_by_parser()"""
        # For 5 regular expressions are created by hand nfa_data structures to
        # match the algorithm. Using create_by_parser() and get_automaton()
        # creates and returns nfa_data for each regular term. Acquired nfa_data
        # structures are then compared with a manually created.

        # 1) RE concatenation
        par = parser("pcre_parser")
        par.set_text("/^ab/")
        aut = b_Automaton()
        aut.create_by_parser(par)
        cp = aut.get_automaton()

        act = nfa_data()
        act.states[0] = b_State(0,set([]))
        act.states[1] = b_State(1,set([]))
        act.states[2] = b_State(2,set([]))
        act.states[3] = b_State(3,set([0]))
        act.alphabet[0] = b_Sym_char("a", "a", 0)
        act.alphabet[1] = b_Sym_char("b", "b", 1)
        act.alphabet[-1] = b_Sym_char("Epsilon", "", -1)
        act.start = 0
        act.final.add(3)
        act.transitions.add( (0, 0, 1) )
        act.transitions.add( (1, -1, 2) )
        act.transitions.add( (2, 1, 3) )

        self.assertTrue(sorted(cp.states.keys()) == sorted(act.states.keys()))
        self.assertTrue(cp.alphabet == act.alphabet)
        self.assertTrue(cp.start == act.start)
        self.assertTrue(cp.final == act.final)
        self.assertTrue(cp.transitions == act.transitions)

        # 2) RE branched
        par = parser("pcre_parser")
        par.set_text("/^a/\n/^b/")
        aut = b_Automaton()
        aut.create_by_parser(par)
        cp = aut.get_automaton()
        
        act = nfa_data()
        act.states[0] = b_State(0,set())
        act.states[1] = b_State(1,set([0]))
        act.states[2] = b_State(2,set())
        act.states[3] = b_State(3,set([1]))
        act.states[4] = b_State(4,set())
        act.alphabet[0] = b_Sym_char("a", "a", 0)
        act.alphabet[1] = b_Sym_char("b", "b", 1)
        act.alphabet[-1] = b_Sym_char("Epsilon", "", -1)
        act.start = 4
        act.final.add(1)
        act.final.add(3)
        act.transitions.add( (4, -1, 0) )
        act.transitions.add( (4, -1, 2) )
        act.transitions.add( (0, 0, 1) )
        act.transitions.add( (2, 1, 3) )

        self.assertTrue(sorted(cp.states.keys()) == sorted(act.states.keys()))
        self.assertTrue(cp.alphabet == act.alphabet)
        self.assertTrue(cp.start == act.start)
        self.assertTrue(cp.final == act.final)
        self.assertTrue(cp.transitions == act.transitions)

        # 3) RE iteration
        par = parser("pcre_parser")
        par.set_text("/^a*/")
        aut = b_Automaton()
        aut.create_by_parser(par)
        cp = aut.get_automaton()

        act = nfa_data()
        act.states[0] = b_State(0,set())
        act.states[1] = b_State(1,set([0]))
        act.states[2] = b_State(2,set())
        act.states[3] = b_State(3,set())
        act.alphabet[0] = b_Sym_char("a", "a", 0)
        act.alphabet[-1] = b_Sym_char("Epsilon", "", -1)
        act.start = 0
        act.final.add(1)
        act.transitions.add( (0, -1, 1) )
        act.transitions.add( (0, -1, 2) )
        act.transitions.add( (2, 0, 3) )
        act.transitions.add( (3, -1, 1) )
        act.transitions.add( (3, -1, 2) )

        self.assertTrue(sorted(cp.states.keys()) == sorted(act.states.keys()))
        self.assertTrue(cp.alphabet == act.alphabet)
        self.assertTrue(cp.start == act.start)
        self.assertTrue(cp.final == act.final)
        self.assertTrue(cp.transitions == act.transitions)

        # 4) RE positive iteration
        par = parser("pcre_parser")
        par.set_text("/^a+/")
        aut = b_Automaton()
        aut.create_by_parser(par)
        cp = aut.get_automaton()

        act = nfa_data()
        act.states[0] = b_State(0,set())
        act.states[1] = b_State(1,set([0]))
        act.alphabet[0] = b_Sym_char("a", "a", 0)
        act.alphabet[-1] = b_Sym_char("Epsilon", "", -1)
        act.start = 0
        act.final.add(1)
        act.transitions.add( (0, 0, 1) )
        act.transitions.add( (1, -1, 0) )

        self.assertTrue(sorted(cp.states.keys()) == sorted(act.states.keys()))
        self.assertTrue(cp.alphabet == act.alphabet)
        self.assertTrue(cp.start == act.start)
        self.assertTrue(cp.final == act.final)
        self.assertTrue(cp.transitions == act.transitions)

        # 5) RE taste everything
        par = parser("pcre_parser")
        par.set_text("/^a[bc]e?.f{3}/")
        aut = b_Automaton()
        aut.create_by_parser(par)
        cp = aut.get_automaton()

        aux = nfa_data()
        act = aux.load_from_file("test_data/RE_vseho_chut.nfa_data")

        self.assertTrue(sorted(cp.states.keys()) == sorted(act.states.keys()))
        self.assertTrue(cp.alphabet == act.alphabet)
        self.assertTrue(cp.start == act.start)
        self.assertTrue(cp.final == act.final)
        self.assertTrue(cp.transitions == act.transitions)

    def test_join(self):
        """join()"""
        # Manual is prepared nfa_data structures over which they will perform
        # tests. At the same time, the connection manually nfa_data structures
        # for potentially problematic pairs nfa_data structures. The potentially
        # problematic pair nfa_data structures applied method join() and
        # compared with manually nfa_data related structures. Mergers need to
        # focus on machines with:
        #   loop in the initial or end state,
        #   one machine is the prefix / suffix second machine.

        # 1) RE ab
        #    RE cd
        RE_ab = nfa_data().load_from_file("test_data/RE_ab.nfa_data")
        RE_cd = nfa_data().load_from_file("test_data/RE_cd.nfa_data")

        aut = b_Automaton()
        aut.create_from_nfa_data(RE_ab)
        aut.join(RE_cd)
        cp = aut.get_automaton()
        act = nfa_data().load_from_file("test_data/join_RE_abcd.nfa_data")

        self.assertTrue(sorted(cp.states.keys()) == sorted(act.states.keys()))
        self.assertTrue(cp.alphabet == act.alphabet)
        self.assertTrue(cp.start == act.start)
        self.assertTrue(cp.final == act.final)
        self.assertTrue(cp.transitions == act.transitions)

        # 2) RE loop in the initial and final state
        RE_ab_smycka = nfa_data().load_from_file( \
        "test_data/RE_d(smycka)_ab_c(smycka).nfa_data")
        RE_ef_smycka = nfa_data().load_from_file( \
        "test_data/RE_h(smycka)_ef_g(smycka).nfa_data")

        aut = b_Automaton()
        aut.create_from_nfa_data(RE_ab_smycka)
        aut.join(RE_ef_smycka)
        cp = aut.get_automaton()
        act = nfa_data().load_from_file("test_data/join_RE_abef_smycky.nfa_data")

        self.assertTrue(sorted(cp.states.keys()) == sorted(act.states.keys()))
        self.assertTrue(cp.alphabet == act.alphabet)
        self.assertTrue(cp.start == act.start)
        self.assertTrue(cp.final == act.final)
        self.assertTrue(cp.transitions == act.transitions)

        # 3) prefix/suffix
        # RE abcd, RE ab, RE cd
        RE_ab = nfa_data().load_from_file("test_data/RE_ab.nfa_data")
        RE_cd = nfa_data().load_from_file("test_data/RE_cd.nfa_data")
        RE_abcd = nfa_data()
        RE_abcd.states[0] = b_State(0,set())
        RE_abcd.states[1] = b_State(1,set())
        RE_abcd.states[2] = b_State(2,set())
        RE_abcd.states[3] = b_State(3,set())
        RE_abcd.states[4] = b_State(4,set([0]))
        RE_abcd.alphabet[0] = b_Sym_char("a", "a", 0)
        RE_abcd.alphabet[1] = b_Sym_char("b", "b", 1)
        RE_abcd.alphabet[2] = b_Sym_char("c", "c", 2)
        RE_abcd.alphabet[3] = b_Sym_char("d", "d", 3)
        RE_abcd.start = 0
        RE_abcd.final.add(4)
        RE_abcd.transitions.add( (0, 0, 1) )
        RE_abcd.transitions.add( (1, 1, 2) )
        RE_abcd.transitions.add( (2, 2, 3) )
        RE_abcd.transitions.add( (3, 3, 4) )

        aut = b_Automaton()
        aut.create_from_nfa_data(RE_abcd)
        aut.join(RE_ab)
        aut.join(RE_cd)
        cp = aut.get_automaton()
        act = nfa_data().load_from_file("test_data/join_RE_abcd_ab_cd.nfa_data")

        self.assertTrue(sorted(cp.states.keys()) == sorted(act.states.keys()))
        self.assertTrue(cp.alphabet == act.alphabet)
        self.assertTrue(cp.start == act.start)
        self.assertTrue(cp.final == act.final)
        self.assertTrue(cp.transitions == act.transitions)

    def test_remove_epsilons(self):
        """remove_epsilons()"""
        # For ready nfa_data need to know how they will look after the resulting
        # remove_epsilons(). Test machines (nfa_data) should affect:
        #   - two epsilon transitions from one state to different states,
        #   - epsilon transition to the state from which the epsilon transition,
        #   - epsilon transition as a cycle within a single state (the same
        #     output as the output state),
        #   - epsilon transition in the machine backwards,
        #   - the machine is connected cycle of epsilon transitions.

        # 1) two epsilon transitions from one state to various state
        RE_a_b = nfa_data()
        RE_a_b.states[0] = b_State(0,set())
        RE_a_b.states[1] = b_State(1,set())
        RE_a_b.states[2] = b_State(2,set())
        RE_a_b.states[3] = b_State(3,set())
        RE_a_b.states[4] = b_State(4,set())
        RE_a_b.states[5] = b_State(5,set([0]))
        RE_a_b.alphabet[0] = b_Sym_char("a", "a", 0)
        RE_a_b.alphabet[1] = b_Sym_char("b", "b", 1)
        RE_a_b.alphabet[-1] = b_Sym_char("Epsilon", "", -1)
        RE_a_b.start = 0
        RE_a_b.final.add(5)
        RE_a_b.transitions.add( (0, -1, 1) )
        RE_a_b.transitions.add( (0, -1, 2) )
        RE_a_b.transitions.add( (1, 0, 3) )
        RE_a_b.transitions.add( (2, 1, 4) )
        RE_a_b.transitions.add( (3, -1, 5) )
        RE_a_b.transitions.add( (4, -1, 5) )

        aut = b_Automaton()
        aut.create_from_nfa_data(RE_a_b)
        aut.remove_epsilons()
        cp = aut.get_automaton()

        # nfa data to compare without epsilon
        act = nfa_data()
        act.states[0] = b_State(0,set())
        act.states[3] = b_State(3,set([0]))
        act.states[4] = b_State(4,set([0]))
        act.alphabet[0] = b_Sym_char("a", "a", 0)
        act.alphabet[1] = b_Sym_char("b", "b", 1)
        act.start = 0
        act.final.add(3)
        act.final.add(4)
        act.transitions.add( (0, 0, 3) )
        act.transitions.add( (0, 1, 4) )
        act.Flags["Epsilon Free"] = True

        self.assertTrue(sorted(cp.states.keys()) == sorted(act.states.keys()))
        self.assertTrue(cp.alphabet == act.alphabet)
        self.assertTrue(cp.start == act.start)
        self.assertTrue(cp.final == act.final)
        self.assertTrue(cp.transitions == act.transitions)
        self.assertTrue(cp.Flags == act.Flags)

        # 2) epsilon transition to the state of which is also epsilon transition
        RE_a = nfa_data()
        RE_a.states[0] = b_State(0,set())
        RE_a.states[1] = b_State(1,set())
        RE_a.states[2] = b_State(2,set())
        RE_a.states[3] = b_State(3,set())
        RE_a.states[4] = b_State(4,set())
        RE_a.states[5] = b_State(5,set([0]))
        RE_a.alphabet[0] = b_Sym_char("a", "a", 0)
        RE_a.alphabet[-1] = b_Sym_char("Epsilon", "", -1)
        RE_a.start = 0
        RE_a.final.add(5)
        RE_a.transitions.add( (0, -1, 1) )
        RE_a.transitions.add( (1, -1, 2) )
        RE_a.transitions.add( (2, 0, 3) )
        RE_a.transitions.add( (3, -1, 4) )
        RE_a.transitions.add( (4, -1, 5) )

        aut = b_Automaton()
        aut.create_from_nfa_data(RE_a)
        aut.remove_epsilons()
        cp = aut.get_automaton()

        # nfa data to compare without epsilon
        act = nfa_data()
        act.states[0] = b_State(0,set())
        act.states[3] = b_State(3,set([0]))
        act.alphabet[0] = b_Sym_char("a", "a", 0)
        act.start = 0
        act.final.add(3)
        act.transitions.add( (0, 0, 3) )
        act.Flags["Epsilon Free"] = True

        self.assertTrue(sorted(cp.states.keys()) == sorted(act.states.keys()))
        self.assertTrue(cp.alphabet == act.alphabet)
        self.assertTrue(cp.start == act.start)
        self.assertTrue(cp.final == act.final)
        self.assertTrue(cp.transitions == act.transitions)
        self.assertTrue(cp.Flags == act.Flags)

        # 3) epsilon transition, as a cycle within a single state (the same
        #    output and the output state)
        RE_a = nfa_data()
        RE_a.states[0] = b_State(0,set())
        RE_a.states[1] = b_State(1,set())
        RE_a.states[2] = b_State(2,set())
        RE_a.states[3] = b_State(3,set([0]))
        RE_a.alphabet[0] = b_Sym_char("a", "a", 0)
        RE_a.alphabet[-1] = b_Sym_char("Epsilon", "", -1)
        RE_a.start = 0
        RE_a.final.add(3)
        RE_a.transitions.add( (0, -1, 1) )
        RE_a.transitions.add( (1, -1, 1) )
        RE_a.transitions.add( (1, -1, 2) )
        RE_a.transitions.add( (2, 0, 3) )

        aut = b_Automaton()
        aut.create_from_nfa_data(RE_a)
        aut.remove_epsilons()
        cp = aut.get_automaton()

        # nfa data to compare without epsilon
        act = nfa_data()
        act.states[0] = b_State(0,set())
        act.states[3] = b_State(3,set([0]))
        act.alphabet[0] = b_Sym_char("a", "a", 0)
        act.start = 0
        act.final.add(3)
        act.transitions.add( (0, 0, 3) )
        act.Flags["Epsilon Free"] = True

        self.assertTrue(sorted(cp.states.keys()) == sorted(act.states.keys()))
        self.assertTrue(cp.alphabet == act.alphabet)
        self.assertTrue(cp.start == act.start)
        self.assertTrue(cp.final == act.final)
        self.assertTrue(cp.transitions == act.transitions)
        self.assertTrue(cp.Flags == act.Flags)

        # 4) epsilon transition in the machine direction back
        RE_a = nfa_data()
        RE_a.states[0] = b_State(0,set())
        RE_a.states[1] = b_State(1,set())
        RE_a.states[2] = b_State(2,set())
        RE_a.states[3] = b_State(3,set([0]))
        RE_a.alphabet[0] = b_Sym_char("a", "a", 0)
        RE_a.alphabet[-1] = b_Sym_char("Epsilon", "", -1)
        RE_a.start = 0
        RE_a.final.add(3)
        RE_a.transitions.add( (0, -1, 1) )
        RE_a.transitions.add( (1, -1, 2) )
        RE_a.transitions.add( (2, -1, 1) )
        RE_a.transitions.add( (2, 0, 3) )

        aut = b_Automaton()
        aut.create_from_nfa_data(RE_a)
        aut.remove_epsilons()
        cp = aut.get_automaton()

        # nfa data to compare without epsilon
        act = nfa_data()
        act.states[0] = b_State(0,set())
        act.states[3] = b_State(3,set([0]))
        act.alphabet[0] = b_Sym_char("a", "a", 0)
        act.start = 0
        act.final.add(3)
        act.transitions.add( (0, 0, 3) )
        act.Flags["Epsilon Free"] = True

        self.assertTrue(sorted(cp.states.keys()) == sorted(act.states.keys()))
        self.assertTrue(cp.alphabet == act.alphabet)
        self.assertTrue(cp.start == act.start)
        self.assertTrue(cp.final == act.final)
        self.assertTrue(cp.transitions == act.transitions)
        self.assertTrue(cp.Flags == act.Flags)

        # 5) the machine have cycle from epsilon transitions
        RE_a = nfa_data()
        RE_a.states[0] = b_State(0,set())
        RE_a.states[1] = b_State(1,set())
        RE_a.states[2] = b_State(2,set())
        RE_a.states[3] = b_State(3,set())
        RE_a.states[4] = b_State(4,set([0]))
        RE_a.alphabet[0] = b_Sym_char("a", "a", 0)
        RE_a.alphabet[-1] = b_Sym_char("Epsilon", "", -1)
        RE_a.start = 0
        RE_a.final.add(4)
        RE_a.transitions.add( (0, -1, 1) )
        RE_a.transitions.add( (1, -1, 2) )
        RE_a.transitions.add( (2, -1, 3) )
        RE_a.transitions.add( (3, -1, 0) )
        RE_a.transitions.add( (2, 0, 4) )

        aut = b_Automaton()
        aut.create_from_nfa_data(RE_a)
        aut.remove_epsilons()
        cp = aut.get_automaton()

        # nfa data to compare without epsilon
        act = nfa_data()
        act.states[0] = b_State(0,set())
        act.states[4] = b_State(4,set([0]))
        act.alphabet[0] = b_Sym_char("a", "a", 0)
        act.start = 0
        act.final.add(4)
        act.transitions.add( (0, 0, 4) )
        act.Flags["Epsilon Free"] = True

        self.assertTrue(sorted(cp.states.keys()) == sorted(act.states.keys()))
        self.assertTrue(cp.alphabet == act.alphabet)
        self.assertTrue(cp.start == act.start)
        self.assertTrue(cp.final == act.final)
        self.assertTrue(cp.transitions == act.transitions)
        self.assertTrue(cp.Flags == act.Flags)

    def test_remove_unreachable(self):
        """remove_unreachable"""
        # For ready nfa_data need to know how they will look after the resulting
        # remove_unreachable(). Test machines (nfa_data) should affect:
        #   - automata with isolated states into which is not coming any
        #     transitions,
        #   - automaton contain under-automaton that is not available from the
        #     initial state, but each state leads to a transition,
        #   - delete way which do not lead to finite state,
        #   - do not exist way to finite state -> empty automaton,
        #   - do not exist way to someone finite state -> remove this alone
        #     finite state
        #   - exist way to someone finite state but not from begin -> remove
        #     this alone finite way

        # 1) machine with isolated states in which there is no transitions
        RE_ab = nfa_data()
        RE_ab.states[0] = b_State(0,set())
        RE_ab.states[1] = b_State(1,set())
        RE_ab.states[2] = b_State(2,set())
        RE_ab.states[3] = b_State(3,set([0]))
        RE_ab.states[4] = b_State(4,set())
        RE_ab.states[5] = b_State(5,set())
        RE_ab.alphabet[0] = b_Sym_char("a", "a", 0)
        RE_ab.alphabet[1] = b_Sym_char("b", "b", 1)
        RE_ab.alphabet[-1] = b_Sym_char("Epsilon", "", -1)
        RE_ab.start = 0
        RE_ab.final.add(3)
        RE_ab.transitions.add( (0, -1, 1) )
        RE_ab.transitions.add( (1, 0, 4) )
        RE_ab.transitions.add( (4, 1, 3) )

        aut = b_Automaton()
        aut.create_from_nfa_data(RE_ab)
        aut.remove_unreachable()
        cp = aut.get_automaton()

        # nfa data to compare without epsilon
        act = nfa_data()
        act.states[0] = b_State(0,set())
        act.states[1] = b_State(1,set())
        act.states[3] = b_State(3,set([0]))
        act.states[4] = b_State(4,set())
        act.alphabet[0] = b_Sym_char("a", "a", 0)
        act.alphabet[1] = b_Sym_char("b", "b", 1)
        act.alphabet[-1] = b_Sym_char("Epsilon", "", -1)
        act.start = 0
        act.final.add(3)
        act.transitions.add( (0, -1, 1) )
        act.transitions.add( (1, 0, 4) )
        act.transitions.add( (4, 1, 3) )

        self.assertTrue(sorted(cp.states.keys()) == sorted(act.states.keys()))
        self.assertTrue(cp.alphabet == act.alphabet)
        self.assertTrue(cp.start == act.start)
        self.assertTrue(cp.final == act.final)
        self.assertTrue(cp.transitions == act.transitions)
        self.assertTrue(cp.Flags == act.Flags)

        # 2) the machine that is not available from the initial state, but each
        #    state leads to some transition
        RE_ab_cd = nfa_data()
        RE_ab_cd.states[0] = b_State(0,set())
        RE_ab_cd.states[1] = b_State(1,set())
        RE_ab_cd.states[2] = b_State(2,set())
        RE_ab_cd.states[3] = b_State(3,set([0]))
        RE_ab_cd.states[4] = b_State(4,set())
        RE_ab_cd.states[5] = b_State(5,set())
        RE_ab_cd.states[6] = b_State(6,set([0]))
        RE_ab_cd.alphabet[0] = b_Sym_char("a", "a", 0)
        RE_ab_cd.alphabet[1] = b_Sym_char("b", "b", 1)
        RE_ab_cd.alphabet[2] = b_Sym_char("c", "c", 2)
        RE_ab_cd.alphabet[3] = b_Sym_char("d", "d", 3)
        RE_ab_cd.alphabet[-1] = b_Sym_char("Epsilon", "", -1)
        RE_ab_cd.start = 0
        RE_ab_cd.final.add(3)
        RE_ab_cd.final.add(6)
        RE_ab_cd.transitions.add( (0, -1, 1) )
        RE_ab_cd.transitions.add( (1, 0, 4) )
        RE_ab_cd.transitions.add( (4, 1, 3) )
        RE_ab_cd.transitions.add( (2, 2, 2) )
        RE_ab_cd.transitions.add( (2, 3, 5) )
        RE_ab_cd.transitions.add( (5, -1, 5) )
        RE_ab_cd.transitions.add( (5, -1, 6) )

        aut = b_Automaton()
        aut.create_from_nfa_data(RE_ab_cd)
        aut.remove_unreachable()
        cp = aut.get_automaton()

        # nfa data to compare without epsilon
        act = nfa_data()
        act.states[0] = b_State(0,set())
        act.states[1] = b_State(1,set())
        act.states[3] = b_State(3,set([0]))
        act.states[4] = b_State(4,set())
        act.alphabet[0] = b_Sym_char("a", "a", 0)
        act.alphabet[1] = b_Sym_char("b", "b", 1)
        act.alphabet[-1] = b_Sym_char("Epsilon", "", -1)
        act.start = 0
        act.final.add(3)
        act.transitions.add( (0, -1, 1) )
        act.transitions.add( (1, 0, 4) )
        act.transitions.add( (4, 1, 3) )

        self.assertTrue(sorted(cp.states.keys()) == sorted(act.states.keys()))
        self.assertTrue(cp.alphabet == act.alphabet)
        self.assertTrue(cp.start == act.start)
        self.assertTrue(cp.final == act.final)
        self.assertTrue(cp.transitions == act.transitions)
        self.assertTrue(cp.Flags == act.Flags)

        # 3) delete way which do not lead to finite state
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set())
        nfaData.states[4] = b_State(4,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,0,2) )
        nfaData.transitions.add( (2,0,3) )
        nfaData.transitions.add( (1,0,4) )
        nfaData.final.add(4)

        act = b_Automaton()
        act.create_from_nfa_data(nfaData)
        act.remove_unreachable()
        cp = act.get_automaton()

        result = nfa_data()
        result.states[0] = b_State(0,set())
        result.states[1] = b_State(1,set())
        result.states[4] = b_State(4,set([0]))
        result.alphabet[0] = b_Sym_char("a", "a", 0)
        result.start = 0
        result.transitions.add( (0,0,1) )
        result.transitions.add( (1,0,4) )
        result.final.add(4)

        self.assertTrue(sorted(cp.states.keys()) == sorted(result.states.keys()))
        self.assertTrue(cp.alphabet == result.alphabet)
        self.assertTrue(cp.start == result.start)
        self.assertTrue(cp.final == result.final)
        self.assertTrue(cp.transitions == result.transitions)
        self.assertTrue(cp.Flags == result.Flags)

        # 4) do not exist way to finite state -> empty automaton
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set())
        nfaData.states[4] = b_State(4,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,0,2) )
        nfaData.transitions.add( (2,0,3) )
        nfaData.final.add(4)

        act = b_Automaton()
        act.create_from_nfa_data(nfaData)
        act.remove_unreachable()
        cp = act.get_automaton()

        result = nfa_data()

        self.assertTrue(sorted(cp.states.keys()) == sorted(result.states.keys()))
        self.assertTrue(cp.alphabet == result.alphabet)
        self.assertTrue(cp.start == result.start)
        self.assertTrue(cp.final == result.final)
        self.assertTrue(cp.transitions == result.transitions)
        self.assertTrue(cp.Flags == result.Flags)

        # 5) do not exist way to someone finite state -> remove this alone
        #    finite state
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set())
        nfaData.states[4] = b_State(4,set([0]))
        nfaData.states[5] = b_State(5,set([1]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,0,2) )
        nfaData.transitions.add( (2,0,3) )
        nfaData.transitions.add( (3,0,4) )
        nfaData.final.add(4)
        nfaData.final.add(5)

        act = b_Automaton()
        act.create_from_nfa_data(nfaData)
        act.remove_unreachable()
        cp = act.get_automaton()

        result = nfa_data()
        result.states[0] = b_State(0,set())
        result.states[1] = b_State(1,set())
        result.states[2] = b_State(2,set())
        result.states[3] = b_State(3,set())
        result.states[4] = b_State(4,set([0]))
        result.alphabet[0] = b_Sym_char("a", "a", 0)
        result.start = 0
        result.transitions.add( (0,0,1) )
        result.transitions.add( (1,0,2) )
        result.transitions.add( (2,0,3) )
        result.transitions.add( (3,0,4) )
        result.final.add(4)

        self.assertTrue(sorted(cp.states.keys()) == sorted(result.states.keys()))
        self.assertTrue(cp.alphabet == result.alphabet)
        self.assertTrue(cp.start == result.start)
        self.assertTrue(cp.final == result.final)
        self.assertTrue(cp.transitions == result.transitions)
        self.assertTrue(cp.Flags == result.Flags)

        # 6) exist way to someone finite state but not from begin -> remove this
        # alone finite way
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set())
        nfaData.states[4] = b_State(4,set([0]))
        nfaData.states[5] = b_State(5,set([1]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,0,4) )
        nfaData.transitions.add( (2,0,3) )
        nfaData.transitions.add( (3,0,5) )
        nfaData.final.add(4)
        nfaData.final.add(5)

        act = b_Automaton()
        act.create_from_nfa_data(nfaData)
        act.remove_unreachable()
        cp = act.get_automaton()

        result = nfa_data()
        result.states[0] = b_State(0,set())
        result.states[1] = b_State(1,set())
        result.states[4] = b_State(4,set([0]))
        result.alphabet[0] = b_Sym_char("a", "a", 0)
        result.start = 0
        result.transitions.add( (0,0,1) )
        result.transitions.add( (1,0,4) )
        result.final.add(4)

        self.assertTrue(sorted(cp.states.keys()) == sorted(result.states.keys()))
        self.assertTrue(cp.alphabet == result.alphabet)
        self.assertTrue(cp.start == result.start)
        self.assertTrue(cp.final == result.final)
        self.assertTrue(cp.transitions == result.transitions)
        self.assertTrue(cp.Flags == result.Flags)

    def test_search(self):
        """search()"""
        # Nfa_data ready for input text and is needed to determine if the text
        # were found correct patterns. The test should be applied for at least
        # two machines, which are all typical structures such as:
        #   branching states,
        #   the cycle in one or more states or nondeterminism in certain states.

        # 1) RE a*e[fg]*
        #    RE abb
        #    RE acc
        act = nfa_data()
        act.states[0] = b_State(0,set())
        act.states[1] = b_State(1,set())
        act.states[2] = b_State(2,set())
        act.states[3] = b_State(3,set())
        act.states[4] = b_State(4,set())
        act.states[5] = b_State(5,set([0]))
        act.states[6] = b_State(6,set([1]))
        act.states[7] = b_State(7,set([2]))
        act.alphabet[0] = b_Sym_char("a", "a", 0)
        act.alphabet[1] = b_Sym_char("b", "b", 1)
        act.alphabet[2] = b_Sym_char("c", "c", 2)
        act.alphabet[3] = b_Sym_char("e", "e", 3)
        act.alphabet[4] = b_Sym_char("f", "f", 4)
        act.alphabet[5] = b_Sym_char("g", "g", 5)
        act.alphabet[-1] = b_Sym_char("Epsilon", "", -1)
        act.start = 0
        act.final.add(5)
        act.final.add(6)
        act.final.add(7)
        act.transitions.add( (0, -1, 1) )
        act.transitions.add( (1, 0, 1) )
        act.transitions.add( (1, 3, 5) )
        act.transitions.add( (5, 4, 5) )
        act.transitions.add( (5, 5, 5) )
        act.transitions.add( (0, 0, 2) )
        act.transitions.add( (2, 1, 3) )
        act.transitions.add( (2, 2, 4) )
        act.transitions.add( (3, 1, 6) )
        act.transitions.add( (4, 2, 7) )

        aut = b_Automaton()
        aut.create_from_nfa_data(act)

        self.assertTrue(aut.search("abb") == [0,1,0])
        self.assertTrue(aut.search("acc") == [0,0,1])
        self.assertTrue(aut.search("abbb") == [0,1,0])
        self.assertTrue(aut.search("accc") == [0,0,1])
        self.assertTrue(aut.search("e") == [1,0,0])
        self.assertTrue(aut.search("a") == [0,0,0])
        self.assertTrue(aut.search("aaaaaaaefffff") == [1,0,0])
        self.assertTrue(aut.search("eggggggg") == [1,0,0])
        self.assertTrue(aut.search("aefgfggggfffg") == [1,0,0])

        # 2) RE abc+
        #    RE abde
        #    RE abd*d
        act = nfa_data()
        act.states[0] = b_State(0,set())
        act.states[1] = b_State(1,set())
        act.states[2] = b_State(2,set())
        act.states[3] = b_State(3,set([0]))
        act.states[4] = b_State(4,set())
        act.states[5] = b_State(5,set([1]))
        act.states[6] = b_State(6,set())
        act.states[7] = b_State(7,set())
        act.states[8] = b_State(8,set([2]))
        act.alphabet[0] = b_Sym_char("a", "a", 0)
        act.alphabet[1] = b_Sym_char("b", "b", 1)
        act.alphabet[2] = b_Sym_char("c", "c", 2)
        act.alphabet[3] = b_Sym_char("d", "d", 3)
        act.alphabet[4] = b_Sym_char("e", "e", 4)
        act.alphabet[-1] = b_Sym_char("Epsilon", "", -1)
        act.start = 0
        act.final.add(3)
        act.final.add(5)
        act.final.add(8)
        act.transitions.add( (0, 0, 1) )
        act.transitions.add( (1, 1, 2) )
        act.transitions.add( (2, 2, 3) )
        act.transitions.add( (3, 2, 3) )
        act.transitions.add( (2, 3, 4) )
        act.transitions.add( (4, 4, 5) )
        act.transitions.add( (1, 1, 6) )
        act.transitions.add( (6, 3, 6) )
        act.transitions.add( (6, -1, 7) )
        act.transitions.add( (7, 3, 8) )

        aut = b_Automaton()
        aut.create_from_nfa_data(act)

        self.assertTrue(aut.search("") == [0,0,0])
        self.assertTrue(aut.search("a") == [0,0,0])
        self.assertTrue(aut.search("abc") == [1,0,0])
        self.assertTrue(aut.search("abccccccc") == [1,0,0])
        self.assertTrue(aut.search("abccccccccc a c") == [1,0,0])
        self.assertTrue(aut.search("abd") == [0,0,1])
        self.assertTrue(aut.search("abddddddddd") == [0,0,1])
        self.assertTrue(aut.search("abde") == [0,1,1])
        
        # Test with EOF
        # 3) RE a*e[fg]*
        #    RE abb$
        #    RE acc$
        act = nfa_data()
        act.states[0] = b_State(0,set())
        act.states[1] = b_State(1,set())
        act.states[2] = b_State(2,set())
        act.states[3] = b_State(3,set())
        act.states[4] = b_State(4,set())
        act.states[5] = b_State(5,set([0]))
        act.states[6] = b_State(6,set())
        act.states[7] = b_State(7,set())
        act.states[8] = b_State(8,set([1]))
        act.states[9] = b_State(9,set([2]))
        act.alphabet[0] = b_Sym_char("a", "a", 0)
        act.alphabet[1] = b_Sym_char("b", "b", 1)
        act.alphabet[2] = b_Sym_char("c", "c", 2)
        act.alphabet[3] = b_Sym_char("e", "e", 3)
        act.alphabet[4] = b_Sym_char("f", "f", 4)
        act.alphabet[5] = b_Sym_char("g", "g", 5)
        act.alphabet[6] = b_Sym_EOF("EOF",6)
        act.alphabet[-1] = b_Sym_char("Epsilon", "", -1)
        act.start = 0
        act.final.add(5)
        act.final.add(8)
        act.final.add(9)
        act.transitions.add( (0, -1, 1) )
        act.transitions.add( (1, 0, 1) )
        act.transitions.add( (1, 3, 5) )
        act.transitions.add( (5, 4, 5) )
        act.transitions.add( (5, 5, 5) )
        act.transitions.add( (0, 0, 2) )
        act.transitions.add( (2, 1, 3) )
        act.transitions.add( (2, 2, 4) )
        act.transitions.add( (3, 1, 6) )
        act.transitions.add( (4, 2, 7) )
        act.transitions.add( (6, 6, 8) )
        act.transitions.add( (7, 6, 9) )
        
        aut = b_Automaton()
        aut.create_from_nfa_data(act)

        self.assertTrue(aut.search("abb") == [0,1,0])
        self.assertTrue(aut.search("acc") == [0,0,1])
        self.assertTrue(aut.search("e") == [1,0,0])
        self.assertTrue(aut.search("a") == [0,0,0])
        self.assertTrue(aut.search("aaaaaaaefffff") == [1,0,0])
        self.assertTrue(aut.search("eggggggg") == [1,0,0])
        self.assertTrue(aut.search("aefgfggggfffg") == [1,0,0])
        self.assertTrue(aut.search("abbb") == [0,0,0])
        self.assertTrue(aut.search("accc") == [0,0,0])
        
        # Test with strided EOF
        # 4) RE a*e[fg]*
        #    RE abb$
        #    RE acc$
        act = nfa_data()
        act.states[0] = b_State(0,set())
        act.states[1] = b_State(1,set())
        act.states[2] = b_State(2,set())
        act.states[3] = b_State(3,set())
        act.states[4] = b_State(4,set())
        act.states[5] = b_State(5,set([0]))
        act.states[6] = b_State(6,set())
        act.states[7] = b_State(7,set())
        act.states[8] = b_State(8,set([1]))
        act.states[9] = b_State(9,set([2]))
        act.alphabet[0] = b_Sym_char("a", "a", 0)
        act.alphabet[1] = b_Sym_char("b", "b", 1)
        act.alphabet[2] = b_Sym_char("c", "c", 2)
        act.alphabet[3] = b_Sym_char("e", "e", 3)
        act.alphabet[4] = b_Sym_char("f", "f", 4)
        act.alphabet[5] = b_Sym_char("g", "g", 5)
        act.alphabet[6] = b_Sym_EOF("EOF",6)
        act.alphabet[-1] = b_Sym_char("Epsilon", "", -1)
        act.start = 0
        act.final.add(5)
        act.final.add(8)
        act.final.add(9)
        act.transitions.add( (0, -1, 1) )
        act.transitions.add( (1, 0, 1) )
        act.transitions.add( (1, 3, 5) )
        act.transitions.add( (5, 4, 5) )
        act.transitions.add( (5, 5, 5) )
        act.transitions.add( (0, 0, 2) )
        act.transitions.add( (2, 1, 3) )
        act.transitions.add( (2, 2, 4) )
        act.transitions.add( (3, 1, 6) )
        act.transitions.add( (4, 2, 7) )
        act.transitions.add( (6, 6, 8) )
        act.transitions.add( (7, 6, 9) )
        
        aut = b_Automaton()
        aut.create_from_nfa_data(act)
        aut.remove_epsilons()
        aut.stride_2()
        aut.stride_2()
        
        self.assertTrue(aut.search("abb") == [0,1,0])
        self.assertTrue(aut.search("acc") == [0,0,1])
        self.assertTrue(aut.search("e") == [1,0,0])
        self.assertTrue(aut.search("a") == [0,0,0])
        self.assertTrue(aut.search("aaaaaaaefffff") == [1,0,0])
        self.assertTrue(aut.search("eggggggg") == [1,0,0])
        self.assertTrue(aut.search("aefgfggggfffg") == [1,0,0])
        self.assertTrue(aut.search("abbb") == [0,0,0])
        self.assertTrue(aut.search("accc") == [0,0,0])
        
        # Test with strided automaton
        # 5) RE abc+
        #    RE abde
        #    RE abd*d
        act = nfa_data()
        act.states[0] = b_State(0,set())
        act.states[1] = b_State(1,set())
        act.states[2] = b_State(2,set())
        act.states[3] = b_State(3,set([0]))
        act.states[4] = b_State(4,set())
        act.states[5] = b_State(5,set([1]))
        act.states[6] = b_State(6,set())
        act.states[7] = b_State(7,set())
        act.states[8] = b_State(8,set([2]))
        act.alphabet[0] = b_Sym_char("a", "a", 0)
        act.alphabet[1] = b_Sym_char("b", "b", 1)
        act.alphabet[2] = b_Sym_char("c", "c", 2)
        act.alphabet[3] = b_Sym_char("d", "d", 3)
        act.alphabet[4] = b_Sym_char("e", "e", 4)
        act.alphabet[-1] = b_Sym_char("Epsilon", "", -1)
        act.start = 0
        act.final.add(3)
        act.final.add(5)
        act.final.add(8)
        act.transitions.add( (0, 0, 1) )
        act.transitions.add( (1, 1, 2) )
        act.transitions.add( (2, 2, 3) )
        act.transitions.add( (3, 2, 3) )
        act.transitions.add( (2, 3, 4) )
        act.transitions.add( (4, 4, 5) )
        act.transitions.add( (1, 1, 6) )
        act.transitions.add( (6, 3, 6) )
        act.transitions.add( (6, -1, 7) )
        act.transitions.add( (7, 3, 8) )

        aut = b_Automaton()
        aut.create_from_nfa_data(act)
        aut.remove_epsilons()
        aut.stride_2()
        aut.stride_2()
        aut.show("test.dot", " ")
        self.assertTrue(aut.search("") == [0,0,0])
        self.assertTrue(aut.search("a") == [0,0,0])
        self.assertTrue(aut.search("abc") == [1,0,0])
        self.assertTrue(aut.search("abccccccc") == [1,0,0])
        self.assertTrue(aut.search("abccccccccc a c") == [1,0,0])
        self.assertTrue(aut.search("abd") == [0,0,1])
        self.assertTrue(aut.search("abddddddddd") == [0,0,1])
        self.assertTrue(aut.search("abde") == [0,1,1])

    def test_resolve_alphabet(self):
        """resolve_alphabet()""" 
        # Alphabet collision free.
        # Example: Alphabet {1:["a", "b", "c"], 2: ["a", "d"]}.
        # After resolve_alphabet() will be Alphabet {1:["b", "c"], 2:["d"], 3:["a]}.

        # 1) empty automaton
        nfaData = nfa_data()

        act = b_Automaton()
        act.create_from_nfa_data(nfaData)
        act.resolve_alphabet()
        cp = act.get_automaton()

        self.assertTrue(sorted(cp.states.keys()) == sorted(nfaData.states.keys()))
        self.assertTrue(cp.alphabet == nfaData.alphabet)
        self.assertTrue(cp.start == nfaData.start)
        self.assertTrue(cp.final == nfaData.final)
        self.assertTrue(cp.transitions == nfaData.transitions)
        self.assertTrue(cp.Flags == nfaData.Flags)

        # 2) alphabet do not contain collisions -> nothing change
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set())
        nfaData.states[4] = b_State(4,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char_class("ch0", set(['b', 'c']), 1)
        nfaData.alphabet[2] = b_Sym_char_class("ch1", set(['d', 'e']), 2)
        nfaData.alphabet[3] = b_Sym_char("f", "f", 3)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (2,2,3) )
        nfaData.transitions.add( (3,3,4) )
        nfaData.final.add(4)

        act = b_Automaton()
        act.create_from_nfa_data(nfaData)
        act.resolve_alphabet()
        cp = act.get_automaton()

        nfaData.Flags["Alphabet collision free"] = True

        self.assertTrue(sorted(cp.states.keys()) == sorted(nfaData.states.keys()))
        self.assertTrue(cp.alphabet == nfaData.alphabet)
        self.assertTrue(cp.start == nfaData.start)
        self.assertTrue(cp.final == nfaData.final)
        self.assertTrue(cp.transitions == nfaData.transitions)
        self.assertTrue(cp.Flags == nfaData.Flags)

        # 3) alphabet contain collisions -> change automaton
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set())
        nfaData.states[4] = b_State(4,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char_class("ch0", set(['a', 'c']), 1)
        nfaData.alphabet[2] = b_Sym_char_class("ch1", set(['f', 'e']), 2)
        nfaData.alphabet[3] = b_Sym_char("f", "f", 3)
        nfaData.alphabet[4] = b_Sym_char_class("ch1", set(['g', 'h']), 2)
        nfaData.alphabet[5] = b_Sym_char_class("ch1", set(['g', 'z']), 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (2,2,3) )
        nfaData.transitions.add( (3,3,4) )
        nfaData.transitions.add( (0,5,1) )
        nfaData.transitions.add( (0,4,1) )
        nfaData.final.add(4)

        act = b_Automaton()
        act.create_from_nfa_data(nfaData)
        act.resolve_alphabet()
        cp = act.get_automaton()
        
        result = nfa_data()
        result.states[0] = b_State(0,set())
        result.states[1] = b_State(1,set())
        result.states[2] = b_State(2,set())
        result.states[3] = b_State(3,set())
        result.states[4] = b_State(4,set([0]))
        result.alphabet[0] = b_Sym_char("a", "a", 4)
        result.alphabet[1] = b_Sym_char("f", "f", 5)
        result.alphabet[2] = b_Sym_char_class("ch0", set(['c']), 0)
        result.alphabet[3] = b_Sym_char_class("ch1", set(['e']), 1)
        result.alphabet[4] = b_Sym_char_class("ch2", set(['h']), 2)
        result.alphabet[5] = b_Sym_char_class("ch1", set(['g']), 6)
        result.alphabet[6] = b_Sym_char_class("ch3", set(['z']), 3)
        result.start = 0
        result.transitions = set([(2, 1, 3), (3, 1, 4), (0, 5, 1), (0, 0, 1),
        (0, 6, 1), (0, 4, 1), (1, 0, 2), (1, 2, 2), (2, 3, 3)])
        result.final.add(4)
        result.Flags["Alphabet collision free"] = True

        self.assertTrue(sorted(cp.states.keys()) == sorted(result.states.keys()))
        self.assertTrue(cp.alphabet == result.alphabet)
        self.assertTrue(cp.start == result.start)
        self.assertTrue(cp.final == result.final)
        self.assertTrue(cp.transitions == result.transitions)
        self.assertTrue(cp.Flags == result.Flags)

        # 4) additional test
        par = parser("pcre_parser")
        par.set_text("/[^1234]/")
        aut = b_Automaton()
        aut.create_by_parser(par)
        aut.resolve_alphabet()
        cp = aut.get_automaton()
        act = nfa_data().load_from_file("test_data/resolve_alphabet.nfa_data")

        self.assertTrue(sorted(cp.states.keys()) == sorted(act.states.keys()))
        self.assertTrue(cp.alphabet == act.alphabet)
        self.assertTrue(cp.start == act.start)
        self.assertTrue(cp.final == act.final)
        self.assertTrue(cp.transitions == act.transitions)
        self.assertTrue(cp.Flags == act.Flags)

    def test_get_state_num(self):
        """get_state_num()"""
        # For manually created nfa_data structure is needed to verify the
        # correct listing of get_state_num(). Listings should be verified at
        # least 5 non-trivial machines. In tests it is necessary to consider the
        # extreme values as:
        #   zero number of states,
        #   machines with / without cycles.

        # Follow 5 non-trivial machines.
        # 1) /<tel[^\x3A]{6}/smi
        nfaData = nfa_data().load_from_file("test_data/RE_viz_get_1.nfa_data")
        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        self.assertTrue(aut.get_state_num() == len(nfaData.states))
        # 2) /iuewiob*asaf+asdi[^iewbnbvios]{500}/
        nfaData = nfa_data().load_from_file("test_data/RE_viz_get_2.nfa_data")
        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        self.assertTrue(aut.get_state_num() == len(nfaData.states))
        # 3) /Uin=\d+\x26Name=.*IP-.*USER-.*TROJAN-.*PORT-.*PASSWORD-.*OS-.*WEBCAM-/smi
        nfaData = nfa_data().load_from_file("test_data/RE_viz_get_3.nfa_data")
        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        self.assertTrue(aut.get_state_num() == len(nfaData.states))
        # 4) /.*\/\.\.\/\.\.\/\.\.\/\.\.\//
        nfaData = nfa_data().load_from_file("test_data/RE_viz_get_4.nfa_data")
        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        self.assertTrue(aut.get_state_num() == len(nfaData.states))
        # 5) /.*Microsoft Windows.*.{15}.*asdfCopyrightasdf1985-.*.{556}.*Microsoft_Corp_/
        nfaData = nfa_data().load_from_file("test_data/RE_viz_get_5.nfa_data")
        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        self.assertTrue(aut.get_state_num() == len(nfaData.states))

        # 6) empty automaton
        nfaData = nfa_data()
        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        self.assertTrue(aut.get_state_num() == len(nfaData.states))

        # 7) cycle
        # the machine is connected to the cycle of epsilon transition
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set())
        nfaData.states[4] = b_State(4,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[-1] = b_Sym_char("Epsilon", "", -1)
        nfaData.start = 0
        nfaData.final.add(4)
        nfaData.transitions.add( (0, -1, 1) )
        nfaData.transitions.add( (1, -1, 2) )
        nfaData.transitions.add( (2, -1, 3) )
        nfaData.transitions.add( (3, -1, 0) )
        nfaData.transitions.add( (2, 0, 4) )

        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        self.assertTrue(aut.get_state_num() == len(nfaData.states))

    def test_get_trans_num(self):
        """get_trans_num()"""
        # For manually created nfa_data structure is needed to verify the
        # correct listing of get_trans_num(). Listings should be verified at
        # least 5 non-trivial machines. In tests it is necessary to consider the
        # extreme values as:
        #   zero number of transitions,
        #   machines with / without cycles.

        # Follow 5 non-trivial machines.
        # 1) /<tel[^\x3A]{6}/smi
        nfaData = nfa_data().load_from_file("test_data/RE_viz_get_1.nfa_data")
        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        self.assertTrue(aut.get_trans_num() == len(nfaData.transitions))
        # 2) /iuewiob*asaf+asdi[^iewbnbvios]{500}/
        nfaData = nfa_data().load_from_file("test_data/RE_viz_get_2.nfa_data")
        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        self.assertTrue(aut.get_trans_num() == len(nfaData.transitions))
        # 3) /Uin=\d+\x26Name=.*IP-.*USER-.*TROJAN-.*PORT-.*PASSWORD-.*OS-.*WEBCAM-/smi
        nfaData = nfa_data().load_from_file("test_data/RE_viz_get_3.nfa_data")
        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        self.assertTrue(aut.get_trans_num() == len(nfaData.transitions))
        # 4) /.*\/\.\.\/\.\.\/\.\.\/\.\.\//
        nfaData = nfa_data().load_from_file("test_data/RE_viz_get_4.nfa_data")
        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        self.assertTrue(aut.get_trans_num() == len(nfaData.transitions))
        # 5) /.*Microsoft Windows.*.{15}.*asdfCopyrightasdf1985-.*.{556}.*Microsoft_Corp_/
        nfaData = nfa_data().load_from_file("test_data/RE_viz_get_5.nfa_data")
        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        self.assertTrue(aut.get_trans_num() == len(nfaData.transitions))

        # 6) empty automaton
        nfaData = nfa_data()
        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        self.assertTrue(aut.get_trans_num() == len(nfaData.transitions))

        # 7) cycle
        # the machine is connected to the cycle of epsilon transition
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set())
        nfaData.states[4] = b_State(4,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[-1] = b_Sym_char("Epsilon", "", -1)
        nfaData.start = 0
        nfaData.final.add(4)
        nfaData.transitions.add( (0, -1, 1) )
        nfaData.transitions.add( (1, -1, 2) )
        nfaData.transitions.add( (2, -1, 3) )
        nfaData.transitions.add( (3, -1, 0) )
        nfaData.transitions.add( (2, 0, 4) )

        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        self.assertTrue(aut.get_trans_num() == len(nfaData.transitions))

    def test_get_alpha_num(self):
        """get_alpha_num()"""
        # For manually created nfa_data structure is needed to verify the
        # correct listing of get_alpha_num(). Listings should be verified at least
        # 5 non-trivial machines. In tests it is necessary to consider the
        # extreme values as:
        #   zero number of symbols,
        #   machines with / without cycles.

        # Follow 5 non-trivial machines.
        # 1) /<tel[^\x3A]{6}/smi
        nfaData = nfa_data().load_from_file("test_data/RE_viz_get_1.nfa_data")
        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        self.assertTrue(aut.get_alpha_num() == len(nfaData.alphabet))
        # 2) /iuewiob*asaf+asdi[^iewbnbvios]{500}/
        nfaData = nfa_data().load_from_file("test_data/RE_viz_get_2.nfa_data")
        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        self.assertTrue(aut.get_alpha_num() == len(nfaData.alphabet))
        # 3) /Uin=\d+\x26Name=.*IP-.*USER-.*TROJAN-.*PORT-.*PASSWORD-.*OS-.*WEBCAM-/smi
        nfaData = nfa_data().load_from_file("test_data/RE_viz_get_3.nfa_data")
        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        self.assertTrue(aut.get_alpha_num() == len(nfaData.alphabet))
        # 4) /.*\/\.\.\/\.\.\/\.\.\/\.\.\//
        nfaData = nfa_data().load_from_file("test_data/RE_viz_get_4.nfa_data")
        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        self.assertTrue(aut.get_alpha_num() == len(nfaData.alphabet))
        # 5) /.*Microsoft Windows.*.{15}.*asdfCopyrightasdf1985-.*.{556}.*Microsoft_Corp_/
        nfaData = nfa_data().load_from_file("test_data/RE_viz_get_5.nfa_data")
        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        self.assertTrue(aut.get_alpha_num() == len(nfaData.alphabet))

        # 6) empty automaton
        nfaData = nfa_data()
        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        self.assertTrue(aut.get_alpha_num() == len(nfaData.alphabet))

        # 7) cycle
        # the machine is connected to the cycle of epsilon transition
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set())
        nfaData.states[4] = b_State(4,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[-1] = b_Sym_char("Epsilon", "", -1)
        nfaData.start = 0
        nfaData.final.add(4)
        nfaData.transitions.add( (0, -1, 1) )
        nfaData.transitions.add( (1, -1, 2) )
        nfaData.transitions.add( (2, -1, 3) )
        nfaData.transitions.add( (3, -1, 0) )
        nfaData.transitions.add( (2, 0, 4) )

        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        self.assertTrue(aut.get_alpha_num() == len(nfaData.alphabet))

    def test_has_cycle(self):
        """has_cycle()"""
        # For manually created nfa_data structure is needed to verify the
        # correct listing of has_cycle(). Listings should be verified at least
        # 5 non-trivial machines. In tests it is necessary to consider the
        # extreme values as:
        #   empty automaton,
        #   machines with / without cycles.

        # Follow 5 non-trivial machines.
        # 1) /<tel[^\x3A]{6}/smi
        nfaData = nfa_data().load_from_file("test_data/RE_viz_get_1.nfa_data")
        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        self.assertTrue(aut.has_cycle() == True)
        # 2) /iuewiob*asaf+asdi[^iewbnbvios]{500}/
        nfaData = nfa_data().load_from_file("test_data/RE_viz_get_2.nfa_data")
        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        self.assertTrue(aut.has_cycle() == True)
        # 3) /Uin=\d+\x26Name=.*IP-.*USER-.*TROJAN-.*PORT-.*PASSWORD-.*OS-.*WEBCAM-/smi
        nfaData = nfa_data().load_from_file("test_data/RE_viz_get_3.nfa_data")
        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        self.assertTrue(aut.has_cycle() == True)
        # 4) /.*\/\.\.\/\.\.\/\.\.\/\.\.\//
        nfaData = nfa_data().load_from_file("test_data/RE_viz_get_4.nfa_data")
        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        self.assertTrue(aut.has_cycle() == True)
        # 5) /.*Microsoft Windows.*.{15}.*asdfCopyrightasdf1985-.*.{556}.*Microsoft_Corp_/
        nfaData = nfa_data().load_from_file("test_data/RE_viz_get_5.nfa_data")
        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        self.assertTrue(aut.has_cycle() == True)

        # 6) empty automaton
        nfaData = nfa_data()
        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        self.assertTrue(aut.has_cycle() == False)

        # 7) cycle
        # the machine is connected to the cycle of epsilon transition
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set())
        nfaData.states[4] = b_State(4,set([0]))
        nfaData.states[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[-1] = b_Sym_char("Epsilon", "", -1)
        nfaData.start = 0
        nfaData.final.add(4)
        nfaData.transitions.add( (0, -1, 1) )
        nfaData.transitions.add( (1, -1, 2) )
        nfaData.transitions.add( (2, -1, 3) )
        nfaData.transitions.add( (3, -1, 0) )
        nfaData.transitions.add( (2, 0, 4) )

        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        self.assertTrue(aut.has_cycle() == True)

    def test_set_flag(self):
        """set_flag()"""
        # Correct setting and reading of flags can be verified as enter selected
        # number of symptoms and testing for their presence. Name and value of
        # symptoms is possible to arbitrarily change it.

        aut = b_Automaton()
        aut.set_flag("Deterministic", True)
        self.assertTrue(aut._automaton.Flags["Deterministic"] == True)
        aut.set_flag("Deterministic", False)
        self.assertTrue(aut._automaton.Flags["Deterministic"] == False)

        aut.set_flag("Strided", True)
        self.assertTrue(aut._automaton.Flags["Strided"] == True)
        aut.set_flag("Strided", False)
        self.assertTrue(aut._automaton.Flags["Strided"] == False)

        aut.set_flag("Stride", 2)
        self.assertTrue(aut._automaton.Flags["Stride"] == 2)
        aut.set_flag("Stride", 4)
        self.assertTrue(aut._automaton.Flags["Stride"] == 4)

        aut.set_flag("Epsilon Free", True)
        self.assertTrue(aut._automaton.Flags["Epsilon Free"] == True)
        aut.set_flag("Epsilon Free", False)
        self.assertTrue(aut._automaton.Flags["Epsilon Free"] == False)

        aut.set_flag("Alphabet collision free", True)
        self.assertTrue(aut._automaton.Flags["Alphabet collision free"] == True)
        aut.set_flag("Alphabet collision free", False)
        self.assertTrue(aut._automaton.Flags["Alphabet collision free"] == False)

        aut.set_flag("Minimal", True)
        self.assertTrue(aut._automaton.Flags["Minimal"] == True)
        aut.set_flag("Minimal", False)
        self.assertTrue(aut._automaton.Flags["Minimal"] == False)

        aut.set_flag("Delay DFA", True)
        self.assertTrue(aut._automaton.Flags["Delay DFA"] == True)
        aut.set_flag("Delay DFA", False)
        self.assertTrue(aut._automaton.Flags["Delay DFA"] == False)

        aut.set_flag("Extend_FA", True)
        self.assertTrue(aut._automaton.Flags["Extend_FA"] == True)
        aut.set_flag("Extend_FA", False)
        self.assertTrue(aut._automaton.Flags["Extend_FA"] == False)

        aut.set_flag("History FA", True)
        self.assertTrue(aut._automaton.Flags["History FA"] == True)
        aut.set_flag("History FA", False)
        self.assertTrue(aut._automaton.Flags["History FA"] == False)

        aut.set_flag("Hybrid FA - one NFA part", True)
        self.assertTrue(aut._automaton.Flags["Hybrid FA - one NFA part"] == True)
        aut.set_flag("Hybrid FA - one NFA part", False)
        self.assertTrue(aut._automaton.Flags["Hybrid FA - one NFA part"] == False)

        aut.set_flag("Hybrid FA - DFA part", True)
        self.assertTrue(aut._automaton.Flags["Hybrid FA - DFA part"] == True)
        aut.set_flag("Hybrid FA - DFA part", False)
        self.assertTrue(aut._automaton.Flags["Hybrid FA - DFA part"] == False)

    def test_has_flag(self):
        """has_flag()"""
        # Correct setting and reading of flags can be verified as enter selected
        # number of symptoms and testing for their presence. Name and value of
        # symptoms is possible to arbitrarily change it.

        aut = b_Automaton()
        self.assertTrue(aut.has_flag("Deterministic") == False)
        aut._automaton.Flags["Deterministic"] = True
        self.assertTrue(aut.has_flag("Deterministic") == True)
        aut._automaton.Flags["Deterministic"] = False
        self.assertTrue(aut.has_flag("Deterministic") == True)

        self.assertTrue(aut.has_flag("Strided") == False)
        aut._automaton.Flags["Strided"] = True
        self.assertTrue(aut.has_flag("Strided") == True)
        aut._automaton.Flags["Strided"] = False
        self.assertTrue(aut.has_flag("Strided") == True)

        self.assertTrue(aut.has_flag("Stride") == False)
        aut._automaton.Flags["Stride"] = 2
        self.assertTrue(aut.has_flag("Stride") == True)
        aut._automaton.Flags["Stride"] = 4
        self.assertTrue(aut.has_flag("Stride") == True)

        self.assertTrue(aut.has_flag("Epsilon Free") == False)
        aut._automaton.Flags["Epsilon Free"] = True
        self.assertTrue(aut.has_flag("Epsilon Free") == True)
        aut._automaton.Flags["Epsilon Free"] = False
        self.assertTrue(aut.has_flag("Epsilon Free") == True)

        self.assertTrue(aut.has_flag("Alphabet collision free") == False)
        aut._automaton.Flags["Alphabet collision free"] = True
        self.assertTrue(aut.has_flag("Alphabet collision free") == True)
        aut._automaton.Flags["Alphabet collision free"] = False
        self.assertTrue(aut.has_flag("Alphabet collision free") == True)

        self.assertTrue(aut.has_flag("Minimal") == False)
        aut._automaton.Flags["Minimal"] = True
        self.assertTrue(aut.has_flag("Minimal") == True)
        aut._automaton.Flags["Minimal"] = False
        self.assertTrue(aut.has_flag("Minimal") == True)

        self.assertTrue(aut.has_flag("Delay DFA") == False)
        aut._automaton.Flags["Delay DFA"] = True
        self.assertTrue(aut.has_flag("Delay DFA") == True)
        aut._automaton.Flags["Delay DFA"] = False
        self.assertTrue(aut.has_flag("Delay DFA") == True)

        self.assertTrue(aut.has_flag("Extend_FA") == False)
        aut._automaton.Flags["Extend_FA"] = True
        self.assertTrue(aut.has_flag("Extend_FA") == True)
        aut._automaton.Flags["Extend_FA"] = False
        self.assertTrue(aut.has_flag("Extend_FA") == True)

        self.assertTrue(aut.has_flag("History FA") == False)
        aut._automaton.Flags["History FA"] = True
        self.assertTrue(aut.has_flag("History FA") == True)
        aut._automaton.Flags["History FA"] = False
        self.assertTrue(aut.has_flag("History FA") == True)

        self.assertTrue(aut.has_flag("Hybrid FA - one NFA part") == False)
        aut._automaton.Flags["Hybrid FA - one NFA part"] = True
        self.assertTrue(aut.has_flag("Hybrid FA - one NFA part") == True)
        aut._automaton.Flags["Hybrid FA - one NFA part"] = False
        self.assertTrue(aut.has_flag("Hybrid FA - one NFA part") == True)

        self.assertTrue(aut.has_flag("Hybrid FA - DFA part") == False)
        aut._automaton.Flags["Hybrid FA - DFA part"] = True
        self.assertTrue(aut.has_flag("Hybrid FA - DFA part") == True)
        aut._automaton.Flags["Hybrid FA - DFA part"] = False
        self.assertTrue(aut.has_flag("Hybrid FA - DFA part") == True)

    def test_get_flag(self):
        """get_flag()"""
        # Correct setting and reading of flags can be verified as enter selected
        # number of symptoms and testing for their presence. Name and value of
        # symptoms is possible to arbitrarily change it.

        aut = b_Automaton()
        aut._automaton.Flags["Deterministic"] = True
        self.assertTrue(aut.get_flag("Deterministic") == True)
        aut._automaton.Flags["Deterministic"] = False
        self.assertTrue(aut.get_flag("Deterministic") == False)

        aut._automaton.Flags["Strided"] = True
        self.assertTrue(aut.get_flag("Strided") == True)
        aut._automaton.Flags["Strided"] = False
        self.assertTrue(aut.get_flag("Strided") == False)

        aut._automaton.Flags["Stride"] = 2
        self.assertTrue(aut.get_flag("Stride") == 2)
        aut._automaton.Flags["Stride"] = 4
        self.assertTrue(aut.get_flag("Stride") == 4)

        aut._automaton.Flags["Epsilon Free"] = True
        self.assertTrue(aut.get_flag("Epsilon Free") == True)
        aut._automaton.Flags["Epsilon Free"] = False
        self.assertTrue(aut.get_flag("Epsilon Free") == False)

        aut._automaton.Flags["Alphabet collision free"] = True
        self.assertTrue(aut.get_flag("Alphabet collision free") == True)
        aut._automaton.Flags["Alphabet collision free"] = False
        self.assertTrue(aut.get_flag("Alphabet collision free") == False)

        aut._automaton.Flags["Minimal"] = True
        self.assertTrue(aut.get_flag("Minimal") == True)
        aut._automaton.Flags["Minimal"] = False
        self.assertTrue(aut.get_flag("Minimal") == False)

        aut._automaton.Flags["Delay DFA"] = True
        self.assertTrue(aut.get_flag("Delay DFA") == True)
        aut._automaton.Flags["Delay DFA"] = False
        self.assertTrue(aut.get_flag("Delay DFA") == False)

        aut._automaton.Flags["Extend_FA"] = True
        self.assertTrue(aut.get_flag("Extend_FA") == True)
        aut._automaton.Flags["Extend_FA"] = False
        self.assertTrue(aut.get_flag("Extend_FA") == False)

        aut._automaton.Flags["History FA"] = True
        self.assertTrue(aut.get_flag("History FA") == True)
        aut._automaton.Flags["History FA"] = False
        self.assertTrue(aut.get_flag("History FA") == False)

        aut._automaton.Flags["Hybrid FA - one NFA part"] = True
        self.assertTrue(aut.get_flag("Hybrid FA - one NFA part") == True)
        aut._automaton.Flags["Hybrid FA - one NFA part"] = False
        self.assertTrue(aut.get_flag("Hybrid FA - one NFA part") == False)

        aut._automaton.Flags["Hybrid FA - DFA part"] = True
        self.assertTrue(aut.get_flag("Hybrid FA - DFA part") == True)
        aut._automaton.Flags["Hybrid FA - DFA part"] = False
        self.assertTrue(aut.get_flag("Hybrid FA - DFA part") == False)

    def test_remove_char_classes(self):
        """remove_char_classes()"""
        # 1)
        # Unless the machine include character classes remain the same.

        # the machine is connected to the cycle of epsilon transition
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set())
        nfaData.states[4] = b_State(4,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[-1] = b_Sym_char("Epsilon", "", -1)
        nfaData.start = 0
        nfaData.final.add(4)
        nfaData.transitions.add( (0, -1, 1) )
        nfaData.transitions.add( (1, -1, 2) )
        nfaData.transitions.add( (2, -1, 3) )
        nfaData.transitions.add( (3, -1, 0) )
        nfaData.transitions.add( (2, 0, 4) )

        act = b_Automaton()
        act.create_from_nfa_data(nfaData)
        act.remove_char_classes()
        cp = act.get_automaton()

        self.assertTrue(sorted(cp.states.keys()) == sorted(nfaData.states.keys()))
        self.assertTrue(cp.alphabet == nfaData.alphabet)
        self.assertTrue(cp.start == nfaData.start)
        self.assertTrue(cp.final == nfaData.final)
        self.assertTrue(cp.transitions == nfaData.transitions)
        # Check if Flags are the same, with exception - "Alphabet collision free" must be set to True
        nfaData.Flags["Alphabet collision free"] = True
        self.assertTrue(cp.Flags == nfaData.Flags)

        # RE abc+
        # RE abde
        # RE abd*d
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set([0]))
        nfaData.states[4] = b_State(4,set())
        nfaData.states[5] = b_State(5,set([1]))
        nfaData.states[6] = b_State(6,set())
        nfaData.states[7] = b_State(7,set())
        nfaData.states[8] = b_State(8,set([2]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.alphabet[3] = b_Sym_char("d", "d", 3)
        nfaData.alphabet[4] = b_Sym_char("e", "e", 4)
        nfaData.alphabet[-1] = b_Sym_char("Epsilon", "", -1)
        nfaData.start = 0
        nfaData.final.add(3)
        nfaData.final.add(5)
        nfaData.final.add(8)
        nfaData.transitions.add( (0, 0, 1) )
        nfaData.transitions.add( (1, 1, 2) )
        nfaData.transitions.add( (2, 2, 3) )
        nfaData.transitions.add( (3, 2, 3) )
        nfaData.transitions.add( (2, 3, 4) )
        nfaData.transitions.add( (4, 4, 5) )
        nfaData.transitions.add( (1, 1, 6) )
        nfaData.transitions.add( (6, 3, 6) )
        nfaData.transitions.add( (6, -1, 7) )
        nfaData.transitions.add( (7, 3, 8) )

        act = b_Automaton()
        act.create_from_nfa_data(nfaData)
        act.remove_char_classes()
        cp = act.get_automaton()

        self.assertTrue(sorted(cp.states.keys()) == sorted(nfaData.states.keys()))
        self.assertTrue(cp.alphabet == nfaData.alphabet)
        self.assertTrue(cp.start == nfaData.start)
        self.assertTrue(cp.final == nfaData.final)
        self.assertTrue(cp.transitions == nfaData.transitions)
        # Check if Flags are the same, with exception - "Alphabet collision free" must be set to True
        nfaData.Flags["Alphabet collision free"] = True
        self.assertTrue(cp.Flags == nfaData.Flags)

        # empty automaton
        nfaData = nfa_data()

        act = b_Automaton()
        act.create_from_nfa_data(nfaData)
        act.remove_char_classes()
        cp = act.get_automaton()

        self.assertTrue(sorted(cp.states.keys()) == sorted(nfaData.states.keys()))
        self.assertTrue(cp.alphabet == nfaData.alphabet)
        self.assertTrue(cp.start == nfaData.start)
        self.assertTrue(cp.final == nfaData.final)
        self.assertTrue(cp.transitions == nfaData.transitions)
        # Check if Flags are the same, with exception - "Alphabet collision free" must be set to True
        nfaData.Flags["Alphabet collision free"] = True
        self.assertTrue(cp.Flags == nfaData.Flags)

        # additional test
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set())
        nfaData.states[4] = b_State(4,set())
        nfaData.states[5] = b_State(5,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[-1] = b_Sym_char("Epsilon", "", -1)
        nfaData.start = 0
        nfaData.final.add(5)
        nfaData.transitions.add( (0, -1, 1) )
        nfaData.transitions.add( (1, -1, 2) )
        nfaData.transitions.add( (2, 0, 3) )
        nfaData.transitions.add( (2, -1, 3) )
        nfaData.transitions.add( (3, 0, 3) )
        nfaData.transitions.add( (3, -1, 4) )
        nfaData.transitions.add( (4, -1, 5) )

        act = b_Automaton()
        act.create_from_nfa_data(nfaData)
        act.remove_char_classes()
        cp = act.get_automaton()

        self.assertTrue(sorted(cp.states.keys()) == sorted(nfaData.states.keys()))
        self.assertTrue(cp.alphabet == nfaData.alphabet)
        self.assertTrue(cp.start == nfaData.start)
        self.assertTrue(cp.final == nfaData.final)
        self.assertTrue(cp.transitions == nfaData.transitions)
        # Check if Flags are the same, with exception - "Alphabet collision free" must be set to True
        nfaData.Flags["Alphabet collision free"] = True
        self.assertTrue(cp.Flags == nfaData.Flags)

        # 2)
        # If the machine contains sym_char_class symbols, these symbols and the
        # corresponding point will be removed and replaced with the
        # corresponding symbols sym_char.
        # Example {a, b, c} -> a, b, c

        # basic test with one char
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set([0]))
        nfaData.alphabet[0] = b_Sym_char_class("{['a']}", set(['a']), 0)
        nfaData.start = 0
        nfaData.final.add(1)
        nfaData.transitions.add( (0, 0, 1) )

        act = b_Automaton()
        act.create_from_nfa_data(nfaData)
        act.remove_char_classes()
        cp = act.get_automaton()

        result = nfa_data()
        result.states[0] = b_State(0,set())
        result.states[1] = b_State(1,set([0]))
        result.alphabet[1] = b_Sym_char('a', 'a', 1)
        result.start = 0
        result.final.add(1)
        result.transitions.add( (0, 1, 1) )
        result.Flags["Alphabet collision free"] = True
        
        self.assertTrue(sorted(cp.states.keys()) == sorted(result.states.keys()))
        self.assertTrue(cp.alphabet == result.alphabet)
        self.assertTrue(cp.start == result.start)
        self.assertTrue(cp.final == result.final)
        self.assertTrue(cp.transitions == result.transitions)
        self.assertTrue(cp.Flags == result.Flags)

        # transition from one state to more states
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set([0]))
        nfaData.states[3] = b_State(3,set([0]))
        nfaData.states[4] = b_State(4,set([0]))
        nfaData.alphabet[0] = b_Sym_char_class("{['a']}", set(['a']), 0)
        nfaData.alphabet[1] = b_Sym_char_class(
            "{'b', 'c', 'd'}", set(['b', 'c', 'd']), 1
        )
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (1,1,3) )
        nfaData.transitions.add( (1,1,4) )
        nfaData.final.add(2)
        nfaData.final.add(3)
        nfaData.final.add(4)

        act = b_Automaton()
        act.create_from_nfa_data(nfaData)
        act.remove_char_classes()
        cp = act.get_automaton()

        result = nfa_data()
        result.states[0] = b_State(0,set())
        result.states[1] = b_State(1,set())
        result.states[2] = b_State(2,set([0]))
        result.states[3] = b_State(3,set([0]))
        result.states[4] = b_State(4,set([0]))
        result.alphabet[5] = b_Sym_char('a', 'a', 5)
        result.alphabet[3] = b_Sym_char('b', 'b', 3)
        result.alphabet[2] = b_Sym_char('c', 'c', 2)
        result.alphabet[4] = b_Sym_char('d', 'd', 4)
        result.start = 0
        result.transitions.add( (0,5,1) )
        result.transitions.add( (1,3,2) )
        result.transitions.add( (1,4,2) )
        result.transitions.add( (1,2,2) )
        result.transitions.add( (1,3,3) )
        result.transitions.add( (1,4,3) )
        result.transitions.add( (1,2,3) )
        result.transitions.add( (1,3,4) )
        result.transitions.add( (1,4,4) )
        result.transitions.add( (1,2,4) )
        result.final.add(2)
        result.final.add(3)
        result.final.add(4)
        result.Flags["Alphabet collision free"] = True
        
        self.assertTrue(sorted(cp.states.keys()) == sorted(result.states.keys()))
        self.assertTrue(cp.alphabet == result.alphabet)
        self.assertTrue(cp.start == result.start)
        self.assertTrue(cp.final == result.final)
        self.assertTrue(cp.transitions == result.transitions)
        self.assertTrue(cp.Flags == result.Flags)

        # normal automaton
        par = parser("pcre_parser")
        par.set_text("/./")
        automat = b_Automaton()
        automat.create_by_parser(par)
        automat.remove_char_classes()
        cp = automat.get_automaton()

        result = nfa_data().load_from_file("test_data/rm_ch_cl_normal.nfa_data")
        result.Flags["Alphabet collision free"] = True
        
        self.assertTrue(sorted(cp.states.keys()) == sorted(result.states.keys()))
        self.assertTrue(cp.alphabet == result.alphabet)
        self.assertTrue(cp.start == result.start)
        self.assertTrue(cp.final == result.final)
        self.assertTrue(cp.transitions == result.transitions)
        self.assertTrue(cp.Flags == result.Flags)

        # 3)
        # If the machine contains symbols sym_kchar containing the character
        # class, these symbols and the corresponding transitions will be removed
        # and replaced with the corresponding symbols not containing sym_kchar
        # character class.
        # Example ({a,b}, {c, d}) -> (a, c), (a, d), (b, c), (b, d)
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set([0]))
        nfaData.alphabet[0] = b_Sym_kchar(
            "ch", (frozenset(["a", "b"]), frozenset(["c", "d"])), 0
        )
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.final.add(1)

        act = b_Automaton()
        act.create_from_nfa_data(nfaData)
        act.remove_char_classes()
        cp = act.get_automaton()

        result = nfa_data().load_from_file("test_data/rm_ch_cl_3.nfa_data")
        result.Flags["Alphabet collision free"] = True
        
        self.assertTrue(sorted(cp.states.keys()) == sorted(result.states.keys()))
        self.assertTrue(cp.alphabet == result.alphabet)
        self.assertTrue(cp.start == result.start)
        self.assertTrue(cp.final == result.final)
        self.assertTrue(cp.transitions == result.transitions)
        self.assertTrue(cp.Flags == result.Flags)

    def test_get_automaton(self):
        """get_automaton()"""
        # Is necessary to test the behavior with a parameter safe = True and False.
        # If we have an object of type b_Automaton and method get_automaton() then:
        #   with safe = False then any changes should be reflected,
        #   with safe = True then changes must not occur.

        # 1) Empty automaton - True
        nfaData = nfa_data()
        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        cp = aut.get_automaton(safe = True)

        aut._automaton.states[0] = b_State(0,set())
        aut._automaton.states[1] = b_State(1,set([0]))
        aut._automaton.alphabet[0] = b_Sym_char("a", "a", 0)
        aut._automaton.start = 0
        aut._automaton.transitions.add( (0,0,1) )
        aut._automaton.final.add(1)

        self.assertTrue(cp.states == dict())
        self.assertTrue(cp.alphabet == dict())
        self.assertTrue(cp.start == -1)
        self.assertTrue(cp.final == set())
        self.assertTrue(cp.transitions == set())

        # 2) Empty automaton - False
        nfaData = nfa_data()
        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        cp = aut.get_automaton(safe = False)

        aut._automaton.states[0] = b_State(0,set())
        aut._automaton.states[1] = b_State(1,set([0]))
        aut._automaton.alphabet[0] = b_Sym_char("a", "a", 0)
        aut._automaton.start = 0
        aut._automaton.transitions.add( (0,0,1) )
        aut._automaton.final.add(1)

        self.assertTrue(sorted(cp.states.keys()) == [0, 1])
        self.assertTrue(sorted(cp.alphabet.keys()) == [0])
        self.assertTrue(cp.start == 0)
        self.assertTrue(cp.final == set([1]))
        self.assertTrue(cp.transitions == set([(0,0,1)]))

        # 3) Automaton with one state without transitions - True
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        cp = aut.get_automaton(safe = True)

        aut._automaton.states[1] = b_State(1,set([0]))
        aut._automaton.alphabet[0] = b_Sym_char("a", "a", 0)
        aut._automaton.start = 0
        aut._automaton.transitions.add( (0,0,1) )
        aut._automaton.final.add(1)

        self.assertTrue(sorted(cp.states.keys()) == [0])
        self.assertTrue(cp.alphabet == dict())
        self.assertTrue(cp.start == -1)
        self.assertTrue(cp.final == set())
        self.assertTrue(cp.transitions == set())

        # 4) Automaton with one state without transitions - False
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        cp = aut.get_automaton(safe = False)

        aut._automaton.states[1] = b_State(1,set([0]))
        aut._automaton.alphabet[0] = b_Sym_char("a", "a", 0)
        aut._automaton.start = 0
        aut._automaton.transitions.add( (0,0,1) )
        aut._automaton.final.add(1)

        self.assertTrue(sorted(cp.states.keys()) == [0, 1])
        self.assertTrue(sorted(cp.alphabet.keys()) == [0])
        self.assertTrue(cp.start == 0)
        self.assertTrue(cp.final == set([1]))
        self.assertTrue(cp.transitions == set([(0,0,1)]))

        # 5) One state with one transition - True
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.transitions.add( (0,0,1) )
        nfaData.start = 0
        nfaData.final.add(1)
        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        cp = aut.get_automaton(safe = True)

        aut._automaton.states[2] = b_State(2,set([1]))
        aut._automaton.alphabet[1] = b_Sym_char("b", "b", 1)
        aut._automaton.start = 1
        aut._automaton.transitions.add( (1,1,2) )
        aut._automaton.final.add(2)

        self.assertTrue(sorted(cp.states.keys()) == [0, 1])
        self.assertTrue(sorted(cp.alphabet.keys()) == [0])
        self.assertTrue(cp.start == 0)
        self.assertTrue(cp.final == set([1]))
        self.assertTrue(cp.transitions == set([(0,0,1)]))

        # 6) One state with one transition - False
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.transitions.add( (0,0,1) )
        nfaData.start = 0
        nfaData.final.add(1)
        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        cp = aut.get_automaton(safe = False)

        aut._automaton.states[2] = b_State(2,set([1]))
        aut._automaton.alphabet[1] = b_Sym_char("b", "b", 1)
        aut._automaton.start = 1
        aut._automaton.transitions.add( (1,1,2) )
        aut._automaton.final.add(2)

        self.assertTrue(sorted(cp.states.keys()) == [0, 1, 2])
        self.assertTrue(sorted(cp.alphabet.keys()) == [0, 1])
        self.assertTrue(cp.start == 1)
        self.assertTrue(cp.final == set([1, 2]))
        self.assertTrue(cp.transitions == set([(0,0,1), (1,1,2)]))

        # 7) Normal automaton - True
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set())
        nfaData.states[4] = b_State(4,set())
        nfaData.states[5] = b_State(5,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.alphabet[3] = b_Sym_char("d", "d", 3)
        nfaData.alphabet[4] = b_Sym_char("e", "e", 4)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (1,2,3) )
        nfaData.transitions.add( (1,3,4) )
        nfaData.transitions.add( (2,4,5) )
        nfaData.transitions.add( (3,4,5) )
        nfaData.transitions.add( (4,4,5) )
        nfaData.final.add(5)
        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        cp = aut.get_automaton(safe = True)

        aut._automaton.states[6] = b_State(6,set([1]))
        aut._automaton.alphabet[5] = b_Sym_char("f", "f", 5)
        aut._automaton.start = 1
        aut._automaton.transitions.add( (4,5,6) )
        aut._automaton.final.add(6)

        self.assertTrue(sorted(cp.states.keys()) == [0, 1, 2, 3, 4, 5])
        self.assertTrue(sorted(cp.alphabet.keys()) == [0, 1, 2, 3, 4])
        self.assertTrue(cp.start == 0)
        self.assertTrue(cp.final == set([5]))
        self.assertTrue(cp.transitions == set([(0,0,1), (1,1,2), (1,2,3),
        (1,3,4), (2,4,5), (3,4,5), (4,4,5)]))

        # 8) Normal automaton - False
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set())
        nfaData.states[4] = b_State(4,set())
        nfaData.states[5] = b_State(5,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.alphabet[3] = b_Sym_char("d", "d", 3)
        nfaData.alphabet[4] = b_Sym_char("e", "e", 4)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (1,2,3) )
        nfaData.transitions.add( (1,3,4) )
        nfaData.transitions.add( (2,4,5) )
        nfaData.transitions.add( (3,4,5) )
        nfaData.transitions.add( (4,4,5) )
        nfaData.final.add(5)
        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        cp = aut.get_automaton(safe = False)

        aut._automaton.states[6] = b_State(6,set([1]))
        aut._automaton.alphabet[5] = b_Sym_char("f", "f", 5)
        aut._automaton.start = 1
        aut._automaton.transitions.add( (4,5,6) )
        aut._automaton.final.add(6)

        self.assertTrue(sorted(cp.states.keys()) == [0, 1, 2, 3, 4, 5, 6])
        self.assertTrue(sorted(cp.alphabet.keys()) == [0, 1, 2, 3, 4, 5])
        self.assertTrue(cp.start == 1)
        self.assertTrue(cp.final == set([5, 6]))
        self.assertTrue(cp.transitions == set([(0,0,1), (1,1,2), (1,2,3),
        (1,3,4), (2,4,5), (3,4,5), (4,4,5), (4, 5, 6)]))

    def test_epsilon_closure(self):
        """epsilon_closure()"""
        # Test whether is for given state correctly computed epsilon closure.
        # Test for the following variants:
        #   - state has no transition,
        #   - state has no epsilon transition,
        #   - state has epsilon transition,
        #   - state has epsilon transitions,
        #   - state has epsilon transition a few consecutive state is achievable
        #     via epsilon transitions

        # tested machine
        StateOutSymbols = {
        0 : set([(0, 1)]),
        1 : set([(-1, 2)]),
        2 : set([(0, 3)]),
        3 : set([(-1, 4), (-1, 5), (-1, 6)]),
        4 : set([]),
        5 : set([]),
        6 : set([(0, 7)]),
        7 : set([(-1, 8)]),
        8 : set([(-1, 9)]),
        9 : set([(-1, 10)]),
        10 : set([(0, 11)]),
        11 : set([])
        }

        # 1) state is not in automaton
        self.assertTrue(b_Automaton().epsilon_closure(15, StateOutSymbols) ==
            set([15]))
        # 2) state has no transition
        self.assertTrue(b_Automaton().epsilon_closure(11, StateOutSymbols) ==
            set([11]))
        # 3) state has no epsilon transition
        self.assertTrue(b_Automaton().epsilon_closure(0, StateOutSymbols) ==
            set([0]))
        # 4) state has epsilon transition
        self.assertTrue(b_Automaton().epsilon_closure(1, StateOutSymbols) ==
            set([1, 2]))
        # 5) state has epsilon transitions
        self.assertTrue(b_Automaton().epsilon_closure(3, StateOutSymbols) ==
            set([3, 4, 5, 6]))
        # 6) state has epsilon transition and few consecutive states is achievable by epsilon transitions
        self.assertTrue(b_Automaton().epsilon_closure(7, StateOutSymbols) ==
            set([7, 8, 9, 10]))

    def test_create_char_classes(self):
        """create_char_classes()"""
        # 1) between two states is maximally one transition -> nothing will change in the machine
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set())
        nfaData.states[4] = b_State(4,set())
        nfaData.states[5] = b_State(5,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.alphabet[3] = b_Sym_char("d", "d", 3)
        nfaData.alphabet[4] = b_Sym_char("e", "e", 4)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (1,2,3) )
        nfaData.transitions.add( (1,3,4) )
        nfaData.transitions.add( (2,4,5) )
        nfaData.transitions.add( (3,4,5) )
        nfaData.transitions.add( (4,4,5) )
        nfaData.final.add(5)

        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        aut.create_char_classes()
        cp = aut.get_automaton()

        result = nfa_data()
        result.states[0] = b_State(0,set())
        result.states[1] = b_State(1,set())
        result.states[2] = b_State(2,set())
        result.states[3] = b_State(3,set())
        result.states[4] = b_State(4,set())
        result.states[5] = b_State(5,set([0]))
        result.alphabet[5] = b_Sym_char("a", "a", 5)
        result.alphabet[6] = b_Sym_char("b", "b", 6)
        result.alphabet[7] = b_Sym_char("c", "c", 7)
        result.alphabet[9] = b_Sym_char("d", "d", 9)
        result.alphabet[8] = b_Sym_char("e", "e", 8)
        result.start = 0
        result.transitions.add( (0,5,1) )
        result.transitions.add( (1,6,2) )
        result.transitions.add( (1,7,3) )
        result.transitions.add( (1,9,4) )
        result.transitions.add( (2,8,5) )
        result.transitions.add( (3,8,5) )
        result.transitions.add( (4,8,5) )
        result.final.add(5)
        result.Flags["Alphabet collision free"] = False

        self.assertTrue(sorted(cp.states.keys()) == sorted(result.states.keys()))
        self.assertTrue(cp.alphabet == result.alphabet)
        self.assertTrue(cp.start == result.start)
        self.assertTrue(cp.final == result.final)
        self.assertTrue(cp.transitions == result.transitions)
        self.assertTrue(cp.Flags == result.Flags)

        # 2) between two states are two or more transitions -> machine will
        # change (connected symbols in one symbol sym_char_class and create a
        # new crossing over the symbol, deleting the original symbol, if not
        # used elsewhere, and deleting the original transition)
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set())
        nfaData.states[4] = b_State(4,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.alphabet[3] = b_Sym_char("d", "d", 3)
        nfaData.alphabet[4] = b_Sym_char("e", "e", 4)
        nfaData.alphabet[5] = b_Sym_char("f", "f", 5)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (1,2,2) )
        nfaData.transitions.add( (2,3,3) )
        nfaData.transitions.add( (2,4,3) )
        nfaData.transitions.add( (2,5,3) )
        nfaData.transitions.add( (3,0,4) )
        nfaData.transitions.add( (3,1,4) )
        nfaData.final.add(4)

        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        aut.create_char_classes()
        cp = aut.get_automaton()

        result = nfa_data()
        result.states[0] = b_State(0,set())
        result.states[1] = b_State(1,set())
        result.states[2] = b_State(2,set())
        result.states[3] = b_State(3,set())
        result.states[4] = b_State(4,set([0]))
        result.alphabet[6] = b_Sym_char_class(
            "set(['c', 'b'])", set(['c', 'b']), 6
        )
        result.alphabet[7] = b_Sym_char("a", "a", 7)
        result.alphabet[8] = b_Sym_char_class(
            "set(['a', 'b'])", set(['a', 'b']), 8
        )
        result.alphabet[9] = b_Sym_char_class(
            "set(['e', 'd', 'f'])", set(['e', 'd', 'f']), 9
        )
        result.start = 0
        result.transitions = set([(0, 7, 1), (1, 6, 2), (2, 9, 3), (3, 8, 4)])
        result.final.add(4)
        result.Flags["Alphabet collision free"] = False

        self.assertTrue(sorted(cp.states.keys()) == sorted(result.states.keys()))
        self.assertTrue(cp.alphabet == result.alphabet)
        self.assertTrue(cp.start == result.start)
        self.assertTrue(cp.final == result.final)
        self.assertTrue(cp.transitions == result.transitions)
        self.assertTrue(cp.Flags == result.Flags)

        # 3) same for k-char
        # Example: transition between states 1 and 2 with (a, b) and (c, d) ->
        # new symbol ({a,c},{b,d})
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set([0]))
        nfaData.alphabet[0] = b_Sym_kchar(
            "ch0", (frozenset(['a']), frozenset(['b'])), 0
        )
        nfaData.alphabet[1] = b_Sym_kchar(
            "ch1", (frozenset(['c']), frozenset(['d'])), 1
        )
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (0,1,1) )
        nfaData.final.add(1)
        nfaData.Flags["Stride"] = 2
        nfaData.Flags["Strided"] = True

        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        aut.create_char_classes()
        cp = aut.get_automaton()

        result = nfa_data()
        result.states[0] = b_State(0,set())
        result.states[1] = b_State(1,set([0]))
        result.alphabet[2] = b_Sym_kchar(
            "ch2", (frozenset(['a', 'c']), frozenset(['b', 'd'])), 2
        )
        result.start = 0
        result.transitions = set([ (0,2,1) ])
        result.final.add(1)
        result.Flags["Stride"] = 2
        result.Flags["Strided"] = True
        result.Flags["Alphabet collision free"] = False
        
        self.assertTrue(sorted(cp.states.keys()) == sorted(result.states.keys()))
        self.assertTrue(cp.alphabet == result.alphabet)
        self.assertTrue(cp.start == result.start)
        self.assertTrue(cp.final == result.final)
        self.assertTrue(cp.transitions == result.transitions)
        self.assertTrue(cp.Flags == result.Flags)

    def test_get_set_of_nondeterministic_states(self):
        """get_set_of_nondeterministic_states()"""
        # Test with mapper = None
        # Result of method must be non-deterministic states.
        # Non-deterministically state is such a state, it would be possible to
        # get from him a passage through a certain symbol in more than one state.
        # try:
        #   - in automaton is not any nondeterministic state,
        #   - behavior in a situation where at least one machine state is
        #     nondeterministically.

        # 1) Empty automaton
        nfaData = nfa_data()
        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        self.assertTrue(aut.get_set_of_nondeterministic_states() == set([]))

        # 2) In automaton is not any nondeterministic state
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set())
        nfaData.states[4] = b_State(4,set())
        nfaData.states[5] = b_State(5,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.alphabet[3] = b_Sym_char("d", "d", 3)
        nfaData.alphabet[4] = b_Sym_char("e", "e", 4)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (1,2,3) )
        nfaData.transitions.add( (1,3,4) )
        nfaData.transitions.add( (2,4,5) )
        nfaData.transitions.add( (3,4,5) )
        nfaData.transitions.add( (4,4,5) )
        nfaData.final.add(5)

        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        self.assertTrue(aut.get_set_of_nondeterministic_states() == set([]))

        # 3) In automaton is any nondeterministic state
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set())
        nfaData.states[4] = b_State(4,set())
        nfaData.states[5] = b_State(5,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.alphabet[3] = b_Sym_char("d", "d", 3)
        nfaData.alphabet[4] = b_Sym_char("e", "e", 4)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (1,1,3) )
        nfaData.transitions.add( (2,2,4) )
        nfaData.transitions.add( (2,2,5) )
        nfaData.transitions.add( (3,4,4) )
        nfaData.transitions.add( (3,4,5) )
        nfaData.final.add(5)

        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        self.assertTrue(
            aut.get_set_of_nondeterministic_states() == set([1, 2, 3])
        )

    def test_get_compute(self):
        """get_compute()"""
        # Test what returns when:
        #   is not set _compute,
        #   is set _compute.

        # 1) _compute is not set
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set([0]))
        nfaData.alphabet[0] = b_Sym_kchar("ch0", ('a', 'b'), 0)
        nfaData.alphabet[1] = b_Sym_kchar("ch1", ('c', 'd'), 1)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (0,1,1) )
        nfaData.final.add(1)

        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)

        self.assertTrue(aut.get_compute() == False)

        # 2) _compute is set
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set([0]))
        nfaData.alphabet[0] = b_Sym_kchar("ch0", ('a', 'b'), 0)
        nfaData.alphabet[1] = b_Sym_kchar("ch1", ('c', 'd'), 1)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (0,1,1) )
        nfaData.final.add(1)

        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        aut._compute = True

        self.assertTrue(aut.get_compute() == True)


    def test_reduce_alphabet(self):
        """reduce_alphabet()"""
        # The principle of the method consists in the fact that the two
        # characters merge in character class only if they are crossing through
        # the table columns for these two symbols the same way - that these
        # symbols are always found together.
        # Try on several variants of automaton. With some enables automatic
        # merge and some not merge symbol.

        # 0) empty automaton
        nfaData = nfa_data()
        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        aut.reduce_alphabet()
        cp = aut.get_automaton()
        result = nfa_data()
        result.Flags['Alphabet collision free'] = True
        self.assertTrue(sorted(cp.states.keys()) == sorted(result.states.keys()))
        self.assertTrue(cp.alphabet == result.alphabet)
        self.assertTrue(cp.start == result.start)
        self.assertTrue(cp.final == result.final)
        self.assertTrue(cp.transitions == result.transitions)
        self.assertTrue(cp.Flags == result.Flags)

        # 1) merge a,b:
        #    0 --a--> 1 --e--> 2 --a--> 3
        #      |-b-|             |-b-|
        # =>
        #    0 --[ab]--> 1 --e--> 2 --[ab]--> 3
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("e", "e", 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (0,1,1) )
        nfaData.transitions.add( (1,2,2) )
        nfaData.transitions.add( (2,0,3) )
        nfaData.transitions.add( (2,1,3) )
        nfaData.final.add(3)

        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        aut.reduce_alphabet()
        cp = aut.get_automaton()

        result = nfa_data()
        result.states[0] = b_State(0,set())
        result.states[1] = b_State(1,set())
        result.states[2] = b_State(2,set())
        result.states[3] = b_State(3,set([0]))
        result.alphabet[2] = b_Sym_char("e", "e", 2)
        result.alphabet[3] = b_Sym_char_class("['a', 'b']", ['a', 'b'], 3)
        result.start = 0
        result.transitions.add( (0,3,1) )
        result.transitions.add( (1,2,2) )
        result.transitions.add( (2,3,3) )
        result.final.add(3)
        result.Flags["Alphabet collision free"] = True

        self.assertTrue(sorted(cp.states.keys()) == sorted(result.states.keys()))
        self.assertTrue(cp.alphabet == result.alphabet)
        self.assertTrue(cp.start == result.start)
        self.assertTrue(cp.final == result.final)
        self.assertTrue(cp.transitions == result.transitions)
        self.assertTrue(cp.Flags == result.Flags)

        # 2) merge a,b:
        #    0 --a--> 1 --e--> 2 --a--> 3
        #      |-b-|             |-b-|
        #                        |-c-|
        # =>
        #    0 --[ab]--> 1 --e--> 2 --[ab]--> 3
        #                           |---c--|
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.alphabet[3] = b_Sym_char("e", "e", 3)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (0,1,1) )
        nfaData.transitions.add( (1,3,2) )
        nfaData.transitions.add( (2,0,3) )
        nfaData.transitions.add( (2,1,3) )
        nfaData.transitions.add( (2,2,3) )
        nfaData.final.add(3)

        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        aut.reduce_alphabet()
        cp = aut.get_automaton()

        result = nfa_data()
        result.states[0] = b_State(0,set())
        result.states[1] = b_State(1,set())
        result.states[2] = b_State(2,set())
        result.states[3] = b_State(3,set([0]))
        result.alphabet[2] = b_Sym_char("c", "c", 2)
        result.alphabet[3] = b_Sym_char("e", "e", 3)
        result.alphabet[4] = b_Sym_char_class("['a', 'b']", ['a', 'b'], 4)
        result.start = 0
        result.transitions.add( (0,4,1) )
        result.transitions.add( (1,3,2) )
        result.transitions.add( (2,2,3) )
        result.transitions.add( (2,4,3) )
        result.final.add(3)
        result.Flags["Alphabet collision free"] = True

        self.assertTrue(sorted(cp.states.keys()) == sorted(result.states.keys()))
        self.assertTrue(cp.alphabet == result.alphabet)
        self.assertTrue(cp.start == result.start)
        self.assertTrue(cp.final == result.final)
        self.assertTrue(cp.transitions == result.transitions)
        self.assertTrue(cp.Flags == result.Flags)

        # 3) not merge a,b:
        #    0 --a--> 1 --e--> 2 --a--> 3
        #      |-b-|             |-c-|
        # =>
        #    0 --a--> 1 --e--> 2 --a--> 3
        #      |-b-|             |-c-|
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.alphabet[3] = b_Sym_char("e", "e", 3)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (0,1,1) )
        nfaData.transitions.add( (1,3,2) )
        nfaData.transitions.add( (2,0,3) )
        nfaData.transitions.add( (2,2,3) )
        nfaData.final.add(3)

        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        aut.reduce_alphabet()
        cp = aut.get_automaton()

        result = nfa_data()
        result.states[0] = b_State(0,set())
        result.states[1] = b_State(1,set())
        result.states[2] = b_State(2,set())
        result.states[3] = b_State(3,set([0]))
        result.alphabet[0] = b_Sym_char("a", "a", 0)
        result.alphabet[1] = b_Sym_char("b", "b", 1)
        result.alphabet[2] = b_Sym_char("c", "c", 2)
        result.alphabet[3] = b_Sym_char("e", "e", 3)
        result.start = 0
        result.transitions.add( (0,0,1) )
        result.transitions.add( (0,1,1) )
        result.transitions.add( (1,3,2) )
        result.transitions.add( (2,0,3) )
        result.transitions.add( (2,2,3) )
        result.final.add(3)
        result.Flags["Alphabet collision free"] = True

        self.assertTrue(sorted(cp.states.keys()) == sorted(result.states.keys()))
        self.assertTrue(cp.alphabet == result.alphabet)
        self.assertTrue(cp.start == result.start)
        self.assertTrue(cp.final == result.final)
        self.assertTrue(cp.transitions == result.transitions)
        self.assertTrue(cp.Flags == result.Flags)

    def test_stride_2(self):
        """stride_2()"""
        # Principle: From initial state creates new transitions in more
        # character slot so that the transition is carried out over two symbols
        # and between baseline and the state in which we reached after two
        # crossings create a transition which has created kchar type symbol of
        # two symbols through which we passed. In case of not make the
        # transition over two symbols - the first target state is the end
        # state - is necessary as species substitute * symbol (ASCII character
        # class 0 to 255, or you can modify the meaning * predanim character
        # class in the parameter all_chars).
        # Try on a few machines with loops, branching, etc.

        # 0) empty automaton
        nfaData = nfa_data()
        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        aut.stride_2()
        cp = aut.get_automaton()
        result = nfa_data()
        self.assertTrue(sorted(cp.states.keys()) == sorted(result.states.keys()))
        self.assertTrue(cp.alphabet == result.alphabet)
        self.assertTrue(cp.start == result.start)
        self.assertTrue(cp.final == result.final)
        self.assertTrue(cp.transitions == result.transitions)
        self.assertTrue(cp.Flags == result.Flags)

        # 1) concatenation
        # 0 -a-> 1 -b-> 2 -c-> 3  =>  0 -(a,b)-> 1 -(c,*)-> 2
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

        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        aut.stride_2()
        cp = aut.get_automaton()
        result = nfa_data().load_from_file("test_data/(1)stride_2.nfa_data")

        self.assertTrue(sorted(cp.states.keys()) == sorted(result.states.keys()))
        self.assertTrue(cp.alphabet == result.alphabet)
        self.assertTrue(cp.start == result.start)
        self.assertTrue(cp.final == result.final)
        self.assertTrue(cp.transitions == result.transitions)
        self.assertTrue(cp.Flags == result.Flags)

        # 2) branch
        #     |-a--> 1 --d--|
        # 0 --|-b--> 2 --e--|--> 4
        #     |-c--> 3 --f--|
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set())
        nfaData.states[3] = b_State(3,set())
        nfaData.states[4] = b_State(4,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.alphabet[3] = b_Sym_char("d", "d", 3)
        nfaData.alphabet[4] = b_Sym_char("e", "e", 4)
        nfaData.alphabet[5] = b_Sym_char("f", "f", 5)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (0,1,2) )
        nfaData.transitions.add( (0,2,3) )
        nfaData.transitions.add( (1,3,4) )
        nfaData.transitions.add( (2,4,4) )
        nfaData.transitions.add( (3,5,4) )
        nfaData.final.add(4)

        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        aut.stride_2()
        cp = aut.get_automaton()
        result = nfa_data().load_from_file("test_data/(2)stride_2.nfa_data")

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
        nfaData.transitions.add( (1,2,2) )
        nfaData.final.add(2)

        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        aut.stride_2()
        cp = aut.get_automaton()
        result = nfa_data().load_from_file("test_data/(3)stride_2.nfa_data")

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
        #    1 <-  d
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
        nfaData.alphabet[3] = b_Sym_char("d", "d", 3)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (2,2,1) )
        nfaData.transitions.add( (2,3,0) )
        nfaData.final.add(2)

        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        aut.stride_2()
        cp = aut.get_automaton()
        result = nfa_data().load_from_file("test_data/(4)stride_2.nfa_data")

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
        # 0 --a--> 1 --d--> 2
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set([0]))
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.alphabet[3] = b_Sym_char("d", "d", 3)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,1) )
        nfaData.transitions.add( (1,2,1) )
        nfaData.transitions.add( (1,3,2) )
        nfaData.final.add(2)

        aut = b_Automaton()
        aut.create_from_nfa_data(nfaData)
        aut.stride_2()
        cp = aut.get_automaton()
        result = nfa_data().load_from_file("test_data/(5)stride_2.nfa_data")

        self.assertTrue(sorted(cp.states.keys()) == sorted(result.states.keys()))
        self.assertTrue(cp.alphabet == result.alphabet)
        self.assertTrue(cp.start == result.start)
        self.assertTrue(cp.final == result.final)
        self.assertTrue(cp.transitions == result.transitions)
        self.assertTrue(cp.Flags == result.Flags)
        
    def test_set_multilanguage(self):
        """set_multilanguage()"""
        # Test if attribute _multilanguage is correctly set.
        
        # 0) Set to false
        aut = b_Automaton()
        aut.set_multilanguage(False)
        self.assertTrue(aut._multilanguage == False)
        
        # 1) Set to true
        aut = b_Automaton()
        aut.set_multilanguage(True)
        self.assertTrue(aut._multilanguage == True)
        
    def test_get_multilanguage(self):
        """get_multilanguage()"""
        # Test if attribute _multilanguage is correctly returned.
        
        # 0) Return false
        aut = b_Automaton()
        aut._multilanguage = False
        self.assertTrue(aut.get_multilanguage() == False)
        
        # 1) Return true
        aut = b_Automaton()
        aut._multilanguage = True
        self.assertTrue(aut.get_multilanguage() == True)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_b_Automaton)
    unittest.TextTestRunner(verbosity=2).run(suite)
