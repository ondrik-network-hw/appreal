###############################################################################
#  sourdis_bispo_nfa.py: Module for PATTERN MATCH
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

# import modules from netbench
from netbench.pattern_match import nfa_data
from netbench.pattern_match import nfa_reductions 
from netbench.pattern_match import b_nfa
from netbench.pattern_match import b_state
from netbench.pattern_match import pcre_parser
from netbench.pattern_match import sym_char_class
from netbench.pattern_match import sym_char
from netbench.pattern_match import sym_string
from netbench.pattern_match import b_symbol
from netbench.pattern_match.sym_cnt_constr import b_Sym_cnt_constr
from netbench.pattern_match.pattern_exceptions import COMPUTE_ERROR, empty_automaton_exception
from netbench.pattern_match import aux_func
# import system modules
import math
import copy
import re

class pcre_block_data:
    """ 
        Class containing informations about PCRE repetitions. 
        
        :param symbol: Repeated symbol.
        :type symbol: b_Symbol
        :param index: Index of PCRE repetition.
        :type index: int
        :param m: Minimal number of repetitions.
        :type m: int
        :param n: Maximal number of repetitions.
        :type n: int
    """
    def __init__(self, symbol, index, m, n = None):
        """ 
            Class constructor. 
            
            :param symbol: Repeated symbol.
            :type symbol: b_Symbol
            :param index: Index of PCRE repetition.
            :type index: int
            :param m: Minimal number of repetitions.
            :type m: int
            :param n: Maximal number of repetitions.
            :type n: int
        """
        self.symbol = symbol
        if n == None:
            self.repetition = [m, m]
        else:
            self.repetition = [m, n]
        self.index = index
    
    def get_block_index_re(self):
        """ 
            Return regular expression for finding the ###index### patterns.
            
            :returns: Regular expression for finding the ###index### patterns.
            :rtype: string
        """
        return "###" + str(self.index) + "###"
        
    def __repr__(self):
        """ 
            Returns string representation of class instance.
            
            :returns: Representation of class instance.
            :rtype: string
        """
        string = "PCRE repeat " + str(self.index) + " MIN = "
        minimal = str(self.repetition[0])
        if self.repetition[1] == float("inf"):
            maximal = "INF"
        else:
            maximal = str(self.repetition[1])
        string += minimal + " TO = " + maximal + "\n"
        string += str(self.symbol)
        return string
        
    def __str__(self):
        """ 
            Returns string representation of class instance.
            
            :returns: Representation of class instance.
            :rtype: string
        """
        return repr(self)
    
class sourdis_bispo_nfa(nfa_reductions.nfa_reductions):
    """
        NFA Pattern Matching algorithm as described in: Sourdis et al. Regular Expression Matching in Reconfigurable Hardware. 
    """
    def __init__(self):
        """
            Class constructor.
        """
        nfa_reductions.nfa_reductions.__init__(self)
        # Set data width - always 8
        self.width = 8
        # Set VHDL template
        self.template = aux_func.getPatternMatchDir() + "/algorithms/sourdis_bispo_nfa/vhdl/sourdis_bispo_nfa.vhd"
        self._statistic = dict()
        # Set number of LUT inputs - always 6 for new Xilinx FPGAs
        self._LUTInputs = 6
        # Init number of LUTs and FFs
        self._luts = 0
        self._ffs = 0
        # Init PCRE repetitions
        self.pcre_repetitions = list()
        
    def compute(self):
        """
            Compute Sourdis_Bispo automata mapping into FPGA.
        """

        # Call initial compute
        nfa_reductions.nfa_reductions.compute(self)
        # Check if compute failed
        if not self.get_compute():
            raise COMPUTE_ERROR
        
        # If automaton is empty raise exception
        if self._automaton.is_empty() == True:
            raise empty_automaton_exception
        
        # remove epsilons
        self.remove_epsilons()
        # share prefixes of automaton
        self.share_prefixes()
        # create string and PCRE symbols
        self.create_string_and_pcre_symbols()
        
        # we need to perform the mapping to know number of used FPGA resources
        self.get_HDL()
        # set compute to true
        self._compute = True
                
    def find_pcre_repetitions(self, FileName):
        """
            Discover .{n} like patterns and extracts them from regular expression.
            Found patterns are replaced by $$$index$$$ so they can be easily found in
            automaton and be replaced by special symbol.
        
            :param FileName: Name of ruleset.
            :type FileName: string
        
            :returns: Preprocessed rules as string.
            :rtype: string
        """
        # init used variables
        new_ruleset = ""
        index = 0
        
        # open ruleset file
        fr = open(FileName, 'r')
        # iterate throught the RE in file and process them into modified RE
        for line in fr.readlines():
            # remove '\n' from end of line
            line = line.rsplit('\n', 1)[0]
            tmp = re.split("(^/)", line, 1)
            begin = tmp[1]
            line = tmp[2]
            tmp = re.split("(/[a-zA-Z]*$)", line, 1)
            line = tmp[0]
            if 'i' in tmp[1]:
                end = '/i'
            else:
                end = '/'
            #pattern = re.compile("([^\{\}]*)")
            # Get pattern for {m,n} subparts of RE
            pattern = re.compile("(\{[0-9]*,?[0-9]*\})")
            # split line to before (split[0]) and after (split[1]) part
            split = re.split(pattern, line)
            #print(split)
            # For all {m,n} subpatterns: process, verify, create 
            # pcre_block_data and insert placeholders
            for i in range(0, len(split)):
                part = split[i]
                # Split exists
                if len(part) > 0:
                    # Check if we realy found start
                    if part[0] == '{':
                        data = None
                        nums = re.split("[{},]", part)
                        # Create {m} variant
                        if len(nums) == 3:
                            #print "{m}"
                            data = pcre_block_data(None, index, int(nums[1]))
                        # Create various {m,n} variants
                        elif len(nums) == 4:
                            if len(nums[1]) > 0 and len(nums[2]) > 0:
                                #print "{m,n}"
                                data = pcre_block_data(None, index, int(nums[1]), int(nums[2]))
                            elif len(nums[1]) > 0 and len(nums[2]) == 0:
                                #print("{m,}")
                                data = pcre_block_data(None, index, int(nums[1]), float("inf"))
                            elif len(nums[1]) == 0 and len(nums[2]) > 0:
                                #print("{,n}")
                                data = pcre_block_data(None, index, 0, int(nums[2]))
                            else:
                                raise Exception
                        else:
                            raise Exception                            
                        
                        nre = "/^"
                        cnt = 0
                        
                        # Verify if the prefix of {m,n} subpart is representable as (), or symbol
                        if split[i - 1][len(split[i - 1]) - 1] != ']':
                            # Detect char class
                            if split[i - 1][len(split[i - 1]) - 1] == ')':
                                if split[i - 1][len(split[i - 1]) - 2] == '\\':
                                    nre += "\\)"
                                    cnt += 2
                                else:
                                    continue
                            # Other type
                            else:
                                # Find start of subpart prefix
                                if (len(split[i - 1]) - 4 >= 0) and (split[i - 1][len(split[i - 1]) - 4] == '\\') and (split[i - 1][len(split[i - 1]) - 3] == 'x'):
                                    nre += split[i - 1][len(split[i - 1]) - 4] + split[i - 1][len(split[i - 1]) - 3] + split[i - 1][len(split[i - 1]) - 2] + split[i - 1][len(split[i - 1]) - 1]
                                    cnt += 4
                                elif (len(split[i - 1]) - 2 >= 0) and (split[i - 1][len(split[i - 1]) - 2] == '\\'):
                                    nre += split[i - 1][len(split[i - 1]) - 2] + split[i - 1][len(split[i - 1]) - 1]
                                    cnt += 2
                                else:
                                    nre += split[i - 1][len(split[i - 1]) - 1]
                                    cnt += 1
                        # Verify if the prefix of {m,n} subpart is representable as []
                        else:
                             # Find start of subpart prefix
                            if split[i - 1][len(split[i - 1]) - 2] == '\\' and split[i - 1][len(split[i - 1]) - 3] != '\\':
                                nre += "\\]"
                                cnt += 2
                            else:
                                 # Find start of subpart prefix
                                inner_re = "]"
                                cnt += 1
                                j = len(split[i - 1]) - 2
                                # Iterate via all subchars in char class
                                while j >= 0:
                                    if split[i - 1][j] != '[':
                                        inner_re = split[i - 1][j] + inner_re
                                        cnt += 1
                                    else:
                                        if j > 0:
                                            if split[i - 1][j - 1] != '\\':
                                                inner_re = split[i - 1][j] + inner_re
                                                cnt += 1
                                                break
                                            else:
                                                if j - 2 >= 0:
                                                    if split[i - 1][j - 2] != '\\':
                                                        inner_re = split[i - 1][j] + inner_re
                                                        cnt += 1
                                                    else:
                                                        inner_re = split[i - 1][j] + inner_re
                                                        cnt += 1
                                                        break
                                                else:
                                                    raise Exception
                                        else:
                                            inner_re = split[i - 1][j] + inner_re
                                            cnt += 1
                                    j = j - 1
                                nre += inner_re
                        # Set end RE
                        nre += end
                        
                        # Parse the prefix subpattern and remove epsilons
                        Test0 = pcre_parser.pcre_parser()
                        Test0.set_text(nre)
                        internal = b_nfa.b_nfa()
                        internal.create_by_parser(Test0)
                        internal.remove_epsilons()
                        
                        # Check if sth. is wrong
                        if len(internal._automaton.alphabet) > 1:
                            print nre
                            print internal._automaton
                            print "Something is tragicaly wrong."
                            #raise Exception 
                            # just ignore it
                            data.symbol = internal._automaton.alphabet[0]
                        else:
                            for ind in internal._automaton.alphabet.keys():
                                data.symbol = internal._automaton.alphabet[ind]
                        # set the parsed symbol
                        self.pcre_repetitions.append(data)
                        
                        # update RE
                        split[i - 1] = split[i - 1][0:(len(split[i - 1]) - cnt)]
                        index += 1
                        # insert placeholder
                        split[i] = "###" + str(index) + "###"
            # Create new RE from parts
            new_re = ""
            new_re += begin
            for i in range(0, len(split)):
                new_re += split[i]
            new_re += end
            new_ruleset += new_re + "\n"
        # Close the input file
        fr.close()
        # Return new ruleset
        return new_ruleset
            
    def get_all_string_subpatterns(self):
        """ 
            Traverse automaton and return dict of all string subpatterns. Dict key is the string and the value is its alphabet id.
            
            :returns: Dict of all string subpatterns.
            :rtype: dict(string->int)
        """
        subpatterns = dict()
        for symbol in self._automaton.alphabet.values():
            if symbol.get_type() == b_symbol.io_mapper["b_Sym_string"]:
                subpatterns[symbol.string] = symbol.get_id()
        return subpatterns
    
    
    def _check_state(self, state, mapper, reverse_mapper):
        """ 
            Check if conditions for string generation continuation are met.
            
            :param nfa: Created NFA.
            :type nfa: nfa_data
            :param state: Checked state.
            :type state: int
            :param mapper: Maps state to symbol and target state.
            :type mapper: dict(int->dict(int->int))
            :param reverse_mapper: Reverse mapping. Maps target state to symbol and state.
            :type reverse_mapper: dict(int->dict(int->int))
        """
        # check i we have only one outgoing symbol
        if len(mapper[state]) > 1:
            return False
        for symbol in mapper[state]:
            # Check if outgoing symbol is char
            if self._automaton.alphabet[symbol].get_type() != b_symbol.io_mapper["b_Sym_char"]:
                return False
            # Check if there is only one outgoing transition for this char
            if len(mapper[state][symbol]) > 1:
                return False
            #if len(reverse_mapper[state]) > 1:
                #return False
            #for psymbol in reverse_mapper[state]:
                    ## Check if state has only one ingoing transition for this symbol
                    #if len(reverse_mapper[state][psymbol]) > 1:
                        #return False
            for tstate in mapper[state][symbol]:
                # Check if target state has only one ingoing symbol
                if len(reverse_mapper[tstate]) > 1:
                    return False
                for tsymbol in reverse_mapper[tstate]:
                    # Check if target state has only one ingoing transition for this symbol
                    if len(reverse_mapper[tstate][tsymbol]) > 1:
                        return False
                    # Check if state is final state
                    if state in self._automaton.final:
                        return False
                    # If above conditions are met return true
                    return True
        # Imposible happend
        return False
   
    def _check_start(self, state, reverse_mapper):
        """ 
            Check if conditions for string generation are met.
            
            :param state: Checked state.
            :type state: int
            :param reverse_mapper: Reverse mapping. Maps target state to symbol and state.
            :type reverse_mapper: dict(int->dict(int->int))
        """
        if len(reverse_mapper[state]) > 1:
            return False
        for psymbol in reverse_mapper[state]:
                # Check if state has only one ingoing transition for this symbol
                if len(reverse_mapper[state][psymbol]) > 1:
                    return False
        return True
   
    def create_string_and_pcre_symbols(self, create_strings = True, create_pcre = True):
        """ 
            Reduces automaton by usage of string and PCRE constraioned repetitions symbols.
            
            :param create_strings: If True string symbols are created, otherwise they are not created.
            :type create_strings: boolean
            :param create_pcre: If True PCRE constrained repetitions symbols are created, otherwise they are not created. NOTE: if create_pcre = False then find_pcre_repetitions() mathod cannot be used.
            :type create_pcre: boolean
        """
        
        # maps relation between state and its outgoing transitions
        mapper = dict()
        for state in self._automaton.states.keys():
            mapper[state] = dict()
        for transition in self._automaton.transitions:
            if mapper[transition[0]].has_key(transition[1]) == True:
                mapper[transition[0]][transition[1]].add(transition[2])
            else:
                mapper[transition[0]][transition[1]] = set()
                mapper[transition[0]][transition[1]].add(transition[2])
                
        # maps relation between state and its ingoing transitions
        reverse_mapper = dict()
        for state in self._automaton.states.keys():
            reverse_mapper[state] = dict()
        for transition in self._automaton.transitions:
            if reverse_mapper[transition[2]].has_key(transition[1]) == True:
                reverse_mapper[transition[2]][transition[1]].add(transition[0])
            else:
                reverse_mapper[transition[2]][transition[1]] = set()
                reverse_mapper[transition[2]][transition[1]].add(transition[0])
        
        # dictionary of detected strings (keys) and set of coresponding state sequences (values)
        strings = dict()
        
        # Set start condition
        stack = list()
        # [current_state, string, [state sequence], [symbol sequence]]
        stack.append([self._automaton.start, "", [self._automaton.start], []])
        
        # Remember visited states
        visited = set()
        visited.add(self._automaton.start)
        
        # Extract all strings
        while len(stack) > 0:
            state = stack.pop()
            # Check if symbol was already processed
            if self._check_state(state[0], mapper, reverse_mapper) == False:
                # Add state into strings dict
                if len(state[1]) > 2:
                    if strings.has_key(state[1]) == True:
                        strings[state[1]].add((tuple(state[2]),tuple(state[3])))
                    else:
                        strings[state[1]] = set()
                        strings[state[1]].add((tuple(state[2]), tuple(state[3])))
                # Traverse throught all out symbols
                for symbol in mapper[state[0]]:
                    # Process all target states
                    for tstate in mapper[state[0]][symbol]:
                        # if state was not visited - continue
                        if tstate not in visited:
                            # Check if symbol is character
                            if self._automaton.alphabet[symbol].get_type() == b_symbol.io_mapper["b_Sym_char"] and self._check_start(tstate, reverse_mapper) == True:
                                # Add char into the current string
                                stack.append([tstate, self._automaton.alphabet[symbol].char, [state[0], tstate], [symbol]])
                                visited.add(tstate)
                            else:
                                # Start new string
                                stack.append([tstate, "", [tstate], []])
                                visited.add(tstate)
            else:
                # Add symbol into state the mapper
                for symbol in mapper[state[0]]:
                    for tstate in mapper[state[0]][symbol]:
                        state[0] = tstate
                        state[1] += self._automaton.alphabet[symbol].char
                        state[2].append(tstate)
                        state[3].append(symbol)
                        visited.add(tstate)
                # Add it into the stack
                stack.append(state)
            
        # Set max index
        index = max(self._automaton.alphabet.keys()) + 1
        
        # Detect PCRE constrained repetition strings and create pcre symbols
        if create_pcre == True:
            # init variables
            remove_list = list()
            add_dict    = dict()
            # process throught all found strings
            for string in strings.keys():
                # Find all {m,n} placeholders
                pcre = re.findall("###[0-9]+###", string)
                # If placeholder was found process it
                if len(pcre) > 0:
                    max_index = max(self._automaton.alphabet.keys())
                    # iterate throught all placeholders
                    for pcre_element in pcre:
                        i = 0
                        # find the placeholder
                        while i < len(self.pcre_repetitions) and pcre_element != self.pcre_repetitions[i].get_block_index_re():
                            i = i + 1
                        #print pcre_element
                        # ignore the unprobable situation when the placeholder
                        # was in the original RE
                        if i == len(self.pcre_repetitions):
                            continue
                        # Check if the prefix of {m,n} is character
                        if self.pcre_repetitions[i].symbol.get_type() == b_symbol.io_mapper["b_Sym_char"]:
                            symbol_data = self.pcre_repetitions[i].symbol.char
                        # Check if the prefix of {m,n} is character class
                        elif self.pcre_repetitions[i].symbol.get_type() == b_symbol.io_mapper["b_Sym_char_class"]:
                            symbol_data = self.pcre_repetitions[i].symbol.charClass
                        # Otherwise raise exception
                        else:
                            print("ERROR: sourdis_bispo_nfa.py: Unsupported symbol found during pcre constraint repetition block construction.")
                            raise Exception()
                        # Create the b_Sym_cnt_constr symbol
                        symbol = b_Sym_cnt_constr(str(self.pcre_repetitions[i]), symbol_data, self.pcre_repetitions[i].repetition[0], self.pcre_repetitions[i].repetition[1], max_index)
                        # Add the symbol into alphabet
                        self._automaton.alphabet[max_index] = symbol
                        ind = string.find(pcre_element)
                        # Modify the transitions
                        for states in strings[string]:
                            self._automaton.transitions.add((states[0][ind], max_index, states[0][ind + len(pcre_element)]))
                            for i in range(ind, ind + len(pcre_element) + 0): # + 1
                                 self._automaton.transitions.discard((states[0][i], states[1][i], states[0][i + 1]))
                            for i in range(ind + 1, ind + len(pcre_element)):
                                if states[0][i] in self._automaton.states.keys():
                                    del self._automaton.states[states[0][i]]
                        max_index += 1
                    
                    # Extract real strings
                    real_strings = re.split("###[0-9]+###", string)
                    remove_list.append(string)
                    
                    # Check if the string part is real string and not placeholder
                    if len(real_strings) > 0:
                        position_index = 0
                        # Add all real strings into the add_dict
                        for real_string in real_strings:
                            if len(real_string) > 2:
                                for states in strings[string]:
                                    ind = string.find(real_string, position_index)
                                    if add_dict.has_key(real_string) == True:
                                        add_dict[real_string].add((states[0][ind:len(real_string) + 1], states[1][ind:len(real_string)]))
                                    else:
                                        add_dict[real_string] = set()
                                        add_dict[real_string].add((states[0][ind:len(real_string) + 1], states[1][ind:len(real_string)]))
                                    position_index += len(real_string)
                            else:
                                position_index += len(real_string)
            # Remove processed placeholders
            for i in range(0, len(remove_list)):
                del strings[remove_list[i]]
            
            # add string parts from add_dict
            for string in add_dict.keys():
                if strings.has_key(string):
                    strings[string] |= add_dict[string]
                else:
                    strings[string] = set()
                    strings[string] = add_dict[string]
        
        # If strings must be created, create them
        if create_strings == True:
            # Create string symbols and update automaton
            for string in strings.keys():
                # Create string symbol
                symbol = sym_string.b_Sym_string(string, string, index)
                # Add symbol into the alphabet
                self._automaton.alphabet[index] = symbol
                
                # Update the transitions
                for states in strings[string]:
                    #print states
                    if len(states[0]) > 0:
                        for i in range(0, len(states[0])):
                            if (i > 0) and (i < len(states[0]) - 1):
                                del self._automaton.states[states[0][i]]
                            if i < len(states[0]) - 1:
                                self._automaton.transitions.remove((states[0][i], states[1][i], states[0][i + 1]))
                        self._automaton.transitions.add((states[0][0], index, states[0][len(states[0]) - 1]))          
                index += 1
            
    def  get_HDL(self):
        """
            Return HDL description of NFA unit implemented by Sourdis et al. approach.
            
            :returns: HDL description of NFA unit implemented by Sourdis et al. approach.
            :rtype: string
        """
        # Open VHDL template file and load the template
        f = open(self.template, "rb");    #Opens file automat
        blob = f.read()
        tmp = re.split("%\$%", blob)
        
        # Init atributes
        self._luts = 0
        
        # Remove epsilons
        self.remove_epsilons()
        
        # Get VHDL description of shared character decoder
        chdec = self._get_char_dec_HDL()
        # Get VHDL description of DCAM logic
        dcam = self._get_dcam_HDL()
        # Get VHDL description of mapped automaton's logic
        logic = self._get_logic_HDL()
        # Get VHDL description of final states
        final = self._get_final_HDL()
        # Concatenate signal description
        dataSignal = chdec[0] + dcam[0] + logic[0] + final[0]
        # Concatenate logic description - architecture
        dataImplementation = chdec[1] + dcam[1] + logic[1] + final[1]
        
        # Set generated code markers - begin
        textSignal = "-- --------------- GENERATED BY SOURDIS_BISPO_NFA.PY ----------------\n"
        textImplementation = "-- --------------- GENERATED BY SOURDIS_BISPO_NFA.PY ----------------\n"
        
        # Add signal description to output
        for element in dataSignal:
            textSignal += element
            
        # Add logic description to output
        for element in dataImplementation:
            textImplementation += element
        
        # Set generated code markers - end
        textSignal += "-- --------------- END ----------------\n"
        textImplementation += "-- --------------- END ----------------\n"
        
        # Add result into loaded VHDL template
        result = tmp[0] + str(self.width) + tmp[1] + str(self._fStateNum) + tmp[2] + textSignal + tmp[3] + textImplementation + tmp[4]
        
        # Return complete VHDL code.
        return result
        
    def _get_char_dec_HDL(self):
        """
            Return HDL description of shared char decoder as 
            (signals, description). 
            
            :returns: HDL description of shared char decoder as                \
                     (signals, description).
            :rtype: tuple(list(string),list(string))
        """
        # Set of all used characters - used to create the shared
        # character decoders
        allChars = set()
        
        # populate the allChars set
        for symbol in self._automaton.alphabet.keys():
            # Add all chars from char class symbol
            if self._automaton.alphabet[symbol].get_type() == b_symbol.io_mapper["b_Sym_char_class"]:
                for char in self._automaton.alphabet[symbol].charClass:
                    allChars.add(char)
            # Add char from char symbol
            if self._automaton.alphabet[symbol].get_type() == b_symbol.io_mapper["b_Sym_char"]:
                allChars.add(self._automaton.alphabet[symbol].char)
            # Add all chars from string symbol
            if self._automaton.alphabet[symbol].get_type() == b_symbol.io_mapper["b_Sym_string"]:
                for i in range(0, len(self._automaton.alphabet[symbol].string)):
                    allChars.add(self._automaton.alphabet[symbol].string[i])
            # Add all chars from cnt_constr symbol   
            if self._automaton.alphabet[symbol].get_type() == b_symbol.io_mapper["b_Sym_cnt_constr"]:
                # Add all chars if the prefix symbol is set
                if isinstance(self._automaton.alphabet[symbol].symbol, set):
                    for char in self._automaton.alphabet[symbol].symbol:
                        allChars.add(char)
                # Otherwise add the char
                else:
                    allChars.add(self._automaton.alphabet[symbol].symbol)
         
        # List of signal definitions   
        signalList = list()
        # list of logic description - architecture
        descriptionList = list()
                    
        # Crate char decoder VHDL description for all used characters
        # Instantiates the VALUE_DECODER module.
        for char in allChars:
            # Add signal definition into signalList
            signalList.append("    signal char_" + str(ord(char)) + " : std_logic;\n")
            # Create VHDL code
            chrDec  = "    VD_" + str(ord(char)) + ": entity work.VALUE_DECODER\n" 
            chrDec += "    generic map(\n"
            chrDec += "        DATA_WIDTH => " + str(self.width) + ",\n"
            chrDec += "        VALUE      => " + str(ord(char)) + "\n"
            chrDec += "    )\n"
            chrDec += "    port map(\n"
            chrDec += "        INPUT  => DATA,\n"
            chrDec += "        OUTPUT => char_" + str(ord(char)) + "\n"
            chrDec += "    );\n\n"
            # Add generated code to descriptionList - architecture
            descriptionList.append(chrDec)
            # Update number of used LUTs
            self._luts += self._countLUTsForInpunts(self.width)
                
        # Create interconection and optionaly char classes
        for symbol in self._automaton.alphabet.keys():
            # Create interconection
            # Create shared char classes if char class symbols are used 
            if self._automaton.alphabet[symbol].get_type() == b_symbol.io_mapper["b_Sym_char_class"]:
                signalList.append("    signal symbol_" + str(symbol) + " : std_logic;\n")
                text = "    symbol_" + str(symbol) + " <= "
                first = True
                # Update number of used LUTs
                self._luts += self._countLUTsForInpunts(len(self._automaton.alphabet[symbol].charClass))
                # Create the char logic
                for char in self._automaton.alphabet[symbol].charClass:
                    if first == True:
                        text += "char_" + str(ord(char))
                        first = False
                    else:
                        text += " or char_" + str(ord(char))
                text += ";\n"
                # Add the description into the logic list
                descriptionList.append(text)
            # Create interconection for char symbols
            if self._automaton.alphabet[symbol].get_type() == b_symbol.io_mapper["b_Sym_char"]:
                signalList.append("    signal symbol_" + str(symbol) + " : std_logic;\n")
                descriptionList.append("    symbol_" + str(symbol) + " <= char_" + str(ord(self._automaton.alphabet[symbol].char)) + ";\n")
            # Create interconection for cnt_constr symbols
            if self._automaton.alphabet[symbol].get_type() == b_symbol.io_mapper["b_Sym_cnt_constr"]:
                signalList.append("    signal symbol_" + str(symbol) + " : std_logic;\n")
                # If prefix is set - crete the char class logic
                if isinstance(self._automaton.alphabet[symbol].symbol, set):
                    text = "    symbol_" + str(symbol) + " <= "
                    first = True
                    # Compute the number of used luts
                    self._luts += self._countLUTsForInpunts(len(self._automaton.alphabet[symbol].symbol))
                    # Create the logic description
                    for char in self._automaton.alphabet[symbol].symbol:
                        if first == True:
                            text += "char_" + str(ord(char))
                            first = False
                        else:
                            text += " or char_" + str(ord(char))
                    text += ";\n"
                    # Add the description into the logic list
                    descriptionList.append(text)
                # Otherwise just crete the connection between the char symbol 
                # decoder and and state input
                else:
                    # Add the description into the logic list
                    descriptionList.append("    symbol_" + str(symbol) + " <= char_" + str(ord(self._automaton.alphabet[symbol].symbol)) + ";\n")
        # Return generated signal and description list
        return (signalList, descriptionList)

    def _get_dcam_HDL(self):
        """ 
            Return HDL description of embeded DCAM. 
            
            :returns: HDL description of embeded DCAM as (signals, description).
            :rtype: tuple(list(string),list(string))
        """
        
        # get strings and coresponding string symbol id's
        strings = self.get_all_string_subpatterns()
        
        # Init the set of delayed characters - tuple containing the char
        # and its position (delay) after start of string
        delayed_chars = set()
        
        # Compute the set of delayed characters
        for string in strings.keys():
            for i in range(0, len(string)):
                delayed_chars.add((string[i], len(string) - 1 - i))
        
        # List of signal definitions
        signalList = list()
        # list of logic description - architecture
        descriptionList = list()
        # Crate DCAM VHDL description for all used characters
        for char in delayed_chars:
            # Add signal into the list of signals
            signalList.append("    signal delayed_char_" + str(ord(char[0])) + "_" + str(char[1]) + " : std_logic;\n")
            # If current char is delayed add the shift register
            if char[1] > 0:
                # Create the description of the shift register instance
                dcam_element  = "    DCAM_DELAY_" + str(ord(char[0])) + "_" + str(char[1]) + ": entity work.sh_reg\n"
                dcam_element += "    generic map(\n"
                dcam_element += "        NUM_BITS    => " + str(char[1]) + "\n";   
                dcam_element += "    )\n"
                dcam_element += "    port map(\n"
                dcam_element += "        CLK      => CLK,\n"
                dcam_element += "        DIN      => char_" + str(ord(char[0])) + ",\n"
                dcam_element += "        CE       => we,\n"
                dcam_element += "        DOUT     => delayed_char_" + str(ord(char[0])) + "_" + str(char[1]) + "\n"
                dcam_element += "    );\n\n"
                # Add the description into the logic list
                descriptionList.append(dcam_element)
                # Count number of used luts
                self._luts += char[1] / 32 + 1;
            else:
                # Just add the connection into the logic description list
                descriptionList.append("    delayed_char_" + str(ord(char[0])) + "_" + str(char[1]) + " <= char_" + str(ord(char[0])) + ";\n")
        
        # Iterste over all strings
        for string in strings.keys():
            # Add the signal definition
            signalList.append("    signal symbol_" + str(strings[string]) + " : std_logic;\n")
            text = "    symbol_" + str(strings[string]) + " <= "
            first = True
            # Count the number of used luts
            self._luts += self._countLUTsForInpunts(len(string))
            # Create the connection logic
            for i in range(0, len(string)):
                if first == True:
                    text += "delayed_char_" + str(ord(string[i])) + "_" + str(len(string) - 1 - i)
                    first = False
                else:
                    text += " and delayed_char_" + str(ord(string[i])) + "_" + str(len(string) - 1 - i)
            text += ";\n"
            # Add generated code to descriptionList - architecture
            descriptionList.append(text)
        # Return generated signal and description list
        return (signalList, descriptionList)
        
    def _get_logic_HDL(self):
        """ 
            Return HDL description of states and transitions as (signals, description). 
            
            :returns: HDL description of states and transitions as (signals, description).
            :rtype: tuple(list(string),list(string)) 
        """
        # List of signal definitions
        signalList = list()
        # list of logic description - architecture
        descriptionList = list()
        
        # Create the dictionary of state having a cnt_constr transition
        pcre_states = dict()
        for transition in self._automaton.transitions:
            if self._automaton.alphabet[transition[1]].get_type() == b_symbol.io_mapper["b_Sym_cnt_constr"]:
                pcre_states[transition[2]] = transition[1]
        
        # For all states generate states modules
        for state in self._automaton.states.keys():
            # Define signals for current state
            signalList.append("    signal state_in_" + str(state) + " : std_logic;\n")
            #signalList.append("    signal state_int_" + str(state) + " : std_logic;\n")
            signalList.append("    signal state_out_" + str(state) + " : std_logic;\n")
            text = ""
            # If state doesn't have cnt_constr transitions create
            # the std. implementation
            if state not in pcre_states.keys():
                # If state is start state of automaton, set generic DEFAULT to '1'
                if state == self._automaton.start:
                    text +=  "    STATE_" + str(state) + ": entity work.STATE\n"
                    text +=  "    generic map(\n"
                    text +=  "        DEFAULT     => '1'\n"
                    text +=  "    )\n"
                    text +=  "    port map(\n"
                    text +=  "        CLK    => CLK,\n"
                    text +=  "        RESET  => local_reset,\n"
                    text +=  "        INPUT  => '0',\n"
                    text +=  "        WE     => we,\n"
                    text +=  "        OUTPUT => state_out_" + str(state) + "\n"
                    text +=  "    );\n\n"
                    # update the number of FFs
                    self._ffs += 1
                # Otherwise set generic DEFAULT to '0' for any other state
                else:
                    text +=  "    STATE_" + str(state) + ": entity work.STATE\n"
                    text +=  "    generic map(\n"
                    text +=  "        DEFAULT     => '0'\n" 
                    text +=  "    )\n"
                    text +=  "    port map(\n"
                    text +=  "        CLK    => CLK,\n"
                    text +=  "        RESET  => local_reset,\n"
                    text +=  "        INPUT  => state_in_" + str(state) + ",\n"
                    text +=  "        WE     => we,\n"
                    text +=  "        OUTPUT => state_out_" + str(state) + "\n"
                    text +=  "    );\n\n"
                    # update the number of FFs
                    self._ffs += 1
            # Handle the cnt_constr states
            else:
                signalList.append("    signal state_in_sym_" + str(state) + " : std_logic;\n")
                # Craete special state for {m}
                if self._automaton.alphabet[pcre_states[state]].m == self._automaton.alphabet[pcre_states[state]].n:
                    text +=  "    STATE_" + str(state) + ": entity work.STATE_PCRE_EXACT\n"
                    text +=  "    generic map(\n"
                    text +=  "        M     => " + str(self._automaton.alphabet[pcre_states[state]].m) + "\n" 
                    text +=  "    )\n"
                    text +=  "    port map(\n"
                    text +=  "        CLK    => CLK,\n"
                    text +=  "        RESET  => local_reset,\n"
                    text +=  "        INPUT  => state_in_" + str(state) + ",\n"
                    text +=  "        SYMBOL => state_in_sym_" + str(state) + ",\n"
                    text +=  "        WE     => we,\n"
                    text +=  "        OUTPUT => state_out_" + str(state) + "\n"
                    text +=  "    );\n\n"
                    # Update the number of FFs
                    self._ffs += int(round(self._automaton.alphabet[pcre_states[state]].m / 33 + 0.5))
                    # Update the number of LUTs
                    self._luts += int(round(self._automaton.alphabet[pcre_states[state]].m / 33 + 0.5))
                # Craete special state for {m,n}
                elif self._automaton.alphabet[pcre_states[state]].m < self._automaton.alphabet[pcre_states[state]].n and self._automaton.alphabet[pcre_states[state]].n != float("inf"):
                    text +=  "    STATE_" + str(state) + ": entity work.STATE_PCRE_AT_MOST\n"
                    text +=  "    generic map(\n"
                    text +=  "        M     => " + str(self._automaton.alphabet[pcre_states[state]].m) + ",\n"
                    text +=  "        N     => " + str(self._automaton.alphabet[pcre_states[state]].n) + "\n"
                    text +=  "    )\n"
                    text +=  "    port map(\n"
                    text +=  "        CLK    => CLK,\n"
                    text +=  "        RESET  => local_reset,\n"
                    text +=  "        INPUT  => state_in_" + str(state) + ",\n"
                    text +=  "        SYMBOL => state_in_sym_" + str(state) + ",\n"
                    text +=  "        WE     => we,\n"
                    text +=  "        OUTPUT => state_out_" + str(state) + "\n"
                    text +=  "    );\n\n"
                    # Update the number of FFs
                    self._ffs += int(round(self._automaton.alphabet[pcre_states[state]].m / 33 + math.log(self._automaton.alphabet[pcre_states[state]].n - self._automaton.alphabet[pcre_states[state]].m, 2) + 0.5))
                    # Update the number LUTs
                    self._luts += int(round(self._automaton.alphabet[pcre_states[state]].m / 33 + math.log(self._automaton.alphabet[pcre_states[state]].n - self._automaton.alphabet[pcre_states[state]].m, 2) + 0.5))
                # Craete special state for {m,}
                elif self._automaton.alphabet[pcre_states[state]].m < self._automaton.alphabet[pcre_states[state]].n and self._automaton.alphabet[pcre_states[state]].n == float("inf"):
                    text +=  "    STATE_" + str(state) + ": entity work.STATE_PCRE_AT_LEAST\n"
                    text +=  "    generic map(\n"
                    text +=  "        M     => " + str(self._automaton.alphabet[pcre_states[state]].m) + "\n" 
                    text +=  "    )\n"
                    text +=  "    port map(\n"
                    text +=  "        CLK    => CLK,\n"
                    text +=  "        RESET  => local_reset,\n"
                    text +=  "        INPUT  => state_in_" + str(state) + ",\n"
                    text +=  "        SYMBOL => state_in_sym_" + str(state) + ",\n"
                    text +=  "        WE     => we,\n"
                    text +=  "        OUTPUT => state_out_" + str(state) + "\n"
                    text +=  "    );\n\n"
                    # Update the number of FFs
                    self._ffs += int(round(math.log(self._automaton.alphabet[pcre_states[state]].m, 2) + 0.5))
                    # Update the number of LUTS
                    self._luts += int(round(math.log(self._automaton.alphabet[pcre_states[state]].m, 2) + 0.5))
            # Add generated state module instantiation to corespondig
            # description list
            descriptionList.append(text)
        
        # Compute for all states their input transitions
        inputTransitions = dict()
        for transition in self._automaton.transitions:
            if inputTransitions.has_key(transition[2]) == True:
                inputTransitions[transition[2]].add((transition[0], transition[1]))
            else:
                inputTransitions[transition[2]] = set()
                inputTransitions[transition[2]].add((transition[0], transition[1]))

        # For all transitions: if transition symbol is string generate 
        # interconection vie sh_reg, otherwise generate plane interconection 
        for transition in self._automaton.transitions:
            signalList.append("    signal state_int_" + str(transition[0]) + "_" + str(transition[1]) + "_" + str(transition[2]) + " : std_logic;\n")
            if self._automaton.alphabet[transition[1]].get_type() == b_symbol.io_mapper["b_Sym_string"]:
                # Create the description of the shift register instance
                delay_element  = "    DELAY_" + str(transition[0]) + "_" + str(transition[1]) + "_" + str(transition[2]) + ": entity work.sh_reg\n"
                delay_element += "    generic map(\n"
                delay_element += "        NUM_BITS    => " + str(len(self._automaton.alphabet[transition[1]].string) - 1) + "\n";   
                delay_element += "    )\n"
                delay_element += "    port map(\n"
                delay_element += "        CLK      => CLK,\n"
                delay_element += "        DIN      => state_out_" + str(transition[0]) + ",\n"
                delay_element += "        CE       => we,\n"
                delay_element += "        DOUT     => state_int_" + str(transition[0]) + "_" + str(transition[1]) + "_" + str(transition[2]) + "\n"
                delay_element += "    );\n\n"
                # Add the description into the logic list
                descriptionList.append(delay_element)
                # Count number of used luts
                self._luts += (len(self._automaton.alphabet[transition[1]].string) - 1) / 32 + 1;
            else:
                # Add code to decription list
                descriptionList.append("    state_int_" + str(transition[0])  + "_" + str(transition[1]) + "_" + str(transition[2]) + " <= state_out_" + str(transition[0]) + ";\n")
                
        # Generate interconection between states and between character decoders
        # and states
        for state in inputTransitions.keys():
            # If only 1 input transition is present just add previous state 
            # output and character decoder output
            if len(inputTransitions[state]) == 1:
                data = inputTransitions[state].pop()
                if state not in pcre_states:
                    # Add code to decription list
                    descriptionList.append("    state_in_" + str(state) + " <= state_int_" + str(data[0]) + "_" + str(data[1]) + "_" + str(state) + " and symbol_" + str(data[1]) + ";\n")
                    # Update number of used LUTs
                    self._luts += self._countLUTsForInpunts(2)
                else:
                    descriptionList.append("    state_in_" + str(state) + " <= state_int_" + str(data[0]) + "_" + str(data[1]) + "_" + str(state) + ";\n")
                    descriptionList.append("    state_in_sym_" + str(state) + " <= symbol_" + str(data[1]) + ";\n")
            # For more input transitions create coresponding conection structure
            # (OUTPUT AND CHAR) or (OUTPUT AND CHAR) or (OUTPUT AND CHAR) or ...
            else:
                text = str()
                first = True
                # Update number of used LUTs
                self._luts += self._countLUTsForInpunts(2*len(inputTransitions[state]))
                # Generate VHDL code
                for transition in inputTransitions[state]:
                    if first == True:
                        text += "    state_in_" + str(state) + " <= (state_int_" + str(transition[0])  + "_" + str(transition[1]) + "_" + str(state) + " and symbol_" + str(transition[1]) + ")"
                        first = False
                    else:
                        text += " or (state_int_" + str(transition[0]) + "_" + str(transition[1]) + "_" + str(state) + " and symbol_" + str(transition[1]) + ")"
                text += ";\n"
                # Add code to decription list
                descriptionList.append(text)
        # Add code to decription list
        return (signalList, descriptionList)
                        
    def _get_final_HDL(self):
        """ 
            Return HDL description of interconection of final states as        \
            (signals, description). 
            
            :returns: HDL description of interconection of final states as     \
                      (signals, description).
            :rtype: tuple(list(string),list(string))
        """
        # List of signal definitions
        signalList = list()
        # list of logic description - architecture
        descriptionList = list()
        
        # Conect final states with their RE numbers
        sameFinal = dict()
        for fstate in self._automaton.final:
            for rnum in self._automaton.states[fstate].get_regexp_number():
                if sameFinal.has_key(rnum) == True:
                    sameFinal[rnum].add(fstate)
                else:
                    sameFinal[rnum] = set()
                    sameFinal[rnum].add(fstate)
        
        # Set number of final states to number of RE
        self._fStateNum = len(sameFinal)
        
        # Create input signal for final_bitmap module
        signalList.append("    signal bitmap_in : std_logic_vector(" + str(len(sameFinal)) + " - 1 downto 0);\n")
        # Create interconection between final states and final_bitmap module
        # inputs - creates 1 bit signals
        for final in sameFinal.keys():
            signalList.append("    signal final_" + str(final) + " : std_logic;\n")
            # If number of final states coresponding to same RE is 1, just 
            # connect them
            if len(sameFinal[final]) == 1:
                state = sameFinal[final].pop()
                # Add code to decription list
                descriptionList.append("    final_" + str(final) + " <= state_out_" + str(state) + ";\n")
            # If number of final states coresponding to same RE higher than 1, 
            # 'or' final states outputs
            else:
                first = True
                # Update number of used LUTs
                self._luts += self._countLUTsForInpunts(len(sameFinal[final]))
                # Compute 'or' code structure
                for pfinal in sameFinal[final]:
                    if first == True:
                        text = "    final_" + str(final) + " <= state_out_" + str(pfinal)
                        first = False
                    else:
                        text += " or state_out_" + str(pfinal)
                text += ";\n"
                # Add code to decription list
                descriptionList.append(text)
                
        # Conect 1 bit signals into input vector of final_bitmap module
        sfKeys = sameFinal.keys()
        for i in range(0, len(sfKeys)):
            # Add code to decription list
            descriptionList.append("    bitmap_in(" + str(i) + ") <= final_" + str(sfKeys[i]) + ";\n")
        
        # Return generated signal and description list 
        return (signalList, descriptionList)

    def report_logic(self):
        """ 
            Reports amount of logic consumed by the algorithm. 
            
            :returns: Amount of logic consumed by the algorithm. (LUTs, FlipFlops, BRAMs)
            :rtype: tuple(int, int, int)
        """
        # If number of LUTs is equal to zero call get_HDL() method to perform 
        # the mapping and to compute number of used LUTs
        if self._luts == 0:
            self.get_HDL()
        
        # Number of used FFs is equivalent to number of states and size of 
        # final_bitmap unit.
        ffSize = self._ffs + self._fStateNum + 1        
        bramSize = 0        
        # Return computed resource consumption
        return (self._luts, ffSize, bramSize)
        
    def _countLUTsForInpunts(self, inputs):
        """
            Counts amount of LUTs necessary for implenentation of inputs-input \
            logic function. This creates simple tree structure of n-input LUTs \
            for inputs-input logical function with 1 output. This method only  \
            gives upper bound of actual implementation by synthesis tool.
            
            :param inputs: Number of logic function inputs
            :type inputs: int
            
            :returns: Amount of LUTs necessary for implenentation of           \
                      inputs-input logic function.
            :rtype: int
        """
        # Set start values
        i = inputs
        res = 0;
        # Number of inputs is lower than number of LUT inputs, just return 1
        if i <= self._LUTInputs:
            res = 1;
        # Else compute simple tree implementation
        else:
            # While number of current level inputs is bigger than number of LUT
            # inputs create new layer of luts
            while i > self._LUTInputs:
                # Perform eventual rounds for border LUTs of current level
                if i/self._LUTInputs == round(i/self._LUTInputs):
                    res = res + int(round((i / self._LUTInputs), 0))
                    i = int(round((i / self._LUTInputs), 0))
                else:
                    res = res + int(round((i / self._LUTInputs) + 0.5, 0))
                    i = int(round((i / self._LUTInputs) + 0.5, 0))
            # Add final level LUT
            res = res + 1;
            
        # Return number of LUTs
        return res
