# -*- coding: iso-8859-2 -*-
###############################################################################
#  test_sym_char.py: Test module for PATTERN MATCH - symbol char class
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

#from netbench.pattern_match.b_state import b_State
#from netbench.pattern_match.sym_kchar import b_Sym_kchar
from netbench.pattern_match.b_symbol import io_mapper 
from netbench.pattern_match.sym_char import b_Sym_char
from netbench.pattern_match.sym_char_class import b_Sym_char_class
from netbench.pattern_match.sym_kchar import b_Sym_kchar
from netbench.pattern_match.sym_string import b_Sym_string
from netbench.pattern_match.pattern_exceptions import \
    symbol_string_to_short, \
    symbol_accept_exception, \
    symbol_import_exception
import unittest

class test_b_Sym_char(unittest.TestCase):
    """A base test class to represent a char symbol."""

    def test_accept(self):
        """accept()"""
        # method accept(text):
        # Check return text if self.char == ""
        sym_char = b_Sym_char('', '', 1)
        self.assertTrue(sym_char.accept("some_text") == "some_text")

        # Check if len(text) == 0,
        # then is call exception symbol_string_to_short
        sym_char = b_Sym_char('a', 'a', 1)
        try:
            sym_char.accept("")
            self.assertTrue(False)
        except symbol_string_to_short: 
            self.assertTrue(True)

        # Check if text[0] == self.char[0], then is return value text[1:]
        sym_char = b_Sym_char('a', 'a', 1)
        self.assertTrue(sym_char.accept("adam") == "dam")

        # In case text[0] != self.char[0],
        # then is call exception symbol_accept_exception
        sym_char = b_Sym_char('a', 'a', 1)
        try:
            sym_char.accept("eva")
            self.assertTrue(False)
        except symbol_accept_exception:
            self.assertTrue(True)

    def test_collision(self):
        """collision()"""
        # method collision(set_of_symbols):
        # Try with suitable objects class sym_char, sym_char_class,
        # sym_string. Check correct output (is / is not collision).
        sym_char = b_Sym_char('a', 'a', 1)
        other_sym_char = b_Sym_char('b', 'b', 2)
        sym_char_class = b_Sym_char_class("set(['c', 'd'])", set(['c', 'd']), 3)
        sym_string = b_Sym_string("adam", "adam", 4)
        set_of_symbols = set([other_sym_char, sym_char_class, sym_string])
        self.assertTrue(sym_char.collision(set_of_symbols) == True)

        sym_string = b_Sym_string("eva", "eva", 4)
        set_of_symbols = set([other_sym_char, sym_char_class, sym_string])
        self.assertTrue(sym_char.collision(set_of_symbols) == False)

    def test_export_symbol(self):
        """export_symbol()"""
        # Check return correct representation of symbol.
        sym_char = b_Sym_char('a', 'a', 1)
        self.assertTrue(sym_char.export_symbol() == "061")
        sym_char = b_Sym_char('á', 'á', 2)
        self.assertTrue(sym_char.export_symbol() == "0e1")

    def test_import_symbol(self):
        """import_symbol()"""
        # method import_symbol(text_repr, tid):
        # Check whether is from text_repr created and returned correct object
        # and having set self._id on tid and all parametrs are correct set.
        sym_char = b_Sym_char('b', 'b', 1)
        self.assertTrue(sym_char.char == 'b')
        self.assertTrue(sym_char._text == 'b')
        self.assertTrue(sym_char._id == 1)

        sym_char.import_symbol("061", 15)
        self.assertTrue(sym_char.char == "a")
        self.assertTrue(sym_char._text == 'a')
        self.assertTrue(sym_char._id == 15)

        sym_char.import_symbol("0e1", 16)
        self.assertTrue(sym_char.char == 'á')
        self.assertTrue(sym_char._text == 'á')
        self.assertTrue(sym_char._id == 16)

        # Check if is text_repr represented by other type, then is call
        # exception symbol_import_exception.
        try:
            sym_char.import_symbol("161", 17)
            self.assertTrue(False)
        except symbol_import_exception:
            self.assertTrue(True)

    def test__str__(self):
        """__str__()"""
        # Check return self.char.
        # For test use call str(object).
        sym_char = b_Sym_char('b', 'b', 1)
        self.assertTrue(sym_char.__str__() == sym_char.char)
        self.assertTrue(sym_char.__str__() == "b")

    def test_compute_equal(self):
        """compute_equal()"""
        # method compute_equal(other):
        # If other is object b_Sym_char class then return True, if arguments
        # char are same.
        sym_char = b_Sym_char('a', 'a', 1)
        other_sym_char = b_Sym_char('b', 'b', 2)
        self.assertTrue(sym_char.compute_equal(other_sym_char) == False)

        sym_char = b_Sym_char('a', 'a', 1)
        other_sym_char = b_Sym_char('a', 'a', 2)
        self.assertTrue(sym_char.compute_equal(other_sym_char) == True)

        # If other is class object b_Sym_char_class, return True, if 
        # len(other.charClass) == 1 and values arguments char and charClass
        # are same.
        sym_char = b_Sym_char('a', 'a', 1)
        sym_char_class = b_Sym_char_class("ch2", set(['c']), 2)
        self.assertTrue(sym_char.compute_equal(sym_char_class) == False)

        sym_char = b_Sym_char('a', 'a', 1)
        sym_char_class = b_Sym_char_class("ch2", set(['a']), 2)
        self.assertTrue(sym_char.compute_equal(sym_char_class) == True)

    def test___hash__(self):
        """__hash__()"""
        # Check return hash(self.char).
        sym_char = b_Sym_char('a', 'a', 1)
        self.assertTrue(sym_char.__hash__() == hash(sym_char.char))

    def test___repr__(self):
        """__repr__()"""
        # Check return self.char.
        sym_char = b_Sym_char('a', 'a', 1)
        self.assertTrue(sym_char.__repr__() == repr(sym_char.char))

    def test_get_support_type(self):
        """get_support_type()"""
        # Check return [b_symbol.io_mapper["b_Sym_char"],
        # b_symbol.io_mapper["b_Sym_char_class"]] 
        sym_char = b_Sym_char('a', 'a', 1)
        self.assertTrue(sym_char.get_support_type() == 
            [io_mapper["b_Sym_char"], io_mapper["b_Sym_char_class"]])

    def test_compute_collision(self):
        """compute_collision()"""
        # method compute_collision(compSymbol):
        # Check compute of collision for object of type sym_char and
        # sym_char_class.

        # sym_char and sym_char ; not collision
        a = b_Sym_char('a', 'a', 1)
        b = b_Sym_char('b', 'b', 2)

        self.assertTrue(a.compute_collision(b) == (set([a]), set(), set([b])))

        # sym_char and sym_char ; collision
        a = b_Sym_char('a', 'a', 1)
        other_a = b_Sym_char('a', 'a', 3)
        from copy import deepcopy
        copy_a = deepcopy(a)
        copy_other_a = deepcopy(other_a)

        result = a.compute_collision(other_a)
        # check there are not changes on original symbols
        new_symbol = result[1].pop()
        self.assertTrue(result[0] == set())
        self.assertTrue(result[2] == set())
        self.assertTrue(new_symbol.char == 'a')
        self.assertTrue(new_symbol._id == -2)

        # sym_char and sym_char_class ; not collision
        a = b_Sym_char('a', 'a', 1)
        c_d = b_Sym_char_class("set(['c', 'd'])", set(['c', 'd']), 4)

        self.assertTrue(a.compute_collision(c_d) == (set([a]), set(), set([c_d])))

        # sym_char and sym_char_class ; collision
        a = b_Sym_char('a', 'a', 1)
        a_b = b_Sym_char_class("set(['a', 'b'])", set(['a', 'b']), 5)
        copy_a = deepcopy(a)
        copy_a_b = deepcopy(a_b)

        result = a.compute_collision(a_b)
        # check there are not changes on original symbols
        self.assertTrue(a == copy_a)
        self.assertTrue(a_b == copy_a_b)
        newSymbol = result[1].pop()
        self.assertTrue(result[0] == set())
        self.assertTrue(newSymbol.char == 'a')
        self.assertTrue(newSymbol._id == -2)
        newSymbol = result[2].pop()
        self.assertTrue(newSymbol.ctype == '1')
        self.assertTrue(newSymbol.charClass == set(['b']))

    def test_is_empty(self):
        """is_empty()"""
        # Check return True if len(self.char) == 0 and self._id != -1,
        # otherwise return False.

        a = b_Sym_char('a', 'a', 1)
        self.assertTrue(a.is_empty() == False)

        epsilon = b_Sym_char('epsilon', '', -1)
        self.assertTrue(epsilon.is_empty() == False)

        a = b_Sym_char('a', 'a', -1)
        self.assertTrue(a.is_empty() == False)

        empty = b_Sym_char('empty', '', 15)
        self.assertTrue(empty.is_empty() == True)

    def test_compute_double_stride(self):
        """compute_double_stride()"""
        # Method compute_double_stride(compSymbol, reverse, last, local_chars)
        # Test with compSymbol type sym_char and sym_char_class.
        # If the reverse is True then change order self and compSymbol.

        # compSymbol type sym_char ; reverse = False
        a = b_Sym_char('a', 'a', 0)
        b = b_Sym_char('b', 'b', 1)
        local_chars = list()
        chars = set()
        for i in range(0,256):
            chars.add(chr(i))
        local_chars.append(chars)

        new_kchar = a.compute_double_stride(b, False, 2, local_chars)[0]
        new_local_chars = a.compute_double_stride(b, False, 2, local_chars)[1]

        reference_kchar = b_Sym_kchar("ab", ('a','b'), 2)
        reference_kchar_2 = \
            b_Sym_kchar("ab", (frozenset(['a']),frozenset(['b'])), 2)
        reference_kchar.last = 2
        reference_kchar_2.last = 2
        reference_local_chars = local_chars[0] - set([b.char])

        self.assertTrue(new_kchar == reference_kchar
            or new_kchar == reference_kchar_2)
        self.assertTrue(new_local_chars[0] == reference_local_chars)
        self.assertTrue(new_kchar.last == 2)

        # compSymbol type sym_char_class ; reverse = False
        a = b_Sym_char('a', 'a', 0)
        bc = b_Sym_char_class("set(['b', 'c'])", set(['b', 'c']), 1)
        local_chars = list()
        chars = set()
        for i in range(0,256):
            chars.add(chr(i))
        local_chars.append(chars)

        new_kchar = a.compute_double_stride(bc, False, 3, local_chars)[0]
        new_local_chars = a.compute_double_stride(bc, False, 3, local_chars)[1]

        reference_kchar = b_Sym_kchar("a[bc]", ('a',set(['b', 'c'])), 2)
        reference_kchar_2 = \
            b_Sym_kchar("a[bc]", (frozenset(['a']),frozenset(['b','c'])), 2)
        reference_kchar.last = 3
        reference_kchar_2.last = 3
        reference_local_chars = local_chars[0] - bc.charClass

        self.assertTrue(new_kchar == reference_kchar
            or new_kchar == reference_kchar_2)
        self.assertTrue(new_local_chars[0] == reference_local_chars)
        self.assertTrue(new_kchar.last == 3)

        # compSymbol type sym_char ; reverse = True
        a = b_Sym_char('a', 'a', 0)
        b = b_Sym_char('b', 'b', 1)
        local_chars = list()
        chars = set()
        for i in range(0,256):
            chars.add(chr(i))
        local_chars.append(chars)

        new_kchar = a.compute_double_stride(b, True, 2, local_chars)[0]
        new_local_chars = a.compute_double_stride(b, True, 2, local_chars)[1]

        reference_kchar = b_Sym_kchar("ba", ('b','a'), 2)
        reference_kchar_2 = \
            b_Sym_kchar("ba", (frozenset(['b']),frozenset(['a'])), 2)
        reference_kchar.last = 2
        reference_kchar_2.last = 2
        reference_local_chars = local_chars[0] - set([a.char])

        self.assertTrue(new_kchar == reference_kchar
            or new_kchar == reference_kchar_2)
        self.assertTrue(new_local_chars[0] == reference_local_chars)
        self.assertTrue(new_kchar.last == 2)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_b_Sym_char)
    unittest.TextTestRunner(verbosity=2).run(suite)
