###############################################################################
#  sym_kstring.py: Module for PATTERN MATCH - symbol k-strided string with  
#                  support for character classes.
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

class b_Sym_kstring (b_symbol.b_Symbol):
    """
        A base class to represent a string symbolwith support for character classes.
        
        :param new_text: Text description of symbol, should be human readeable.
        :type new_text: string
        :param new_id: Symbol identification number, must be unique.
        :type new_id: int
        :param string: String symbol
        :type string: tuple(tuple(frozenset(char))
    """
    def __init__(self, new_text, string, new_id):
        """
            A base class to represent a k-strided string symbol with support for 
            character classes.
        
            :param new_text: Text description of symbol, should be human readeable.
            :type new_text: string
            :param new_id: Symbol identification number, must be unique.
            :type new_id: int
            :param string: String symbol
            :type string: tuple(tuple(frozenset(char))
        """
        b_symbol.b_Symbol.__init__(self, new_text, new_id)
        self.string = string
        self.ctype = b_symbol.io_mapper["b_Sym_kstring"]
        self.stride = len(string[0])
        self.last = 0

    def accept(self, text):
        """
            If symbol is at the beginning of the text, is removed from the text and reminder is returned. Otherwise accept_exception is raised.
            
            :param text: Text to be parsed.
            :type text: string
            
            :returns: Text without begining.
            :rtype: string
            
            :rises: accept_exception if symbol is not at the begining of the text.
        """
        if len(self.string) == 0:
            return text

        max_len = len(self.string) * self.stride - self.last
        
        if len(text) < max_len:
            raise pattern_exceptions.symbol_string_to_short()

        for i in range(0, len(self.string)):
            for j in range(0, self.stride):
                matched = False
                position = i * self.stride + j
                if position < max_len:
                    for char in self.string[i][j]:
                        if text[position] == self.string[i][j]:
                            matched = True
                    if matched == False:
                        raise pattern_exceptions.symbol_accept_exception()

        return text[max_len:]

    def collision(self, set_of_symbols):
        """ 
            Return True if two or more symbols from set_of_symbols can be accepted for the same text.
            
            :param set_of_symbols: Set of symbols.
            :type set_of_symbols: set(b_Symbol)
            :returns: True if at least two symbols are in collision, otherwise False is returned.
            :rtype: boolean
        """
        for sym in set_of_symbols:
            if sym.get_type() == b_symbol.io_mapper["b_Sym_kstring"]:
                match = True
                if self.stride != sym.stride:
                    # This should never happen unless we support some 
                    # variable-stride algorithm in the future.
                    continue
                for i in xrange(min([len(self.string), len(sym.string)])):
                    for j in xrange(0, self.stride):
                        if len(self.string[i][j].intersection(sym.string[i][j])) == 0:
                            match = False
                if match == True:
                    return True
            elif sym.get_type() == b_symbol.io_mapper["b_Sym_kchar"]:
                if self.stride != len(other.kchar):
                    # This should never happen unless we support some 
                    # variable-stride algorithm in the future.
                    continue
                match = True
                for j in xrange(0, self.stride):
                    if isinstance(other.kchar[j], frozenset):
                        if len(self.string[0][j].intersection(sym.kchar[j])) == 0:
                            match = False
                    else:
                        if not(len(self.string[0][j]) == 1 and sym.kchar[j] in self.string[0][j]):
                            match = False
                if match == True:
                    return True
        return False

    def export_symbol(self):
        """ 
            Returns symbol representation compatible with FSM tools - http://www2.research.att.com/~fsmtools/fsm/man4/fsm.5.html.
            The symbol is encoded in string without whitespace chars. First char is used for symbol class specification and therefore is not part of the encoded symbol.
            Symbol class specification char for this symbol class is defined by b_symbol.io_mapper["b_Sym_kstring"].
            
            :returns: Symbol representation compatible with FSM tools.
            :rtype: string
        """
        hex_repr = "|" + str(self.stride)
        for kchar in self.string:
            for symbol in kchar:
                hex_repr += "|"
                for char in symbol:
                    chex_repr = hex(ord(char))[2:]
                    if len(chex_repr) == 1:
                        chex_repr = "0" + chex_repr
                    hex_repr += chex_repr

        return b_symbol.io_mapper["b_Sym_kstring"] + hex_repr

    def import_symbol(self, text_repr, tid):
        """             
            Creates symbol from its string representation compatible with FSM tools. See export method for more datails.
            
            :param text_repr: String representation.
            :type text_repr: string
            :param tid: Symbol identification number, must be unique.
            :type tid: int
        """
        if text_repr[0] != b_symbol.io_mapper["b_Sym_kstring"]:
            msg = "b_Sym_kstring: Symbol class specification char '" + b_symbol.io_mapper["b_Sym_kstring"] + "' expected but '" + text_repr[0] + "' found!"
            raise pattern_exceptions.symbol_import_exception(msg)

        self._id = tid

        hex_repr = text_repr[2:]
        splited_hex_repr = hex_repr.split("|")
        
        self.string = list()
        self._text = ""
        self.stride = int(splited_hex_repr[0])
        
        for i in range(1, len(splited_hex_repr)):
            self._text += "{"
            kchar = list()
            for j in xrange(0, self.stride):
                self._text += "["
                charClass = set()
                for j in range(0, len(splited_hex_repr[i]) / 2):
                    chex_repr = splited_hex_repr[i][j * 2] + splited_hex_repr[i][j * 2 + 1]
                    charClass.add(chr(int(chex_repr, 16)))
                    self._text += chr(int(chex_repr, 16))
                self._text += "]"
                kchar.append(frozenset(charClass))
            self._text += "}"
            self.string.append(tuple(kchar))
        self.string = tuple(self.string)

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
        if other.get_type() == b_symbol.io_mapper["b_Sym_kclass"]:
            if len(self.string) == len(other.string) and self.stride == other.stride:
                for i in xrange(0, len(self.string)):
                    for j in xrange(0, self.stride):
                        if self.string[i][j].issubset(other.string[i][j]) and self.string[i][j].issuperset(other.string[i][j]):
                            continue
                        else:
                            return False
                return True
            else:
                return False
        elif other.get_type() == b_symbol.io_mapper["b_Sym_kchar"]:
            if len(self.string) == 1 and self.stride == len(other.kchar):
                for j in xrange(0, self.stride):
                    if isinstance(other.kchar[j], frozenset):
                        if self.string[0][j].issubset(other.kchar[j]) and self.string[0][j].issuperset(other.kchar[j]):
                            continue
                        else:
                            return False
                    else:
                        if len(self.string[0][j]) == 1 and other.kchar[j] in self.string[0][j]:
                            continue
                        else:
                            return False
                return True
            else:
                return False
        else:
            return False
        return True

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

        return [b_symbol.io_mapper["b_Sym_kchar"],  b_symbol.io_mapper["b_Sym_kstring"]]

    def is_empty(self):
        """
            Return True if symbol is empty. False if is not empty.
            
            :returns: True if symbol is empty. False if is not empty.
            :rtype: boolean
        """

        if len(self.string) == 0:
            return True
        else:
            return False

    def __len__(self):
        """
            Return length of the string.
            
            :returns: Length of the string.
            :rtype: int
        """
        return len(self.string)

###############################################################################
# End of File sym_kstring.py                                                  #
###############################################################################
