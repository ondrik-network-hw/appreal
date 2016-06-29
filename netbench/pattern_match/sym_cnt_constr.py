###############################################################################
#  sym_cnt_constr.py: Module for PATTERN MATCH - symbol class for PCRE
#                         constraint repetition blocks
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

class b_Sym_cnt_constr (b_symbol.b_Symbol):
    """ 
        A base class to represent a char symbol.
        
        :param new_text: Text description of symbol, should be human readeable.
        :type new_text: string
        :param new_id: Symbol identification number, must be unique.
        :type new_id: int
        :param symbol: Char or char class accepted.
        :type symbol: set(string of length 1) or string of length 1
        :param m: Minimal count of symbol repetitions
        :type m: int
        :param n: Maximal count of symbol repetitions
        :type n: int
    """
    def __init__(self, new_text, symbol, m, n, new_id):
        """ Symbol class constructor.
        
            :param new_text: Text description of symbol, should be human readeable.
            :type new_text: string
            :param new_id: Symbol identification number, must be unique.
            :type new_id: int
            :param symbol: Char or char class accepted.
            :type symbol: set(string of length 1) or string of length 1
            :param m: Minimal count of symbol repetitions
            :type m: int
            :param n: Maximal count of symbol repetitions
            :type n: int
        """
        b_symbol.b_Symbol.__init__(self, new_text, new_id)
        self.symbol = symbol
        self.m = m
        self.n = n
        self.ctype = b_symbol.io_mapper["b_Sym_cnt_constr"]
        # This attributes controls behavior of accept method use set_greedy(), set_limit(), get_greedy() and get_limit() to set/get thouse attributes
        self.greedy = False
        self.limit = -1

    def accept(self, text):
        """  
            If symbol is at the beginning of the text, is removed from the text and reminder is returned. Otherwise accept_exception is raised. Behavior of this method is controled by attributes greedy and limit. The limit attribute has bigger priority than the greedy one.  Limit sets exact number of accepted characters. If -1 is set, the greedy attribute will be used. If greedy is True, the accept() method will consume as much characters from input string as posible. If greedy is False, the accept() mathod will consume only minimal number of characters from input string with respect to the m parameter.
            
            :param text: Text to be parsed.
            :type text: string
            
            :returns: Text without begining.
            :rtype: string
            
            :rises: accept_exception if symbol is not at the begining of the text.
        """
        if self.limit > -1:
            if self.limit < self.m or self.limit > self.n:
                raise pattern_exceptions.symbol_accept_exception()

            if len(text) < self.limit:
                raise pattern_exceptions.symbol_accept_exception()

            if self.limit == 0:
                return text

            for i in range(0, self.limit):
                if isinstance(self.symbol, set) or isinstance(self.symbol, frozenset):
                    accepted = False
                    for char in self.symbol:
                        if char[0] == text[i]:
                            accepted = True
                    if accepted == False:
                        raise pattern_exceptions.symbol_accept_exception()
                else:
                    if self.symbol[0] != text[i]:
                        raise pattern_exceptions.symbol_accept_exception()

            return text[self.limit:]
        else:
            index = 0

            if len(text) < self.m:
                raise pattern_exceptions.symbol_accept_exception()

            for i in range(0, len(text)+1):
                if index == self.m and self.greedy == False:
                    break
                if index == self.n:
                    break
                if i == len(text):
                    return ""

                if isinstance(self.symbol, set) or isinstance(self.symbol, frozenset):
                    accepted = False
                    for char in self.symbol:
                        if char[0] == text[i]:
                            accepted = True
                    if accepted == False:
                        if index < self.m:
                            raise pattern_exceptions.symbol_accept_exception()
                        else:
                            return text[index:]
                else:
                    if self.symbol[0] != text[i]:
                        if index < self.m:
                            raise pattern_exceptions.symbol_accept_exception()
                        else:
                            return text[index:]
                    
                index = i

            return text[index:]


    def collision(self, set_of_symbols):
        """ 
            This symbol is used only for representing PCRE constraint          \
            repetition block. This method implements prefix collision.
            
            :param set_of_symbols: Set of symbols.
            :type set_of_symbols: set(b_Symbol)
            :returns: True if at least two symbols are in collision, otherwise False is returned.
            :rtype: boolean
        """
        for other in set_of_symbols:
            # Detect prefix collisions when other symbol is b_Sym_cnt_constr
            if other.get_type() == b_symbol.types["b_Sym_cnt_constr"]:
                if isinstance(self.symbol, set) or isinstance(self.symbol, frozenset):
                    if isinstance(other.symbol, set) or isinstance(other.symbol, frozenset):
                        if self.symbol.isdisjoint(other.symbol) == False:
                            return True
                    else:
                        other_set = set([other.symbol])
                        if self.symbol.isdisjoint(other_set) == False:
                            return True
                else:
                    if isinstance(other.symbol, set) or isinstance(other.symbol, frozenset):
                        self_set = set([self.symbol])
                        if self_set.isdisjoint(other.symbol) == False:
                            return True
                    else:
                        if self.symbol == other.symbol:
                            return True
            elif other.get_type() == b_symbol.types["b_Sym_string"]:
                try:
                    self.accept(other.string)
                except:
                    pref = True
                    for char in other.string:
                        if isinstance(self.symbol, set) or isinstance(self.symbol, frozenset):
                            if char not in self.symbol:
                                pref = False
                        else:
                            if char != self.symbol:
                                pref = False
                        if pref == True:
                            return True
                else:
                    return True
            elif other.get_type() == b_symbol.types["b_Sym_char"]:
                if len(other.char) == 0:
                    return True
                if isinstance(self.symbol, set) or isinstance(self.symbol, frozenset):
                    if other.char in self.symbol:
                        return True
                else:
                    if other.char == self.symbol:
                        return True
            elif other.get_type() == b_symbol.types["b_Sym_char_class"]:
                if isinstance(self.symbol, set) or isinstance(self.symbol, frozenset):
                    if self.symbol.isdisjoint(other.charClass) == False:
                        return True
                else:
                    self_set = set([self.symbol])
                    if self_set.isdisjoint(other.charClass) == False:
                        return True
            elif other.get_type() == b_symbol.types["b_Sym_kchar"]:
                # No sane automaton should combine b_Sym_kchar and b_Sym_cnt_constr,
                # If striding of b_Sym_cnt_constr is needed special symbol class
                # should be implemented. If somebody needs this collision test, 
                # he/she/it must implement the test.
                pass
                    
        return False        

    def export_symbol(self):
        """
            Returns symbol representation compatible with FSM tools - http://www2.research.att.com/~fsmtools/fsm/man4/fsm.5.html.
            The symbol is encoded in string without whitespace chars. First char is used for symbol class specification and therefore is not part of the encoded symbol.
            Symbol class specification char for this symbol class is defined by b_symbol.io_mapper["b_Sym_cnt_constr"].
            
            :returns: Symbol representation compatible with FSM tools.
            :rtype: string
        """
        hex_repr = ""
        if isinstance(self.symbol, set) or isinstance(self.symbol, frozenset):
            for char in self.symbol:
                chex_repr = hex(ord(char))[2:]
                if len(chex_repr) == 1:
                    chex_repr = "0" + chex_repr
                hex_repr += chex_repr
        else:
            hex_repr = hex(ord(self.symbol[0]))[2:]
            if len(hex_repr) == 1:
                hex_repr = "0" + hex_repr

        return b_symbol.io_mapper["b_Sym_cnt_constr"] + "|" + str(self.m) + "|" + str(self.n) + "|" +  hex_repr

    def import_symbol(self, text_repr, tid):
        """             
            Creates symbol from its string representation compatible with FSM tools. See export method for more datails.
            
            :param text_repr: String representation.
            :type text_repr: string
            :param tid: Symbol identification number, must be unique.
            :type tid: int
        """
        if text_repr[0] != b_symbol.io_mapper["b_Sym_cnt_constr"]:
            msg = "b_Sym_cnt_constr: Symbol class specification char '" + b_symbol.io_mapper["b_Sym_cnt_constr"] + "' expected but '" + text_repr[0] + "' found!"
            raise pattern_exceptions.symbol_import_exception(msg)

        self._id = tid

        splited = text_repr.split("|")

        self.m = int(splited[1])

        if splited[2] == "inf":
            self.n = float(splited[2])
        else:
            self.n = int(splited[2])

        hex_repr = splited[3]

        if len(hex_repr) == 2:
            self.symbol = chr(int(hex_repr, 16))
            self._text = chr(int(hex_repr, 16))
        else:
            self.symbol = set()
            self._text = "["

            for i in range(0, len(hex_repr) / 2):
                chex_repr = hex_repr[i * 2] + hex_repr[i * 2 + 1]
                self.charClass.add(chr(int(chex_repr, 16)))
                self._text += chr(int(chex_repr, 16))

            self._text += "]"

        self._text += "{" + str(self.m) + "," + str(self.n) + "}"

    def __str__(self):
        """
            Returns string representation of symbol.
            
            :returns: String representation of symbol. 
            :rtype: string
        """
        return repr(self)

    def compute_equal(self, other):
        """
            Compute if two symbols (self and other) are equivalent.
            
            :param other: Other symbol.
            :type Other: b_Symbol
            
            :returns: True if the symbols are equivalent, otherwise returns False.
            :rtype: boolean
        """
        raise pattern_exceptions.general_not_implemented("b_Sym_cnt_constr.compute_equal()")
        
        

    def __eq__(self, other):
        """
            Compute if two symbols (self and other) are equivalent.
            
            :param other: Other symbol.
            :type Other: b_Symbol
            
            :returns: True if the symbols are equivalent, otherwise returns False.
            :rtype: boolean
            
            :raises: symbol_equality_exception() if equivalention can't be computed.
        """
        try:
            if other.get_type() == b_symbol.io_mapper["b_Sym_cnt_constr"]:
                if (self.symbol == other.symbol) and (self.m == other.m) and (self.n == other.n):
                    return True
                else:
                    return False
            else:
                return False
        except (AttributeError, TypeError):
            return False

    def __ne__(self, other):
        """
            Compute if two symbols (self and other) are not equivalent.
            
            :param other: Other symbol.
            :type Other: b_Symbol
            
            :returns: True if the symbols are equivalent, otherwise returns False.
            :rtype: boolean
            
            :raises: symbol_equality_exception() if equivalention can't be computed.
        """
        try:
            if other.get_type() == b_symbol.io_mapper["b_Sym_cnt_constr"]:
                if (self.symbol != other.symbol) or (self.m != other.m) or (self.n != other.n):
                    return True
                else:
                    return False
            else:
                return True
        except (AttributeError, TypeError):
            return True

    def __hash__(self):
        """
            Returns hash representation of symbol.
            
            :returns: Hash representation of symbol.
            :rtype: int
        """
        sym = None
        if isinstance(self.symbol, set):
            sym = frozenset(self.symbol)
        else:
            sym = self.symbol
        return hash((sym, self.m, self.n))

    def __repr__(self):
        """
            Returns string representation of symbol.
            
            :returns: String representation of symbol. 
            :rtype: string
        """
        return str(self.symbol) + " {" + str(self.m) + ", " + str(self.n) + "}"

    def get_support_type(self):
        """ 
            Return supported types of symbols for current type of symbol.
            
            :returns: Supported types of symbols for current type of symbol.
            :rtype: list(int)
        """
        return [b_symbol.io_mapper["b_Sym_char"], b_symbol.io_mapper["b_Sym_char_class"], b_symbol.io_mapper["b_Sym_string"], b_symbol.io_mapper["b_Sym_kchar"], b_symbol.types["b_Sym_cnt_constr"]]

    def compute_double_stride(self, compSymbol, reverse, last, local_chars):
        """
            Compute double stride using self and compSymbol. This method should be called only by double_stride method.
            
            NOTE: This method is not implemented.
            
            :param compSymbol: Other symbol.
            :type compSymbol: b_Symbol
            :param last: Number of last chars. Usualy equal to current stride. Used only if self is final state.
            :type last: int
            :param reverse: Determinates if self and compSymbol have to be swaped (usefull when original self in double_stride() method can't compute the double stride).
            :type reverse: boolean
            :param local_chars: List of Set of local_chars. Set of all posible chars. used to have striding deterministic. Number of sets in the list is equal to len(self.kchar).
            :type local_chars: list(set(char))
                        
            :returns: New strided symbol.
            :rtype: sym_kchar
        """
        raise pattern_exceptions.general_not_implemented("b_Sym_cnt_constr.compute_double_stride()")
    
    def compute_collision(self, compSymbol):
        """ 
            Compute collision between self and compSymbol.
            
            NOTE: This method is not implemented.
            
            :param other: Other symbol.
            :type other: b_Symbol
            
            :returns: Resolved collision - changes to the symbols and new ones, if they are created.
            :rtype: tuple(set(b_Symbol), set(b_Symbol), set(b_Symbol))
        """
        raise pattern_exceptions.general_not_implemented("b_Sym_cnt_constr.compute_collision()")

    def set_greedy(self, greedy):
        """ 
            Set greedy attribute of this symbol. This attribute is used to controle behavior of the accept method.
            
            :param greedy: New value of the attribute:
            
                If greedy is True, the accept() method will consume as much characters from input string as posible.
                
                If greedy is False, the accept() mathod will consume only minimal number of characters from input string with respect to the m parameter.
            :type greedy: boolean
        """
        self.greedy = greedy

    def get_greedy(self):
        """ 
            Return value of the greedy attribute.
            
            :returns: Value of the greedy attribute.
            :rtype: boolean
        """
        return self.greedy

    def set_limit(self, limit):
        """ 
            Set limit attribute of this symbol. This attribute is used to controle behavior of the accept() method and has bigger priority than greedy attribute.
            
            :param limit: Sets exact number of accepted characters. If -1 is set, the greedy attribute will be used.
            :type limit: int
        """
        self.limit = limit

    def get_limit(self):
        """ 
            Return value of the limit attribute.
            
            :returns: Value of the limit attribute.
            :rtype: int
        """
        return self.limit

    def is_empty(self):
        """
            Return True if symbol is empty. False if is not empty.
            
            :returns: True if symbol is empty. False if is not empty.
            :rtype: boolean
        """

        if len(self.symbol) == 0:
            return True
        else :
            return False

###############################################################################
# End of File sym_cnt_constr                                              #
###############################################################################
