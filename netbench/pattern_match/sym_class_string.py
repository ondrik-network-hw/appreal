###############################################################################
#  sym_class_string.py: Module for PATTERN MATCH - symbol string with support 
#                       for character classes.
#  Copyright (C) 2015 Brno University of Technology, ANT @ FIT
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

import b_symbol
import pattern_exceptions

class b_Sym_class_string (b_symbol.b_Symbol):
    """
        A base class to represent a string symbolwith support for character classes.
        
        :param new_text: Text description of symbol, should be human readeable.
        :type new_text: string
        :param new_id: Symbol identification number, must be unique.
        :type new_id: int
        :param string: String symbol
        :type string: list(set(string of length 1))
    """
    def __init__(self, new_text, string, new_id):
        """
            A base class to represent a string symbolwith support for character classes.
        
            :param new_text: Text description of symbol, should be human readeable.
            :type new_text: string
            :param new_id: Symbol identification number, must be unique.
            :type new_id: int
            :param string: String symbol
            :type string: list(set(string of length 1))
        """
        b_symbol.b_Symbol.__init__(self, new_text, new_id)
        self.string = string
        self.ctype = b_symbol.io_mapper["b_Sym_class_string"]

    def accept(self, text):
        """
            If symbol is at the beginning of the text, is removed from the text and reminder is returned. Otherwise accept_exception is raised.
            
            :param text: Text to be parsed.
            :type text: string
            
            :returns: Text without begining.
            :rtype: string
            
            :rises: accept_exception if symbol is not at the begining of the text.
        """
        if self.string == "":
            return text

        if len(text) < len(self.string):
            raise pattern_exceptions.symbol_string_to_short()

        for i in range(0, len(self.string)):
            matched = False
            for char in self.string[i]:
                if text[i] == self.string[i]:
                    matched = True
            if matched == False:
                raise pattern_exceptions.symbol_accept_exception()

        return text[len(self.string):]

    def collision(self, set_of_symbols):
        """ 
            Return True if two or more symbols from set_of_symbols can be accepted for the same text.
            
            :param set_of_symbols: Set of symbols.
            :type set_of_symbols: set(b_Symbol)
            :returns: True if at least two symbols are in collision, otherwise False is returned.
            :rtype: boolean
        """
        for sym in set_of_symbols:
            if sym.get_type() == b_symbol.io_mapper["b_Sym_string"]:
                try:
                    self.accept(sym.string)
                except:
                    pass
                else:
                    return True
            if sym.get_type() == b_symbol.io_mapper["b_Sym_char"]:
                try:
                    self.accept(sym.char)
                except:
                    pass
                else:
                    return True
            if sym.get_type() == b_symbol.io_mapper["b_Sym_char_class"]:
                if len(self.string) == 1:
                    if len(self.string[0].intersection(sym.charClass)) != 0:
                        return True
            if sym.get_type() == b_symbol.io_mapper["b_Sym_class_string"]:
                match = True
                for i in xrange(min([len(self.string), len(sym.string)])):
                    if len(self.string[i].intersection(sym.string[i])) == 0:
                        match = False
                if match == True:
                    return True

        return False

    def export_symbol(self):
        """ 
            Returns symbol representation compatible with FSM tools - http://www2.research.att.com/~fsmtools/fsm/man4/fsm.5.html.
            The symbol is encoded in string without whitespace chars. First char is used for symbol class specification and therefore is not part of the encoded symbol.
            Symbol class specification char for this symbol class is defined by b_symbol.io_mapper["b_Sym_string"].
            
            :returns: Symbol representation compatible with FSM tools.
            :rtype: string
        """
        hex_repr = ""
        for symbol in self.string:
            hex_repr += "|"
            for char in symbol:
                chex_repr = hex(ord(char))[2:]
                if len(chex_repr) == 1:
                    chex_repr = "0" + chex_repr
                hex_repr += chex_repr

        return b_symbol.io_mapper["b_Sym_class_string"] + hex_repr

    def import_symbol(self, text_repr, tid):
        """             
            Creates symbol from its string representation compatible with FSM tools. See export method for more datails.
            
            :param text_repr: String representation.
            :type text_repr: string
            :param tid: Symbol identification number, must be unique.
            :type tid: int
        """
        if text_repr[0] != b_symbol.io_mapper["b_Sym_class_string"]:
            msg = "b_Sym_class_string: Symbol class specification char '" + b_symbol.io_mapper["b_Sym_class_string"] + "' expected but '" + text_repr[0] + "' found!"
            raise pattern_exceptions.symbol_import_exception(msg)

        self._id = tid

        hex_repr = text_repr[2:]
        splited_hex_repr = hex_repr.split("|")
        
        self.string = list()
        self._text = ""

        for i in range(1, len(splited_hex_repr)):
            self._text += "["
            charClass = set()
            for j in range(0, len(splited_hex_repr[i]) / 2):
                chex_repr = splited_hex_repr[i][j * 2] + splited_hex_repr[i][j * 2 + 1]
                charClass.add(chr(int(chex_repr, 16)))
                self._text += chr(int(chex_repr, 16))
            self._text += "]"
            self.string.append(charClass)
        self._text += ""

    def __str__(self):
        """
            Returns string representation of symbol.
            
            :returns: String representation of symbol. 
            :rtype: string
        """
        return self._text

    def compute_equal(self, other):
        """
            Compute if two symbols (self and other) are equivalent.
            
            :param other: Other symbol.
            :type Other: b_Symbol
            
            :returns: True if the symbols are equivalent, otherwise returns False.
            :rtype: boolean
        """
        if other.get_type() == b_symbol.io_mapper["b_Sym_class_string"]:
            if len(self.string) == len(other.string):
                for i in xrange(len(self.string)):
                    if not (self.string[i].issubset(other.string[i]) and self.string[i].issuperset(other.string[i])):
                        return False
                return True
            else:
                return False
        elif other.get_type() == b_symbol.io_mapper["b_Sym_string"]:
            if len(self.string) == len(other.string):
                for sym in self.string:
                    if len(sym) != 1:
                        return False
                for i in xrange(len(other.string)):
                        for csym in self.string[i]:
                            if other.string[i] != csym:
                                return False
                return True
            else:
                return False
        elif other.get_type() == b_symbol.io_mapper["b_Sym_char"]:
            if len(self.string) == 1:
                if len(self.string[0]) != 1:
                    return False
                csym = list(self.string[0])
                if csym[0] == other.char:
                    return True
                else:
                    return False
            else:
                return False
        elif other.get_type() == b_symbol.io_mapper["b_Sym_char_class"]:
            if len(self.string) == 1:
                if self.string[0].issubset(other.charClass) and self.string[0].issuperset(other.charClass):
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    def __hash__(self):
        """
            Returns hash representation of symbol.
            
            :returns: Hash representation of symbol.
            :rtype: int
        """
        return hash(self.string)

    def __repr__(self):
        """
            Returns string representation of symbol.
            
            :returns: String representation of symbol. 
            :rtype: string
        """
        return repr(self.string)

    def get_support_type(self):
        """ 
            Return supported types of symbols for current type of symbol.
            
            :returns: Supported types of symbols for current type of symbol.
            :rtype: list(int)
        """

        return [b_symbol.io_mapper["b_Sym_char"], b_symbol.io_mapper["b_Sym_char_class"], b_symbol.io_mapper["b_Sym_string"], , b_symbol.io_mapper["b_Sym_class_string"]]

    def is_empty(self):
        """
            Return True if symbol is empty. False if is not empty.
            
            :returns: True if symbol is empty. False if is not empty.
            :rtype: boolean
        """

        if len(self.string) == 0:
            return True
        else :
            return False

###############################################################################
# End of File sym_class_string.py                                                     #
###############################################################################
