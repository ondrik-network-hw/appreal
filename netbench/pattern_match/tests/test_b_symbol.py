###############################################################################
#  test_b_symbol.py: Test module for PATTERN MATCH - Base symbol class
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
from netbench.pattern_match.b_symbol import DEF_SYMBOLS
from netbench.pattern_match.b_symbol import b_Symbol
from netbench.pattern_match.sym_char import b_Sym_char
from netbench.pattern_match.sym_char_class import b_Sym_char_class
from netbench.pattern_match.sym_kchar import b_Sym_kchar
from netbench.pattern_match.pattern_exceptions import \
    symbol_resolve_collision_exception, \
    symbol_equality_exception, \
    symbol_double_stride_exception
import unittest

class test_b_Symbol(unittest.TestCase):
    """A base test class to represent a symbol."""

    def test_get_text(self):
        """get_text()"""
        # Check whether the returned content self._text.
        symbol = b_Symbol("symbol", 1)
        self.assertTrue(symbol.get_text() == "symbol")
        self.assertTrue(symbol.get_text() == symbol._text)

    def test_set_text(self):
        """set_text()""" 
        # Check whether the parameter is assigned the contents of text
        # into self._text methods.
        symbol = b_Symbol("symbol", 1)
        self.assertTrue(symbol._text == "symbol")
        symbol.set_text("other symbol")
        self.assertTrue(symbol._text == "other symbol")

    def test_get_id(self):
        """get_id()"""
        # Check whether the returned content self._id.
        symbol = b_Symbol("symbol", 1)
        self.assertTrue(symbol.get_id() == 1)
        self.assertTrue(symbol.get_id() == symbol._id)

    def test_set_id(self):
        """set_id()""" 
        # Method set_id(new_id):
        #   Check whether the content of parameter new_id is assigned to the
        #   self._id.
        symbol = b_Symbol("symbol", 1)
        self.assertTrue(symbol._id == 1)
        symbol.set_id(25)
        self.assertTrue(symbol._id == 25)

    def test_get_type(self):
        """get_type()"""
        # Check whether the returned content self.ctype. It must be
        # manually set as the base class constructor self.ctype
        # argument is not configurable.
        symbol = b_Symbol("symbol", 1)
        symbol.ctype = 0
        self.assertTrue(symbol.ctype == 0)

    def test_resolve_collision(self):
        """resolve_collision()"""
        # Test all three branches of code.
        # - Check the situation when a collision is able to solve the self.
        # - Check the situation when a collision is able to solve compSymbol.
        # - Check a situation where it is not able to resolve the conflict
        #   nor the self nor compSymbol - check thrown
        #   symbol_resolve_collision_exception.
        a = b_Sym_char("symbol", 'a', 0)
        def_1 = DEF_SYMBOLS("default", 1)
        def_2 = DEF_SYMBOLS("default", 2)

        self.assertTrue(def_1.resolve_collision(a) ==
            (set([def_1]), set([]), set([a])))

        self.assertTrue(def_1.resolve_collision(def_2) ==
            (set(), set([def_2]), set()))

        # There is no way how to throw this exception.
        #def_1.ctype = '3'
        #def_2.ctype = '3'
        #try:
        #    def_1.resolve_collision(def_2)
        #    self.assertTrue(False)
        #except symbol_resolve_collision_exception:
        #    self.assertTrue(True)

    def test_double_stride(self):
        """double_stride()"""
        symbol = b_Sym_char("symbol", 'a', 1)
        comp_symbol = b_Sym_char("comp_symbol", 'b', 2)
        cd = b_Sym_char_class("cd", set(['c', 'd']), 3)
        ef = b_Sym_char_class("ef", set(['e', 'f']), 4)
        # check returned local_chars for type char class
        self.assertTrue(cd.double_stride(ef, 2, [set(["e", "f", "g", "h"])])[1]
            == [set(["g", "h"])])

        self.assertTrue(symbol.double_stride(ef, 2,
            [set(["e", "f", "g", "h"])])[1] == [set(["g", "h"])])

        self.assertTrue(symbol.double_stride(cd, 2,
            [set(["e", "f", "g", "h"])])[1] == [set(["e", "f", "g", "h"])])

        # - Check a situation where the operation is able to solve self.
        self.assertTrue(
            symbol.double_stride(comp_symbol, 2, [set(["a", "b"])])[0].ctype
            == '4')
        self.assertTrue(
            symbol.double_stride(comp_symbol, 2, [set(["a", "b"])])[0].kchar
            == (frozenset(['a']), frozenset(['b'])))
        self.assertTrue(
            symbol.double_stride(comp_symbol, 2, [set(["a", "b"])])[0].last
            == 2)
        self.assertTrue(
            symbol.double_stride(comp_symbol, 2, [set(["a", "b"])])[1]
            == [set(['a'])])

        # - Check a situation where the operation is able to solve compSymbol.
        self.assertTrue(
            comp_symbol.double_stride(symbol, 2, [set(["a", "b"])])[0].ctype
            == '4')
        self.assertTrue(
            comp_symbol.double_stride(symbol, 2, [set(["a", "b"])])[0].kchar
            == (frozenset(['b']), frozenset(['a'])))
        self.assertTrue(
            comp_symbol.double_stride(symbol, 3, [set(["a", "b"])])[0].last
            == 3)
        self.assertTrue(
            comp_symbol.double_stride(symbol, 2, [set(["a", "b"])])[1]
            == [set(['b'])])

        # - Check a situation where the operation is not able to resolve
        #   the double stride neither self nor compSymbol - check thrown
        #   symbol_double_stride_exception.
        symbol.ctype = '5'
        comp_symbol.ctype = '5'
        try:
            comp_symbol.double_stride(symbol, 2, [set(["a", "b"])])
            self.assertTrue(False)
        except symbol_double_stride_exception:
            self.assertTrue(True)

    def test___eq__(self):
        """__eq__()"""
        # Test using the operator ==
        # Test all code branches.
        # - Check the situation when compared to able to solve the self.
        # - Check the situation when compared to able to solve other.
        # - Check the situation when the comparison is not able to solve
        #   even the self or other - check thrown symbol_equality_exception.
        # - Check a situation where the self or the other is of a
        #   different type than the inherit by b_symbol -> returns false.
        symbol = b_Sym_char("symbol", 'a', 1)
        comp_symbol = b_Sym_char("comp_symbol", 'a', 2)
        self.assertTrue(symbol == comp_symbol)
        self.assertTrue(comp_symbol == symbol)

        symbol.ctype = '4'
        comp_symbol.ctype = '4'
        try:
            symbol == comp_symbol
            self.assertTrue(False)
        except symbol_equality_exception:
            self.assertTrue(True)

        symbol = b_Sym_char("symbol", 'a', 1)
        state = b_State(0, set([]))
        self.assertTrue((symbol == state) == False)

    def test___ne__(self):
        """__ne__()"""
        # Test using the operator !=
        # Test all code branches.
        # - Check the situation when compared to able to solve the self.
        # - Check the situation when compared to able to solve other.
        # - Check the situation when the comparison is not able to solve
        #   even the self or other - check thrown symbol_equality_exception.
        # - Check a situation where the self or the Other is of a
        #   different type than the inherit from b_symbol -> returns True.
        symbol = b_Sym_char("symbol", 'a', 1)
        comp_symbol = b_Sym_char("comp_symbol", 'b', 2)
        self.assertTrue(symbol != comp_symbol)
        self.assertTrue(comp_symbol != symbol)

        symbol.ctype = '4'
        comp_symbol.ctype = '4'
        try:
            symbol != comp_symbol
            self.assertTrue(False)
        except symbol_equality_exception:
            self.assertTrue(True)

        symbol = b_Sym_char("symbol", 'a', 1)
        state = b_State(0, set([]))
        self.assertTrue(symbol != state)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_b_Symbol)
    unittest.TextTestRunner(verbosity=2).run(suite)
