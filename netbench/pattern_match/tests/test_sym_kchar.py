###############################################################################
#  test_kchar.py: Test module for PATTERN MATCH
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

class test_b_Sym_kchar(unittest.TestCase):
    """A base test class to represent a k-char symbol. Chars can be char or
       char classes."""

    def test_accept(self):
        """accept()"""
        # method accept(text):
        # Check if len(text) < len(self.kchar) then is thrown exception
        # symbol_string_to_short.
        abc = b_Sym_kchar("abc", ('a', 'b', 'c'), 0)
        try:
            abc.accept("ab")
            self.assertTrue(False)
        except symbol_string_to_short:
            self.assertTrue(True)

        # If begin of text is same as any combination of kchar then return
        # text[len(self.kchar):]
        abc = b_Sym_kchar("abc", ('a', 'b', 'c'), 0)
        self.assertTrue(abc.accept("abcdef") == "def")

        # In case there is no combination then thrown exception
        # symbol_accept_exception.
        try:
            abc.accept("wrong_text")
            self.assertTrue(False)
        except symbol_accept_exception:
            self.assertTrue(True)

    def test_collision(self):
        """collision()"""
        # method collision(set_of_symbols):
        # Try with suitable objects of class sym_kchar and check correct
        # result - is / is not collision.
        abc = b_Sym_kchar("abc", ('a', 'b', 'c'), 0)
        ac = b_Sym_char_class("ac", set(['a', 'c']), 1)
        b = b_Sym_char("b", 'b', 2)
        efg = b_Sym_kchar("efg", ('e', 'f', 'g'), 3)
        set_of_symbols = set([efg, ac, b])
        self.assertTrue(abc.collision(set_of_symbols) == False)

        a = b_Sym_char("a", 'a', 4)
        set_of_symbols.add(a)
        self.assertTrue(abc.collision(set_of_symbols) == False)

        cba = b_Sym_kchar("cba", ('c', 'b', 'a'), 5)
        set_of_symbols.add(cba)
        self.assertTrue(abc.collision(set_of_symbols) == False)

        abc_2 = b_Sym_kchar("abc", ('a', 'b', 'c'), 6)
        set_of_symbols.add(abc_2)
        self.assertTrue(abc.collision(set_of_symbols) == True)

    def test_export_symbol(self):
        """export_symbol()"""
        # Check correct output.
        abc = b_Sym_kchar("abc", ('a', 'b', 'c'), 0)
        self.assertTrue(abc.export_symbol() == "40000|61|62|63")

    def test_import_symbol(self):
        """import_symbol()"""
        # Check that is from test_repr created and returned correct object
        # having set self._id on tid and all parametrs are correct set.
        abc = b_Sym_kchar("abc", ('a', 'b', 'c'), 0)
        abc.import_symbol("40000|65|66|67", 1)

        self.assertTrue(abc.kchar == ('e', 'f', 'g')) 
        self.assertTrue(abc._id == 1)
        self.assertTrue(abc._text == "{efg}")

        # Check if is text_repr of different type, then is thrown exception
        # symbol_import_exception.
        try:
            abc.import_symbol("0|65|66|67", 1)
            self.assertTrue(False)
        except symbol_import_exception:
            self.assertTrue(True)

    def test___str__(self):
        """__str__()"""
        # Check output str(self.kchar).
        abc = b_Sym_kchar("abc", ('a', 'b', 'c'), 0)
        self.assertTrue(abc.__str__() == str(abc.kchar))

    def test_compute_equal(self):
        """compute_equal()"""
        # method compute_equal(other):
        # If is other type sym_kchar, then return True if are arguments
        # kchar same.
        abc = b_Sym_kchar("abc", ('a', 'b', 'c'), 0)
        efg = b_Sym_kchar("efg", ('e', 'f', 'g'), 1)
        self.assertTrue(abc.compute_equal(efg) == False)

        abc_2 = b_Sym_kchar("abc", (frozenset(['a']), frozenset(['b']),
            frozenset(['c'])), 2)
        self.assertTrue(abc.compute_equal(abc_2) == True)

        # If is other type sym_string, then return True if is
        # len(other.string) == len(self.kchar), all subsymbols kchar have
        # length one (len(self.kchar[i]) == 1) and value string is straight
        # value kchar.
        kchar_abc = b_Sym_kchar("abc", ('a', 'b', 'c'), 0)
        string_abc = b_Sym_string("abc", "abc", 1)
        string_abcde = b_Sym_string("abcde", "abcde", 2)
        self.assertTrue(kchar_abc.compute_equal(string_abc) == True)
        self.assertTrue(kchar_abc.compute_equal(string_abcde) == False)

        # If is other type sym_char, then return True if is
        # len(self.kchar) == 1 and len(self.kchar[0]) == 1 and their
        # arguments are same.
        kchar_a = b_Sym_kchar("kchar_a", ('a'), 0)
        a = b_Sym_char("a", 'a', 1)
        self.assertTrue(kchar_a.compute_equal(a) == True)
        b = b_Sym_char("b", 'b', 2)
        self.assertTrue(kchar_a.compute_equal(b) == False)

        # If is other type sym_char_class, then return True if is
        # len(self.kchar) == 1 and len(other.charClass) == len(self.kchar[0])
        # and values of arguments are same.
        kchar_abc = b_Sym_kchar("kchar_[abc]", (frozenset(['a', 'b', 'c']),), 0)
        set_abc = b_Sym_char_class("[abc]", set(['a', 'b', 'c']), 1)
        self.assertTrue(kchar_abc.compute_equal(set_abc) == True)
        cd = b_Sym_char_class("set(['c', 'd'])", set(['c', 'd']), 2)
        self.assertTrue(kchar_abc.compute_equal(cd) == False)

    def test___hash__(self):
        """__hash__()"""
        # Check return hash(self.kchar).
        abc = b_Sym_kchar("abc", ('a', 'b', 'c'), 0)
        self.assertTrue(abc.__hash__() == hash(abc.kchar))

    def test___repr__(self):
        """__repr__()"""
        # Check return repr(self.kchar).
        abc = b_Sym_kchar("abc", ('a', 'b', 'c'), 0)
        self.assertTrue(abc.__repr__() == repr(abc.kchar))

    def test_get_support_type(self):
        """get_support_type()"""
        # Check return [b_symbol.io_mapper["b_Sym_char"],
        # b_symbol.io_mapper["b_Sym_char_class"],
        # b_symbol.io_mapper["b_Sym_string"],
        # b_symbol.io_mapper["b_Sym_kchar"]] 
        abc = b_Sym_kchar("abc", ('a', 'b', 'c'), 0)
        self.assertTrue(abc.get_support_type() == [io_mapper["b_Sym_char"],
            io_mapper["b_Sym_char_class"], io_mapper["b_Sym_string"],
            io_mapper["b_Sym_kchar"]])

    def test_is_empty(self):
        """is_empty()"""
        # Check return True for len(self.kchar) == 0, otherwise return False.
        abc = b_Sym_kchar("abc", ('a', 'b', 'c'), 0)
        self.assertTrue(abc.is_empty() == False)

        empty = b_Sym_kchar("empty", (), 1)
        self.assertTrue(empty.is_empty() == True)

    def test_compute_double_stride(self):
        """compute_double_stride()"""
        # compute_double_stride(compSymbol, reverse, last, local_chars):
        # Test with compSymbol of type sym_kchar.
        # If is reverse True, check in result kchar reverse sort self and comp.
        # Check in result kchar that last value is same as called.
        # Chech that local_chars[i] for i in len(local_chars) have value
        # local_chars[i] = local_chars[i] - compSymbol.kchar[i]
        ab = b_Sym_kchar("ab", ('a', 'b'), 0)
        ef = b_Sym_kchar("ef", ('e', 'f'), 1)
        local_chars = list()
        chars = set()
        for i in range(0, 256):
            chars.add(chr(i))
            local_chars.append(chars.copy())

        new_kchar = ab.compute_double_stride(ef, False, 2, local_chars)[0]
        new_local_chars = \
            ab.compute_double_stride(ef, False, 2, local_chars)[1]

        reference_kchar = b_Sym_kchar("abef", ('a', 'b', 'e', 'f'), 2)
        reference_kchar_2 = \
            b_Sym_kchar("abef", ('a', 'b', 'e', 'f'), 2)
        reference_kchar.last = 2
        reference_kchar_2.last = 2
        
        reference_local_chars = local_chars[0] - set([ef.kchar])

        self.assertTrue(new_kchar == reference_kchar
           or new_kchar == reference_kchar_2)
        self.assertTrue(new_local_chars[0] == reference_local_chars)
        self.assertTrue(new_kchar.last == 2)

        # reverse = True
        ab = b_Sym_kchar("ab", ('a', 'b'), 0)
        ef = b_Sym_kchar("ef", ('e', 'f'), 1)
        local_chars = list()
        chars = set()
        for i in range(0, 256):
            chars.add(chr(i))
            local_chars.append(chars.copy())

        new_kchar = ab.compute_double_stride(ef, True, 2, local_chars)[0]
        new_local_chars = \
            ab.compute_double_stride(ef, True, 2, local_chars)[1]

        reference_kchar = b_Sym_kchar("efab", ('e', 'f', 'a', 'b'), 2)
        reference_kchar_2 = \
            b_Sym_kchar("efab", ('e', 'f', 'a', 'b'), 2)
        reference_kchar.last = 2
        reference_kchar_2.last = 2
        reference_local_chars = local_chars[0] - set([ab.kchar])

        self.assertTrue(new_kchar == reference_kchar
           or new_kchar == reference_kchar_2)
        self.assertTrue(new_local_chars[0] == reference_local_chars)
        self.assertTrue(new_kchar.last == 2)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_b_Sym_kchar)
    unittest.TextTestRunner(verbosity=2).run(suite)
