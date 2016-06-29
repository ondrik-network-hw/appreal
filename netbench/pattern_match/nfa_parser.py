###############################################################################
#  nfa_parser.py: Module for PATTERN MATCH
#  Copyright (C) 2010 Brno University of Technology, ANT @ FIT
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

class nfa_parser:
    """
        A base class for parsing of regular expressions. 
    """
    def __init__(self):
        """
            Class constructor
        """
        self._automaton = None
        self._text = None
        self._nfa = None
        self._position = -1
     
    def load_file(self, filename):
        """
            This function is used to specify input file and load the whole \
            file into the input text atribute. Format of this file is simple - \
            one regular expression on each line. Regular expression (RE) must \
            have following form: /RE/M - where RE is regular expression and M \
            are PCRE modifiers.
            
            :param filename: Name of file.
            :type filename: string
        """
        f = open(filename,"rb");    #Opens file automat
        blob = f.read()
        lines = list()
        i = 0;
        trueLine = str()
        while i < len(blob):
            if (blob[i] != '\n'):
                trueLine = trueLine + blob[i]
            else:
                trueLine = trueLine + blob[i]
                lines.insert(len(lines), copy.deepcopy(trueLine))
                #print(str(trueLine))
                trueLine = str()
            i = i + 1
        f.close();
        
        if len(trueLine) != 0:
            lines.insert(len(lines), copy.deepcopy(trueLine))
        
        self._text = lines
        self._position = 0


    def set_text(self, input_text):
        """
            Set text to parse - can have multiple text lines. Format of the \
            text is simple - one regular expression on each line. Regular \
            expression (RE) must have following form: /RE/M - where RE is \
            regular expression and M are PCRE modifiers.
            
            :param input_text: Regular expressions.
            :type input_text: string
        """
        lines = list()
        i = 0;
        trueLine = str()
        while i < len(input_text):
            if (input_text[i] != '\n'):
                trueLine = trueLine + input_text[i]
            else:
                trueLine = trueLine + input_text[i]
                lines.insert(len(lines), copy.deepcopy(trueLine))
                #print(str(trueLine))
                trueLine = str()
            i = i + 1
            
        if len(trueLine) != 0:
            lines.insert(len(lines), copy.deepcopy(trueLine))
        
        self._text = lines
        self._position = 0

    def get_nfa(self):
        """
            Parse a current line and returns parsed nfa.
            
            :returns: Created automaton in nfa_data format. Returns None if failure happens.
            :rtype: nfa_data or None
        """

    def next_line(self):
        """
            Move to the next line (next regular expression)
            
            :returns: True if move was performed, Otherwise False is returned.
            :rtype: boolean
        """
        if self._text == None:
            return False
        if self._position + 1 < len(self._text):
            self._position += 1
            return True
        else:
            return False

    def move_to_line(self, line):
        """
            Move to the specified line
            
            :param line: Line number.
            :type line: int
            
            :returns: True if move was performed, Otherwise False is returned.
            :rtype: boolean
        """
        if self._text == None:
            return False
        
        if line < len(self._text) and line >= 0:
            self._position = line
            return True
        else:
            return False

    def num_lines(self):
        """ 
            Returns number of lines.
            
            :returns: Number of lines. Each line corespond to single regular expression.
            :rtype: int
        """
        if self._text == None:
            return 0
        else:
            return len(self._text)

    def reset(self):
        """ 
            Reset the position counter to 0. Parsing will continue from the begining.
        """
        self._position = 0
        
    def get_position(self):
        """ 
            Returns position in ruleset. 
            
            :returns: Position in ruleset. 
            :rtype: int
        """
        return self._position

###############################################################################
# End of File nfa_parser.py                                                   #
###############################################################################