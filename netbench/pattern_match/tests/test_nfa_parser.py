###############################################################################
#  test_nfa_parser.py: Module for PATTERN MATCH tests
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

from netbench.pattern_match.nfa_parser import nfa_parser
import unittest

class test_nfa_parser(unittest.TestCase):
    """A base class for testing parsing of regular expressions."""

    def test_load_file(self):
        """load_file()"""
        # Check whether REs loaded (from file) into attribute _text
        # and set _position attribute to 0. In attribute _text is list()
        # whose elements are strings. Each string contains one RE.

        parser = nfa_parser()
        parser.load_file("../rules/Snort/http-bots.reg")
        self.assertTrue(parser._text == ['/^GET/\n', '/^POST/\n'])
        self.assertTrue(parser._position == 0)

    def test_set_text(self):
        """set_text()"""
        # Check whether there is a saving of REs to _text the attribute and the
        # attribute _position is set to 0.
        # Check for an one RE and for more than one REs in the input string.
        # Each RE is in the input strings separated by \n.

        parser = nfa_parser()
        parser.set_text("first RE")
        self.assertTrue(parser._text == ['first RE'])
        self.assertTrue(parser._position == 0)

        parser.set_text("first RE\nSECONDre\nthirdRegularExpresion")
        self.assertTrue(parser._text == ['first RE\n', 'SECONDre\n',
            'thirdRegularExpresion'])
        self.assertTrue(parser._position == 0)


    def test_next_line(self):
        """next_line()"""
        # In case no one RE is set, check return false.
        parser = nfa_parser()
        self.assertTrue(parser.next_line() == False)

        # If the RE is set, and if the attribute _position is smaller than the
        # length attribute _text - 1, a check returning True and increase, by 1
        # attribute _position.
        parser = nfa_parser()
        parser.set_text("first RE\nSECONDre\nthirdRegularExpresion")
        self.assertTrue(parser._position == 0)
        self.assertTrue(parser.next_line() == True)
        self.assertTrue(parser._position == 1)
        self.assertTrue(parser.next_line() == True)
        self.assertTrue(parser._position == 2)

        # If the RE is set, and if the attribute _position is equal to the
        # length _text - 1, and check return False _position attribute does not change.
        self.assertTrue(parser.next_line() == False)
        self.assertTrue(parser._position == 2)


    def test_move_to_line(self):
        """move_to_line()"""
        # In case it does not set any RE, check return false.
        parser = nfa_parser()
        self.assertTrue(parser.move_to_line(15) == False)

        # If the RE is set, and if the parameter line in the interval
        # <0, len(_text)) to check the returning True and setting the attribute
        # _position to line number.
        parser = nfa_parser()
        parser.set_text("first RE\nSECONDre\nthirdRegularExpresion")
        self.assertTrue(parser._position == 0)

        self.assertTrue(parser.move_to_line(2) == True)
        self.assertTrue(parser._position == 2)

        # If the RE is set, and if the parameter line is not in the interval
        # <0, len(_text)) check and returning False _position attribute does
        # not change.
        self.assertTrue(parser.move_to_line(3) == False)
        self.assertTrue(parser._position == 2)

        self.assertTrue(parser.move_to_line(-2) == False)
        self.assertTrue(parser._position == 2)

    def test_num_lines(self):
        """num_lines()"""
        # Check whether the correct number of REs is returned.
        parser = nfa_parser()
        parser.set_text("first RE\nSECONDre\nthirdRegularExpresion")
        self.assertTrue(parser.num_lines() == 3)

    def test_reset(self):
        """reset()"""
        # Check whether the attribute _position is set to 0.
        parser = nfa_parser()
        parser.set_text("first RE\nSECONDre\nthirdRegularExpresion")
        self.assertTrue(parser._position == 0)

        self.assertTrue(parser.move_to_line(1) == True)
        self.assertTrue(parser._position == 1)

        parser.reset()
        self.assertTrue(parser._position == 0)

    def test_get_position(self):
        """get_position()"""
        # Check whether the returned attribute value _position.
        parser = nfa_parser()
        parser.set_text("first RE\nSECONDre\nthirdRegularExpresion")
        self.assertTrue(parser.get_position() == 0)

        self.assertTrue(parser.move_to_line(1) == True)
        self.assertTrue(parser.get_position() == 1)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_nfa_parser)
    unittest.TextTestRunner(verbosity=2).run(suite)
