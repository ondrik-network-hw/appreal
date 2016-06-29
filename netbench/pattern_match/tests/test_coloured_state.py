###############################################################################
#  test_coloured_state.py: Test module for PATTERN MATCH - state with
#  asociated colors
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

from netbench.pattern_match.b_state import b_State, types
from netbench.pattern_match.coloured_state import ColouredState
from netbench.pattern_match.pattern_exceptions import state_join_exception
from netbench.pattern_match.pattern_exceptions import \
    state_colour_operation_not_supported_exception
import unittest

class test_ColouredState(unittest.TestCase):
    """Test module for class ColoureState."""

    def test_get_text(self):
        """get_text()"""
        # Check whether the returned value is str(self._id).
        c_state = ColouredState(6, set([0]), set([11]))
        self.assertTrue(c_state.get_text() == "\"6~11\"")

        c_state = ColouredState(0, set([1]), set([11, 15, 4]))
        self.assertTrue(c_state.get_text() == "\"0~11~4~15\"")

    def test_get_id(self):
        """get_id()"""
        # Check whether the returned value is self._id.
        c_state = ColouredState(2, set([1]), set([11, 15, 4]))
        self.assertTrue(c_state.get_id() == c_state._id == 2)

    def test_set_id(self):
        """set_id()"""
        # Check whether the adjustable self._id properly.
        c_state = ColouredState(2, set([1]), set([11, 15, 4]))
        self.assertTrue(c_state._id == 2)
        c_state.set_id(15)
        self.assertTrue(c_state._id == 15)

    def test_is_final(self):
        """is_final()"""
        # If len(self._rnum) == 0 then returns False, otherwise it returns True.
        c_state = ColouredState(2, set([]), set([11]))
        self.assertTrue(c_state.is_final() == False)

        c_state = ColouredState(5, set([0]), set([11, 15]))
        self.assertTrue(c_state.is_final() == True)

        c_state = ColouredState(5, set([0, 1, 2]), set([11, 15]))
        self.assertTrue(c_state.is_final() == True)

    def test_get_regexp_number(self):
        """get_regexp_number()"""
        # Check whether the returned value is self._rnum.
        c_state = ColouredState(2, set([]), set([11]))
        self.assertTrue(c_state.get_regexp_number() == c_state._rnum
            == set([]))

        c_state = ColouredState(5, set([0]), set([11, 15]))
        self.assertTrue(c_state.get_regexp_number() == c_state._rnum
            == set([0]))

        c_state = ColouredState(7, set([0, 1, 2]), set([11, 14]))
        self.assertTrue(c_state.get_regexp_number() == c_state._rnum
            == set([0, 1, 2]))

    def test_set_regexp_number(self):
        """set_regexp_number()"""
        # Check whether the adjustable self._rnum properly.
        c_state = ColouredState(2, set([]), set([11]))
        self.assertTrue(c_state._rnum == set([]))
        c_state.set_regexp_number(set([1]))
        self.assertTrue(c_state._rnum == set([1]))

        c_state = ColouredState(7, set([0, 1, 2]), set([11, 14]))
        self.assertTrue(c_state._rnum == set([0, 1, 2]))
        c_state.set_regexp_number(set([1, 3, 5]))
        self.assertTrue(c_state._rnum == set([1, 3, 5]))

    def test_get_type(self):
        """get_type()"""
        # Check whether the returned value is self.ctype and if
        # equal b_state.types["ColouredState"].
        c_state = ColouredState(7, set([0, 1, 2]), set([11, 14]))
        self.assertTrue(c_state.get_type() == c_state.ctype ==
            types["ColouredState"])
        
    def test_get_support_type(self):
        """get_support_type()"""
        # Check whether the returned value is self.stypes and if
        # equal to [types["b_State"], types["ColouredState"]]
        c_state = ColouredState(7, set([0, 1, 2]), set([11, 14]))
        self.assertTrue(c_state.get_support_type() == c_state.stypes ==
            [types["b_State"], types["ColouredState"]])

    def test_get_colours(self):
        """get_colours()"""
        # Check whether the returned value is self.colours.
        c_state = ColouredState(7, set([0, 1, 2]), set([11, 14]))
        self.assertTrue(c_state.get_colours() == c_state.colours ==
            set([11, 14]))

    def test_set_colours(self):
        """set_colours()"""
        # Check whether the adjustable self.colours properly.
        c_state = ColouredState(7, set([0, 1, 2]), set([11, 14]))
        self.assertTrue(c_state.colours == set([11, 14]))
        c_state.set_colours(set([3, 5, 7]))
        self.assertTrue(c_state.colours == set([3, 5, 7]))
        
    def test_get_join_method(self):
        """get_join_method()"""
        # Check whether the returned value is self.join_method. Check
        # whether the returned value is one of the union, intersection,
        # difference, symmetric_difference.
        c_state = ColouredState(0, set([]), set([1]))
        self.assertTrue(c_state.get_join_method() == c_state.join_method)
        self.assertTrue(c_state.get_join_method() == "union"
            or c_state.get_join_method() == "intersection"
            or c_state.get_join_method() == "difference"
            or c_state.get_join_method() == "symmetric_difference"
        )

        c_state = ColouredState(0, set([]), set([1]), "intersection")
        self.assertTrue(c_state.get_join_method() == c_state.join_method)
        self.assertTrue(c_state.get_join_method() == "union"
            or c_state.get_join_method() == "intersection"
            or c_state.get_join_method() == "difference"
            or c_state.get_join_method() == "symmetric_difference"
        )

        c_state = ColouredState(0, set([]), set([1]), "difference")
        self.assertTrue(c_state.get_join_method() == c_state.join_method)
        self.assertTrue(c_state.get_join_method() == "union"
            or c_state.get_join_method() == "intersection"
            or c_state.get_join_method() == "difference"
            or c_state.get_join_method() == "symmetric_difference"
        )

        c_state = ColouredState(0, set([]), set([1]), "symmetric_difference")
        self.assertTrue(c_state.get_join_method() == c_state.join_method)
        self.assertTrue(c_state.get_join_method() == "union"
            or c_state.get_join_method() == "intersection"
            or c_state.get_join_method() == "difference"
            or c_state.get_join_method() == "symmetric_difference"
        )

    def test_set_join_method(self):
        """set_join_method()"""
        # Check whether the adjustable self.join_method properly.
        c_state = ColouredState(0, set([]), set([1]))
        self.assertTrue(c_state.join_method == "union")

        c_state.set_join_method("difference")
        self.assertTrue(c_state.join_method == "difference")

        c_state.set_join_method("intersection")
        self.assertTrue(c_state.join_method == "intersection")

    def test_join(self):
        """join()"""
        # Check whether _rnum of returned object contains values of
        # two _rnum b_State() class objects.
        # Create a class object ColouredState and try whether there would
        # be successful united in cases:
        #   - the self is ColouredState
        #   - other is ColouredState

        # SAME CODE AS IN "test_b_state.py"

        # check join two b_State - self join other
        self_state = b_State()
        other_state = b_State()
        self.assertTrue((self_state.join(other_state))._rnum == set())

        self_state = b_State()
        self_state._rnum = set([0])
        other_state = b_State()
        self.assertTrue((self_state.join(other_state))._rnum == set([0]))

        self_state = b_State()
        other_state = b_State()
        other_state._rnum = set([0])
        self.assertTrue((self_state.join(other_state))._rnum == set([0]))

        self_state = b_State()
        self_state._rnum = set([0])
        other_state = b_State()
        other_state._rnum = set([1])
        self.assertTrue((self_state.join(other_state))._rnum == set([0,1]))

        # check join two b_State - other join self
        self_state = b_State()
        other_state = b_State()
        self.assertTrue((other_state.join(self_state))._rnum == set())

        self_state = b_State()
        self_state._rnum = set([0])
        other_state = b_State()
        self.assertTrue((other_state.join(self_state))._rnum == set([0]))

        self_state = b_State()
        other_state = b_State()
        other_state._rnum = set([0])
        self.assertTrue((other_state.join(self_state))._rnum == set([0]))

        self_state = b_State()
        self_state._rnum = set([0])
        other_state = b_State()
        other_state._rnum = set([1])
        self.assertTrue((other_state.join(self_state))._rnum == set([0,1]))

        # self is ColouredState class and other is b_State class
        self_state = ColouredState(0, set([11]), set([1]))
        other_state = b_State(1, set([15]))
        self.assertTrue((self_state.join(other_state))._rnum == set([11, 15]))

        self_state = ColouredState(2, set([14]), set([1]))
        other_state = b_State(3, set([2, 3]))
        self.assertTrue((other_state.join(self_state))._rnum == set([2,3,14]))

        # try error
        self_state.stypes = []
        try :
            self_state.join(other_state)
            self.assertTrue(False)
        except state_join_exception:
            self.assertTrue(True)

        # ColouredState - self join other
        self_state = ColouredState(0, set([]), set([1]))
        other_state = ColouredState(1, set([]), set([5]))
        self.assertTrue((self_state.join(other_state))._rnum == set())

        self_state = ColouredState(0, set([0]), set([1]))
        other_state = ColouredState(1, set([]), set([5]))
        self.assertTrue((self_state.join(other_state))._rnum == set([0]))

        self_state = ColouredState(0, set([0]), set([1]))
        other_state = ColouredState(1, set([1]), set([5]))
        self.assertTrue((self_state.join(other_state))._rnum == set([0, 1]))

        # ColouredState - other join self
        self_state = ColouredState(0, set([]), set([1]))
        other_state = ColouredState(1, set([]), set([5]))
        self.assertTrue((other_state.join(self_state))._rnum == set())

        self_state = ColouredState(0, set([0]), set([1]))
        other_state = ColouredState(1, set([]), set([5]))
        self.assertTrue((other_state.join(self_state))._rnum == set([0]))

        self_state = ColouredState(0, set([]), set([1]))
        other_state = ColouredState(1, set([1]), set([5]))
        self.assertTrue((other_state.join(self_state))._rnum == set([1]))

        self_state = ColouredState(0, set([0]), set([1]))
        other_state = ColouredState(1, set([1]), set([5]))
        self.assertTrue((other_state.join(self_state))._rnum == set([0, 1]))

    def test_compute_join(self):
        """compute_join()"""
        # - Check whether _rnum returned object contains the values of the
        #   two _rnum ColouredState object class.
        # - Check whether the colors returned object contains the values
        #   of colors for the two class object ColouredState()
        #   concentrations under all 4 (union, intersection, difference,
        #   symmetric_difference) connectivity colors - join_method attribute.
        # - If join_method other than 4 appear at the top, check thrown.
        # - Check whether the returned object _id is equal to -2.
        c_state = ColouredState(5, set([0]), set([1, 2]), "union")
        other_state = ColouredState(6, set([1]), set([3, 4]))
        join_state = c_state.compute_join(other_state)
        self.assertTrue(join_state._rnum == set([0,1]))
        self.assertTrue(join_state.colours == set([1,2,3,4]))
        self.assertTrue(join_state._id == -2)

        c_state = ColouredState(5, set([0]), set([1, 2]), "intersection")
        other_state = ColouredState(6, set([1]), set([3, 4]))
        join_state = c_state.compute_join(other_state)
        self.assertTrue(join_state._rnum == set([0,1]))
        self.assertTrue(join_state.colours == set([]))
        self.assertTrue(join_state._id == -2)

        c_state = ColouredState(5, set([0]), set([1, 2, 3, 4]), "intersection")
        other_state = ColouredState(6, set([1]), set([3, 4]))
        join_state = c_state.compute_join(other_state)
        self.assertTrue(join_state._rnum == set([0,1]))
        self.assertTrue(join_state.colours == set([3,4]))
        self.assertTrue(join_state._id == -2)

        c_state = ColouredState(5, set([]), set([1, 2]), "difference")
        other_state = ColouredState(6, set([]), set([3, 4]))
        join_state = c_state.compute_join(other_state)
        self.assertTrue(join_state._rnum == set([]))
        self.assertTrue(join_state.colours == set([1,2]))
        self.assertTrue(join_state._id == -2)

        c_state = ColouredState(5, set([1,2]), set([1, 2]), "difference")
        other_state = ColouredState(6, set([3,4]), set([2,3, 4]))
        join_state = c_state.compute_join(other_state)
        self.assertTrue(join_state._rnum == set([1,2,3,4]))
        self.assertTrue(join_state.colours == set([1]))
        self.assertTrue(join_state._id == -2)

        c_state = ColouredState(5, set([0]),set([1,2,3]),"symmetric_difference")
        other_state = ColouredState(6, set([1]), set([3,4,5]))
        join_state = c_state.compute_join(other_state)
        self.assertTrue(join_state._rnum == set([0,1]))
        self.assertTrue(join_state.colours == set([1,2,4,5]))
        self.assertTrue(join_state._id == -2)

        c_state = ColouredState(5, set([0]),set([1,2]),"error_join")
        other_state = ColouredState(6, set([1]), set([3,4]))
        try:
            c_state.compute_join(other_state)
            self.assertTrue(False)
        except state_colour_operation_not_supported_exception:
            self.assertTrue(True)

    def test__str__(self):
        """__str__()"""
        # Determine whether the returned string corresponding to
        # str(self._id) + ", " + str(self.colours). Call the object
        # function str(object).
        c_state = ColouredState(5, set([0]),set([1, 2]))
        self.assertTrue(c_state.__str__() ==
            str(c_state._id) + ", " + str(c_state.colours))

    def test__repr__(self):
        """__repr__()"""
        # Determine whether the returned string corresponding to
        # "<" + str(self._id) + ", " + str(self._rnum) + ", " +
        # str(self.colours) + ">". To call the object function repr(object).
        c_state = ColouredState(5, set([0]),set([1, 2]))
        self.assertTrue(c_state.__repr__() ==
            "<" + str(c_state._id) + ", " + str(c_state._rnum) + ", " +
            str(c_state.colours) + ">")

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_ColouredState)
    unittest.TextTestRunner(verbosity=2).run(suite)
