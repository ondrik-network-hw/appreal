###############################################################################
#  sym_kchar.py: Module for PATTERN MATCH - k-char symbol for strided automata
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

import b_symbol
import copy
import pattern_exceptions
import sym_kchar

class b_Sym_kchar (b_symbol.b_Symbol):
    """ 
        A base class to represent a k-char symbol. Chars can be char or char classes.
        
        :param new_text: Text description of symbol, should be human readeable.
        :type new_text: string
        :param new_id: Symbol identification number, must be unique.
        :type new_id: int
        :param kchar: k-char
        :type kchar: tuple(frozenset(char) or char)
    """
    def __init__(self, new_text,kchar,new_id):
        """ 
            Class constructor.
            
            :param new_text: Text description of symbol, should be human readeable.
            :type new_text: string
            :param new_id: Symbol identification number, must be unique.
            :type new_id: int
            :param kchar: k-char
            :type kchar: tuple(frozenset(char) or char)
        """
        b_symbol.b_Symbol.__init__(self, new_text, new_id)
        # kchar is tupple of (frozen sets of chars or char)
        self.kchar = kchar
        self.ctype = b_symbol.io_mapper["b_Sym_kchar"]
        self.last = 0
        # Can be only set True when second symbol for stride is sym_eof
        self.eof = False

    def accept(self, text):
        """
            If symbol is at the beginning of the text, is removed from the text and reminder is returned. Otherwise accept_exception is raised.
            
            :param text: Text to be parsed.
            :type text: string
            
            :returns: Text without begining.
            :rtype: string
            
            :rises: accept_exception if symbol is not at the begining of the text.
        """
        acceptable = True
        epsCnt = 0

        search_len = len(self.kchar) - self.last
        
        if len(text) < search_len:
            raise pattern_exceptions.symbol_string_to_short()

        for i in range(0, search_len):
            if isinstance(self.kchar[i], frozenset):
                kacceptable = False
                for char in self.kchar[i]:
                    if char == "":
                        kacceptable = True
                        epsCnt += 1
                    if text[i] == char[0]:
                        kacceptable = True
                if kacceptable == True:
                    acceptable = True
                else:
                    raise pattern_exceptions.symbol_accept_exception()
            else:
                if self.kchar[i] == "":
                    acceptable = True
                    epsCnt += 1
                if text[i] == self.kchar[i][0]:
                    acceptable = True
                else:
                    raise pattern_exceptions.symbol_accept_exception()

        if self.eof == True and len(text) > search_len:
            acceptable = False
                
        if acceptable == True:
            if epsCnt == len(self.kchar):
                return text
            else:
                return text[search_len:]
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
            if sym.get_type() == b_symbol.io_mapper["b_Sym_kchar"]:
                if len(sym.kchar) == len(self.kchar):
                    collision = True
                    self_set = set()
                    sym_set = set()
                    for i in range(0, len(self.kchar)):
                        if isinstance(self.kchar[i], frozenset) == True:
                            self_set = self.kchar[i]
                        else:
                            self_set = set()
                            self_set.add(self.kchar[i])
                        if isinstance(sym.kchar[i], frozenset) == True:
                            sym_set = sym.kchar[i]
                        else:
                            sym_set = set()
                            sym_set.add(sym.kchar[i])

                        if self_set.isdisjoint(sym_set) == True:
                            collision = False
                    if collision == True:
                        return True
                else:
                    # Sane strided automaton should not have strided symbols with different stride so prefix collision is not implemented.
                    pass
            else:
                # from current symbols none can be in collision, unless strided string char is implemented (prefix collision)
                pass

        return False

    def _get_texts(self):
        """ 
            Return list of all possible strings created from k-char.
            
            :returns: List of alll possible strings created from k-char.
            :rtype: list(string)
        """
        newList = list()
        oldList = list()

        if isinstance(self.kchar[0], frozenset):
            for char in self.kchar[0]:
                newList.append(char)
        else:
            newList.append(self.kchar[0])

        for i in range(1, len(self.kchar)):
            oldList = copy.deepcopy(newList)
            newList = list()
            if isinstance(self.kchar[i], frozenset):
                for char in self.kchar[i]:
                    for text in oldList:
                        newList.append(text + char)
            else:
                for text in oldList:
                    newList.append(text + self.kchar[i])

        return newList

    def export_symbol(self):
        """
            Returns symbol representation compatible with FSM tools - http://www2.research.att.com/~fsmtools/fsm/man4/fsm.5.html.
            The symbol is encoded in string without whitespace chars. First char is used for symbol class specification and therefore is not part of the encoded symbol.
            Symbol class specification char for this symbol class is defined by b_symbol.io_mapper["b_Sym_kchar"].
            
            :returns: Symbol representation compatible with FSM tools.
            :rtype: string
        """
        hex_repr = ""
        for i in range(0, len(self.kchar)):
            hex_repr += "|"
            if isinstance(self.kchar[i], frozenset):
                for char in self.kchar[i]:
                    chex_repr = hex(ord(char))[2:]
                    if len(chex_repr) == 1:
                        chex_repr = "0" + chex_repr
                    hex_repr += chex_repr
            else:
                chex_repr = hex(ord(self.kchar[i]))[2:]
                if len(chex_repr) == 1:
                    chex_repr = "0" + chex_repr
                hex_repr += chex_repr
        
        last_hex = hex(self.last)[2:]
        if len(last_hex) == 1:
            last_hex = "0" + last_hex
        
        eof_hex = ""
        if self.eof == True:
            eof_hex += "01"
        else:
            eof_hex += "00"
        
        return b_symbol.io_mapper["b_Sym_kchar"] + last_hex + eof_hex + hex_repr 

    def import_symbol(self, text_repr, tid):
        """             
            Creates symbol from its string representation compatible with FSM tools. See export method for more datails.
            
            :param text_repr: String representation.
            :type text_repr: string
            :param tid: Symbol identification number, must be unique.
            :type tid: int
        """
        if text_repr[0] != b_symbol.io_mapper["b_Sym_kchar"]:
            msg = "b_Sym_kchar: Symbol class specification char '" + b_symbol.io_mapper["b_Sym_kchar"] + "' expected but '" + text_repr[0] + "' found!"
            raise pattern_exceptions.symbol_import_exception(msg)

        self._id = tid
        self.last = int(text_repr[1] + text_repr[2], 16)
        eof = text_repr[3] + text_repr[4]
        if eof == "00":
            self.eof = False
        else:
            self.eof = True
            
        hex_repr = text_repr[5:]

        splited_hex_repr = hex_repr.split("|")

        self._text = "{"
        kchar = list()

        for i in range(1, len(splited_hex_repr)):
            if len(splited_hex_repr[i]) > 2:
                charClass = set()
                self._text += "["

                for j in range(0, len(splited_hex_repr[i]) / 2):
                    chex_repr = splited_hex_repr[i][j * 2] + splited_hex_repr[i][j * 2 + 1]
                    charClass.add(chr(int(chex_repr, 16)))
                    self._text += chr(int(chex_repr, 16))

                self._text += "]"
                kchar.append(charClass)
            else:
                kchar.append(chr(int(splited_hex_repr[i], 16)))
                self._text += chr(int(splited_hex_repr[i], 16))

        self._text += "}"
        self.kchar = tuple(kchar)

    def __str__(self):
        """
            Returns string representation of symbol.
            
            :returns: String representation of symbol. 
            :rtype: string
        """
        return str(self.kchar)

    def compute_equal(self, other):
        """
            Compute if two symbols (self and other) are equivalent.
            
            :param other: Other symbol.
            :type Other: b_Symbol
            
            :returns: True if the symbols are equivalent, otherwise returns False.
            :rtype: boolean
        """
        if other.get_type() == b_symbol.io_mapper["b_Sym_kchar"]:
            if self.kchar == other.kchar:
                if self.last == other.last and self.eof == other.eof:
                    return True
                else:
                    return False
            else:
                if len(self.kchar) != len(other.kchar):
                    return False
                else:
                    for i in range(0, len(self.kchar)):
                        if (isinstance(self.kchar[i], frozenset) and isinstance(other.kchar[i], frozenset)) or (not isinstance(self.kchar[i], frozenset) and not isinstance(other.kchar[i], frozenset)):
                            if self.kchar[i] != other.kchar[i]:
                                return False
                        else:
                            if isinstance(self.kchar[i], frozenset):
                                if len(self.kchar[i]) != 1:
                                    return False
                                else:
                                    for sym in self.kchar[i]:
                                        if sym != other.kchar[i]:
                                            return False
                            elif isinstance(other.kchar[i], frozenset):
                                if len(other.kchar[i]) != 1:
                                    return False
                                else:
                                    for sym in other.kchar[i]:
                                        if sym != self.kchar[i]:
                                            return False
            if self.last == other.last and self.eof == other.eof:
                return True
            else:
                return False
        elif other.get_type() == b_symbol.io_mapper["b_Sym_string"]:
            if len(self.kchar) == len(other.string):
                for i in range(0, len(self.kchar)):
                    if isinstance(self.kchar[i], frozenset) and len(self.kchar[i] > 1):
                        return False
                if other.string in self._get_texts():
                    return True
                else:
                    return False
            else:
                return False
        elif other.get_type() == b_symbol.io_mapper["b_Sym_char"]:
            if len(self.kchar) == 1:
                if len(self._get_texts()) == 1 and other.char in self._get_texts():
                    return True
                else:
                    return False
            else:
                return False
        elif other.get_type() == b_symbol.io_mapper["b_Sym_char_class"]:
            if len(self.kchar) == 1:
                s = set()
                if isinstance(self.kchar[0], frozenset):
                    s = self.kchar[0]
                else:
                    s.add(self.kchar[0])
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
        return hash(self.kchar) + hash(self.last) + hash(self.eof)

    def __repr__(self):
        """
            Returns string representation of symbol.
            
            :returns: String representation of symbol. 
            :rtype: string
        """
        return repr(self.kchar)

    def get_support_type(self):
        """ 
            Return supported types of symbols for current type of symbol.
            
            :returns: Supported types of symbols for current type of symbol.
            :rtype: list(int)
        """
        return [b_symbol.io_mapper["b_Sym_char"], b_symbol.io_mapper["b_Sym_char_class"], b_symbol.io_mapper["b_Sym_string"], b_symbol.io_mapper["b_Sym_kchar"]]

    def is_empty(self):
        """
            Return True if symbol is empty. False if is not empty.
            
            :returns: True if symbol is empty. False if is not empty.
            :rtype: boolean
        """

        if len(self.kchar) == 0:
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
            :param local_chars: List of Set of local_chars. Set of all posible chars. used to have striding deterministic. Number of sets in the list is equal to len(self.kchar).
            :type local_chars: list(set(char))
                        
            :returns: New strided symbol.
            :rtype: sym_kchar
        """
        a = self
        b = compSymbol
        
        first = None
        second = None
        
        previous_last = 0
        
        first = list(a.kchar)
        if reverse == True:
            previous_last = b.last
            
            # remove used symbol from local copy of complete alphabet.
            for i in range(len(a.kchar)):
                if isinstance(a.kchar[i], frozenset):
                    local_chars[i] = local_chars[i] - a.kchar[i]
                else:
                    aset = set([a.kchar[i]])
                    local_chars[i] = local_chars[i] - aset
                
                    
        if b.get_type() == b_symbol.io_mapper["b_Sym_kchar"]:
            second = list(b.kchar)

            if reverse == False:
                previous_last = a.last
                # remove used symbol from local copy of complete alphabet.
                for i in range(len(b.kchar)):
                    if isinstance(b.kchar[i], frozenset):
                        local_chars[i] = local_chars[i] - b.kchar[i]
                    else:
                        bset = set([b.kchar[i]])
                        local_chars[i] = local_chars[i] - bset
            
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
        new_symbol = b_Sym_kchar(complete_str, complete, 0)
        new_symbol.last = a.last + b.last + last
        new_symbol.eof = self.eof or compSymbol.eof
        
        return (new_symbol, local_chars)

    def _create_text(self, complete):
        """
            Return text representation of kchar.

            :param complete: k-char
            :type complete: tuple(frozenset(char) or char)
            :returns: text representation of k-char.
            :rtype: string
        """

        complete_str = "{"

        for i in range(0, len(complete)):
            if len(complete[i]) == 1:
                for char in complete[i]:
                    complete_str += str(char)
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
        return complete_str

    def compute_collision(self, compSymbol):
        """ 
            Compute collision between self and compSymbol.
            
            :param other: Other symbol.
            :type other: b_Symbol
            
            :returns: Resolved collision - changes to the symbols and new ones, if they are created.
            :rtype: tuple(set(b_Symbol), set(b_Symbol), set(b_Symbol))
        """

        first = list()
        second = list()
        intersect = list()

        if len(self.kchar) != len(compSymbol.kchar):
            return(set([self]),set(),set([compSymbol]))
        
        for f,s in zip(self.kchar, compSymbol.kchar):
            if isinstance(f, str):
                f = frozenset([f])
            if isinstance(s, str):
                s = frozenset([s])
            intersect.append(f & s)
            first.append(f - s)
            second.append(s - f)
        
        newKchars1 = list()
        newKchars2 = list()
        for i in range(1, 2 ** len(first)):
            # all possible combinations
            item = list()
            item2 = list()
            for j in range(len(first)):
                if (i >> j) % 2:
                    item.append(first[j])
                    item2.append(second[j])
                else:
                    item.append(intersect[j])
                    item2.append(intersect[j])
            # ignore symbols with empty classes
            if frozenset([]) not in item:
                newKchars1.append(item)
            if frozenset([]) not in item2:
                newKchars2.append(item2)
        
        str1 = self._create_text(intersect)
        interSymbol = b_Sym_kchar(str1, tuple(intersect), -2)
        interSymbol.last = min(self.last, compSymbol.last)
        newSymbols1 = set()
        newSymbols2 = set()

        for i in newKchars1:
            str1 = self._create_text(i)
            sym1 = b_Sym_kchar(str1, tuple(i), -2)
            sym1.last = self.last
            sym1.eof = self.eof
            newSymbols1.add(sym1)
        for i in newKchars2:
            str2 = self._create_text(i)
            sym2 = b_Sym_kchar(str2, tuple(i), -2)
            sym2.last = compSymbol.last
            sym2.eof = compSymbol.eof
            newSymbols2.add(sym2)

        return(newSymbols1, set([interSymbol]), newSymbols2)


###############################################################################
# End of File sym_kchar.py                                                    #
###############################################################################
