###############################################################################
#  sym_char.py: Module for PATTERN MATCH - symbol char class
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
import b_symbol
import sym_string
import sym_kchar
import pattern_exceptions

class b_Sym_char (b_symbol.b_Symbol):
    """
        A base class to represent a char symbol.
        
        :param new_text: Text description of symbol, should be human readeable.
        :type new_text: string
        :param new_id: Symbol identification number, must be unique.
        :type new_id: int
        :param char: Char symbol
        :type char: string of length 1
    """
    def __init__(self, new_text, char, new_id):
        """
            Class constructor.
            
            :param new_text: Text description of symbol, should be human readeable.
            :type new_text: string
            :param new_id: Symbol identification number, must be unique.
            :type new_id: int
            :param char: Char symbol
            :type char: string of length 1
        """
        b_symbol.b_Symbol.__init__(self, new_text, new_id)
        self.char = char
        self.ctype = b_symbol.io_mapper["b_Sym_char"]

    def accept(self, text):
        """
            If symbol is at the beginning of the text, is removed from the text and reminder is returned. Otherwise accept_exception is raised.
            
            :param text: Text to be parsed.
            :type text: string
            
            :returns: Text without begining.
            :rtype: string
            
            :rises: accept_exception if symbol is not at the begining of the text.
        """
        if self.char == "":
            return text
        if len(text) == 0:
            raise pattern_exceptions.symbol_string_to_short()
        if text[0] == self.char[0]:
            return text[1:]
        else:
            raise pattern_exceptions.symbol_accept_exception()

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
                sym.accept(self.char)
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
            Symbol class specification char for this symbol class is defined by b_symbol.io_mapper["b_Sym_char"].
            
            :returns: Symbol representation compatible with FSM tools.
            :rtype: string
        """
        hex_repr = ""
        if len(self.char) > 0:
            hex_repr = hex(ord(self.char[0]))[2:]
            if len(hex_repr) == 1:
                hex_repr = "0" + hex_repr

        return b_symbol.io_mapper["b_Sym_char"] + hex_repr

    def import_symbol(self, text_repr, tid):
        """             
            Creates symbol from its string representation compatible with FSM tools. See export method for more datails.
            
            :param text_repr: String representation.
            :type text_repr: string
            :param tid: Symbol identification number, must be unique.
            :type tid: int
        """
        if text_repr[0] != b_symbol.io_mapper["b_Sym_char"]:
            msg = "b_Sym_char: Symbol class specification char '" + b_symbol.io_mapper["b_Sym_char"] + "' expected but '" + text_repr[0] + "' found!"
            raise pattern_exceptions.symbol_import_exception(msg)

        self._id = tid

        hex_repr = text_repr[1:]

        if len(hex_repr) > 0:
            self.char = chr(int(hex_repr, 16))
            self._text = chr(int(hex_repr, 16))
        else:
            self.char = ""
            self._text = "eps"

    def __str__(self):
        """
            Returns string representation of symbol.
            
            :returns: String representation of symbol. 
            :rtype: string
        """
        return self.char

    def compute_equal(self, other):
        """
            Compute if two symbols (self and other) are equivalent.
            
            :param other: Other symbol.
            :type Other: b_Symbol
            
            :returns: True if the symbols are equivalent, otherwise returns False.
            :rtype: boolean
        """
        if other.get_type() == b_symbol.io_mapper["b_Sym_char"]:
            if self.char == other.char:
                return True
            else:
                return False
        elif other.get_type() == b_symbol.io_mapper["b_Sym_char_class"]:
            if len(other.charClass) == 1:
                for sym in other.charClass:
                    if sym == self.char:
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
        return hash(self.char)

    def __repr__(self):
        """
            Returns string representation of symbol.
            
            :returns: String representation of symbol. 
            :rtype: string
        """
        return repr(self.char)

    def get_support_type(self):
        """ 
            Return supported types of symbols for current type of symbol.
            
            :returns: Supported types of symbols for current type of symbol.
            :rtype: list(int)
        """

        return [b_symbol.io_mapper["b_Sym_char"], b_symbol.io_mapper["b_Sym_char_class"]]

    def compute_collision(self, compSymbol):
        """ 
            Compute collision between self and compSymbol.
            
            :param other: Other symbol.
            :type other: b_Symbol
            
            :returns: Resolved collision - changes to the symbols and new ones, if they are created.
            :rtype: tuple(set(b_Symbol), set(b_Symbol), set(b_Symbol))
        """

        symbol = copy.deepcopy(self)
        compSymbol = copy.deepcopy(compSymbol)
        newSymbols = set()

        if compSymbol.get_type() == b_symbol.io_mapper["b_Sym_char"]:
            if symbol.char == compSymbol.char:
                newSymbols.add(
                    b_Sym_char(
                        new_text = symbol.char,
                        char = symbol.char,
                        # id will be set in resolve_alphabet()
                        new_id = -2
                    )
                )
                return (set(), newSymbols, set())
            else :
                return (set([symbol]), set(), set([compSymbol]))
        elif compSymbol.get_type() == b_symbol.io_mapper["b_Sym_char_class"]:
            if symbol.char in compSymbol.charClass:
                newSymbols.add(
                    b_Sym_char(
                        new_text = symbol.char,
                        char = symbol.char,
                        # id will be set in resolve_alphabet()
                        new_id = -2
                    )
                )
                compSymbol.charClass.remove(symbol.char)
                # don't return empty symbol
                if compSymbol.is_empty():
                    return(set(), newSymbols, set())
                return (set(), newSymbols, set([compSymbol]))
            else :
                return (set([symbol]), set(), set([compSymbol]))

    def is_empty(self):
        """
            Return True if symbol is empty. False if is not empty.
            
            :returns: True if symbol is empty. False if is not empty.
            :rtype: boolean
        """

        if len(self.char) == 0 and self._id != -1:
            return True
        else :
            return False
            
    def compute_double_stride(self, compSymbol, reverse, last, local_chars):
        """
            Compute double stride using self and compSymbol. This method should be called only by double_stride method.
            
            :param compSymbol: Other symbol.
            :type compSymbol: b_Symbol
            :param last: Number of last chars. Usualy equal to current stride. Used only if self is final state.
            :type last: int
            :param reverse: Determinates if self and compSymbol have to be swaped (usefull when original self in double_stride() method can't compute the double stride).
            :type reverse: boolean
            :param local_chars: List of set of local_chars. Set of all posible chars for each new subsymbol of final kchar (char + char = 2 strided kchar, list will have exactly 1 set present). used to have striding deterministic.
            :type local_chars: list(set(char))
            :returns: New strided symbol and unused symbols from local chars.
            :rtype: tuple(b_Symbol, list(set()))
        """
        a = self
        b = compSymbol
        
        first = None
        second = None

        first_s = set()
        first_s.add(a.char)
        first_s = frozenset(first_s)
        first = list()
        first.append(first_s)
        if reverse == True:
            # remove used symbol from local copy of complete alphabet.
            local_chars[0] = local_chars[0] - first_s

        if b.get_type() == b_symbol.io_mapper["b_Sym_char_class"]:
            second_s = frozenset(b.charClass)
            second = list()
            second.append(second_s)

            if reverse == False:
                # remove used symbol from local copy of complete alphabet.
                local_chars[0] = local_chars[0] - b.charClass

        if b.get_type() == b_symbol.io_mapper["b_Sym_char"]:
            second_s = set()
            second_s.add(b.char)
            second_s = frozenset(second_s)
            second = list()
            second.append(second_s)
            
            if reverse == False:
                # remove used symbol from local copy of complete alphabet.
                local_chars[0] = local_chars[0] - second_s
            
        if reverse == True:
            xchg = first
            first = second
            second = xchg

        # crate complete strided symbol
        complete = list()
        complete += first
        complete += second
        complete = tuple(complete)

        # create complete strided symbol description (will be shown in graphicasl representation)
        complete_str = "{"

        for i in range(0, len(complete)):
            if len(complete[i]) == 1:
                for char in complete[i]:
                    complete_str += str(char)
                    #print str(complete)
            else:
                complete_str += "["
                complete_str_w = ""
                for char in complete[i]:
                    complete_str_w += char
                if len(complete_str_w) > 128:
                    s_a = []
                    for i in range(0, 256):
                        s_a.append(chr(i))
                    for c in complete_str_w:
                        if c in s_a:
                            s_a.remove(c)
                    s = ""
                    for c in s_a:
                        s += c
                    complete_str_w = "^" + s
                complete_str +=  complete_str_w + "]"

        complete_str += "}"

        # Create strided symbol object
        new_symbol = sym_kchar.b_Sym_kchar(complete_str, complete, 0)
        new_symbol.last = last

        return (new_symbol, local_chars)

###############################################################################
# End of File sym_char.py                                                     #
###############################################################################
