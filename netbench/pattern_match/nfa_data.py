# -*- coding: utf-8 -*-
###############################################################################
#  nfa_data.py: Module for PATTERN MATCH - class for NFA representation
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

import cPickle
import sym_char
import sym_char_class
from b_state import b_State
import b_symbol
import sym_char
import sym_char_class
import sym_kchar
import sym_cnt_constr
import sym_string
import pattern_exceptions
import aux_func

# ------------------------------------------------------------------
#
#    Data structure for NFA representation
#
# ------------------------------------------------------------------

class nfa_data:
    """
        A class to specify NFA automaton (Q,T,q0,Delta,F).

        .. list-table::
            :widths: 15 15 70
            :header-rows: 1

            * - Attribute
              - Type
              - Description

            * - states
              - dict(int, b_State)
              - Finite set of states.
            * - alphabet
              - dict(int, b_Symbol)
              - Symbols of alphabet.
            * - start
              - int
              - ID of Start state.
            * - transitions
              - set(tupple(int, int, int))
              - Transitions. Format (Start state ID, Symbol ID, End state ID)
            * - final
              - set(int)
              - Final states.
            * - Flags
              - dict(string, any type)
              - Flags for specified properties.

        Flags dictionary stores various properties of automaton. The list of all supported flags is in the next table.

        .. list-table::
            :widths: 15 15 70
            :header-rows: 1

            * - Flag
              - Type
              - Description
            * - Deterministic
              - boolean
              - Is automaton deterministic?
            * - Strided
              - boolean
              - Is automaton strided (accept multiple characters)?
            * - Stride
              - int
              - Number of characters accepted at once by the automaton.
            * - Epsilon Free
              - boolean
              - Is automaton without epsilon transitions?
            * - Alphabet collision free
              - boolean
              - Is alphabet without collisions?
            * - Minimal
              - boolean
              - Is DFA minimal?
            * - Delay DFA
              - boolean
              - Is automaton Delay DFA?
            * - Extend_FA
              - boolean
              - Is automaton Extend DFA?
            * - History FA
              - boolean
              - Is automaton History DFA?
            * - Hybrid FA - one NFA part
              - boolean
              - Is automaton NFA part of Hybrid DFA?
            * - Hybrid FA - DFA part
              - boolean
              - Is automaton DFA part of Hybrid DFA?
    """
    def __init__(self):
        """
            Constructor for initialisation of object atributes.
        """
        self.states      = dict();      # Finite set of states
        self.alphabet    = dict();      # Symbols of alphabet
        self.start       = -1;          # ID of Start state
        self.transitions = set();       # Transitions
        self.final       = set();       # Final states
        self.Flags       = dict();      # Flags for specified properties


    """NFA representation"""
    def save_to_file(self, FileName):
        """
            Save nfa_data to file (serialisation).

            :param FileName: Name of file in which nfa_data will be saved.
            :type FileName: string

            :returns: True if success, False otherwise.
            :rtype: boolean
        """
        File = open(FileName,'w')
        cPickle.dump(self,File)
        File.close()
        return True

    def load_from_file(self, FileName):
        """
            Load nfa_data from file (serialisation).

            :param FileName: Name of file from which nfa_data will be loaded.
            :type FileName: string

            :returns: Object created from file is returned.
            :rtype: nfa_data
        """
        File = open(FileName,'r')
        test = cPickle.load(File)
        File.close()
        return test

    def show(self, FileName, sizeStr=" size=\"8,5\"\n"):
        """
            Save graphviz dot file, representing graphical structure of nfa_data.

            :param FileName: Name of file into which nfa_data graphical representation will be saved.
            :type FileName: string
            :param sizeStr: Size of resulting image. Set to " " to set unbounded dimensions. Format of                  this parameter is / size="x,y"\\n/ to set width to x inches and height to y inches.
            :type sizeStr: string
            :returns: True if success, False otherwise.
            :rtype: boolean
        """
        # If object does not contain automaton, stop.
        if len(self.states) == 0:
            return False
        else:
            # Otherwise open file and save the representation.
            f = open(FileName,"w")

            #Print header of the dot file
            f.write("digraph \" Automat \" {\n    rankdir=LR;\n "+sizeStr);
            f.write("node [shape = doublecircle];\n");

            #Print end states as double circles
            for EndSt in self.final:
                f.write(self.states[EndSt].get_text())
                f.write(";\n");

            f.write("node [shape=circle];\n");

            #print all transitions. States are print as a circle
            for Source in self.transitions:
                f.write(self.states[Source[0]].get_text())
                f.write(" -> ")
                f.write(self.states[Source[2]].get_text())
                f.write(" [ label = \"")

                s = self.alphabet[Source[1]].get_text()
                i = 0
                modStr = str()

               # unprintable characters save in hexa
                while i < len(s):
                       if (ord(s[i]) > 127 or ord(s[i]) < 30):
                           modStr = modStr + "\\\\" + hex(ord(s[i]))
                       elif s[i] == '"':
                           modStr = modStr + "\\\\" + hex(ord(s[i]))
                       elif s[i] == '\'':
                           modStr = modStr + "\\\\" + hex(ord(s[i]))
                       elif s[i] == '\\':
                           modStr = modStr + "\\\\"
                       else:
                           modStr = modStr + s[i]
                       i = i + 1
                f.write(modStr)
                f.write("\" ];\n")
            f.write("}")
            f.close();
            return True

    def __repr__(self):
        """
            Returns representation of object.

            :returns: Representation of object.
            :rtype: string
        """
        return "States: " + str(self.states) + "\nAlphabet: " + str(self.alphabet) + "\nStart: " + str(self.start) + "\nTransitions: " + str(self.transitions) + "\nFinal: " + str(self.final) + "\nFlags: " + str(self.Flags) + "\n"

    def __str__(self):
        """
            Returns representation of object.

            :returns: Representation of object.
            :rtype: string
        """
        return repr(self)

    def export_to_fsm(self, FileName="automaton.fsm", SymbolFileName = "automaton.sym"):
        """
            Save automaton to file in FSM format. Based on FSM man page: http://www2.research.att.com/~fsmtools/fsm/man4.html

            :param FileName: File name to which the fsm part will be exported.
            :type FileName: string
            :param SymbolFileName: File name to which the sym part will be exported.
            :type SymbolFileName: string

        """

        fw = open(FileName, 'w') # file write
        t_s = {}                 # transitions sorted

        # sort transitions
        for s in self.states:
            t_s[s] = []
        for t in self.transitions:
            t_s[t[0]].append(t)

        states = list(sorted(self.states))
        states.remove(self.start)
        # save transitions for start state
        for t in t_s[self.start]:
            fw.write(str(self.start) + ' ' + str(t[2]) \
            + ' ' + str(self.alphabet[ t[1] ].export_symbol()) + '\n')
            # check final state
            if self.start in self.final:
                fw.write(str(self.start) + '\n')
        # save transitions for other states
        for s in states:
            for t in t_s[s]:
                fw.write(str(s) + ' ' + str(t[2]) + ' ' \
                + str(self.alphabet[ t[1] ].export_symbol()) + '\n')
            # check final state
            if s in self.final:
                fw.write(str(s) + '\n')
        fw.close()

        # Write exported symbols to symbol file
        fs = open(SymbolFileName, 'w')
        for symbol in self.alphabet.keys():
            fs.write(self.alphabet[symbol].export_symbol() + " " + str(symbol + 1) + "\n")
        fs.close()

    def import_from_fsm(self, FileName="automaton.fsm", SymbolFileName = "automaton.sym"):
        """
            Load automaton from file in FSM format. Based on FSM man
            page: http://www2.research.att.com/~fsmtools/fsm/man4.html . This method must be updated if new symbol is added to Netbench. Raises Exception if unknown symbol string type is found and coresponding class can not be determinated.

            :param FileName: File name from which the fsm part will be imported.
            :type FileName: string
            :param SymbolFileName: File name from which the sym part will be imported.
            :type SymbolFileName: string
            :raises: nfa_data_import_exception if unknown symbol string type is found and coresponding class can not be determinated.

        """

        # initialization
        self.states      = dict();      # Finite set of states
        self.alphabet    = dict();      # Symbols of alphabet
        self.start       = -1;          # ID of Start state
        self.transitions = set();       # Transitions
        self.final       = set();       # Final states
        self.Flags       = dict();      # Flags for specified properties

        # Load symbols from symbol file
        fs = open(SymbolFileName, 'r')

        symbol_mapper = dict()

        # Read all symbols
        for line in fs.readlines():
            # Split line
            line = line.split()
            # Get symbol ID - subtract 1 (FSM Library use 0 for epsilon symbol, Netbench use -1 for epsilon symbol)
            symbol_id = int(line[1]) - 1
            # maps symbol string to its id
            symbol_mapper[line[0]] = symbol_id
            # get name of symbol class
            try:
                cls = b_symbol.io_reverse_mapper[line[0][0]]
            except:
                raise nfa_data_import_exception(line[0][0])
            symbol = None
            # Create new object of selected class
            if cls == "b_Sym_char":
                symbol = sym_char.b_Sym_char("","", 0)
            if cls == "b_Sym_char_class":
                symbol = sym_char_class.b_Sym_char_class("", set(), 0)
            if cls == "b_Sym_string":
                symbol = sym_string.b_Sym_string("","", 0)
            if cls == "b_Sym_kchar":
                symbol = sym_kchar.b_Sym_kchar("",("",""), 0)
            if cls == "DEF_SYMBOLS":
                symbol = b_symbol.DEF_SYMBOLS("", 0)
            if cls == "b_Sym_cnt_constr":
                symbol = sym_cnt_constr.b_Sym_cnt_constr("","",0,0,0)
            if symbol == None:
                raise nfa_data_import_exception(line[0][0])
            else:
                # Import symbol
                symbol.import_symbol(line[0], symbol_id)
                # Add to alphabet
                self.alphabet[symbol_id] = symbol

        fs.close()

        fr = open(FileName, 'r') # file read

        # first line indicating start state
        line = fr.readline()
        line = line.split()
        src = int(line[0])
        self.start = src
        self.states[src] = b_State(mid = src)
        # line is transition
        if len(line) > 1:
            des = int(line[1])
            if src != des:
                self.states[des] = b_State(mid = des)
            self.transitions.add((src, symbol_mapper[line[2]], des))
        # first line is start state and too final state
        # (line is final state)
        else :
            self.final.add(src)
            self.states[src]._rnum = src

        # from 2 line to EndOfFile
        for line in fr.readlines():
            line = line.split()
            src = int(line[0])
            if src not in self.states:
                self.states[src] = b_State(mid = src)
            # line is transition
            if len(line) > 1:
                des = int(line[1])
                if des not in self.states:
                    self.states[des] = b_State(mid = des)
                self.transitions.add((src, symbol_mapper[line[2]], des))
            # line is final state
            else :
                self.final.add(src)
                self.states[src]._rnum = src

        self.Flags["ImportFromFsm"] = True
        fr.close()

    def remove_states(self, states):
        """
            Removes states from automaton. States can be list, tuple, set and frozen set of ids. States can also be an id. If state is final state, the state will be also removed from final.

            :param states: States id to be removed.
            :type states: list(int), tuple(int), set(int), frozenset(int) or int

            :raises: general_unsupported_type if type of states is not supported.
        """
        # TODO: remove from start
        if isinstance(states, list) or isinstance(states, set) or isinstance(states, tuple) or isinstance(states, frozenset):
            for state in states:
                if self.states.has_key(state):
                    del self.states[state]
                    if state in self.final:
                        self.final.remove(state)
                    if state == self.start:
                        self.start = -1
        elif isinstance(states, int):
            if self.states.has_key(states):
                del self.states[states]
                if states in self.final:
                    self.final.remove(states)
                if states == self.start:
                    self.start = -1
        else:
            raise pattern_exceptions.general_unsupported_type("nfa_data.remove_states()", "states", states)

    def remove_symbols(self, symbols):
        """
            Removes symbols from automaton. Symbols can be list, tuple, set and frozen set of ids. Symbols can also be an id.

            :param symbols: Symbols id to be removed.
            :type symbols: list(int), tuple(int), set(int), frozenset(int) or int

            :raises: general_unsupported_type if type of symbols is not supported.
        """
        if isinstance(symbols, list) or isinstance(symbols, set) or isinstance(symbols, tuple) or isinstance(symbols, frozenset):
            for symbol in symbols:
                if self.alphabet.has_key(symbol):
                    del self.alphabet[symbol]
        elif isinstance(symbols, int):
            if self.alphabet.has_key(symbols):
                del self.alphabet[symbols]
        else:
            raise pattern_exceptions.general_unsupported_type("nfa_data.remove_symbols()", "symbols", symbols)

    def remove_transitions(self, transitions):
        """
            Removes transitions from automaton. Transitions can be list, tuple, set and frozen set of tuple(int, int, int). Transitions can also be a tuple(int, int, int).

            :param transitions: Transitions to be removed.
            :type transitions: list(tuple(int, int, int)), tuple(tuple(int, int, int)), set(tuple(int, int, int)), frozenset(tuple(int, int, int)) or tuple(int, int, int)

            :raises: general_unsupported_type if type of transitions is not supported.
        """
        if isinstance(transitions, list) or isinstance(transitions, set) or (isinstance(transitions, tuple) and isinstance(transitions[0], tuple)) or isinstance(transitions, frozenset):
            for transition in transitions:
                self.transitions.discard(transition)

        elif isinstance(transitions, tuple):
            self.transitions.discard(transitions)
        else:
            raise pattern_exceptions.general_unsupported_type("nfa_data.remove_transitions()", "transitions", transitions)

    def get_max_state_id(self):
        """
            Returns max id of states.

            :returns: Max id of states.
            :rtype: int
        """
        return max(self.states.keys())

    def get_max_alphabet_id(self):
        """
            Returns max id of symbols

            :returns: Max id of symbols.
            :rtype: int
        """
        return max(self.alphabet.keys())

    def is_consistent(self, syndrome = None):
        """
            Return True if nfa_data structure is consistent, otherwise returns False. This method is intended for debuging purposes.


            :param syndrome: Dict of inconsistency syndromes. The dict have to be set to empty dict (If the dict is nonempty, it will be cleared). If syndrome is None no syndrome is returned.       Syndrome keys are ints describing kind of inconsitency, the values are lists of appropriate objects.

                ======= ================================================================================
                Key     Description
                ======= ================================================================================
                0       Check if values of the states dict are states failed.
                1       Check if values of the alphabet dict are symbols failed.
                2       Check if values of the transitions set are tuples with at least 3 items failed.
                3       Check if transitions are valid failed.
                4       Check if final set is valid.
                5       Check if start is valid.
                6       Check if id in the state object is same as key in the states dict.
                7       Check if id in the symbol object is same as key in the alphabet dict.
                ======= ================================================================================

                ======= ================================================================================
                Key     Values
                ======= ================================================================================
                0       List of failed states' ids.
                1       List of failed symbol's ids.
                2       List of failed transitions.
                3       List of failed transitions (set of tuples).
                4       List of failed states' ids.
                5       List of failed states' ids.
                6       List of failed states' ids.
                7       List of failed symbol's ids.
                ======= ================================================================================
            :type syndrome: dict(int->int)

            :returns: True if nfa_data structure is consistent, otherwise returns False.
            :rtype: boolean
        """
        ok = True
        isi = isinstance(syndrome, dict)
        if isi == True:
            syndrome.clear()

        # Check data types
        # States
        for state in self.states.keys():
            try:
                self.states[state].is_final()
            except Exception:
                ok = False
                if isi == True:
                    if syndrome.has_key(0) == False:
                        syndrome[0] = list()
                    syndrome[0].append(state)


        # Alphabet
        for symbol in self.alphabet.keys():
            try:
                self.alphabet[symbol].get_type()
            except Exception:
                ok = False
                if isi == True:
                    if syndrome.has_key(1) == False:
                        syndrome[1] = list()
                    syndrome[1].append(symbol)

        # Transitions
        for transition in self.transitions:
            if (isinstance(transition, tuple) == False) or (len(transition) < 3):
                ok = False
                if isi == True:
                    if syndrome.has_key(2) == False:
                        syndrome[2] = list()
                    syndrome[2].append(transition)

        # Check the transitions - all states and symbol must exist
        for transition in self.transitions:
            try:
                self.states[transition[0]].is_final()
                self.alphabet[transition[1]].get_type()
                self.states[transition[2]].is_final()
            except Exception:
                ok = False
                if isi == True:
                    if syndrome.has_key(3) == False:
                        syndrome[3] = list()
                    syndrome[3].append(transition)

        # Check the final set - all states must exist
        for state in self.final:
            try:
                self.states[state].is_final()
            except Exception:
                ok = False
                if isi == True:
                    if syndrome.has_key(4) == False:
                        syndrome[4] = list()
                    syndrome[4].append(state)

        # Check the start
        if self.start < -1:
            ok = False
            if isi == True:
                if syndrome.has_key(5) == False:
                    syndrome[5] = list()
                syndrome[5].append(self.start)
        elif self.states.has_key(self.start) == False:
            ok = False
            if isi == True:
                if syndrome.has_key(5) == False:
                    syndrome[5] = list()
                syndrome[5].append(self.start)

        # Check corespondence of inner object id with outer object id
        # States
        for state in self.states.keys():
            if self.states[state].get_id() != state:
                ok = False
                if isi == True:
                    if syndrome.has_key(6) == False:
                        syndrome[6] = list()
                    syndrome[6].append(state)

        # Alphabet
        for symbol in self.alphabet.keys():
            if self.alphabet[symbol].get_id() != symbol:
                ok = False
                if isi == True:
                    if syndrome.has_key(7) == False:
                        syndrome[7] = list()
                    syndrome[7].append(symbol)

        # All is OK
        return ok

    def has_symbol(self, symbol):
        """
            This method returns True if symbol is in alphabet, otherwise returns False.

            :param symbol: Symbol to be checked.
            :type symbol: b_Symbol

            :returns: True if symbol is in alphabet, otherwise returns False.
            :rtype: boolean
        """

        for sym in self.alphabet.values():
            if sym == symbol:
                return True

        return False

    def get_symbol_id(self, symbol):
        """
            This method returns id of equivalent symbol is in alphabet, otherwise throws exception unknown_symbol.

            :param symbol: Symbol to be checked.
            :type symbol: b_Symbol

            :returns: Id of equivalent symbol in alphabet.
            :rtype: int

            :raises: symbol_not_found if symbol is not in alphabet.
        """

        for sym in self.alphabet.keys():
            if self.alphabet[sym] == symbol:
                return sym

        raise pattern_exceptions.symbol_not_found(str(symbol))

    def add_transitions(self, transitions):
        """
            Add transitions to automaton. Transitions can be list, tuple, set and frozen set of tuple(int, int, int). Transitions can also be a tuple(int, int, int).

            :param transitions: Transitions to add.
            :type transitions: list(tuple(int, int, int)), tuple(tuple(int, int, int)), set(tuple(int, int, int)), frozenset(tuple(int, int, int)) or tuple(int, int, int)

            :raises: general_unsupported_type if type of transitions is not supported.
        """
        if isinstance(transitions, list) or isinstance(transitions, set) or (isinstance(transitions, tuple) and isinstance(transitions[0], tuple)) or isinstance(transitions, frozenset):
            for transition in transitions:
                self.transitions.add(transition)

        elif isinstance(transitions, tuple):
            self.transitions.add(transitions)
        else:
            raise pattern_exceptions.general_unsupported_type("nfa_data.add_transitions()", "transitions", transitions)

    def add_states(self, states):
        """
            Add states to automaton. States can be list, tuple, set and frozen set of states objects. States can also be an an state object (object of b_State class or class derived from b_State class). If state is final its added to the final set of automaton. If state can not be added due an id collision exception is raised and rollback on states and final is performed.

            :param states: States id to add.
            :type states: list(b_State), tuple(b_State), set(b_State), frozenset(b_State) or b_State

            :raises: general_unsupported_type if type of states is not supported.
        """
        back_states = self.states.copy()
        back_final = self.final.copy()
        if isinstance(states, list) or isinstance(states, set) or isinstance(states, tuple) or isinstance(states, frozenset):
            for state in states:
                if self.states.has_key(state.get_id()):
                    self.states = back_states
                    self.final = back_final
                    raise pattern_exceptions.state_id_collision(state.get_id())
                else:
                    self.states[state.get_id()] = state
                    if state.is_final() == True:
                        self.final.add(state.get_id())
        elif isinstance(states, b_State):
            if self.states.has_key(states.get_id()):
                raise pattern_exceptions.state_id_collision(states.get_id())
            else:
                self.states[states.get_id()] = states
                if states.is_final() == True:
                    self.final.add(states.get_id())
        else:
            raise pattern_exceptions.general_unsupported_type("nfa_data.add_states()", "states", states)

    def add_symbols(self, symbols):
        """
            Add symbols to automaton. Symbols can be list, tuple, set and frozen set of symbol objects (objects of classes derived from b_Symbol). Symbols can also be a symbol object. If symbol can not be added due an id collision exception is raised and rollback on symbols is performed. Before calling this method, the symbols must be checked by check_symbols() or has_symbol() method and all symbol must be unique (result of this methods must be False).

            :param symbols: Symbols id to add.
            :type symbols: list(b_Symbol), tuple(b_Symbol), set(b_Symbol), frozenset(b_Symbol) or b_Symbol

            :raises: general_unsupported_type if type of symbols is not supported.
        """
        back_symbols = self.alphabet.copy()
        if isinstance(symbols, list) or isinstance(symbols, set) or isinstance(symbols, tuple) or isinstance(symbols, frozenset):
            for symbol in symbols:
                if self.alphabet.has_key(symbol.get_id()):
                    self.alphabet = back_symbols
                    raise pattern_exceptions.symbol_id_collision(symbol.get_id())
                else:
                    self.alphabet[symbol.get_id()] = symbol
        elif isinstance(symbols, b_symbol.b_Symbol):
            if self.alphabet.has_key(symbols.get_id()):
                raise pattern_exceptions.symbol_id_collision(symbols.get_id())
            else:
                self.alphabet[symbols.get_id()] = symbols
        else:
            raise pattern_exceptions.general_unsupported_type("nfa_data.add_symbols()", "symbols", symbols)

    def check_symbols(self, symbols):
        """
            This method checks if symbols in symbols are in automaton alphabet. Symbols can be list, tuple, set and frozen set of symbolobjects. Returns list of boolean values - True if symbol is in alphabet, otherwise False.

            :param symbols: Symbols id to check.
            :type symbols: list(b_Symbol), tuple(b_Symbol), set(b_Symbol), or frozenset(b_Symbol)

            :returns: Mapping of symbols to their presence in automaton.
            :rtype: list(tuple(b_Symbol, boolean))

            :raises: general_unsupported_type if type of symbols is not supported.
        """
        if isinstance(symbols, list) or isinstance(symbols, set) or isinstance(symbols, tuple) or isinstance(symbols, frozenset):
            return map(self.has_symbol, symbols)
        else:
            raise pattern_exceptions.general_unsupported_type("nfa_data.check_symbols()", "symbols", symbols)

    def is_empty(self):
        """
            Return True if nfa_data structure is empty, false otherwise.

            :returns: True if nfa_data structure is empty, false otherwise.
            :rtype: boolean
        """
        if len(self.states) == 0:
            return True
        else:
            return False

    ###########################################################################
    # Deprecated methods                                                      #
    ###########################################################################
    def SaveToFile(self, FileName):
        """
            Save nfa_data to file (serialisation).

            :param FileName: Name of file in which nfa_data will be saved.
            :type FileName: string

            :returns: True if success, False otherwise.
            :rtype: boolean

            NOTE: This method is deprecated. Use save_to_file().
        """
        aux_func.deprecation_warning("method", "SaveToFile()", "save_to_file()")
        return self.save_to_file(FileName)

    def LoadFromFile(self, FileName):
        """
            Load nfa_data from file (serialisation).

            :param FileName: Name of file from which nfa_data will be loaded.
            :type FileName: string

            :returns: Object created from file is returned.
            :rtype: nfa_data

            NOTE: This method is deprecated. Use load_from_file().
        """
        aux_func.deprecation_warning("method", "LoadFromFile()", "load_from_file()")
        return self.load_from_file(FileName)

    def Show(self, FileName, sizeStr=" size=\"8,5\"\n"):
        """
            Save graphviz dot file, representing graphical structure of nfa_data.

            :param FileName: Name of file into which nfa_data graphical representation will be saved.
            :type FileName: string
            :param sizeStr: Size of resulting image. Set to " " to set unbounded dimensions. Format of                  this parameter is / size="x,y"\\n/ to set width to x inches and height to y inches.
            :type sizeStr: string
            :returns: True if success, False otherwise.
            :rtype: boolean

            NOTE: This method is deprecated. Use show().
        """
        aux_func.deprecation_warning("method", "Show()", "show()")
        return self.show(FileName, sizeStr)

    def ExportToFsm(self, FileName="automaton.fsm", SymbolFileName = "automaton.sym"):
        """
            Save automaton to file in FSM format. Based on FSM man
            page: http://www2.research.att.com/~fsmtools/fsm/man4.html

            :param FileName: File name to which the fsm part will be exported.
            :type FileName: string
            :param SymbolFileName: File name to which the sym part will be exported.
            :type SymbolFileName: string

            NOTE: This method is deprecated. Use export_to_fsm().
        """
        aux_func.deprecation_warning("method", "ExportToFsm()", "export_to_fsm()")
        self.export_to_fsm(FileName, SymbolFileName)

    def ImportFromFsm(self, FileName="automaton.fsm", SymbolFileName = "automaton.sym"):
        """
            Load automaton from file in FSM format. Based on FSM man
            page: http://www2.research.att.com/~fsmtools/fsm/man4.html . This method must be updated if new symbol is added to Netbench. Raises Exception if unknown symbol string type is found and coresponding class can not be determinated.

            :param FileName: File name from which the fsm part will be imported.
            :type FileName: string
            :param SymbolFileName: File name from which the sym part will be imported.
            :type SymbolFileName: string
            :raises: nfa_data_import_exception if unknown symbol string type is found and coresponding class can not be determinated.

            NOTE: This method is deprecated. Use import_from_fsm().
        """
        aux_func.deprecation_warning("method", "ImportFromFsm()", "import_from_fsm()")
        self.import_from_fsm(FileName, SymbolFileName)

###############################################################################
# End of File nfa_data.py                                                     #
###############################################################################
