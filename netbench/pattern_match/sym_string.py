###############################################################################
#  sym_string.py: Module for PATTERN MATCH - symbol string
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

import b_symbol
import pattern_exceptions

class b_Sym_string (b_symbol.b_Symbol):
    """
        A base class to represent a string symbol.
        
        :param new_text: Text description of symbol, should be human readeable.
        :type new_text: string
        :param new_id: Symbol identification number, must be unique.
        :type new_id: int
        :param string: String symbol
        :type string: string
    """
    def __init__(self, new_text, string, new_id):
        """
            A base class to represent a string symbol.
            
            :param new_text: Text description of symbol, should be human readeable.
            :type new_text: string
            :param new_id: Symbol identification number, must be unique.
            :type new_id: int
            :param string: String symbol
            :type string: string
        """
        b_symbol.b_Symbol.__init__(self, new_text, new_id)
        self.string = string
        self.ctype = b_symbol.io_mapper["b_Sym_string"]

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
            if text[i] != self.string[i]:
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
            try:
                sym.accept(self.string)
            except:
                pass
            else:
                return True
            if sym.get_type() == b_symbol.io_mapper["b_Sym_string"]:
                try:
                    self.accept(sym.string)
                except:
                    pass
                else:
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
        for char in self.string:
            chex_repr = hex(ord(char))[2:]
            if len(chex_repr) == 1:
                chex_repr = "0" + chex_repr
            hex_repr += chex_repr

        return b_symbol.io_mapper["b_Sym_string"] + hex_repr

    def import_symbol(self, text_repr, tid):
        """             
            Creates symbol from its string representation compatible with FSM tools. See export method for more datails.
            
            :param text_repr: String representation.
            :type text_repr: string
            :param tid: Symbol identification number, must be unique.
            :type tid: int
        """
        if text_repr[0] != b_symbol.io_mapper["b_Sym_string"]:
            msg = "b_Sym_string: Symbol class specification char '" + b_symbol.io_mapper["b_Sym_string"] + "' expected but '" + text_repr[0] + "' found!"
            raise pattern_exceptions.symbol_import_exception(msg)

        self._id = tid

        hex_repr = text_repr[1:]

        self.string = ""
        self._text = ""

        for i in range(0, len(hex_repr) / 2):
            chex_repr = hex_repr[i * 2] + hex_repr[i * 2 + 1]
            self.string += chr(int(chex_repr, 16))
            self._text += chr(int(chex_repr, 16))

        self._text += ""

    def __str__(self):
        """
            Returns string representation of symbol.
            
            :returns: String representation of symbol. 
            :rtype: string
        """
        return self.string

    def compute_equal(self, other):
        """
            Compute if two symbols (self and other) are equivalent.
            
            :param other: Other symbol.
            :type Other: b_Symbol
            
            :returns: True if the symbols are equivalent, otherwise returns False.
            :rtype: boolean
        """
        if other.get_type() == b_symbol.io_mapper["b_Sym_string"]:
            if self.string == other.string:
                return True
            else:
                return False
        elif other.get_type() == b_symbol.io_mapper["b_Sym_char"]:
            if len(self.string) == 1:
                if self.string == other.char:
                    return True
                else:
                    return False
            else:
                return False
        elif other.get_type() == b_symbol.io_mapper["b_Sym_char_class"]:
            if len(self.string) == 1:
                s = set()
                s.add(self.string)
                if s.issubset(other.charClass) and s.issuperset(other.charClass):
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

        return [b_symbol.io_mapper["b_Sym_char"], b_symbol.io_mapper["b_Sym_char_class"], b_symbol.io_mapper["b_Sym_string"]]

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
# End of File sym_string.py                                                     #
###############################################################################
