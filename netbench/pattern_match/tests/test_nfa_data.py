###############################################################################
#  test_nfa_data.py:
#    Module for PATTERN MATCH - test class for NFA representation
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
from netbench.pattern_match.b_state import b_State, types
from netbench.pattern_match.sym_char import b_Sym_char
from netbench.pattern_match.sym_char_class import b_Sym_char_class
from netbench.pattern_match.b_automaton import b_Automaton
from netbench.pattern_match.pattern_exceptions import general_unsupported_type,\
symbol_not_found, state_id_collision, symbol_id_collision
import unittest, os, subprocess

class test_nfa_data(unittest.TestCase):
    """A base test class for NFA DATA."""

    def test_save_to_file(self):
        """save_to_file()"""
        # To test whether the file it creates, whether it is recorded using
        # load_from_file and results are the same.

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

        try:
            nfaData.save_to_file("try_save_to_file.nfa_data")
            self.assertTrue(True)
        except:
            self.assertTrue(False)

        try:
            load_nfaData = nfa_data().load_from_file(
                "try_save_to_file.nfa_data")
            self.assertTrue(True)
        except:
            self.assertTrue(False)

        try:
            self.assertTrue(sorted(nfaData.states.keys()) ==
                sorted(load_nfaData.states.keys()))
            self.assertTrue(nfaData.alphabet == load_nfaData.alphabet)
            self.assertTrue(nfaData.start == load_nfaData.start)
            self.assertTrue(nfaData.final == load_nfaData.final)
            self.assertTrue(nfaData.transitions == load_nfaData.transitions)
            self.assertTrue(nfaData.Flags == load_nfaData.Flags)
            self.assertTrue(True)
        except:
            self.assertTrue(False)

        try:
            os.unlink("try_save_to_file.nfa_data")
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    def test_load_from_file(self):
        """load_from_file()"""
        # To test whether the file it creates, whether it is recorded using
        # load_from_file and results are the same.

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

        try:
            nfaData.save_to_file("try_load_from_file.nfa_data")
            self.assertTrue(True)
        except:
            self.assertTrue(False)

        try:
            load_nfaData = nfa_data().load_from_file(
                "try_load_from_file.nfa_data")
            self.assertTrue(True)
        except:
            self.assertTrue(False)

        try:
            self.assertTrue(sorted(nfaData.states.keys()) ==
                sorted(load_nfaData.states.keys()))
            self.assertTrue(nfaData.alphabet == load_nfaData.alphabet)
            self.assertTrue(nfaData.start == load_nfaData.start)
            self.assertTrue(nfaData.final == load_nfaData.final)
            self.assertTrue(nfaData.transitions == load_nfaData.transitions)
            self.assertTrue(nfaData.Flags == load_nfaData.Flags)
            self.assertTrue(True)
        except:
            self.assertTrue(False)

        try:
            os.unlink("try_load_from_file.nfa_data")
            self.assertTrue(True)
        except:
            self.assertTrue(False)

        # Test laod file saved by other supported version of Python - are
        # supported version 2.6 and 2.7.

        try:
            load_nfaData = nfa_data().load_from_file(
                "test_data/save_to_file(by_2.7).nfa_data")
            self.assertTrue(True)
        except:
            self.assertTrue(False)

        try:
            self.assertTrue(sorted(nfaData.states.keys()) ==
                sorted(load_nfaData.states.keys()))
            self.assertTrue(nfaData.alphabet == load_nfaData.alphabet)
            self.assertTrue(nfaData.start == load_nfaData.start)
            self.assertTrue(nfaData.final == load_nfaData.final)
            self.assertTrue(nfaData.transitions == load_nfaData.transitions)
            self.assertTrue(nfaData.Flags == load_nfaData.Flags)
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    def test_show(self):
        """show()"""
        # Take the code from the test_b_automaton because show() b_automaton
        # calling this method (from nfa_data).

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

    def test___repr__(self):
        """__repr__()"""
        # To test whether the output corresponds to:
        # "States: " + str(self.states) +
        # "\nAlphabet: " + str(self.alphabet) +
        # "\nStart: " + str(self.start) +
        # "\nTransitions: " + str(self.transitions) +
        # "\nFinal: " + str(self.final) +
        # "\nFlags: " + str(self.Flags) + "\n"

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

        self.assertTrue(
            nfaData.__repr__()
            ==
            "States: " + str(nfaData.states) +
            "\nAlphabet: " + str(nfaData.alphabet) +
            "\nStart: " + str(nfaData.start) +
            "\nTransitions: " + str(nfaData.transitions) +
            "\nFinal: " + str(nfaData.final) +
            "\nFlags: " + str(nfaData.Flags) + "\n"
        )

    def test___str__(self):
        """__str__()"""
        # To test whether the output corresponds to:
        # "States: " + str(self.states) +
        # "\nAlphabet: " + str(self.alphabet) +
        # "\nStart: " + str(self.start) +
        # "\nTransitions: " + str(self.transitions) +
        # "\nFinal: " + str(self.final) +
        # "\nFlags: " + str(self.Flags) + "\n"

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

        self.assertTrue(
            nfaData.__str__()
            ==
            "States: " + str(nfaData.states) +
            "\nAlphabet: " + str(nfaData.alphabet) +
            "\nStart: " + str(nfaData.start) +
            "\nTransitions: " + str(nfaData.transitions) +
            "\nFinal: " + str(nfaData.final) +
            "\nFlags: " + str(nfaData.Flags) + "\n"
        )

    def test_export_to_fsm(self):
        """export_to_fsm()"""
        # To test whether the file is created (by export_to_fsm())
        # and could be load by import_from_fsm()
        # and load nfa_data are same as exported.
        # To test whether a created file reply to canned.

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

        # create files
        nfaData.export_to_fsm(
            FileName="automaton.fsm",
            SymbolFileName = "automaton.sym"
        )

        # check created files
        with open("automaton.fsm") as gen_fsm:
            with open("test_data/hand_fsm.fsm") as hand_fsm:
                self.assertTrue(gen_fsm.readlines() == hand_fsm.readlines())
        with open("automaton.sym") as gen_sym:
            with open("test_data/hand_sym.sym") as hand_sym:
                self.assertTrue(gen_sym.readlines() == hand_sym.readlines())

        # check same nfa_data
        import_nfaData = nfa_data()
        import_nfaData.import_from_fsm(
            FileName="automaton.fsm",
            SymbolFileName = "automaton.sym"
        )
        self.assertTrue(sorted(nfaData.states.keys()) ==
            sorted(import_nfaData.states.keys()))
        self.assertTrue(nfaData.alphabet == import_nfaData.alphabet)
        self.assertTrue(nfaData.start == import_nfaData.start)
        self.assertTrue(nfaData.final == import_nfaData.final)
        self.assertTrue(nfaData.transitions == import_nfaData.transitions)
        nfaData.Flags["ImportFromFsm"] = True
        self.assertTrue(nfaData.Flags == import_nfaData.Flags)

        # delete created files
        os.unlink("automaton.fsm")
        os.unlink("automaton.sym")

    def test_import_from_fsm(self):
        """import_from_fsm()"""
        # Test whether could be imported canned files.

        # saved structure
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

        # load structure
        import_nfaData = nfa_data()
        import_nfaData.import_from_fsm(
            FileName="test_data/hand_fsm.fsm",
            SymbolFileName = "test_data/hand_sym.sym"
        )

        # check structure
        self.assertTrue(sorted(nfaData.states.keys()) ==
            sorted(import_nfaData.states.keys()))
        self.assertTrue(nfaData.alphabet == import_nfaData.alphabet)
        self.assertTrue(nfaData.start == import_nfaData.start)
        self.assertTrue(nfaData.final == import_nfaData.final)
        self.assertTrue(nfaData.transitions == import_nfaData.transitions)
        nfaData.Flags["ImportFromFsm"] = True
        self.assertTrue(nfaData.Flags == import_nfaData.Flags)

    def test_remove_states(self):
        """remove_states()"""
        # To test whether the parameterized states removed.
        # Check the elimination of final and starting.
        # Check functionality for all supported types of input data:
        #   - types = {"b_State":'0', "ColouredState":'1'}

        # 0) test raises: general_unsupported_type if type of states is not
        #    supported
        try:
            nfaData = nfa_data()
            nfaData.states[0] = b_State(0,set())
            nfaData.remove_states({0: "dictionary can not be parametr"})
            self.assertTrue(False)
        except general_unsupported_type:
            self.assertTrue(True)

        # 1) To test whether the parameterized states removed.
        # will use some non empty structure (b_State)

        # called parametr is int
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
        nfaData.remove_states(1)
        self.assertTrue(sorted(nfaData.states.keys()) == [0, 2])
        nfaData.remove_states(2)
        self.assertTrue(nfaData.final == set([]))

        # called parametr is list
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
        nfaData.remove_states([1])
        self.assertTrue(sorted(nfaData.states.keys()) == [0, 2])

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
        nfaData.remove_states([0, 1])
        self.assertTrue(sorted(nfaData.states.keys()) == [2])
        self.assertTrue(nfaData.start == -1)

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
        nfaData.remove_states([0, 1, 2])
        self.assertTrue(sorted(nfaData.states.keys()) == [])
        self.assertTrue(nfaData.final == set([]))

        # called parametr is tuple
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
        nfaData.remove_states((1))
        self.assertTrue(sorted(nfaData.states.keys()) == [0, 2])

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
        nfaData.remove_states((0, 1))
        self.assertTrue(sorted(nfaData.states.keys()) == [2])
        self.assertTrue(nfaData.start == -1)

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
        nfaData.remove_states((0, 1, 2))
        self.assertTrue(sorted(nfaData.states.keys()) == [])
        self.assertTrue(nfaData.final == set([]))

        # called parametr is set
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
        nfaData.remove_states(set([1]))
        self.assertTrue(sorted(nfaData.states.keys()) == [0, 2])

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
        nfaData.remove_states(set([0, 1]))
        self.assertTrue(sorted(nfaData.states.keys()) == [2])
        self.assertTrue(nfaData.start == -1)

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
        nfaData.remove_states(set([0, 1, 2]))
        self.assertTrue(sorted(nfaData.states.keys()) == [])
        self.assertTrue(nfaData.final == set([]))

        # called parametr is frozentset
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
        nfaData.remove_states(frozenset([1]))
        self.assertTrue(sorted(nfaData.states.keys()) == [0, 2])

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
        nfaData.remove_states(frozenset([0, 1]))
        self.assertTrue(sorted(nfaData.states.keys()) == [2])
        self.assertTrue(nfaData.start == -1)

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
        nfaData.remove_states(frozenset([0, 1, 2]))
        self.assertTrue(sorted(nfaData.states.keys()) == [])
        self.assertTrue(nfaData.final == set([]))

        # 2) To test whether the parameterized states removed.
        # will use some non empty structure (ColouredState)

        # called parametr is int
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[0].ctype = types["ColouredState"]
        nfaData.states[0].stypes = [types["ColouredState"]]
        nfaData.states[1] = b_State(1,set())
        nfaData.states[1].ctype = types["ColouredState"]
        nfaData.states[1].stypes = [types["ColouredState"]]
        nfaData.states[2] = b_State(2,set([0]))
        nfaData.states[2].ctype = types["ColouredState"]
        nfaData.states[2].stypes = [types["ColouredState"]]
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (1,2,2) )
        nfaData.final.add(2)
        nfaData.remove_states(1)
        self.assertTrue(sorted(nfaData.states.keys()) == [0, 2])

        # called parametr is list
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[0].ctype = types["ColouredState"]
        nfaData.states[0].stypes = [types["ColouredState"]]
        nfaData.states[1] = b_State(1,set())
        nfaData.states[1].ctype = types["ColouredState"]
        nfaData.states[1].stypes = [types["ColouredState"]]
        nfaData.states[2] = b_State(2,set([0]))
        nfaData.states[2].ctype = types["ColouredState"]
        nfaData.states[2].stypes = [types["ColouredState"]]
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (1,2,2) )
        nfaData.final.add(2)
        nfaData.remove_states([1])
        self.assertTrue(sorted(nfaData.states.keys()) == [0, 2])

        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[0].ctype = types["ColouredState"]
        nfaData.states[0].stypes = [types["ColouredState"]]
        nfaData.states[1] = b_State(1,set())
        nfaData.states[1].ctype = types["ColouredState"]
        nfaData.states[1].stypes = [types["ColouredState"]]
        nfaData.states[2] = b_State(2,set([0]))
        nfaData.states[2].ctype = types["ColouredState"]
        nfaData.states[2].stypes = [types["ColouredState"]]
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (1,2,2) )
        nfaData.final.add(2)
        nfaData.remove_states([0, 1])
        self.assertTrue(sorted(nfaData.states.keys()) == [2])
        self.assertTrue(nfaData.start == -1)

        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[0].ctype = types["ColouredState"]
        nfaData.states[0].stypes = [types["ColouredState"]]
        nfaData.states[1] = b_State(1,set())
        nfaData.states[1].ctype = types["ColouredState"]
        nfaData.states[1].stypes = [types["ColouredState"]]
        nfaData.states[2] = b_State(2,set([0]))
        nfaData.states[2].ctype = types["ColouredState"]
        nfaData.states[2].stypes = [types["ColouredState"]]
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (1,2,2) )
        nfaData.final.add(2)
        nfaData.remove_states([0, 1, 2])
        self.assertTrue(sorted(nfaData.states.keys()) == [])
        self.assertTrue(nfaData.final == set([]))

        # called parametr is tuple
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[0].ctype = types["ColouredState"]
        nfaData.states[0].stypes = [types["ColouredState"]]
        nfaData.states[1] = b_State(1,set())
        nfaData.states[1].ctype = types["ColouredState"]
        nfaData.states[1].stypes = [types["ColouredState"]]
        nfaData.states[2] = b_State(2,set([0]))
        nfaData.states[2].ctype = types["ColouredState"]
        nfaData.states[2].stypes = [types["ColouredState"]]
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (1,2,2) )
        nfaData.final.add(2)
        nfaData.remove_states((1))
        self.assertTrue(sorted(nfaData.states.keys()) == [0, 2])

        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[0].ctype = types["ColouredState"]
        nfaData.states[0].stypes = [types["ColouredState"]]
        nfaData.states[1] = b_State(1,set())
        nfaData.states[1].ctype = types["ColouredState"]
        nfaData.states[1].stypes = [types["ColouredState"]]
        nfaData.states[2] = b_State(2,set([0]))
        nfaData.states[2].ctype = types["ColouredState"]
        nfaData.states[2].stypes = [types["ColouredState"]]
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (1,2,2) )
        nfaData.final.add(2)
        nfaData.remove_states((0, 1))
        self.assertTrue(sorted(nfaData.states.keys()) == [2])
        self.assertTrue(nfaData.start == -1)

        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[0].ctype = types["ColouredState"]
        nfaData.states[0].stypes = [types["ColouredState"]]
        nfaData.states[1] = b_State(1,set())
        nfaData.states[1].ctype = types["ColouredState"]
        nfaData.states[1].stypes = [types["ColouredState"]]
        nfaData.states[2] = b_State(2,set([0]))
        nfaData.states[2].ctype = types["ColouredState"]
        nfaData.states[2].stypes = [types["ColouredState"]]
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (1,2,2) )
        nfaData.final.add(2)
        nfaData.remove_states((0, 1, 2))
        self.assertTrue(sorted(nfaData.states.keys()) == [])
        self.assertTrue(nfaData.final == set([]))

        # called parametr is set
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[0].ctype = types["ColouredState"]
        nfaData.states[0].stypes = [types["ColouredState"]]
        nfaData.states[1] = b_State(1,set())
        nfaData.states[1].ctype = types["ColouredState"]
        nfaData.states[1].stypes = [types["ColouredState"]]
        nfaData.states[2] = b_State(2,set([0]))
        nfaData.states[2].ctype = types["ColouredState"]
        nfaData.states[2].stypes = [types["ColouredState"]]
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (1,2,2) )
        nfaData.final.add(2)
        nfaData.remove_states(set([1]))
        self.assertTrue(sorted(nfaData.states.keys()) == [0, 2])

        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[0].ctype = types["ColouredState"]
        nfaData.states[0].stypes = [types["ColouredState"]]
        nfaData.states[1] = b_State(1,set())
        nfaData.states[1].ctype = types["ColouredState"]
        nfaData.states[1].stypes = [types["ColouredState"]]
        nfaData.states[2] = b_State(2,set([0]))
        nfaData.states[2].ctype = types["ColouredState"]
        nfaData.states[2].stypes = [types["ColouredState"]]
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (1,2,2) )
        nfaData.final.add(2)
        nfaData.remove_states(set([0, 1]))
        self.assertTrue(sorted(nfaData.states.keys()) == [2])
        self.assertTrue(nfaData.start == -1)

        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[0].ctype = types["ColouredState"]
        nfaData.states[0].stypes = [types["ColouredState"]]
        nfaData.states[1] = b_State(1,set())
        nfaData.states[1].ctype = types["ColouredState"]
        nfaData.states[1].stypes = [types["ColouredState"]]
        nfaData.states[2] = b_State(2,set([0]))
        nfaData.states[2].ctype = types["ColouredState"]
        nfaData.states[2].stypes = [types["ColouredState"]]
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (1,2,2) )
        nfaData.final.add(2)
        nfaData.remove_states(set([0, 1, 2]))
        self.assertTrue(sorted(nfaData.states.keys()) == [])
        self.assertTrue(nfaData.final == set([]))

        # called parametr is frozentset
        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[0].ctype = types["ColouredState"]
        nfaData.states[0].stypes = [types["ColouredState"]]
        nfaData.states[1] = b_State(1,set())
        nfaData.states[1].ctype = types["ColouredState"]
        nfaData.states[1].stypes = [types["ColouredState"]]
        nfaData.states[2] = b_State(2,set([0]))
        nfaData.states[2].ctype = types["ColouredState"]
        nfaData.states[2].stypes = [types["ColouredState"]]
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (1,2,2) )
        nfaData.final.add(2)
        nfaData.remove_states(frozenset([1]))
        self.assertTrue(sorted(nfaData.states.keys()) == [0, 2])

        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[0].ctype = types["ColouredState"]
        nfaData.states[0].stypes = [types["ColouredState"]]
        nfaData.states[1] = b_State(1,set())
        nfaData.states[1].ctype = types["ColouredState"]
        nfaData.states[1].stypes = [types["ColouredState"]]
        nfaData.states[2] = b_State(2,set([0]))
        nfaData.states[2].ctype = types["ColouredState"]
        nfaData.states[2].stypes = [types["ColouredState"]]
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (1,2,2) )
        nfaData.final.add(2)
        nfaData.remove_states(frozenset([0, 1]))
        self.assertTrue(sorted(nfaData.states.keys()) == [2])
        self.assertTrue(nfaData.start == -1)

        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[0].ctype = types["ColouredState"]
        nfaData.states[0].stypes = [types["ColouredState"]]
        nfaData.states[1] = b_State(1,set())
        nfaData.states[1].ctype = types["ColouredState"]
        nfaData.states[1].stypes = [types["ColouredState"]]
        nfaData.states[2] = b_State(2,set([0]))
        nfaData.states[2].ctype = types["ColouredState"]
        nfaData.states[2].stypes = [types["ColouredState"]]
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.start = 0
        nfaData.transitions.add( (0,0,1) )
        nfaData.transitions.add( (1,1,1) )
        nfaData.transitions.add( (1,1,2) )
        nfaData.transitions.add( (1,2,2) )
        nfaData.final.add(2)
        nfaData.remove_states(frozenset([0, 1, 2]))
        self.assertTrue(sorted(nfaData.states.keys()) == [])
        self.assertTrue(nfaData.final == set([]))

    def test_remove_symbols(self):
        """remove_symbols()"""
        # To test whether the symbols are passed to be removed.
        # Check functionality for all supported types of input data.

        # 0) test raises: general_unsupported_type if type of symbols is not
        #    supported.
        try:
            nfaData = nfa_data()
            nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
            nfaData.remove_symbols({0: "dictionary can not be parametr"})
            self.assertTrue(False)
        except general_unsupported_type:
            self.assertTrue(True)

        # 1) To test whether the symbols are passed to be removed.

        # called parametr is int
        nfaData = nfa_data()
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.remove_symbols(1)
        self.assertTrue(sorted(nfaData.alphabet.keys()) == [0, 2])

        # called parametr is list
        nfaData = nfa_data()
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.remove_symbols([1])
        self.assertTrue(sorted(nfaData.alphabet.keys()) == [0, 2])

        nfaData = nfa_data()
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.remove_symbols([0, 1])
        self.assertTrue(sorted(nfaData.alphabet.keys()) == [2])

        nfaData = nfa_data()
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.remove_symbols([0, 1, 2])
        self.assertTrue(sorted(nfaData.alphabet.keys()) == [])

        # called parametr is tuple
        nfaData = nfa_data()
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.remove_symbols((1))
        self.assertTrue(sorted(nfaData.alphabet.keys()) == [0, 2])

        nfaData = nfa_data()
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.remove_symbols((0, 1))
        self.assertTrue(sorted(nfaData.alphabet.keys()) == [2])

        nfaData = nfa_data()
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.remove_symbols((0, 1, 2))
        self.assertTrue(sorted(nfaData.alphabet.keys()) == [])

        # called parametr is set
        nfaData = nfa_data()
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.remove_symbols(set([1]))
        self.assertTrue(sorted(nfaData.alphabet.keys()) == [0, 2])

        nfaData = nfa_data()
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.remove_symbols(set([0, 1]))
        self.assertTrue(sorted(nfaData.alphabet.keys()) == [2])

        nfaData = nfa_data()
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.remove_symbols(set([0, 1, 2]))
        self.assertTrue(sorted(nfaData.alphabet.keys()) == [])

        # called parametr is frozentset
        nfaData = nfa_data()
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.remove_symbols(frozenset([1]))
        self.assertTrue(sorted(nfaData.alphabet.keys()) == [0, 2])

        nfaData = nfa_data()
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.remove_symbols(frozenset([0, 1]))
        self.assertTrue(sorted(nfaData.alphabet.keys()) == [2])

        nfaData = nfa_data()
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        nfaData.remove_symbols(frozenset([0, 1, 2]))
        self.assertTrue(sorted(nfaData.alphabet.keys()) == [])

    def test_remove_transitions(self):
        """remove_transitions()"""
        # To test whether the parameters (transitions) are removed.
        # Check functionality for all supported types of input data.

        # 0) test raises: general_unsupported_type if type of transitions is not
        #    supported.
        try:
            nfaData = nfa_data()
            nfaData.transitions = set([(0, 0, 1), (1, 1, 2), (2, 2, 3)])
            nfaData.remove_transitions({0: "dictionary can not be parametr"})
            self.assertTrue(False)
        except general_unsupported_type:
            self.assertTrue(True)

        # 1) To test whether the parameters (transitions) are removed.
        # Check functionality for all supported types of input data.

        # parametr is tuple(int, int, int)
        nfaData = nfa_data()
        nfaData.transitions = set([(0, 0, 1), (1, 1, 2), (2, 2, 3)])
        nfaData.remove_transitions((0, 0, 1) )
        self.assertTrue(nfaData.transitions == set([(1, 1, 2), (2, 2, 3)]))

        # parametr is list(tuple(int, int, int))
        nfaData = nfa_data()
        nfaData.transitions = set([(0, 0, 1), (1, 1, 2), (2, 2, 3)])
        nfaData.remove_transitions([(0, 0, 1), (1, 1, 2)])
        self.assertTrue(nfaData.transitions == set([(2, 2, 3)]))

        # parametr is tuple(tuple(int, int, int))
        nfaData = nfa_data()
        nfaData.transitions = set([(0, 0, 1), (1, 1, 2), (2, 2, 3)])
        nfaData.remove_transitions(((0, 0, 1), (1, 1, 2)))
        self.assertTrue(nfaData.transitions == set([(2, 2, 3)]))

        # parametr is set(tuple(int, int, int))
        nfaData = nfa_data()
        nfaData.transitions = set([(0, 0, 1), (1, 1, 2), (2, 2, 3)])
        nfaData.remove_transitions(set([(0, 0, 1), (1, 1, 2)]))
        self.assertTrue(nfaData.transitions == set([(2, 2, 3)]))

        # parametr is frozenset(tuple(int, int, int))
        nfaData = nfa_data()
        nfaData.transitions = set([(0, 0, 1), (1, 1, 2), (2, 2, 3)])
        nfaData.remove_transitions(frozenset([(0, 0, 1), (1, 1, 2)]))
        self.assertTrue(nfaData.transitions == set([(2, 2, 3)]))

    def test_get_max_state_id(self):
        """get_max_state_id()"""
        # Check whether returns the maximum state id

        nfaData = nfa_data()
        nfaData.states[0] = b_State(0,set())
        nfaData.states[1] = b_State(1,set())
        nfaData.states[2] = b_State(2,set([0]))
        self.assertTrue(nfaData.get_max_state_id() == 2)

    def test_get_max_alphabet_id(self):
        """get_max_alphabet_id()"""
        # Check whether returns the maximum symbol id

        nfaData = nfa_data()
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        self.assertTrue(nfaData.get_max_alphabet_id() == 2)

    def test_has_symbol(self):
        """has_symbol()"""
        # Try whether the object is located in the symbol alphabet.

        nfaData = nfa_data()
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        self.assertTrue(nfaData.has_symbol(
            b_Sym_char("daad", "a", 100)
            ) == True)
        self.assertTrue(nfaData.has_symbol(
            b_Sym_char_class("daad", set(["a"]), 100)
            ) == True)
        self.assertTrue(nfaData.has_symbol(
            b_Sym_char("daad", "e", 100)
            ) == False)
        self.assertTrue(nfaData.has_symbol(
            b_Sym_char_class("daad", set(["e"]), 100)
            ) == False)

    def test_get_symbol_id(self):
        """get_symbol_id()"""
        # If the object is located in the symbol alphabet to check returning
        # the id of the symbol alphabet. Otherwise, check thrown.

        nfaData = nfa_data()
        nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
        nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
        self.assertTrue(nfaData.get_symbol_id(
            b_Sym_char("daad", "b", 200)
            ) == 1)
        try:
            nfaData.get_symbol_id(b_Sym_char("daad", "g", 200))
            self.assertTrue(False)
        except symbol_not_found:
            self.assertTrue(True)

    def test_add_states(self):
        """add_states()"""
        # To test whether states are passed additions, eventually if not thrown.
        # Check added to final.
        # Check functionality for all supported types of input data.

        # 0) test raises: general_unsupported_type if type of states is not
        #    supported.
        try:
            nfaData = nfa_data()
            nfaData.states[0] = b_State(0,set())
            nfaData.states[1] = b_State(1,set())
            nfaData.states[2] = b_State(2,set([0]))
            nfaData.add_states({0: "dictionary can not be parametr"})
            self.assertTrue(False)
        except general_unsupported_type:
            self.assertTrue(True)

        # 1) check adding states / adding to final
        # parametr is type b_State
        nfaData = nfa_data()
        nfaData.add_states(b_State(0,set()))
        self.assertTrue(sorted(nfaData.states.keys()) == [0])
        self.assertTrue(nfaData.final == set([]))
        try:
            nfaData.add_states(b_State(0,set()))
            self.assertTrue(False)
        except state_id_collision:
            self.assertTrue(True)

        nfaData.add_states(b_State(1,set([0])))
        self.assertTrue(sorted(nfaData.states.keys()) == [0, 1])
        self.assertTrue(nfaData.final == set([1]))

        # parametr is type list(b_State)
        nfaData = nfa_data()
        nfaData.add_states([b_State(2,set()), b_State(3,set([1]))])
        self.assertTrue(sorted(nfaData.states.keys()) == [2, 3])
        self.assertTrue(nfaData.final == set([3]))

        # parametr is type tuple(b_State)
        nfaData = nfa_data()
        nfaData.add_states((b_State(2,set()), b_State(3,set([1]))))
        self.assertTrue(sorted(nfaData.states.keys()) == [2, 3])
        self.assertTrue(nfaData.final == set([3]))

        # parametr is type set(b_State)
        nfaData = nfa_data()
        nfaData.add_states(set([b_State(2,set()), b_State(3,set([1]))]))
        self.assertTrue(sorted(nfaData.states.keys()) == [2, 3])
        self.assertTrue(nfaData.final == set([3]))

        # parametr is type frozenset(b_State)
        nfaData = nfa_data()
        nfaData.add_states(frozenset([b_State(2,set()), b_State(3,set([1]))]))
        self.assertTrue(sorted(nfaData.states.keys()) == [2, 3])
        self.assertTrue(nfaData.final == set([3]))

    def test_add_symbols(self):
        """add_symbols()"""
        # To test whether the symbols are passed additions, eventually if not
        # thrown.
        # Check functionality for all supported types of input data.

        # 0) test raises: general_unsupported_type if type of symbols is not
        #    supported.
        try:
            nfaData = nfa_data()
            nfaData.alphabet[0] = b_Sym_char("a", "a", 0)
            nfaData.alphabet[1] = b_Sym_char("b", "b", 1)
            nfaData.alphabet[2] = b_Sym_char("c", "c", 2)
            nfaData.add_symbols({0: "dictionary can not be parametr"})
            self.assertTrue(False)
        except general_unsupported_type:
            self.assertTrue(True)

        # 1) check adding symbols for all types of parametr
        # parametr is type b_Symbol
        nfaData = nfa_data()
        self.assertTrue(nfaData.has_symbol(b_Sym_char("a", "a", 0)) == False)
        nfaData.add_symbols(b_Sym_char("a", "a", 0))
        self.assertTrue(sorted(nfaData.alphabet.keys()) == [0])
        try:
            nfaData.add_symbols(b_Sym_char("a", "a", 0))
            self.assertTrue(False)
        except symbol_id_collision:
            self.assertTrue(True)

        # parametr is type list(b_Symbol)
        nfaData = nfa_data()
        self.assertTrue(nfaData.check_symbols(
            [b_Sym_char("a", "a", 0), b_Sym_char("b", "b", 1)]
            ) == [False, False])
        nfaData.add_symbols(
            [b_Sym_char("a", "a", 0), b_Sym_char("b", "b", 1)]
        )
        self.assertTrue(sorted(nfaData.alphabet.keys()) == [0, 1])

        # parametr is type tuple(b_Symbol)
        nfaData = nfa_data()
        self.assertTrue(nfaData.check_symbols(
            [b_Sym_char("a", "a", 0), b_Sym_char("b", "b", 1)]
            ) == [False, False])
        nfaData.add_symbols(
            (b_Sym_char("a", "a", 0), b_Sym_char("b", "b", 1))
        )
        self.assertTrue(sorted(nfaData.alphabet.keys()) == [0, 1])

        # parametr is type set(b_Symbol)
        nfaData = nfa_data()
        self.assertTrue(nfaData.check_symbols(
            [b_Sym_char("a", "a", 0), b_Sym_char("b", "b", 1)]
            ) == [False, False])
        nfaData.add_symbols(
            set([b_Sym_char("a", "a", 0), b_Sym_char("b", "b", 1)])
        )
        self.assertTrue(sorted(nfaData.alphabet.keys()) == [0, 1])

        # parametr is type frozenset(b_Symbol)
        nfaData = nfa_data()
        self.assertTrue(nfaData.check_symbols(
            [b_Sym_char("a", "a", 0), b_Sym_char("b", "b", 1)]
            ) == [False, False])
        nfaData.add_symbols(
            frozenset([b_Sym_char("a", "a", 0), b_Sym_char("b", "b", 1)])
        )
        self.assertTrue(sorted(nfaData.alphabet.keys()) == [0, 1])

    def test_add_transitions(self):
        """add_transitions()"""
        # To test whether transitions are passed added.
        # Check functionality for all supported types of input data.

        # 0) test raises: general_unsupported_type if type of transitions is not
        #    supported
        try:
            nfaData = nfa_data()
            nfaData.transitions.add( (0,0,1) )
            nfaData.transitions.add( (1,1,1) )
            nfaData.transitions.add( (1,1,2) )
            nfaData.add_transitions({0: "dictionary can not be parametr"})
            self.assertTrue(False)
        except general_unsupported_type:
            self.assertTrue(True)

        # 1) check adding transitions for all called types
        # called type is tuple(int, int, int)
        nfaData = nfa_data()
        nfaData.add_transitions( (0, 0, 1) )
        self.assertTrue(nfaData.transitions == set([(0, 0, 1)]))

        # called type is list(tuple(int, int, int))
        nfaData = nfa_data()
        nfaData.add_transitions( [(0, 0, 1), (1, 1, 2)] )
        self.assertTrue(nfaData.transitions == set([(0, 0, 1), (1, 1, 2)]))

        # called type is tuple(tuple(int, int, int))
        nfaData = nfa_data()
        nfaData.add_transitions( ((0, 0, 1), (1, 1, 2)) )
        self.assertTrue(nfaData.transitions == set([(0, 0, 1), (1, 1, 2)]))

        # called type is set(tuple(int, int, int))
        nfaData = nfa_data()
        nfaData.add_transitions( set([(0, 0, 1), (1, 1, 2)]) )
        self.assertTrue(nfaData.transitions == set([(0, 0, 1), (1, 1, 2)]))

        # called type is frozenset(tuple(int, int, int))
        nfaData = nfa_data()
        nfaData.add_transitions( frozenset([(0, 0, 1), (1, 1, 2)]) )
        self.assertTrue(nfaData.transitions == set([(0, 0, 1), (1, 1, 2)]))

    def test_check_symbols(self):
        """check_symbols()"""
        # Check whether the result corresponds to the passed symbols and
        # alphabet.

        # 0) test raises: general_unsupported_type if type of symbols is not
        #    supported.
        try:
            nfaData = nfa_data()
            nfaData.check_symbols({0: "dictionary can not be parametr"})
            self.assertTrue(False)
        except general_unsupported_type:
            self.assertTrue(True)

        # 1) check correct output
        # called parametr is type list(b_Symbol)
        nfaData = nfa_data()
        nfaData.alphabet[0] = b_Sym_char('a', 'a', 5)
        self.assertTrue(
            nfaData.check_symbols(
                [
                b_Sym_char('b', 'a', 13),
                b_Sym_char_class("set(['a', 'b'])", set(['a', 'b']), 10)
                ]
            )
            == [True, False]
        )

        # called parametr is type tuple(b_Symbol)
        nfaData = nfa_data()
        nfaData.alphabet[0] = b_Sym_char('a', 'a', 5)
        self.assertTrue(
            nfaData.check_symbols(
                (
                b_Sym_char('b', 'a', 13),
                b_Sym_char_class("set(['a', 'b'])", set(['a', 'b']), 10)
                )
            )
            == [True, False]
        )

        # called parametr is type set(b_Symbol)
        nfaData = nfa_data()
        nfaData.alphabet[0] = b_Sym_char('a', 'a', 5)
        self.assertTrue(
            nfaData.check_symbols(
                set([
                b_Sym_char('b', 'a', 13),
                b_Sym_char_class("set(['a', 'b'])", set(['a', 'b']), 10)
                ])
            )
            == [True, False]
        )

        # called parametr is type frozenset(b_Symbol)
        nfaData = nfa_data()
        nfaData.alphabet[0] = b_Sym_char('a', 'a', 5)
        self.assertTrue(
            nfaData.check_symbols(
                frozenset([
                b_Sym_char('b', 'a', 13),
                b_Sym_char_class("set(['a', 'b'])", set(['a', 'b']), 10)
                ])
            )
            == [True, False]
        )

    def test_is_empty(self):
        """is_empty()"""
        # Check whether the object with only nfa_data (self.states) == 0 returns
        # True and in case of the len() is greater returns False.

        nfaData = nfa_data()
        self.assertTrue(nfaData.is_empty() == True)

        nfaData.add_states(b_State(3, set([1])))
        self.assertTrue(nfaData.is_empty() == False)
        nfaData.add_states(b_State(4, set([])))
        self.assertTrue(nfaData.is_empty() == False)

        nfaData.remove_states([3, 4])
        self.assertTrue(nfaData.is_empty() == True)

    def test_is_consistent(self):
        """is_consistent()"""
        # Test functionality with syndrome = None and syndrome = dict().
        # At the correct object nfa_data should return True if errors in it
        # must return False.
        # List of errors:
        #   - in self.states are not states
        #   - in self.alphabet are not symbols
        #   - in transition are not objects of type tuple or a tuple has
        #     different length than 3
        #   - all symbols and states referenced from transitions must exist
        #   - all states linked from final must exist
        #   - symbols linked from the start must exist or the start must be -1
        #   - for all states must correct self._id with self.states.keys()
        #   - for all symbols must correct self._id with self.alphabet.keys()
        # In dictionary "syndrome" are found the id / transitions
        # which this caused.

        # 1) At the correct object nfa_data should return True if errors in it
        # must return False.
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
        self.assertTrue(nfaData.is_consistent() == True)
        # 4 ) in transition are not objects of type tuple or a tuple has
        # different length than 3
        nfaData.add_transitions( (0, 2) )
        self.assertTrue(nfaData.is_consistent() == False)
        nfaData.remove_transitions( [ (0, 2) ] )
        self.assertTrue(nfaData.is_consistent() == True)
        nfaData.states[0] = b_Sym_char("a", "a", 0)
        nfaData.alphabet[2] = b_State(1,set([0]))
        mistakes = {}
        self.assertTrue(nfaData.is_consistent(mistakes) == False)
        self.assertTrue(mistakes == {0: [0], 3: [(0, 0, 1)], 7: [2]})

        # 2) in self.states are not states
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
        self.assertTrue(nfaData.is_consistent() == True)
        nfaData.remove_states([0])
        mistakes = {}
        self.assertTrue(nfaData.is_consistent(mistakes) == False)
        self.assertTrue(mistakes[3] == [(0,0,1)] and mistakes[5] == [-1])

        # 3) in self.alphabet are not symbols
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
        self.assertTrue(nfaData.is_consistent() == True)
        nfaData.remove_symbols(2)
        mistakes = {}
        self.assertTrue(nfaData.is_consistent(mistakes) == False)
        self.assertTrue(mistakes[3] == [(1, 2, 2)])

        # 5) all symbols and states referenced from transitions must exist
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
        self.assertTrue(nfaData.is_consistent() == True)
        nfaData.add_transitions( (3, 0, 4) )
        self.assertTrue(nfaData.is_consistent() == False)
        nfaData.remove_transitions( (3, 0, 4) )
        self.assertTrue(nfaData.is_consistent() == True)
        nfaData.add_transitions( (1, 5, 2) )
        mistakes = {}
        self.assertTrue(nfaData.is_consistent(mistakes) == False)
        self.assertTrue(mistakes[3] == [(1, 5, 2)])

        # 6) all states linked from final must exist
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
        self.assertTrue(nfaData.is_consistent() == True)
        nfaData.add_transitions( (2, 1, 0) )
        self.assertTrue(nfaData.is_consistent() == True)
        nfaData.final.add(3)
        mistakes = {}
        self.assertTrue(nfaData.is_consistent(syndrome = mistakes) == False)
        self.assertTrue(mistakes[4] == [3])

        # 7) symbols linked from the start must exist or the start must be -1
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
        self.assertTrue(nfaData.is_consistent() == True)
        nfaData.start = 1
        nfaData.remove_transitions( (0, 0, 1) )
        nfaData.remove_symbols( [0] )
        nfaData.remove_states( [0] )
        self.assertTrue(nfaData.is_consistent() == True)

        # 8) for all states must correct self._id with self.states.keys()
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
        self.assertTrue(nfaData.is_consistent() == True)
        nfaData.states[0].set_id( 15 )
        mistakes = {}
        self.assertTrue(nfaData.is_consistent(syndrome = mistakes) == False)
        self.assertTrue(mistakes[6] == [0])

        # 9) for all symbols must correct self._id with self.alphabet.keys()
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
        self.assertTrue(nfaData.is_consistent() == True)
        nfaData.alphabet[0].set_id( 15 )
        self.assertTrue(nfaData.is_consistent() == False)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_nfa_data)
    unittest.TextTestRunner(verbosity=2).run(suite)
