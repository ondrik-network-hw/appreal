###############################################################################
#  test_def_symbols.py: Test module for PATTERN MATCH - default symbol class
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

from netbench.pattern_match.b_symbol import DEF_SYMBOLS, io_mapper
from netbench.pattern_match.sym_char import b_Sym_char
from netbench.pattern_match.pattern_exceptions import \
    symbol_accept_exception, \
    symbol_import_exception
import unittest

class test_DEF_SYMBOLS(unittest.TestCase):
    """Test class for default symbol, which is used in Delay DFA."""

    def test_accept(self):
        """accept()"""
        # Method accept(text):
        # Check that always returns the text.
        # Check that never raises an exception accept_exception.
        def_symbol = DEF_SYMBOLS("default", 3)

        try:
            self.assertTrue(def_symbol.accept("text1") == "text1")
            self.assertTrue(True)
        except symbol_accept_exception:
            self.assertTrue(False)

        try:
            self.assertTrue(def_symbol.accept("other text") == "other text")
            self.assertTrue(True)
        except symbol_accept_exception:
            self.assertTrue(False)

    def test_collision(self):
        """collision()"""
        # The method of collision(set_of_symbols):
        # Returns True only if one object from the set_of_symbols is 
        # object of class DEF_SYMBOLS. In another case, always returns False.
        def_symbol_1 = DEF_SYMBOLS("default_1", 3)
        def_symbol_2 = DEF_SYMBOLS("default_2", 4)
        char_symbol_1 = b_Sym_char("a", "a", 1)
        char_symbol_2 = b_Sym_char("b", "b", 2)
        set_of_symbols = set([char_symbol_1, char_symbol_2])
        self.assertTrue(def_symbol_1.collision(set_of_symbols) == False)

        set_of_symbols = set([char_symbol_1, char_symbol_2, def_symbol_2])
        self.assertTrue(def_symbol_1.collision(set_of_symbols) == True)

    def test_export_symbol(self):
        """export_symbol()"""
        # Check that returns the correct representation of the symbol.
        def_symbol = DEF_SYMBOLS("default", 3)
        self.assertTrue(def_symbol.export_symbol() == io_mapper["DEF_SYMBOLS"])
        self.assertTrue(def_symbol.export_symbol() == '5')

    def test_import_symbol(self):
        """import_symbol()"""
        # Method import_symbol(text_repr, tid):
        # Check whether the text_repr created and returned the correct
        # object and having to set self._id on tid and self._text on "default".
        # Check that if text_repr representation of another type, then
        # the exception is thrown symbol_import_exception.
        def_symbol = DEF_SYMBOLS("some_text", 0)
        self.assertTrue(def_symbol._id == 0)
        self.assertTrue(def_symbol._text == "some_text")

        def_symbol.import_symbol('5', 15)
        self.assertTrue(def_symbol._id == 15)
        self.assertTrue(def_symbol._text == "default")

        try:
            def_symbol.import_symbol('6', 16)
            self.assertTrue(False)
        except symbol_import_exception:
            self.assertTrue(True)

    def test_compute_collision(self):
        """compute_collision()"""
        # Method compute_collision(other):
        # Check the correct outputs.
        # Self can be in a collision only if other is class object DEF_SYMBOLS
        def_symbol = DEF_SYMBOLS("default", 3)
        char_symbol = b_Sym_char("a", "a", 1)
        self.assertTrue(def_symbol.compute_collision(char_symbol) ==
            (set([def_symbol]), set(), set([char_symbol])))

        other_def_symbol = DEF_SYMBOLS("default", 4)
        self.assertTrue(def_symbol.compute_collision(other_def_symbol) ==
            (set(), set([other_def_symbol]), set()))

    def test_compute_equal(self):
        """compute_equal()"""
        # compute_equal(other):
        # Return True if other is object of DEF_SYMBOLS class, otherwise
        # return False.
        def_symbol = DEF_SYMBOLS("default", 3)
        char_symbol = b_Sym_char("a", "a", 1)
        self.assertTrue(def_symbol.compute_equal(char_symbol) == False)

        other_def_symbol = DEF_SYMBOLS("default", 4)
        self.assertTrue(def_symbol.compute_equal(other_def_symbol) == True)

    def test_get_support_type(self):
        """get_support_type()"""
        # Check correct output:
        # [io_mapper["b_Sym_char"], io_mapper["b_Sym_char_class"],
        # io_mapper["b_Sym_string"], io_mapper["b_Sym_kchar"],
        # io_mapper["DEF_SYMBOLS"]] 
        def_symbol = DEF_SYMBOLS("default", 3)
        self.assertTrue(def_symbol.get_support_type() == 
            [io_mapper["b_Sym_char"], io_mapper["b_Sym_char_class"],
            io_mapper["b_Sym_string"], io_mapper["b_Sym_kchar"],
            io_mapper["DEF_SYMBOLS"]])

    def test_is_empty(self):
        """is_empty()"""
        # Check return False.
        def_symbol = DEF_SYMBOLS("default", 3)
        self.assertTrue(def_symbol.is_empty() == False)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_DEF_SYMBOLS)
    unittest.TextTestRunner(verbosity=2).run(suite)
