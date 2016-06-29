###############################################################################
#  pcre_parser.py: Module for PATTERN MATCH - Wrapper for new pcre parser.
#                  The pcre parser is independent program written in
#                  C + flex + bison.
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

import commands
import os
import re
import nfa_data
from nfa_parser import nfa_parser
import copy
import sym_char
import sym_char_class
from b_state import b_State
import sys
import aux_func
import pattern_exceptions
import sym_cnt_constr
import sym_eof

class pcre_parser(nfa_parser):
    """
        Class for parsing RE using new C pcre parser. For the correct work of this class it is required that the path to the netbench was in the system variable NETBENCHPATH..
    
        FORMAT of Automata file (MSFM2) version 2:
        
        1. Number of the States in the automaton
        
        2. Number of the transition in the automaton
        
        3. Number of start state
        
        4. Each transition is represenetd by one line in the file. Line is in format Source_State|Symbol|Target_State|Epsilon
        
        5. End of the transition table is represented by line of #
        
        6. Number of the end states
        
        7. Line with identifikator of the endState. Every endstate is folowed by , (coma)
        
        8. End of endState section is represented by line of #
        
        9. Number of the symbols in symbol table
        
        10. Every symbol is stored on its own line and it is represented as Symbol_Number:Character1|Character2| . Characters are encoded as hexa numbers.
        
        11. End of the file
        
    """
    def __init__(self, create_cnt_constr = False, create_eof_symbols = False, *args):
        """ 
            Class constructor. Inits the seed of random generator. If neccessery parser is compiled. 
        """
        nfa_parser.__init__(self)           #Calling the parent function
        last = ""
        
        # find where we are
        msfm_path = aux_func.getPatternMatchDir()
        work_path = os.getcwd()
        
        # Make parser - check if parser sources ware modified
        cmd = "cd " + msfm_path +"/pcre_parser; make parser; cd " + work_path +""
        commands.getstatusoutput(cmd)
        
        # Check if parser can be run
        res = commands.getstatusoutput(msfm_path + "/pcre_parser/parser -h")
        if res[0] != 0:
            # Compile parser during init
            cmd = "cd " + msfm_path +"/pcre_parser; make clean; make parser; cd " + work_path +""
            res = commands.getstatusoutput(cmd)
        # Check again if parser can be run
        res = commands.getstatusoutput(msfm_path + "/pcre_parser/parser -h")
        if res[0] != 0:
            raise pattern_exceptions.pcre_parser_failure()
        
        self.create_cnt_constr = create_cnt_constr
        self.create_eof_symbols = create_eof_symbols
         
    def get_nfa(self):
        """
            Parse a current line and returns parsed nfa.
            
            :returns: Created automaton in nfa_data format. Returns None if failure happens.
            :rtype: nfa_data or None
        """
        # Check if some reg. exp. are set. 
        if (self._position < 0):
            return None
        
        # Create random value.
        #value = random.randint(0, sys.maxint)
        
        # Get line.
        line = self._text[self._position]
        
        # Remove trailing \n
        if line[len(line) - 1] == '\n':
            line = line[0:len(line)-1]

        #line = "/" + line + "/"
        
        self.last = line
              
        # find where we are
        msfm_path = aux_func.getPatternMatchDir()
        work_path = os.getcwd()
                
        # invoke C regexp parser
        #cmd = "echo '" + line + "' | " + msfm_path + "/pcre_parser/parser -o STDOUT -s"
        #res = aux_func.getstatusoutput(cmd)
        cmd = ""
        
        # Create cnt_constr symbols if requested
        if self.create_cnt_constr == False:
            cmd = msfm_path + "/pcre_parser/parser -o STDOUT -s" 
        else:
            cmd = msfm_path + "/pcre_parser/parser -o STDOUT -s -c"
        # Do not create eof symbols if requested
        if self.create_eof_symbols == False:
            cmd += " -E"
        
        res = aux_func.getstatusoutput(cmd, line)
        # Print stderr if there is some content
        if len(res[2]) != 0:
            sys.stderr.write(res[2] + "\n")
        # If error, stop.
        if res[0] != 0:
            sys.stderr.write("PARSER ERROR:\n")
            sys.stderr.write("CMD: " + cmd + "\n")
            sys.stderr.write("PCRE: " + line + "\n")
            sys.stderr.write("MSFM:\n");
            sys.stderr.write(res[1] + "\n");
            return None;
        else:
            try:
                # Create empty object
                nfa = nfa_data.nfa_data()              
                
                # Preprocess automaton file
                FSMfile = res[1].split("\n")

                # Get start state of NFA
                nfa.start = int(FSMfile[2])
                del FSMfile[2]
                
                # FORMAT of Automata file
                #  - Number of the States in the automaton
                #  - Number of the transition in the automaton
                #  - Each transition is represenetd by one line in the file. Line 
                #    is in format Source_State|Symbol|Target_State|Epsilon
                #  - End of the transition table is represented by line of #
                #  - Number of the end states
                #  - Line with identifikator of the endState. Every endstate is 
                #    folowed by , (coma)
                #  - End of endState section is represented by line of #
                #  - Number of the symbols in symbol table
                #  - Every symbol is stored on its own line and it is represented 
                #    as Symbol_Number:Character1|Character2|
                #  - End of the file
        
                TransitionTable = [x.split("|") for x in FSMfile[2:int(FSMfile[1])+2]];         
                # Transition table is list of the list and represents the whole 
                # transition table of the automata.  2 is an index of the first 
                # transition FSMfile[1] is the number of the transition in automaton
                
                # List of the endStates is stored after all transition (FSMfile[1])
                # and after 4 other lines (number of states, number of transitions,
                # number of endstates, and the line of ####
                # Endstates are isolated by , (coma) 
                Endstates = FSMfile[int(FSMfile[1])+4].split(",")
                
                # Alphabet symbols start on the index FSMfile[1] 
                # (all transitions) + 7 (4 as before + line of #, 
                # line of endstates and number of symbols) 
                Symbols = (FSMfile[int(FSMfile[1])+7:]);
                            
                # Creates end states objects.
                for state in Endstates:
                    if state != "":
                        Tmp = b_State(int(state),set([self._position]))     #Creates state which is described by the int(State)
                        nfa.states[Tmp.get_id()] = Tmp
                        nfa.final.add(Tmp.get_id())
                
                all_msfm_syms = dict()
                
                # For every symbol in alphabet
                for ActSym in Symbols:                        
                    # Separate symbol number and symbol data (done by first :)
                    StartSym = ActSym.find(":");
                    if ActSym[StartSym+1] == '#':
                        # Split at #
                        sharp_split = ActSym[StartSym+1:len(ActSym)-1].split("#")
                        # Get m
                        m = int(sharp_split[1])
                        # Get n
                        n = 0
                        # Check if infinite number of symbols can occure
                        if sharp_split[2] == '':
                            n = float("inf")
                        else:
                            n = int(sharp_split[2])
                        # Get symbol part of encoded cnt constr
                        SymSym = ActSym.rfind("#");
                        symSet = set([x for x in ActSym[SymSym+1:len(ActSym)-1].split("|")])
                        symSetMod = set()
                        # convert hex to char
                        for s in symSet:
                            symSetMod.add(chr(long(s,16) & 255))
                        # Create symbol
                        symbol = None
                        text_info = ""
                        if not (m == 0 and n == 0):
                            # Create char if number of symbols is 1.
                            if len(symSetMod) == 1:
                                char = symSetMod.pop()
                                symbol = char
                                text_info += char + "{" + str(m) + "," + str(n) + "}"
                            else:
                                # Create char class otherwise.
                                strSymSetMod = str()
                                for sym in symSetMod:
                                    strSymSetMod += sym
                                strSymSetMod = "[" + strSymSetMod + "]"
                                text_info += strSymSetMod  + "{" + str(m) + "," + str(n) + "}"
                                symbol = symSetMod
                            # Create sym_cnt_constr object
                            Tmp = sym_cnt_constr.b_Sym_cnt_constr(text_info, symbol, m ,n, int(ActSym[:StartSym], 16))
                            nfa.alphabet[Tmp.get_id()] = Tmp
                            # Create mapping from symbol chars to their ids
                            if (m,n,frozenset(symbol)) not in all_msfm_syms:
                                all_msfm_syms[(m,n,frozenset(symbol))] = set()
                            all_msfm_syms[(m,n,frozenset(symbol))].add(int(ActSym[:StartSym], 16))
                        else:
                            #BUG: Workaround for bug in parser, when cnt constr symbols are generated even construction such as s+, d*, .+, ... are converted. This behaviaor is not OK, but fix of the parser would consume to mauch time. This workaround works OK.
                            # Create mapping from symbol chars to their ids
                            if frozenset(symSetMod) not in all_msfm_syms:
                                all_msfm_syms[frozenset(symSetMod)] = set()
                            all_msfm_syms[frozenset(symSetMod)].add(int(ActSym[:StartSym], 16))
                            
                            # Create char if number of symbols is 1.
                            if len(symSetMod) == 1:
                                char = symSetMod.pop()
                                Symbol = sym_char.b_Sym_char(char,char,int(ActSym[:StartSym], 16))
                                nfa.alphabet[Symbol.get_id()] = Symbol
            #                    nfa.alphabet[int(ActSym[:StartSym], 16)] = sym_char.b_Sym_char(char, char)
                            else:
                                # Create char class otherwise.
            #                    nfa.alphabet[int(ActSym[:StartSym], 16)] = sym_char_class.b_Sym_char_class(str(symSetMod), symSetMod)
                                strSymSetMod = str()
                                for sym in symSetMod:
                                    strSymSetMod += sym
                                strSymSetMod = "[" + strSymSetMod + "]"
                                #nfa.alphabet[int(ActSym[:StartSym], 16)] 
                                Tmp = sym_char_class.b_Sym_char_class(strSymSetMod,symSetMod,int(ActSym[:StartSym], 16))
                                nfa.alphabet[Tmp.get_id()] = Tmp
                    elif ActSym[StartSym+1:] == "EOF|":
                        # Add EOF symbol into alphabet
                        Symbol = sym_eof.b_Sym_EOF("EOF", int(ActSym[:StartSym], 16))
                        nfa.alphabet[Symbol.get_id()] = Symbol
                        # Create mapping from symbol chars to their ids
                        if "EOF" not in all_msfm_syms:
                            all_msfm_syms["EOF"] = set()
                        all_msfm_syms["EOF"].add(int(ActSym[:StartSym], 16))
                    else:
                        symSet = set([x for x in ActSym[StartSym+1:len(ActSym)-1].split("|")])
                        symSetMod = set()
                        # convert hex to char
                        for s in symSet:
                            symSetMod.add(chr(long(s,16) & 255))
                        
                        # Create mapping from symbol chars to their ids
                        if frozenset(symSetMod) not in all_msfm_syms:
                            all_msfm_syms[frozenset(symSetMod)] = set()
                        all_msfm_syms[frozenset(symSetMod)].add(int(ActSym[:StartSym], 16))
                        
                        # Create char if number of symbols is 1.
                        if len(symSetMod) == 1:
                            char = symSetMod.pop()
                            Symbol = sym_char.b_Sym_char(char,char,int(ActSym[:StartSym], 16))
                            nfa.alphabet[Symbol.get_id()] = Symbol
        #                    nfa.alphabet[int(ActSym[:StartSym], 16)] = sym_char.b_Sym_char(char, char)
                        else:
                            # Create char class otherwise.
        #                    nfa.alphabet[int(ActSym[:StartSym], 16)] = sym_char_class.b_Sym_char_class(str(symSetMod), symSetMod)
                            strSymSetMod = str()
                            for sym in symSetMod:
                                strSymSetMod += sym
                            strSymSetMod = "[" + strSymSetMod + "]"
                            #nfa.alphabet[int(ActSym[:StartSym], 16)] 
                            Tmp = sym_char_class.b_Sym_char_class(strSymSetMod,symSetMod,int(ActSym[:StartSym], 16))
                            nfa.alphabet[Tmp.get_id()] = Tmp
                        
                # TODO: use special class for Epsilon?
                # Epsilon is representad now as sym_char object with char "" and index -1
                #nfa.alphabet[-1] 
                Tmp = sym_char.b_Sym_char("Epsilon", "",-1)
                nfa.alphabet[Tmp.get_id()] = Tmp
                
                # removeable symbols
                removeable_symbols = set()
                nonremoveable_symbols = set()
                # Add non final states to automaton.
                for transition in TransitionTable:
                    # if not in states, add start state of transition.
                    if not (int(transition[0]) in nfa.states):
                        nfa.states[int(transition[0])] = b_State(int(transition[0]), set())
                    
                    # if not in states, add end state of transition.
                    if not (int(transition[2]) in nfa.states):
                        nfa.states[int(transition[2])] = b_State(int(transition[2]), set())
                    
                    # Handle epsilon transitions.
                    alphaNum = -1
                    if transition[3] == '1':
                        alphaNum = -1
                        removeable_symbols.add(int(transition[1], 16))
                    else:
                        alphaNum = int(transition[1], 16)
                        nonremoveable_symbols.add(alphaNum)
                                       
                    # Add transition to automaton.
                    nfa.transitions.add((int(transition[0]), alphaNum, int(transition[2])))
                
                # Corect the removeable symbols
                removeable_symbols -= nonremoveable_symbols
                
                # Remove unused symbols
                for rsymbol in removeable_symbols:
                    del nfa.alphabet[rsymbol]
                
                # Remove duplicit symbols
                sym_mapping = dict()
                
                # Create mapping between current ids and the ids which will be used.
                # Only non removed id can be used as key
                #print all_msfm_syms
                #print removeable_symbols
                for key in all_msfm_syms:
                    sym = all_msfm_syms[key].pop()
                    if sym not in removeable_symbols:
                        all_msfm_syms[key].add(sym)
                    else:
                        found = 0
                        syms = set()
                        syms.add(sym)
                        while found == 0:
                            if len(all_msfm_syms[key]) == 0:
                                break
                            sym = all_msfm_syms[key].pop()
                            syms.add(sym)
                            if sym not in removeable_symbols:
                                found = 1
                                all_msfm_syms[key] |= syms
                                
                    for sid in all_msfm_syms[key]:
                        sym_mapping[sid] = sym
                    
                sym_mapping[-1] = -1
                
                add_transitions = set()
                #print sym_mapping
                for transition in nfa.transitions:
                    #print transition
                    add_transitions.add((transition[0], sym_mapping[transition[1]], transition[2]))
                
                nfa.transitions = add_transitions
                
                for sid in sym_mapping:
                    if sid != sym_mapping[sid]:
                        if sid not in removeable_symbols:
                            del nfa.alphabet[sid]

                # Somethimg is wrong with the msfm file, try autodetect the start state
                if nfa.start < 0:
                    # Determinate start station
                    # Dictionary mapping between states and their previous states.
                    StateInSymbols = dict()
                    # Autodetect start state of NFA - remove when start state is aded to the msfm format
                    # Compute the mapping between states and their transitions.
                    for state in nfa.states.keys():
                        StateInSymbols[state] = set()
                    for transition in nfa.transitions:
                        if StateInSymbols.has_key(transition[2]) == True:
                            StateInSymbols[transition[2]].add(transition[0])
                        else:
                            StateInSymbols[transition[2]] = set()
                            StateInSymbols[transition[2]].add(transition[0])
                    
                    # Autodetection - start state can have only 0 or 1 in transition originating from itself - problem /^(abc)+..../
                    for state in StateInSymbols.keys():
                        if len(StateInSymbols[state]) == 0:
                            nfa.start =state
                        elif (len(StateInSymbols[state]) == 1) and (list(StateInSymbols[state])[0] == state):
                            nfa.start = state
                
                return nfa
            except None:
                sys.stderr.write("ERROR while parsing msfm output of parser:\n")
                sys.stderr.write("CMD: " + cmd + "\n")
                sys.stderr.write("PCRE: " + line + "\n")
                sys.stderr.write("MSFM:\n");
                sys.stderr.write(res[1] + "\n");
                return None

###############################################################################
# End of File pcre_parser.py                                                  #
###############################################################################
