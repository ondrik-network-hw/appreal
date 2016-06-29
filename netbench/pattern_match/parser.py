###############################################################################
#  parser.py: Module for PATTERN MATCH, mataclass wrapping any parser based
#             on nfa_parser base class.
#  Copyright (C) 2011 Brno University of Technology, ANT @ FIT
#  Author(s): Vlastimil Kosar <ikosar@fit.vutbr.cz>
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

import copy
from nfa_parser import nfa_parser
import pcre_parser
import pattern_exceptions

class parser(nfa_parser):
    """
        A mata class wrapping under single interface any class for parsing of \
        regular expressions based on base class nfa_parser.

        :param selected_parser: Which class is used for parsing of regular \
        expressions. Defaults to "pcre_parser". This parameter can be either \
        name of parser class (eg. pcre_parser) or object of class based on \
        nfa_parser class.
        :type selected_parser: string or nfa_parser
        
        :param args: any parser parameters. NOTE: Caller is suppossed to assign \
        corect parametrs of corect types. If parameters excess the number of \
        accepted parameters, then they are discarded.
        :type args: list(Any type)
    """
    def __init__(self, selected_parser = "pcre_parser", *args):
        """
            Class constructor
        """
        self.parser = None
        if isinstance(selected_parser, str):
            if selected_parser == "msfm_parser":
                sys.stderr.write("ERROR: The class msfm_parser and coresponding \
                RE parser was removed as deprecated. Use the class pcre_parser.\
                \n")
                exit()
            elif selected_parser == "pcre_parser":
                self.parser = pcre_parser.pcre_parser(*args)
            else:
                raise pattern_exceptions.unknown_parser(selected_parser)
        else:
            if isinstance(selected_parser, nfa_parser):
                self.parser = selected_parser
            else:
               raise pattern_exceptions.unknown_parser(repr(selected_parser))

     
    def load_file(self, filename):
        """
            This function is used to specify input file and load the whole file into the input text atribute.
            
            :param filename: Name of file.
            :type filename: string
        """
        self.parser.load_file(filename)


    def set_text(self, input_text):
        """
            Set text to parse - can have multiple text lines
            
            :param input_text: Regular expressions.
            :type input_text: string
        """
        self.parser.set_text(input_text)


    def get_nfa(self):
        """
            Parse a current line and returns parsed nfa.
            
            :returns: Created automaton in nfa_data format. Returns None if failure happens.
            :rtype: nfa_data or None
        """
        return self.parser.get_nfa()
        
    def next_line(self):
        """
            Move to the next line (next regular expression)
            
            :returns: True if move was performed, Otherwise False is returned.
            :rtype: boolean
        """
        return self.parser.next_line()

    def move_to_line(self, line):
        """
            Move to the specified line
            
            :param line: Line number.
            :type line: int
            
            :returns: True if move was performed, Otherwise False is returned.
            :rtype: boolean
        """
        return self.parser.move_to_line(line)


    def num_lines(self):
        """ 
            Returns number of lines.
            
            :returns: Number of lines. Each line corespond to single regular expression.
            :rtype: int
        """
        return self.parser.num_lines()

    def reset(self):
        """ 
            Reset the position counter to 0. Parsing will continue from the begining.
        """
        return self.parser.reset()
        
    def get_position(self):
        """ 
            Returns position in ruleset. 
            
            :returns: Position in ruleset. 
            :rtype: int
        """
        return self.parser.get_position()

###############################################################################
# End of File parser.py                                                       #
###############################################################################