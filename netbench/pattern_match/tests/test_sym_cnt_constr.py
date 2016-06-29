###############################################################################
#  test_sym_cnt_constr.py: Test module for PATTERN MATCH
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
from netbench.pattern_match.sym_cnt_constr import b_Sym_cnt_constr
from netbench.pattern_match.sym_char import b_Sym_char
from netbench.pattern_match.sym_char_class import b_Sym_char_class
from netbench.pattern_match.sym_string import b_Sym_string

from netbench.pattern_match.pattern_exceptions import \
    symbol_accept_exception, \
    general_not_implemented, \
    symbol_import_exception
import unittest

class test_b_Sym_cnt_constr(unittest.TestCase):
    """A base test class to represent a char symbol."""

    def test_accept(self):
        """accept()"""
        # method accept(text):
        # If is set self.limit > -1:
        #   - If is self.limit < self.m or self.limit > self.n, then thrown
        #     exception symbol_accept_exception
        try:
            a = b_Sym_cnt_constr('a', 'a', 3, 5, 0)
            a.set_limit(2)
            a.accept("text")
            self.assertTrue(False)
        except symbol_accept_exception:
            self.assertTrue(True)

        try:
            a = b_Sym_cnt_constr('a', 'a', 3, 5, 0)
            a.set_limit(6)
            a.accept("text")
            self.assertTrue(False)
        except symbol_accept_exception:
            self.assertTrue(True)

        #   - If is len(text) < len(self.limit), then thrown exception
        #     symbol_accept_exception. 
        try:
            a = b_Sym_cnt_constr('a', 'a', 3, 5, 0)
            a.set_limit(15)
            a.accept("text")
            self.assertTrue(False)
        except symbol_accept_exception:
            self.assertTrue(True)

        #  - If is self.limit == 0, then return text
        a = b_Sym_cnt_constr('a', 'a', 0, 5, 0)
        a.set_limit(0)
        self.assertTrue(a.accept("hello") == "hello")

        #  - If is on begin of text self.limit X self.symbol, then return
        #    text[self.limit:]
        a = b_Sym_cnt_constr('a', 'a', 3, 5, 0)
        a.set_limit(4)
        self.assertTrue(a.accept("aaaao") == "o")

        #  - If is NOT on begin of text self.limit X self.symbol then is
        #    thrown exception symbol_accept_exception
        try:
            a = b_Sym_cnt_constr('a', 'a', 3, 5, 0)
            a.set_limit(4)
            a.accept("aaoaa")
            self.assertTrue(False)
        except symbol_accept_exception:
            self.assertTrue(True)

        # If is limit <= -1:
        #   - Behavior determines parametr self.greedy. If is false then is
        #     accepted just self.m chars. If is true then is accepted maximally
        #     n chars.
        a = b_Sym_cnt_constr('a', 'a', 3, 5, 0)
        a.set_limit(-3)
        a.set_greedy(False)
        self.assertTrue(a.accept("aaaao") == "ao")
        a.set_greedy(True)
        self.assertTrue(a.accept("aaaaaaa") == "aa")

        #   - If is len(text) < self.m, then is thrown exception
        #     symbol_accept_exception.
        try:
            a = b_Sym_cnt_constr('a', 'a', 3, 5, 0)
            a.set_limit(-4)
            a.accept("hh")
            self.assertTrue(False)
        except symbol_accept_exception:
            self.assertTrue(True)

        #   - If the number of chars at the begining of the string 
        #     corresponding to self.symbol less then self.m then is thrown
        #     exception symbol_accept_exception.
        try:
            a = b_Sym_cnt_constr('a', 'a', 3, 5, 0)
            a.set_limit(-4)
            a.accept("aa")
            self.assertTrue(False)
        except symbol_accept_exception:
            self.assertTrue(True)

        #   - If the number of chars on begining of the string
        #     corresponding to self.symbol in interval <self.m, self.n>,
        #     then is returned text[index:], where index is number of chars.
        a = b_Sym_cnt_constr('a', 'a', 3, 5, 0)
        a.set_limit(-4)
        self.assertTrue(a.accept("aaa") == "")
        self.assertTrue(a.accept("aaaa") == "a")
        self.assertTrue(a.accept("aaaaa") == "aa")
        self.assertTrue(a.accept("aaaaaaa") == "aaaa")
        
        #   - If the number of chars on begining of the string
        #     corresponding to self.symbol in interval <self.m, self.n>,
        #     then is returned text[index:], where index is number of chars.
        #     Greedy variant of previous test.
        a = b_Sym_cnt_constr('a', 'a', 3, 5, 0)
        a.set_greedy(True)
        a.set_limit(-4)
        self.assertTrue(a.accept("aaa") == "")
        self.assertTrue(a.accept("aaaa") == "")
        self.assertTrue(a.accept("aaaaa") == "")
        self.assertTrue(a.accept("aaaaaaa") == "aa")

    def test_collision(self):
        """collision()"""
        # method collision(set_of_symbols):
        # Try with suitable objects class sym_char, sym_char_class,
        # sym_string, sym_cnt_constr. Check correct output 
        # (is / is not collision).
        ac = b_Sym_cnt_constr('a', 'a', 3, 5, 0)
        bc = b_Sym_cnt_constr('b', 'b', 3, 5, 0)
        b = b_Sym_char('b', 'b', 0)
        cd = b_Sym_char_class("set(['c', 'd'])", set(['c', 'd']), 1)

        adam = b_Sym_string("baba", "baba", 3)
        set_of_symbols = set([b, bc, cd, adam])
        self.assertTrue(ac.collision(set_of_symbols) == False)

        c = b_Sym_cnt_constr('a', 'a', 1, 9, 0)
        set_of_symbols = set([c, b, bc, cd, adam])
        self.assertTrue(ac.collision(set_of_symbols) == True)
        
        c = b_Sym_char('a', 'a', 0)
        set_of_symbols = set([c, b, bc, cd, adam])
        self.assertTrue(ac.collision(set_of_symbols) == True)
        
        c = b_Sym_char_class("set(['a', 'd'])", set(['a', 'd']), 1)
        set_of_symbols = set([c, b, bc, cd, adam])
        self.assertTrue(ac.collision(set_of_symbols) == True)
        
        c = b_Sym_char('a', 'a', 0)
        set_of_symbols = set([c, b, bc, cd, adam])
        self.assertTrue(ac.collision(set_of_symbols) == True)
        
        c = b_Sym_string("aaaa", "aaaa", 3)
        set_of_symbols = set([c, b, bc, cd, adam])
        self.assertTrue(ac.collision(set_of_symbols) == True)
        
        c = b_Sym_string("aa", "aa", 3)
        set_of_symbols = set([c, b, bc, cd, adam])
        self.assertTrue(ac.collision(set_of_symbols) == True)
        
        c = b_Sym_string("aaaaaaaaaaaa", "aaaaaaaaaaaa", 3)
        set_of_symbols = set([c, b, bc, cd, adam])
        self.assertTrue(ac.collision(set_of_symbols) == True)

    def test_export_symbol(self):
        """export_symbol()"""
        # Check, that returning correct representation of symbol.
        a = b_Sym_cnt_constr('a', 'a', 3, 5, 0)
        self.assertTrue(a.export_symbol() == "6|3|5|61")

    def test_import_symbol(self):
        """import_symbol()"""
        # Check whether is from text_repr created and returned correct object
        # and having set self._id on tid and all parametrs are correctly set.
        a = b_Sym_cnt_constr('a', 'a', 3, 5, 0)
        a.import_symbol("6|2|15|65", 28)
        self.assertTrue(a._id == 28)
        self.assertTrue(a._text == "e{2,15}")
        self.assertTrue(a.symbol == 'e')
        self.assertTrue(a.m == 2)
        self.assertTrue(a.n == 15)
        self.assertTrue(a.ctype == io_mapper["b_Sym_cnt_constr"])
        self.assertTrue(a.greedy == False)
        self.assertTrue(a.limit == -1)

        # Check, if is test_repr of different type, then call exception
        # symbol_import_exception
        try:
            a = b_Sym_cnt_constr('a', 'a', 3, 5, 0)
            a.import_symbol("5|2|15|65", 28)
            self.assertTrue(False)
        except symbol_import_exception:
            self.assertTrue(True)

    def test___str__(self):
        """__str__()"""
        # Check whether returning repr(self).
        a = b_Sym_cnt_constr('a', 'a', 3, 5, 0)
        self.assertTrue(a.__str__() == repr(a))

    def test___eq__(self):
        """__eq__()"""
        # method __eq__(other):
        # Test by ==
        # If is other type sym_cont_constr and is (self.symbol == other.symbol)
        # and (self.m == other.m) and (self.n == other.n), return True, other-
        # wise return False.
        a = b_Sym_cnt_constr('a', 'a', 3, 5, 0)
        a_2 = b_Sym_cnt_constr('a_2', 'a', 3, 5, 1)
        b = b_Sym_cnt_constr('b', 'b', 3, 5, 2)
        self.assertTrue((a == b) == False)
        self.assertTrue((a == a_2) == True)

    def test___ne__(self):
        """__ne__()"""
        # method __ne__(other):
        # Test by !=
        # If is other type sym_cont_constr and is (self.symbol == other.symbol)
        # and (self.m == other.m) and (self.n == other.n), return False, other-
        # wise return True
        a = b_Sym_cnt_constr('a', 'a', 3, 5, 0)
        a_2 = b_Sym_cnt_constr('a_2', 'a', 3, 5, 1)
        b = b_Sym_cnt_constr('b', 'b', 3, 5, 2)
        self.assertTrue((a != b) == True)
        self.assertTrue((a != a_2) == False)

    def test_hash(self):
        """hash()"""
        # Check whether return hash( (self.symbol, self.m, self.n) )
        a = b_Sym_cnt_constr('a', 'a', 3, 5, 0)
        self.assertTrue(a.__hash__() == hash( (a.symbol, a.m, a.n) ))

    def test___repr__(self):
        """__repr__()"""
        # Check whether return str(self.symbol) +
        # " {" + str(self.m) + ", " + str(self.n) + "}" 
        a = b_Sym_cnt_constr('a', 'a', 3, 5, 0)
        self.assertTrue(a.__repr__() == (str(a.symbol) + 
            " {" + str(a.m) + ", " + str(a.n) + "}"))

    def test_get_support_type(self):
        """get_support_type()"""
        # Check return [io_mapper["b_Sym_char"], io_mapper["b_Sym_char_class"], 
        # io_mapper["b_Sym_string"], io_mapper["b_Sym_kchar"], 
        # io_mapper["b_Sym_cnt_constr"]]. 
        a = b_Sym_cnt_constr('a', 'a', 3, 5, 0)
        self.assertTrue(a.get_support_type() ==
        [io_mapper["b_Sym_char"],   io_mapper["b_Sym_char_class"], 
         io_mapper["b_Sym_string"], io_mapper["b_Sym_kchar"], 
         io_mapper["b_Sym_cnt_constr"]])

    def test_set_greedy(self):
        """set_greedy()"""
        # method set_greedy(greedy):
        # Check whether is set argument self.greedy on greedy.
        a = b_Sym_cnt_constr('a', 'a', 3, 5, 0)
        self.assertTrue(a.greedy == False)
        a.set_greedy(True)
        self.assertTrue(a.greedy == True)

    def test_get_greedy(self):
        """get_greedy()"""
        # Check whether returning self.greedy.
        a = b_Sym_cnt_constr('a', 'a', 3, 5, 0)
        self.assertTrue(a.get_greedy() == False)
        a.greedy = True
        self.assertTrue(a.get_greedy() == True)

    def test_set_limit(self):
        """set_limit()"""
        # method set_limit(limit):
        # Check whether set argument self.limit on limit.
        a = b_Sym_cnt_constr('a', 'a', 3, 5, 0)
        self.assertTrue(a.limit == -1)
        a.set_limit(458)
        self.assertTrue(a.limit == 458)

    def test_get_limit(self):
        """get_limit()"""
        # Check whether returning self.limit.
        a = b_Sym_cnt_constr('a', 'a', 3, 5, 0)
        self.assertTrue(a.get_limit() == -1)
        a.limit = 458
        self.assertTrue(a.get_limit() == 458)

    def test_is_empty(self):
        """is_empty()"""
        # Check whether returning True for len(self.symbol) == 0, otherwise
        # return False.
        a = b_Sym_cnt_constr('a', 'a', 3, 5, 0)
        self.assertTrue(a.is_empty() == False)
        empty = b_Sym_cnt_constr('empty', '', 2, 15, 1)
        self.assertTrue(empty.is_empty() == True)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_b_Sym_cnt_constr)
    unittest.TextTestRunner(verbosity=2).run(suite)
