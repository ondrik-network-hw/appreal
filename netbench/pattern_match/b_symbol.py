###############################################################################
#  b_symbol.py: Module for PATTERN MATCH - Base symbol class
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

import pattern_exceptions

io_mapper = {"b_Sym_char":'0', "b_Sym_char_class":'1', "b_Sym_string":'2', "b_Sym_kchar":'4', "DEF_SYMBOLS":'5', "b_Sym_cnt_constr":'6', "b_Sym_EOF":'7', "b_Sym_class_string":'8', "b_Sym_kstring":'9' }
""" 
    Maps class name to coresponding class specification char. If new symbol is added, io_mapper, io_reverse_mapper and nfa_data class method ImportFromFsm must be updated.
"""

types = io_mapper
"""
    Maps class name to coresponding class specification char. It contains same values as io_mapper, but it can be redefined in future. For testing if object is of specified symbol class this dictionary have to be used.
"""

io_reverse_mapper = {'0':"b_Sym_char", '1':"b_Sym_char_class", '2':"b_Sym_string", '4':"b_Sym_kchar", '5':"DEF_SYMBOLS", '6':"b_Sym_cnt_constr", '7':"b_Sym_EOF", '8':"b_Sym_class_string", '9':"b_Sym_kstring"}
""" 
    Maps class specification char to coresponding class name. If new symbol is added, io_mapper, io_reverse_mapper and nfa_data class method ImportFromFsm must be updated.
"""

class b_Symbol:
    """ 
        A base class to represent a symbol.
        
        :param new_text: Text description of symbol, should be human readeable.
        :type new_text: string
        :param new_id: Symbol identification number, must be unique.
        :type new_id: int
    """
    def __init__(self, new_text, new_id):
        """ 
            Constructor of base class
        
            :param new_text: Text description of symbol, should be human readeable.
            :type new_text: string
            :param new_id: Symbol identification number, must be unique.
            :type new_id: int
        """
        self._id    =  new_id    # Symbol identification value
        self._text  = new_text;  # Symbol text

    def get_text(self):
        """
            Return symbol description for graph representation.
            
            :returns: Symbol description for graph representation.
            :rtype: string
        """
        return self._text;

    def set_text(self, text):
        """ 
            Sets the text description of symbol to text.
            
            :param text: Description of symbol.
            :type text: string
        """
        self._text = text

    def get_id(self):
        """
            Return symbol identification number.
            
            :returns: Symbol identification number.
            :rtype: int
        """
        return self._id

    def set_id(self, new_id):
        """ 
            Sets the id of symbol to new_id.
            
            :param new_id: Symbol identification value.
            :type new_id: int
        """
        self._id = new_id

    def accept(self, text):
        """
            If symbol is at the beginning of the text, is removed from the text and reminder is returned. Otherwise accept_exception is raised.
            
            :param text: Text to be parsed.
            :type text: string
            
            :returns: Text without begining.
            :rtype: string
            
            :rises: accept_exception if symbol is not at the begining of the text.
        """

    def collision(self, set_of_symbols):
        """ 
            Return True if two or more symbols from set_of_symbols can be accepted for the same text.
            
            :param set_of_symbols: Set of symbols.
            :type set_of_symbols: set(b_Symbol)
            :returns: True if at least two symbols are in collision, otherwise False is returned.
            :rtype: boolean
        """

    def export_symbol(self):
        """ 
            Returns symbol representation compatible with FSM tools - http://www2.research.att.com/~fsmtools/fsm/man4/fsm.5.html.
            The symbol is encoded in string without whitespace chars. First char is used for symbol class specification and therefore is not part of the encoded symbol.
            Symbol class spcification char should be in [0-9a-zA-Z] and must be unique.
            
            :returns: Symbol representation compatible with FSM tools.
            :rtype: string
        """

    def import_symbol(self, text_repr, tid):
        """ 
            Creates symbol from its string representation compatible with FSM tools. See export method for more datails.
            
            :param text_repr: String representation.
            :type text_repr: string
            :param tid: Symbol identification number, must be unique.
            :type tid: int
        """
    def get_type(self):
        """
            Return type of symbol.
            
            :returns: Type of symbol.
            :rtype: int
        """

        return self.ctype

    def get_support_type(self):
        """ 
            TODO: dohodnout se na schuzi
            Return supported types of symbols for current type of symbol and method.
            
            :param method: Specifies method for which supported symbols are requested.
            :type methos: string
            :returns: Set of supported types.
            :rtype: set(int)
        """

    def resolve_collision(self, compSymbol):
        """ 
            Resolve collision with self and compSymbol.
            
            :param compSymbol: Other symbol.
            :type compSymbol: b_Symbol
            
            :returns: Resolved collision - changes to the symbols and new ones, if they are created.
            :rtype: tuple(set(b_Symbol), set(b_Symbol), set(b_Symbol))
            
            :raises: symbol_resolve_collision_exception() if collision can't be computed.
        """

        if compSymbol.get_type() in self.get_support_type():
            return self.compute_collision(compSymbol)
        elif self.get_type() in compSymbol.get_support_type():
            return (compSymbol.compute_collision(self)[2],
                compSymbol.compute_collision(self)[1],
                compSymbol.compute_collision(self)[0])
        else :
            raise pattern_exceptions.symbol_resolve_collision_exception(self.get_type(), compSymbol.get_type())


    def double_stride(self, compSymbol, last, local_chars):
        """ 
            Double stride using self and compSymbol.
            
            :param compSymbol: Other symbol.
            :type compSymbol: b_Symbol
            :param last: Number of last chars. Usualy equal to current stride. Used only if self is final state.
            :type last: int
            :param local_chars: List of set of local_chars. Set of all posible chars for each new subsymbol of final kchar (char + char = 2 strided kchar, list will have exactly 1 set present). used to have striding deterministic.
            
            :returns: New strided symbol and unused symbols from local chars.
            :rtype: tuple(b_Symbol, set())
            
            :raises: symbol_double_stride_exception if double stride can't be computed.
        """
        if compSymbol.get_type() in self.get_support_type():
            return self.compute_double_stride(compSymbol, False, last, local_chars)
        elif self.get_type() in compSymbol.get_support_type():
            return compSymbol.compute_double_stride(self, True, last, local_chars)
        else :
            raise pattern_exceptions.symbol_double_stride_exception(self.get_type(), compSymbol.get_type())

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
            
            :returns: New strided symbol and unused symbols from local chars.
            :rtype: tuple(b_Symbol, set())
        """
        
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
            if other.get_type() in self.get_support_type():
                return self.compute_equal(other)
            elif self.get_type() in other.get_support_type():
                return other.compute_equal(self)
            else :
                raise pattern_exceptions.symbol_equality_exception(self.get_type(), other.get_type())
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
            if other.get_type() in self.get_support_type():
                return not self.compute_equal(other)
            elif self.get_type() in other.get_support_type():
                return not other.compute_equal(self)
            else :
                raise pattern_exceptions.symbol_equality_exception(self.get_type(), other.get_type())
        except (AttributeError, TypeError):
            return True

    def is_empty(self):
        """
            Return True if symbol is empty. False if is not empty.
            
            :returns: True if symbol is empty. False if is not empty.
            :rtype: boolean
        """

class DEF_SYMBOLS(b_Symbol):
    """
        Class for default symbol, which is used in Delay DFA.
        
        :param new_text: Text description of symbol, should be human readeable.
        :type new_text: string
        :param new_id: Symbol identification number, must be unique.
        :type new_id: int
    """

    def __init__(self, new_text, new_id):
        """ 
            Constructor of DEF_SYMBOLS class
        
            :param new_text: Text description of symbol, should be human readeable.
            :type new_text: string
            :param new_id: Symbol identification number, must be unique.
            :type new_id: int
        """
        b_Symbol.__init__(self, new_text, new_id)
        self.ctype = io_mapper["DEF_SYMBOLS"]

    def accept(self, text):
        """
            If symbol is at the beginning of the text, is removed from the text and reminder is returned. Otherwise accept_exception is raised.
            
            :param text: Text to be parsed.
            :type text: string
            :returns: Text without begining.
            :rtype: string
            :rises: accept_exception if symbol is not at the begining of the text.
        """

        return text

    def collision(self, set_of_symbols):
        """
            Returns True if def_symbol is present in set_of_symbols otherwise returns False. From definition this symbol can be in collision only with self.
         
            :param set_of_symbols: Set of symbols.
            :type set_of_symbols: set(b_Symbol)
            :returns: True if at least two symbols are in collision, otherwise False is returned.
            :rtype: boolean
         """
        for sym in set_of_symbols:
            if sym.get_type() == io_mapper["DEF_SYMBOLS"]:
                return True
        return False

    def export_symbol(self):
        """ 
            Returns symbol representation compatible with FSM tools - http://www2.research.att.com/~fsmtools/fsm/man4/fsm.5.html.
            The symbol is encoded in string without whitespace chars. First char is used for symbol class specification and therefore is not part of the encoded symbol.
            Symbol class specification char for this symbol class is defined by b_symbol.io_mapper["DEF_SYMBOLS"].
                      
            :returns: Symbol representation compatible with FSM tools.
            :rtype: string
        """
        return io_mapper["DEF_SYMBOLS"]

    def import_symbol(self, text_repr, tid):
        """ 
            Creates symbol from its string representation compatible with FSM tools. See export method for more datails.
            
            :param text_repr: String representation.
            :type text_repr: string
            :param tid: Symbol identification number, must be unique.
            :type tid: int
        """
        if text_repr[0] != io_mapper["DEF_SYMBOLS"]:
            msg = "DEF_SYMBOLS: Symbol class specification char '" + io_mapper["DEF_SYMBOLS"] + "' expected but '" + text_repr[0] + "' found!"
            raise pattern_exceptions.symbol_import_exception(msg)

        self._id = tid

        self._text = "default"

    def compute_collision(self, other):
        """ 
            Compute collision with def_symbol. Collision can be only with other def_symbol.
            
            :param other: Other symbol.
            :type other: b_Symbol
            
            :returns: Resolved collision - changes to the symbols and new ones, if they are created.
            :rtype: tuple(set(b_Symbol), set(b_Symbol), set(b_Symbol))
        """
        if other.get_type() == io_mapper["DEF_SYMBOLS"]:
            return (set(), set([other]), set())
        else:
            return (set([self]), set(), set([other]))

    def compute_equal(self, other):
        """
            Compute if two symbols (self and other) are equivalent.
            
            :param other: Other symbol.
            :type Other: b_Symbol
            
            :returns: True if the symbols are equivalent, otherwise returns False.
            :rtype: boolean
        """
        if other.get_type() == io_mapper["DEF_SYMBOLS"]:
            return True
        else:
            return False

    def get_support_type(self):
        """ 
            Return supported types of symbols for current type of symbol.
        """
        return [io_mapper["b_Sym_char"], io_mapper["b_Sym_char_class"], io_mapper["b_Sym_string"], io_mapper["b_Sym_kchar"], io_mapper["DEF_SYMBOLS"]]

    def is_empty(self):
        """
            Return True if symbol is empty. False if is not empty.
            
            :returns: True if symbol is empty. False if is not empty.
            :rtype: boolean
        """

        return False
    
    def __hash__(self):
        """
            Returns hash representation of symbol.
            
            :returns: Hash representation of symbol.
            :rtype: int
        """
        return hash("Default symbol: HASH string: Salt:!@#$%^&*()_+{}:<>?1234567890-=[];,." + str(self._id))

###############################################################################
# End of File b_symbol.py                                                     #
###############################################################################
