###############################################################################
#  sindhu_prasana_nfa.py: Module for PATTERN MATCH
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

# Import general modules
import copy
import re
# Import Netbench modules
from netbench.pattern_match import nfa_data
from netbench.pattern_match import nfa_reductions 
from netbench.pattern_match import b_nfa 
from netbench.pattern_match import b_state
from netbench.pattern_match import sym_char_class
from netbench.pattern_match import sym_char
from netbench.pattern_match import b_symbol
from netbench.pattern_match.pattern_exceptions import COMPUTE_ERROR
from netbench.pattern_match.pattern_exceptions import empty_automaton_exception
from netbench.pattern_match.pattern_exceptions import not_strided_exception
from netbench.pattern_match import aux_func

class sindhu_prasana_nfa(nfa_reductions.nfa_reductions):
    """
        Implementation of NFA in FPGA acording:
        Reetinder Sidhu and Viktor K. Prasana: Fast Regular Expression Matching\
        using FPGAs, In Proceedings of the 9. Annual IEEE Symposium on         \
        Field-Programmable Custom Computing Machines (FCCM'01), 2001.
        
        Generated VHDL code depends on those modules: value_decoder.vhd,       \
        state.vhd and final_bitmap.vhd. Those modules are located in directory \
        templates/vhdl.
        
        Supported symbols for this algorithm are sym_char and sym_kchar if     \
        stride parameter is bigger than 1. When strided automaton is used, char\
        classes are used as char class removal for strided nfa generate very   \
        huge automata.
        
        Experimantal extension for strided symbols added.
        
        :param stride: Number of characters accepted in one clock cycle.       \
                       Defaults to 1 char per CLK.
        :type stride: int
    """
    def __init__(self, stride = 1):
        """ 
            Class constructor.
        
            Experimantal extension for strided symbols added.
            
            :param stride: Number of characters accepted in one clock cycle.   \
                           Defaults to 1 char per CLK. Only powers of 2 are    \
                           supported.
            :type stride: int
        """
        nfa_reductions.nfa_reductions.__init__(self)
        # Set stride specific value
        self.width = 8 * stride
        # Set stride independent values
        self.template = aux_func.getPatternMatchDir() + "/algorithms/sindhu_prasana_nfa/vhdl/sindhu_prasana_nfa.vhd"
        self._statistic = dict()
        self._useBram = False
        self._LUTInputs = 6
        self._luts = 0
        self.stride = stride
        
    def compute(self):
        """
            Compute Sindhu_Prasana automata mapping into FPGA.
        """
        
        # Call parent compute
        nfa_reductions.nfa_reductions.compute(self)
        # Check if parent compute is OK
        if not self.get_compute():
            raise COMPUTE_ERROR
        
        # Check if automaton is loaded into object
        if self._automaton.is_empty() == True:
            raise empty_automaton_exception
        
        # Remove epsilon transitions
        self.remove_epsilons()
        
        # Compute strided automaton
        stride = 1
        while stride < self.stride:
            self.stride_2()
            stride = stride * 2
        
        # Remove char classes if clasic automaton is used
        # For strided automaton char class removal is contraproductive due 
        # * constructions. For example **** 4-strided symbol after char class
        # removal creates 2^32 transitions.
        if self.stride == 1:
            self.remove_char_classes()
        
        # we need to perform the mapping to know number of used FPGA resources
        self.get_HDL()
        # Set compute value to True to indicate that all is computed
        self._compute = True
        
    def  get_HDL(self):
        """
            Return HDL description of NFA unit implemented by Sindhu and       \
            Prasana's approach.
            
            :returns: HDL description of NFA unit implemented by Sindhu and    \
                      Prasana's approach.
            :rtype: string
        """
        # Checks specific for strided automaton
        if self.stride > 1:
            # Check if automaton is strided
            if self._automaton.Flags.has_key("Stride") and self._automaton.Flags["Stride"] > 1:
                self.width = self._automaton.Flags["Stride"] * 8
            else:
                raise not_strided_exception
        
        # Open VHDL template file and load the template
        f = open(self.template, "rb");    #Opens file automat
        blob = f.read()
        tmp = re.split("%\$%", blob)
        
        # Init atributes
        self._luts = 0
        
        # Remove epsilons - TODO: Add check if automaton is epsilon free and 
        # then remove this.
        self.remove_epsilons()
        
        # Get VHDL description of shared character decoder
        chdec = self._get_char_dec_HDL()
        # Get VHDL description of mapped automaton's logic
        logic = self._get_logic_HDL()
        # Get VHDL description of final states
        final = self._get_final_HDL()
        # Concatenate signal description
        dataSignal = chdec[0] + logic[0] + final[0]
        # Concatenate logic description - architecture
        dataImplementation = chdec[1] + logic[1] + final[1]
        
        # Set generated code markers - begin
        textSignal = "-- --------------- GENERATED BY SINDHU_PRASANA_NFA.PY ----------------\n"
        textImplementation = "-- --------------- GENERATED BY SINDHU_PRASANA_NFA.PY ----------------\n"
        
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
            Return HDL description of dedicated char decoders as (signals, description). 
            
            :returns: HDL description of dedicated char decoders as (signals, description).
            :rtype: tuple(list(string),list(string))
        """
        
        # If automaton is strided, generate specific character decoders for 
        # strided automaton
        if self._automaton.Flags.has_key("Stride"):
            # Set width of input
            self.width = self._automaton.Flags["Stride"] * 8
            # List of signal definitions
            signalList = list()
            # list of logic description - architecture
            descriptionList = list()
            # Generate character decoder for all state in transitions
            for transition in self._automaton.transitions:
                # Set of all used characters, every subsymbol is represented by
                # one item.
                allChars = list()
                # Init the list by empty sets
                for i in range(0, self._automaton.Flags["Stride"]):
                    allChars.append(set())
                    
                # populate the allChars set
                for i in range(0, self._automaton.Flags["Stride"]):
                    # Add all chars from char class subsymbol
                    if isinstance(self._automaton.alphabet[transition[1]].kchar[i], frozenset):
                        for char in self._automaton.alphabet[transition[1]].kchar[i]:
                            allChars[i].add(char)
                    # Add char from char symbol
                    else:
                        allChars[i].add(self._automaton.alphabet[transition[1]].kchar[i])
                
                # Crate char decoder VHDL descriptions for all used 
                # subcharacters
                for i in range(0, self._automaton.Flags["Stride"]):
                    # Crate char decoder VHDL description for all used 
                    # subcharacters in current part of strided symbol.
                    # Instantiates the VALUE_DECODER module.
                    for char in allChars[i]:
                        signalList.append("    signal char_" + str(ord(char)) + "_" + str(i)  + "_" + str(transition[0]) + "_" + str(transition[2]) + " : std_logic;\n")
                        chrDec  = "    VD_" + str(ord(char)) + "_" + str(i)  + "_" + str(transition[0]) + "_" + str(transition[2]) + ": entity work.VALUE_DECODER\n" 
                        chrDec += "    generic map(\n"
                        chrDec += "        DATA_WIDTH => " + "8" + ",\n"
                        chrDec += "        VALUE      => " + str(ord(char)) + "\n"
                        chrDec += "    )\n"
                        chrDec += "    port map(\n"
                        chrDec += "        INPUT  => DATA(" + str((i + 1) * 8 - 1)  + " downto " + str(i*8) + "),\n"
                        chrDec += "        OUTPUT => char_" + str(ord(char)) + "_" + str(i)  + "_" + str(transition[0]) + "_" + str(transition[2]) + "\n"
                        chrDec += "    );\n\n"
                        descriptionList.append(chrDec)
                        # Update number of used LUTs
                        self._luts += self._countLUTsForInpunts(8)
                        
                # Create list of char classes for all subchars of kchar   
                allCharClasses = list()
                # Dict of char classes
                classDict      = list()
                # Init those structures
                for i in range(0, self._automaton.Flags["Stride"]):
                    allCharClasses.append(set())
                    classDict.append(dict())
                
                # Populate allCharClasses list
                for i in range(0, self._automaton.Flags["Stride"]):
                    if isinstance(self._automaton.alphabet[transition[1]].kchar[i], frozenset):
                        allCharClasses[i].add(self._automaton.alphabet[transition[1]].kchar[i])
                
                # For all subsymbols create interconection
                # Create shared char classes        
                for i in range(0, self._automaton.Flags["Stride"]):           
                    index = 0
                    for cls in allCharClasses[i]:
                        # Populate allCharClasses list
                        classDict[i][cls] = index
                        # Create signal definition
                        signalList.append("    signal class_" + str(index) + "_" + str(i) + "_" + str(transition[0]) + "_" + str(transition[2]) + " : std_logic;\n")
                        # Create code start for current char class
                        text = "    class_" + str(index) + "_" + str(i) + "_" + str(transition[0]) + "_" + str(transition[2]) + " <= "
                        first = True
                        # Populate allCharClasses list
                        self._luts += self._countLUTsForInpunts(len(cls))
                        # Create code
                        for char in cls:
                            if first == True:
                                text += "char_" + str(ord(char)) + "_" + str(i) + "_" + str(transition[0]) + "_" + str(transition[2]) 
                                first = False
                            else:
                                text += " or char_" + str(ord(char)) + "_" + str(i) + "_" + str(transition[0]) + "_" + str(transition[2]) 
                        text += ";\n"
                        # Create code
                        descriptionList.append(text)
                        # Update current class index by 1
                        index += 1
                        
                # Create signal definition for whole kchar
                signalList.append("    signal symbol_" + str(transition[1]) + "_" + str(transition[0]) + "_" + str(transition[2]) + " : std_logic;\n")
                # Create definitions and descriptions for subsymbols
                for i in range(0, self._automaton.Flags["Stride"]):
                    # Create signal definition for subsymbol
                    signalList.append("    signal symbol_" + str(transition[1]) + "_" + str(i) + "_" + str(transition[0]) + "_" + str(transition[2]) + " : std_logic;\n")
                    
                    # If subsymbol is char class cretate interconection to 
                    # this charclass
                    if isinstance(self._automaton.alphabet[transition[1]].kchar[i], frozenset):
                        descriptionList.append("    symbol_" + str(transition[1]) + "_" + str(i) + "_" + str(transition[0]) + "_" + str(transition[2]) + " <= class_" + str(classDict[i][self._automaton.alphabet[transition[1]].kchar[i]]) + "_" + str(i) + "_" + str(transition[0]) + "_" + str(transition[2]) + ";\n")
                    # Update current class index by 1
                    else:
                        descriptionList.append("    symbol_" + str(transition[1]) + "_" + str(i) + "_" + str(transition[0]) + "_" + str(transition[2]) + " <= char_" + str(ord(self._automaton.alphabet[transition[1]].kchar[i])) + "_" + str(i) + "_" + str(transition[0]) + "_" + str(transition[2]) + ";\n")
                # Create interconection between subsymbols and whole kchars
                # - description part        
                text = "    symbol_" + str(transition[1]) + "_" + str(transition[0]) + "_" + str(transition[2]) + " <= "
                first = True
                # Update current class index by 1
                self._luts += self._countLUTsForInpunts(self._automaton.Flags["Stride"])
                # Create 'or' code
                for i in range(0, self._automaton.Flags["Stride"]):
                    if first == True:
                        text += "symbol_" + str(transition[1]) + "_" + str(i) + "_" + str(transition[0]) + "_" + str(transition[2])
                        first = False
                    else:
                        text += " and symbol_" + str(transition[1]) + "_" + str(i) + "_" + str(transition[0]) + "_" + str(transition[2])
                text += ";\n"
                # Update current class index by 1
                descriptionList.append(text)
            # Return generated signal and description list     
            return (signalList, descriptionList)
        # Shared character decoders for clasic automaton
        else:
            # Set of all used characters - used to create the shared
            # character decoders
            allChars = set()
            # Detect if char classes are present.
            have_class = False
            for symbol in self._automaton.alphabet.keys():
                if self._automaton.alphabet[symbol].get_type() == b_symbol.io_mapper["b_Sym_char_class"]:
                    for char in self._automaton.alphabet[symbol].charClass:
                        have_class = True
            # Remove char classes if needed
            if have_class == True:
                self.remove_char_classes()
            
            # List of signal definitions
            signalList = list()
            # list of logic description - architecture
            descriptionList = list()
            
            # Crate char decoder VHDL description for all used characters
            # Instantiates the VALUE_DECODER module.
            for transition in self._automaton.transitions:
                # Char from symbol
                char = self._automaton.alphabet[transition[1]].char
                # Add signal definition into signalList
                signalList.append("    signal symbol_" + str(transition[1]) + "_" + str(transition[0]) + "_" + str(transition[2]) + " : std_logic;\n")
                # Create VHDL code
                chrDec  = "    VD_" + str(transition[1]) + "_" + str(transition[0]) + "_" + str(transition[2]) + ": entity work.VALUE_DECODER\n" 
                chrDec += "    generic map(\n"
                chrDec += "        DATA_WIDTH => " + str(self.width) + ",\n"
                chrDec += "        VALUE      => " + str(ord(char)) + "\n"
                chrDec += "    )\n"
                chrDec += "    port map(\n"
                chrDec += "        INPUT  => DATA,\n"
                chrDec += "        OUTPUT => symbol_" + str(transition[1]) + "_" + str(transition[0]) + "_" + str(transition[2]) + "\n"
                chrDec += "    );\n\n"
                # Add generated code to descriptionList - architecture
                descriptionList.append(chrDec)
                # Update number of used LUTs
                self._luts += self._countLUTsForInpunts(self.width) 
                
            # Return generated signal and description list         
            return (signalList, descriptionList)
                
    def _get_logic_HDL(self):
        """ 
            Return HDL description of states and transitions as                \
            (signals, description). 
            
            :returns: HDL description of states and transitions as             \
                     (signals, description).
            :rtype: tuple(list(string),list(string)) 
        """
        # List of signal definitions
        signalList = list()
        # list of logic description - architecture
        descriptionList = list()
        
         # For all states generate state modules
        for state in self._automaton.states.keys():
            # Define signals for current state
            signalList.append("    signal state_in_" + str(state) + " : std_logic;\n")
            signalList.append("    signal state_out_" + str(state) + " : std_logic;\n")
            # If state is start state of automaton, set generic DEFAULT to '1'
            if state == self._automaton.start:
                text  =  "    STATE_" + str(state) + ": entity work.STATE\n"
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
            # Otherwise set generic DEFAULT to '0' for any other state
            else:
                text  =  "    STATE_" + str(state) + ": entity work.STATE\n"
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
        
        # Generate interconection between states and between character decoders
        # and states                        
        for state in inputTransitions.keys():
            # If only 1 input transition is present just add previous state 
            # output and character decoder output
            if len(inputTransitions[state]) == 1:
                data = inputTransitions[state].pop()
                # Add code to decription list
                descriptionList.append("    state_in_" + str(state) + " <= state_out_" + str(data[0]) + " and symbol_" + str(data[1]) + "_" + str(data[0]) + "_" + str(state) + ";\n")
                # Update number of used LUTs
                self._luts += self._countLUTsForInpunts(2)
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
                        text += "    state_in_" + str(state) + " <= (state_out_" + str(transition[0]) + " and symbol_" + str(transition[1]) + "_" + str(transition[0]) + "_" + str(state) + ")"
                        first = False
                    else:
                        text += " or (state_out_" + str(transition[0]) + " and symbol_" + str(transition[1]) + "_" + str(transition[0]) + "_" + str(state) + ")"
                text += ";\n"
                # Add code to decription list
                descriptionList.append(text)
        # Return generated signal and description list         
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
            # Add signal to list of signals
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
            
            :returns: Amount of logic consumed by the algorithm                \
                      (LUTs, FlipFlops, BRAMs)
            :rtype: tuple(int, int, int)
        """
        # If number of LUTs is equal to zero call get_HDL() method to perform 
        # the mapping and to compute number of used LUTs
        if self._luts == 0:
            self.get_HDL()
            
        # Number of used FFs is equivalent to number of states and size of 
        # final_bitmap unit
        ffSize = len(self._automaton.states) + self._fStateNum + 1
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

