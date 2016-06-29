###############################################################################
#  test_b_state.py: Module for PATTERN MATCH - test base state class
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

from netbench.pattern_match.b_state import b_State
from netbench.pattern_match.b_state import types
from netbench.pattern_match.coloured_state import ColouredState
from netbench.pattern_match.pattern_exceptions import state_join_exception
import unittest


class test_b_State(unittest.TestCase):
    """Test class for base class for state representation."""

    def test_get_text(self):
        """get_text()"""
        # Check whether the returned value is equal to str(self._id).
        state = b_State(1, set([1]))
        self.assertTrue(state.get_text() == "1")

    def test_get_id(self):
        """get_id()"""
        # Check whether the returned value is self._id.
        state = b_State(1, set([1]))
        self.assertTrue(state.get_id() == 1)

    def test_set_id(self):
        """set_id()"""
        # Check whether the adjustable self._id properly.
        state = b_State(1, set([1]))
        state.set_id(15)
        self.assertTrue(state._id == 15)

    def test_is_final(self):
        """is_final()"""
        # If len(self._rnum) == 0, then returns False, otherwise it returns
        # True.
        state = b_State()
        self.assertTrue(state.is_final() == False)

        final_state = b_State(15, set([0]))
        self.assertTrue(final_state.is_final() == True)

    def test_get_regexp_number(self):
        """get_regexp_number()"""
        # Check whether the returned value is self._rnum.
        state = b_State()
        self.assertTrue(state.get_regexp_number() == set())
        self.assertTrue(state.get_regexp_number() == state._rnum)

        state = b_State(1, set([0]))
        self.assertTrue(state.get_regexp_number() == set([0]))
        self.assertTrue(state.get_regexp_number() == state._rnum)

    def test_set_regexp_number(self):
        """set_regexp_number()"""
        # Check whether the adjustable self._rnum properly.
        state = b_State()
        state.set_regexp_number(set([1]))
        self.assertTrue(state._rnum == set([1]))

    def test_get_type(self):
        """get_type()"""
        # Check whether the returned value is self.ctype and if equal
        # b_state.types["b_State"].
        state = b_State()
        self.assertTrue(state.get_type() == state.ctype and state.get_type() ==
            types["b_State"])

        state = b_State()
        state.ctype = types["ColouredState"]
        state.stypes = [types["ColouredState"]]
        self.assertTrue(state.get_type() == state.ctype and state.get_type() ==
            types["ColouredState"])

    def test_get_support_type(self):
        """get_support_type()"""
        # Check whether the returned value is self.stypes and if it is equal to
        # [b_state.types ["b_State"]].
        state = b_State()
        self.assertTrue(state.get_support_type() == state.stypes
            and state.get_support_type() == [types["b_State"]])

        state = b_State()
        state.ctype = types["ColouredState"]
        state.stypes = [types["ColouredState"]]
        self.assertTrue(state.get_support_type() == state.stypes
            and state.get_support_type() == [types["ColouredState"]])

    def test_join(self):
        """join()"""
        # Check whether _rnum return object contains the values of the two
        # _rnum b_State() class object.
        # Create a class object and try ColouredState whether there would be
        # united in successful cases:
        #   - self is ColouredState
        #   - other is ColouredState

        # SAME CODE AS IN "test_coloured_state.py"

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
        # Check whther _rnum returned object contains the values of the two
        # _rnum b_State() class object.
        state_one = b_State(rnum = set([0]))
        state_two = b_State(rnum = set([1]))
        self.assertTrue((state_one.compute_join(state_two))._rnum == set([0,1]))

    def test___str__(self):
        """__str__()"""
        # determine whether the returned string corresponding str(self._id),
        # call the object function str(object)
        state = b_State()
        self.assertTrue(state.__str__() == "0")

        state = b_State(mid = 15)
        self.assertTrue(state.__str__() == "15")

    def test___repr__(self):
        """__repr__()"""
        # determine whether the returned string corresponding to
        # "<" + str(self._id) + ", " + str(self._rnum) + ">",
        # call the object function repr(object)

        state = b_State()
        self.assertTrue(state.__repr__() == "<0, set([])>")

        state = b_State(mid = 15, rnum = set([0,1]))
        self.assertTrue(state.__repr__() == "<15, set([0, 1])>")

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_b_State)
    unittest.TextTestRunner(verbosity=2).run(suite)
