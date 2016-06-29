###############################################################################
#  test_sym_string.py: Test module for PATTERN MATCH
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
from netbench.pattern_match.sym_string import b_Sym_string
from netbench.pattern_match.sym_char_class import b_Sym_char_class
from netbench.pattern_match.pattern_exceptions import \
    symbol_string_to_short, \
    symbol_accept_exception, \
    symbol_import_exception
import unittest

class test_b_Sym_string(unittest.TestCase):
    """A base test class to represent a string symbol."""

    def test_accept(self):
        """accept()"""
        # method accept(text):
        # Check return text if self.string == ""
        empty = b_Sym_string("", "", 0)
        self.assertTrue(empty.accept("hello") == "hello")

        # Chech if len(text) < len(self.string) then exception
        # symbol_string_to_short is thrown.
        abcd = b_Sym_string("abcd", "abcd", 0)
        try:
            abcd.accept("ba")
            self.assertTrue(False)
        except symbol_string_to_short:
            self.assertTrue(True)

        # Check if self.string is equal begin of text then is returned value
        # text[len(self.string):]
        abcd = b_Sym_string("abcd", "abcd", 0)
        self.assertTrue(abcd.accept("abcdefg") == "efg")

        # In case that self.string is not equal begin of text then is
        # thrown exception symbol_accept_exception
        abcd = b_Sym_string("abcd", "abcd", 0)
        try:
            abcd.accept("different_text")
            self.assertTrue(False)
        except symbol_accept_exception:
            self.assertTrue(True)

    def test_collision(self):
        """collision()"""
        # method collision(set_of_symbols):
        # Try with suitable objects of class sym_char, sym_char_class,
        # sym_string. Check correct output.
        abcd = b_Sym_string("abcd", "abcd", 0)
        e = b_Sym_char('e', 'e', 1)
        fg = b_Sym_char_class("[fg]", set(['f', 'g']), 2)
        hello = b_Sym_string("hello", "hello", 3)
        set_of_symbols = set([e, fg, hello])
        self.assertTrue(abcd.collision(set_of_symbols) == False)

        a = b_Sym_char('a', 'a', 4)
        set_of_symbols.add(a)
        self.assertTrue(abcd.collision(set_of_symbols) == True)
        set_of_symbols.remove(a)
        self.assertTrue(abcd.collision(set_of_symbols) == False)

        ab = b_Sym_char_class("[ab]", set(['a', 'b']), 5)
        set_of_symbols.add(ab)
        self.assertTrue(abcd.collision(set_of_symbols) == True)
        set_of_symbols.remove(ab)
        self.assertTrue(abcd.collision(set_of_symbols) == False)

        abcd_2 = b_Sym_string("abcd_2", "abcd", 6)
        set_of_symbols.add(abcd_2)
        self.assertTrue(abcd.collision(set_of_symbols) == True)

    def test_export_symbol(self):
        """export_symbol()"""
        # Check return correct representation of symbol.
        hello = b_Sym_string("hello", "hello", 0)
        self.assertTrue(hello.export_symbol() == "268656c6c6f")

    def test_import_symbol(self):
        """import_symbol()"""
        # Check that is text_repr created and returned correctly and having
        # set self._id on tid and all parametrs are correct set.
        hello = b_Sym_string("hello", "hello", 0)
        hello.import_symbol("24a41524f534c4156", 1)
        self.assertTrue(hello._id == 1)
        self.assertTrue(hello.string == "JAROSLAV")
        self.assertTrue(hello._text == "JAROSLAV")

        # Check, if text_repr is representation of different type, then
        # thrown exception symbol_import_exception.
        hello = b_Sym_string("hello", "hello", 0)
        try:
            hello.import_symbol("14a41524f534c4156", 1)
            self.assertTrue(False)
        except symbol_import_exception:
            self.assertTrue(True)

    def test___str__(self):
        """__str__()"""
        # Check return self.string.
        hello = b_Sym_string("hello", "hello", 0)
        self.assertTrue(hello.__str__() == hello.string)

    def test_compute_equal(self):
        """compute_equal()"""
        # method compute_equal(other):
        # If is other object of class sym_string, then return True if are
        # their arguments string same.
        hello = b_Sym_string("hello", "hello", 0)
        abba = b_Sym_string("abba", "abba", 1)
        self.assertTrue(hello.compute_equal(abba) == False)
        hello_2 = b_Sym_string("hello_2", "hello", 2)
        self.assertTrue(hello.compute_equal(hello_2) == True)

        # If is other object of type sym_char, then return True if is length
        # of string equal to 1 and argument char is same as argument string.
        hello_short = b_Sym_string("h", "h", 0)
        a = b_Sym_char('a', 'a', 1)
        self.assertTrue(hello_short.compute_equal(a) == False)
        h = b_Sym_char('h', 'h', 2)
        self.assertTrue(hello_short.compute_equal(h) == True)

        # If is other object of class sym_char_class, then return True if is
        # len(other.charClass) == 1, length string equal to 1 and values of
        # arguments string and charClass are same.
        hello_short = b_Sym_string("h", "h", 0)
        set_a = b_Sym_char_class('[a]', set(['a']), 1)
        self.assertTrue(hello_short.compute_equal(set_a) == False)
        set_h = b_Sym_char_class('[h]', set(['h']), 2)
        self.assertTrue(hello_short.compute_equal(set_h) == True)

    def test___hash__(self):
        """__hash__()"""
        # Check return hash(self.string).
        hello = b_Sym_string("hello", "hello", 0)
        self.assertTrue(hello.__hash__() == hash(hello.string))

    def test___repr__(self):
        """__repr__()"""
        # Check return repr(self.string).
        hello = b_Sym_string("hello", "hello", 0)
        self.assertTrue(hello.__repr__() == repr(hello.string))

    def test_get_support_type(self):
        """get_support_type()"""
        # Check return [io_mapper["b_Sym_char"], io_mapper["b_Sym_char_class"],
        # io_mapper["b_Sym_string"]] 
        hello = b_Sym_string("hello", "hello", 0)
        self.assertTrue(hello.get_support_type() == [io_mapper["b_Sym_char"],
            io_mapper["b_Sym_char_class"], io_mapper["b_Sym_string"]])

    def test_is_empty(self):
        """is_empty()"""
        # Check return True for len(self.string) == 0, otherwise return False.
        hello = b_Sym_string("hello", "hello", 0)
        self.assertTrue(hello.is_empty() == False)
        empty = b_Sym_string("empty", "", 1)
        self.assertTrue(empty.is_empty() == True)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_b_Sym_string)
    unittest.TextTestRunner(verbosity=2).run(suite)
