###############################################################################
#  test_sym_char_class.py: Test module for PATTERN MATCH - symbol char class
#                          class
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

from netbench.pattern_match.b_symbol import io_mapper
from netbench.pattern_match.sym_char import b_Sym_char
from netbench.pattern_match.sym_kchar import b_Sym_kchar
from netbench.pattern_match.sym_string import b_Sym_string
from netbench.pattern_match.sym_char_class import b_Sym_char_class
from netbench.pattern_match.pattern_exceptions import \
    symbol_string_to_short, \
    symbol_accept_exception, \
    symbol_import_exception
import unittest

class test_b_Sym_char_class(unittest.TestCase):
    """A base test class to represent a char class symbol."""

    def test_accept(self):
        """accept()"""
        # method accept(text):

        # Check if len(text) == 0,
        # then is call exception symbol_string_to_short
        ab = b_Sym_char_class("ab", set(['a', 'b']), 0)
        try:
            ab.accept("")
            self.assertTrue(False)
        except symbol_string_to_short: 
            self.assertTrue(True)

        # Check if text[0] in self.charClass, then is return value text[1:]
        ab = b_Sym_char_class("ab", set(['a', 'b']), 0)
        self.assertTrue(ab.accept("adam") == "dam")

        # In case text[0] != self.char[0],
        # then is call exception symbol_accept_exception
        ab = b_Sym_char_class("ab", set(['a', 'b']), 0)
        try:
            ab.accept("eva")
            self.assertTrue(False)
        except symbol_accept_exception:
            self.assertTrue(True)

    def test_collision(self):
        """collision()"""
        # method collision(set_of_symbols):
        # Try with suitable objects class sym_char, sym_char_class,
        # sym_string. Check correct output (is / is not collision).
        a = b_Sym_char('a', 'a', 0)
        cd = b_Sym_char_class("set(['c', 'd'])", set(['c', 'd']), 1)
        ef = b_Sym_char_class("set(['e', 'f'])", set(['e', 'f']), 2)
        adam = b_Sym_string("baba", "baba", 3)
        set_of_symbols = set([a, cd, adam])
        self.assertTrue(ef.collision(set_of_symbols) == False)

        fg = b_Sym_char_class("set(['f', 'g'])", set(['f', 'g']), 4)
        set_of_symbols = set([a, fg, adam])
        self.assertTrue(ef.collision(set_of_symbols) == True)

    def test_export_symbol(self):
        """export_symbol()"""
        # Check return correct representation of symbol.
        cd = b_Sym_char_class("set(['c', 'd'])", set(['c', 'd']), 0)
        self.assertTrue(cd.export_symbol() == "16364")

    def test_import_symbol(self):
        """import_symbol()"""
        # method import_symbol(text_repr, tid):
        # Check whether is from text_repr created and returned correct object
        # and having set self._id on tid and all parametrs are correct set.
        cd = b_Sym_char_class("set(['c', 'd'])", set(['c', 'd']), 0)
        cd.import_symbol("16566", 15)
        self.assertTrue(cd.charClass == set(['e', 'f']))
        self.assertTrue(cd._text == "[ef]")
        self.assertTrue(cd._id == 15)

        # Check if is text_repr represented by other type, then is call
        # exception symbol_import_exception.
        try:
            cd.import_symbol("061", 17)
            self.assertTrue(False)
        except symbol_import_exception:
            self.assertTrue(True)

    def test___str__(self):
        """__str__()"""
        # Check return self.charClass
        cd = b_Sym_char_class("set(['c', 'd'])", set(['c', 'd']), 0)
        self.assertTrue(cd.__str__() == str(cd.charClass))

    def test_compute_equal(self):
        """compute_equal()"""
        # method compute_equal(other):
        # If is other object of type sym_char_class return True if
        # arguments are same, otherwise return False.
        cd = b_Sym_char_class("set(['c', 'd'])", set(['c', 'd']), 0)
        ef = b_Sym_char_class("set(['e', 'f'])", set(['e', 'f']), 1)
        self.assertTrue(cd.compute_equal(ef) == False)

        ef = b_Sym_char_class("set(['c', 'd'])", set(['d', 'c']), 1)
        self.assertTrue(cd.compute_equal(ef) == True)

        a = b_Sym_char('a', 'a', 0)
        self.assertTrue(cd.compute_equal(a) == False)

    def test___hash__(self):
        """__hash__()"""
        # Check return hash(frozenset(self.charClass)).
        ef = b_Sym_char_class("set(['e', 'f'])", set(['e', 'f']), 1)
        self.assertTrue(ef.__hash__() == hash(frozenset(ef.charClass)))

    def test___repr__(self):
        """__repr__()"""
        # Check return self.charClass.
        ef = b_Sym_char_class("set(['e', 'f'])", set(['e', 'f']), 1)
        self.assertTrue(ef.__repr__() == repr(ef.charClass))

    def test_get_support_type(self):
        """get_support_type()"""
        # Check return [b_symbol.io_mapper["b_Sym_char_class"]]. 
        ef = b_Sym_char_class("set(['e', 'f'])", set(['e', 'f']), 1)
        self.assertTrue(ef.get_support_type() ==
            [io_mapper["b_Sym_char_class"]])

    def test_compute_collision(self):
        """compute_collision()"""
        # Check correct compute of collision for objects of type sym_char_class.
        cd = b_Sym_char_class("set(['c', 'd'])", set(['c', 'd']), 0)
        ef = b_Sym_char_class("set(['e', 'f'])", set(['e', 'f']), 1)
        self.assertTrue(cd.compute_collision(ef) == (set([cd]), set(), set([ef])))

        ef = b_Sym_char_class("set(['e', 'f'])", set(['c', 'f']), 1)
        result = cd.compute_collision(ef)
        newSymbol = result[0].pop()
        self.assertTrue(newSymbol.charClass == set(['d']))
        newSymbol = result[2].pop()
        self.assertTrue(newSymbol.charClass == set(['f']))
        newSymbol = result[1].pop()
        self.assertTrue(newSymbol.charClass == set(['c']))

    def test_get_text(self):
        """get_text()"""
        # Check return correct representation.
        ef = b_Sym_char_class("set(['e', 'f'])", set(['e', 'f']), 1)
        self.assertTrue(ef.get_text() == "[ef]")

        chars = set()
        for i in range(0, 256):
            chars.add(chr(i))
        chars.remove('2')
        chars.remove('3')
        chars.remove('4')
        chars.remove('7')
        chars.remove('8')
        chars.remove('9')
        big_set = b_Sym_char_class("big_set", chars, 2)
        self.assertTrue(big_set.get_text() == "^[234789]")

    def test_is_empty(self):
        """is_empty()"""
        # If is len(self.charClass) == 0 and self._id != -1 return True,
        # otherwise return False.
        ef = b_Sym_char_class("set(['e', 'f'])", set(['e', 'f']), 1)
        self.assertTrue(ef.is_empty() == False)

        near_empty = b_Sym_char_class("near_empty", set(), -1)
        self.assertTrue(near_empty.is_empty() == False)

        empty = b_Sym_char_class("empty", set(), 15)
        self.assertTrue(empty.is_empty() == True)

    def test_compute_double_stride(self):
        """compute_double_stride()"""
        # Method compute_double_stride(compSymbol, reverse, last, local_chars)
        # Test with compSymbol type sym_char and sym_char_class.
        # If the reverse is True then change order self and compSymbol.

        # compSymbol type sym_char ; reverse = False
        ac = b_Sym_char_class('ac', set(['a', 'c']), 0)
        b = b_Sym_char('b', 'b', 1)
        local_chars = list()
        chars = set()
        for i in range(0,256):
            chars.add(chr(i))
        local_chars.append(chars)

        new_kchar = ac.compute_double_stride(b, False, 2, local_chars)[0]
        new_local_chars = ac.compute_double_stride(b, False, 2, local_chars)[1]

        reference_kchar = b_Sym_kchar("[ac]b", (set(['a', 'c']),'b'), 2)
        reference_kchar_2 = \
            b_Sym_kchar("[ac]b", (frozenset(['a', 'c']),frozenset(['b'])), 2)
        reference_kchar.last = 2
        reference_kchar_2.last = 2
        reference_local_chars = local_chars[0] - set([b.char])

        self.assertTrue(new_kchar == reference_kchar
            or new_kchar == reference_kchar_2)
        self.assertTrue(new_local_chars[0] == reference_local_chars)
        self.assertTrue(new_kchar.last == 2)

        # compSymbol type sym_char_class ; reverse = False
        ac = b_Sym_char_class('ac', set(['a', 'c']), 0)
        bc = b_Sym_char_class("set(['b', 'c'])", set(['b', 'c']), 1)
        local_chars = list()
        chars = set()
        for i in range(0,256):
            chars.add(chr(i))
        local_chars.append(chars)

        new_kchar = ac.compute_double_stride(bc, False, 3, local_chars)[0]
        new_local_chars = ac.compute_double_stride(bc, False, 3, local_chars)[1]
        
        reference_kchar = b_Sym_kchar("[ac][bc]",
            (set(['a', 'c']), set(['b', 'c'])), 2)
        reference_kchar_2 = \
            b_Sym_kchar("[ac][bc]",
                (frozenset(['a', 'c']),frozenset(['b','c'])), 2)
        reference_kchar.last = 3
        reference_kchar_2.last = 3

        reference_local_chars = local_chars[0] - bc.charClass

        self.assertTrue(new_kchar == reference_kchar
            or new_kchar == reference_kchar_2)
        self.assertTrue(new_local_chars[0] == reference_local_chars)
        self.assertTrue(new_kchar.last == 3)

        # compSymbol type sym_char ; reverse = True
        ac = b_Sym_char_class('ac', set(['a', 'c']), 0)
        b = b_Sym_char('b', 'b', 1)
        local_chars = list()
        chars = set()
        for i in range(0,256):
            chars.add(chr(i))
        local_chars.append(chars)

        new_kchar = ac.compute_double_stride(b, True, 2, local_chars)[0]
        new_local_chars = ac.compute_double_stride(b, True, 2, local_chars)[1]

        reference_kchar = b_Sym_kchar("b[ac]", ('b', set(['a', 'c'])), 2)
        reference_kchar_2 = \
            b_Sym_kchar("b[ac]", (frozenset(['b']),frozenset(['a', 'c'])), 2)
        reference_kchar.last = 2
        reference_kchar_2.last = 2
        reference_local_chars = local_chars[0] - ac.charClass

        self.assertTrue(new_kchar == reference_kchar
            or new_kchar == reference_kchar_2)
        self.assertTrue(new_local_chars[0] == reference_local_chars)
        self.assertTrue(new_kchar.last == 2)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_b_Sym_char_class)
    unittest.TextTestRunner(verbosity=2).run(suite)
