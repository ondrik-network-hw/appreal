###############################################################################
#  phf_dfa.py: Module for DFA with PHF
#  Copyright (C) 2010 Brno University of Technology, ANT @ FIT
#  Author(s): Jan Kastil <ikastil@fit.vutbr.cz> 
#             Milan Dvorak <xdvora66@stud.fit.vutbr.cz>
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

import math
import sys
import copy
# Import Netbench modules
from netbench.pattern_match import sym_char, sym_char_class
from netbench.pattern_match.b_dfa import b_dfa
from netbench.pattern_match.bin.library.b_hash import *
from netbench.pattern_match.bin.library.bdz import bdz
from netbench.pattern_match.bin.library.jenkins import *
from netbench.pattern_match.pattern_exceptions import *
# Import bitstring module
from netbench.pattern_match.bin.library.bitstring import BitStream, BitArray

BUFF_SIZE = 10000 # size of buffer in search method

class PHF_DFA(b_dfa):
    """ 
        Class for the DFA based on perfect hashing. Extension with faulty     \
        transition table is also implemented. To enable this extension, use   \
        method enable_faulty_transitions.

        Based on:
            Kastil, J., Korenek, J., Lengal, O.: Methodology for Fast Pattern \
            Matching by Deterministic Finite Automaton with Perfect Hashing,  \
            In: 12th EUROMICRO Conference on Digital System Design DSD 2009,  \
            Patras, GR, IEEE CS, 2009, p. 823-289, ISBN 978-0-7695-3782-5
            URL: http://www.fit.vutbr.cz/research/view_pub.php?id=9054

            Kastil, J., Korenek, J.: High Speed Pattern Matching Algorithm    \
            Based on Deterministic Finite Automata with Faulty Transition     \
            Table, In: Proceedings of the 6th ACM/IEEE Symposium on           \
            Architectures for Networking and Communications Systems, La Jolla,\
            US, ACM, 2010, p. 2, ISBN 978-1-4503-0379-8
            URL: http://www.fit.vutbr.cz/research/view_pub.php?id=9380

        This class uses bitstring module:                                     \
            http://code.google.com/p/python-bitstring/
    """

    def __init__(self):
        """
            Constructor - initialization of object attributes.
        """
        b_dfa.__init__(self)

        self._automaton1 = self._automaton # copy of nfa_data, see enable_fallback_state
       
        self.state_bits = 10   # number of bits for state representation
        self.symbol_bits = 12  # number of bits for symbol representation

        self.hash_function = None # PHF hash function
        self.trans_table = None # PHF table
        self.ran = 0 # number of lines in PHF table

        self.fallback = False # enables/disables fallback state - used, when no transition could be made. False means that search stops
        self.fallback_state = -1 # id of fallback state, -1 means that state with most incoming transitons will be chosen
        self.faulty = False # enables/disables faulty transitions
        self.check_faulty = False # experimental - check if generated PHF is non faulty
        self.compress_hash = None # hash function for transitions keys compression
        self.compress_bits = 0 # output size of compress_hash function
        self.bad_transitions = 0 # bad transitions counter
        self.collisions = dict() # transitions for which the collision occured

    def compute(self):
        """
            This method computes DFA with Perfect hashing.

            Note that PHF table generation may fail, depending on PHF class   \
            parameters (limit, ratio), so _compute may not be set to True.
        """
        # We need deterministic alphabet
        self.resolve_alphabet()
        # Call parrent compute - compute DFA
        b_dfa.compute(self)
        # Check if dfa was computed.
        if not self.get_compute():
            raise COMPUTE_ERROR("b.dfa.compute() failed")
        # copy the nfa_data (see enable_fallback_state)
        self._automaton1 = copy.deepcopy(self._automaton)
        # enable fallback state and remove fallback transitions
        if self.fallback:
            if self.fallback_state == -1:
                self.fallback_state = self._get_frequent_state()
            self.remove_fallback_transitions()
        # Create PHF table
        self._compute = self.generate_PHF_table()

        # Experimental code
        i = 1
        if self.check_faulty:
            while not self._check_faulty_table():
                #print "iterations", i
                i += 1
                self.enable_faulty_transitions(self.compress_bits)
                self.hash_function = None
                self._compute = self.generate_PHF_table()
            print "PHF generated after", i, "iterations."

    def enable_faulty_transitions(self, hash_size, compress_hash=None):
        """
            Enable faulty transition table. Uniform hash function is used to  \
            compress the transition representation. If small hash size is     \
            chosen, collisions and faults in pattern matching may occure. PHF \
            table must be (re)generated after enabling faulty transitions     \
            (method generate_PHF_table() or compute()). This method sets      \
            _compute to False.

            :param hash_size: Size in bits of hash function output.
            :type hash_size: int
            :param compress_hash: Instance of class implementing the compress \
                hash function. In not specified, jenkins_compress class is    \
                created with output size of hash_size.
            :type compress_hash: b_hash
        """
        self.faulty = True
        self._compute = False
        self.compress_bits = hash_size
        if not compress_hash:
            # use default compress hash - jenkins
            a = jenkins_compress(self.compress_bits)
            a.generate_seed()
            self.compress_hash = a
        else:
            # use specified hash function
            self.compress_hash = compress_hash

    def disable_faulty_transitions(self):
        """
            Disable faulty transition table. _compute is set to False.
        """
        self.faulty = False
        self._compute = False

    def enable_faulty_check(self):
        """
            Experimental method - enables generation of nonfaulty table.
        """
        self.check_faulty = True
        self._compute = False

    def _check_faulty_table(self):
        """
            Experimental method - check if PHF table is collision free.
        """
        for state in self._automaton1.states:
            for symbol in self._automaton1.alphabet:
                tran = self._transition_rep((state, symbol))
                self.validate_transition(tran)
                if self.bad_transitions:
                    self.bad_transitions = 0
                    return False
        return True

    def get_table_parameters(self):
        """
            This function returns 2-tuple of integers. First integer is the   \
            number of bit used for the representation of the state. The second\
            integer is a number of bits representing symbol in the transition \
            table. State and symbol together represents the key to the        \
            transition table. 

            :returns: Table parameters - number of bits used for              \
                the representation of state and symbol.
            :rtype: tuple(int, int)
        """
        return (self.state_bits,self.symbol_bits)

    def set_table_parameters(self,bit_nums):
        """
            This function sets the number of bits representing the state and  \
            symbol in the transition table. The parameter is a 2-tuple of     \
            integers. The first one sets the size of the state representation \
            and the second position represents the size of symbol.
            NOTE: number of states/symbols must be less than                  \
            2 ** state_bits/symbol_bits !

            :param bit_nums: Table parameters - number of bits used for the   \
                representation of state and symbol.
            :type bit_nums: tuple(int, int)
        """
        self.state_bits = bit_nums[0]
        self.symbol_bits = bit_nums[1]
        self._compute = False

    def report_memory_real(self):
        """
            Report consumed memory in bytes - the size of PHF table.

            :returns: Size of PHF table in bytes.
            :rtype: int
        """
        if self.faulty:
            # faulty table -> transitions are stored as hash value + next state
            return int(self.ran * math.ceil((2 + self.compress_bits + self.state_bits) / 8.0))
        else:
            # not faulty -> transitions are state + symbol + next state
            return int(self.ran * math.ceil((2 + self.state_bits + self.symbol_bits + self.state_bits) / 8.0))

    def report_memory_optimal(self):
        """
            Report consumed memory in bytes. Optimal mapping algorithm is used \
            (with oracle). Basic algorithm for this variant of mapping is:     \
            M = \|transitions\| * ceil(log(\|states\|, 2) / 8)

            :returns: Returns number of bytes.
            :rtype: int
        """
        tr_len = len(self._automaton1.transitions)
        st_len = len(self._automaton1.states)
        return int(tr_len * math.ceil(math.log(st_len, 2) / 8))

    def report_memory_naive(self):
        """
            Report consumed memory in bytes. Naive mapping algorithm is used \
            (2D array). Basic algorithm for this variant of mapping is:      \
            M = \|states\| * \|alphabet\| * ceil(log(\|states\| + 1, 2) / 8)

            :returns: Returns number of bytes.
            :rtype: int
        """
        st_len = len(self._automaton1.states)
        al_len = len(self._automaton1.alphabet)
        return int(st_len * al_len * math.ceil(math.log(st_len + 1, 2) / 8))

    def get_state_num(self):
        """
            Number of states of nfa_data object
        """
        return len(self._automaton1.states)

    def get_trans_num(self):
        """
            Number of transitions of nfa_data object
        """
        return len(self._automaton1.transitions)

    def get_alpha_num(self):
        """
            Number of symbols in alphabet in nfa_data object
        """
        return len(self._automaton1.alphabet)


    def enable_fallback_state(self, state=-1, warning=True):
        """
            This function sets the fallback state. This requires fully defined\
            automaton! If state is not specified, the one with most incoming  \
            transitions is used. Warning about fully defined automaton is     \
            printed on stdout, unless the parameter warning is set to False.  \
            _compute is set to False.

            :param state: ID of state to be set as fallback state. All        \
                transitions to this state will be removed.
            :type state: int
            :param warning: Disables the printing of warning about need of    \
                fully defined automaton.
            :type warning: boolean
        """
        if warning:
            print "WARNING: setting of fallback state requires fully defined automaton!"
        if state == -1:
            state = self._get_frequent_state()
        self.fallback_state = state
        self.fallback = True
        self._compute = False

    def disable_fallback_state(self):
        """
            Fallback state is disabled. _compute is set to False.
        """
        self.fallback = False
        self.fallback_state = -1
        self._compute = False

    def remove_fallback_transitions(self):
        """
            Remove all transitions to given state in nfa_data _automaton1.    \
            _automaton is unchanged, so dfa algorithms used in compute (like  \
            determinization or minimize) are working. This method should only \
            be called from compute() and it sets _compute to False.

            :param state: ID of the fallback state. All transitions to this   \
                state will be removed.
            :type state: int
        """
        state = self.fallback_state
        if state == -1 or not self.fallback:
            # fallback state disabled
            return

        toRemove = set() # all transitions to fallback state
        for tran in self._automaton1.transitions:
            if tran[2] == state:
                toRemove.add(tran)
        # remove transitions
        for tran in toRemove:
            self._automaton1.transitions.remove(tran)
        self._compute = False

    def _get_frequent_state(self):
        """
            Find state with most incoming transitions. If more states have    \
            same number of incoming transitions, the one with lower ID is     \
            chosen.

            :returns: ID of state with most incoming transitions.
            :rtype: int
        """
        stateTrans = dict() # number of transitions to each state
        for tran in self._automaton1.transitions:
            stateTrans[tran[2]] = stateTrans.get(tran[2], 0) + 1

        # find state with most incoming transitions
        max = 0
        state = -1
        for s, count in stateTrans.iteritems():
            if  count > max:
                state = s
                max = count
            elif count == max and s < state:
                # state with lower ID is preferred
                state = s
        return state

    def _prepare_transitions(self):
        """
            This function is only for intertal use. It creates string         \
            representation for every transition. It uses function             \
            _transition_rep to generate the string representation.
        """
        self._string_transitions = list()
        for x in self._automaton1.transitions:
            self._string_transitions.append(self._transition_rep(x))

    def _transition_rep(self,transition):
        """
            Create string representation for one transition.

            :param transition: Automaton transition.
            :type transition: tuple(b_State, b_Symbol, b_State)
            :returns: Tuple of string representation of given transition.
            :rtype: tuple(string, string)
        """
        data = BitArray(uint=transition[0],length=self.state_bits)
        data1 = BitArray(uint=transition[1],length=self.symbol_bits)
#        trans_rep = data+data1 # !!! changes data1, to not use
        string1 = data.tobytes()
        string2 = data1.tobytes()
        return (string2,string1);

    def set_PHF_class(self, phf_class):
        """
            Set the PHF class for PHF table generation. _compute is set to    \
            False.

            :param phf_class: Class implementing the perfect hash function
            :type phf_class: bdz()
        """
        self.hash_function = phf_class
        self._compute = False

    def generate_PHF_table(self):
        """
            This method generates the PHF table containing the transition table.

            PHF table has 4 columns:
                - 2 bits required by bdz algorithm
                - transition representation (state and symbol)
                    (empty lines contain maximum symbol and state id, computed \
                    from symbol_bits and state_bits)
                - next state
                - compressed value of transition representation (faulty trans)

            :returns: True if table was generated succesfully. False otherwise.
            :rtype: Boolean
        """
        self._prepare_transitions()
        if not self.hash_function:
            a = bdz() # create new PHF
            a.set_iteration_limit(10)
        else:
            a = self.hash_function

        a.set_keys(self._string_transitions)
       
        try: # compute PHF
            if (a.generate_seed() == False):
                return False;
        except NoData,(instance):
            print(instance.message)
            exit()
        
        # Generate transition table
        self.ran = a.get_range()
        # max values of symbol and state id = default (nonexistent) transition in the table
        sym_max = 2 ** self.symbol_bits - 1
        state_max = 2 ** self.state_bits - 1
        # init whole trans (phf) table to default values
        #                   bdz,            transiton,   next state, compressed trans
        self.trans_table = [[3, self._transition_rep([state_max, sym_max, 0]), 0, 0] for i in range(self.ran)]
        for tr in self._automaton1.transitions:
            x = a.hash(self._transition_rep(tr)) # index to table
            g = a.get_g()[x] # g value for bdz algorithm
            tran = self._transition_rep(tr)
            state = tr[2]
            compress = 0
            if self.faulty and self.compress_hash:
                # the compressed value in the last column
                compress = self.compress_hash.hash(tran)
            # stole line in transition table
            self.trans_table[x] = (g,tran,state,compress)
        self.hash_function = a;
        return True

    def decode_symbol(self, input, fromState=-1):
        """
            Compute the symbol accepting the beggining of input string.

            :param input: Input string.
            :type input: string
            :param fromState: The active state of automaton. This would be    \
                required with nondeterministic alphabet (not implemented).
            :type fromState: int
            :returns: ID of found symbol or -1 if no symbol was found and the \
                remainder of input string.
            :rtype: tuple(string, int)
        """
        
        symbols = self._automaton1.alphabet.iterkeys()
        # Get stride length
        stride = 1
        if self.has_flag("Stride"):
            stride = self.get_flag("Stride")

        accepted = 0
        retSym = -1
        for symID in symbols: # check all symbols in alphabet
            sym = self._automaton1.alphabet[symID]
            try:
                res = sym.accept(input) # try to accept symbol
            except:
                pass
            else:
                # symbol was accepted
                if accepted:
                    # not the first accepted symbol
                    print >> sys.stderr, "NONDETERMINISTIC ALPHABET!"
                    pass
                else:
                    retSym = symID
                accepted = 1 # found symbol
                break
        
        if accepted == 0: # symbol was not found
            res = input[stride:] # remove symbol from input string

        return (res, retSym)


    def validate_transition(self, tran):
        """
            Validate given transition. If faulty transitions are enabled,     \
            validation is made based on the compressed value and the result   \
            may be faulty. In that case, counter self.bad_transitions is      \
            incremented and collision is stored in dictionary self.collisions.

            :param tran: Representation of transition to be validated.
            :type tran: tuple(string, string)
            :returns: True if the transition is valid in this automaton.      \
                Otherwise False is returned.
            :rtype: boolean
        """

        index = self.hash_function.hash(tran)
        if index == -1: # nonexistent transition
            # PHF fail
            return False
        if not self.faulty:
            # compare transition representations
            if self.trans_table[self.hash_function.hash(tran)][1] == tran:
                return True
        elif self.compress_hash:
            # check if fault occur
            if (self.trans_table[self.hash_function.hash(tran)][1] == tran) != (self.trans_table[self.hash_function.hash(tran)][3] == self.compress_hash.hash(tran)):
                self.bad_transitions += 1 # collision of compress hash -> bad transition
                self.collisions.setdefault(tran, 0) # store collision for debuging
                self.collisions[tran] += 1
            # validate transition using compressed values
            if self.trans_table[self.hash_function.hash(tran)][3] == self.compress_hash.hash(tran):
                return True # validate OK
        
        return False

    def search(self, input_string):
        """
            Search for the pattern in the given string.

            :param input_string: Input string.
            :param input_string: string
            :returns: Bitmap of matched regular expressions.
            :rtype: list(int)
        """

        # Create mapping between reg. exp. number and coresponding final states.
        sameFinal = dict()
        for fstate in self._automaton1.final:
            rnums = self._automaton1.states[fstate].get_regexp_number()
            for rnum in rnums:
                if sameFinal.has_key(rnum) == True:
                    sameFinal[rnum].add(fstate)
                else:
                    sameFinal[rnum] = set()
                    sameFinal[rnum].add(fstate)

        # Compute number of reg. exp.
        rules = len(sameFinal)
        # dictionary is no longer needed.
        sameFinal = None

        # Init bitmap to zeros.
        bitmap = [0] * rules

        ActiveState = self._automaton1.start
        
        # buffering for speed up with long inputs
        if len(input_string) > 2 * BUFF_SIZE:
            buffer = input_string
            remain = buffer[:2 * BUFF_SIZE]
            buffer = input_string[2 * BUFF_SIZE:]
        else:
            buffer = ""
            remain = input_string

        while(len(remain) >0):
            if buffer and len(remain) < BUFF_SIZE:
                # load more data from buffer
                remain += buffer[:BUFF_SIZE]
                buffer = buffer[BUFF_SIZE:]

            symbolOK = True
            remain, symID = self.decode_symbol(remain, ActiveState)
            if symID == -1:
                symbolOK = False # no suitable symbol
            else:
                tran = self._transition_rep((ActiveState,symID))

            if symbolOK and self.validate_transition(tran):
                # make the transition
                ActiveState = self.trans_table[self.hash_function.hash(tran)][2]
            else:
                # no transition found, use fallback state or end the search
                if self.fallback_state != -1:
                    ActiveState = self.fallback_state
                else:
                    return bitmap

            if self._automaton1.states[ActiveState].is_final() == True:  # input_string accepted
                for rnum in self._automaton1.states[ActiveState].get_regexp_number():
                    bitmap[rnum] = 1

        return bitmap

    def print_conf_file(self, FileName):
        """
            Experimental code, intended only for internal use.
            This function creates text file containing binary representation
            of the transition table.

            :param FileName: The name of output file.
            :type FileName: string
        """
        limit = int(self.hash_function.get_range()/self.hash_function.get_order())
        InFile = open(FileName,"w")
        InFile.write(BitArray(int=self.hash_function.seed["hashes"][0].get_seed(),length=32).bin[2:]+'\n')
        InFile.write(BitArray(int=self.hash_function.seed["hashes"][1].get_seed(),length=32).bin[2:]+'\n')
        InFile.write(BitArray(int=self.hash_function.seed["hashes"][2].get_seed(),length=32).bin[2:]+'\n')
        sym_size = self.symbol_bits
        state_size = self.state_bits
        for index in range(0,self.ran):
            pom = int(index/limit)
            if pom > 2 : continue
            Adr_line = BitArray(uint=int(pom),length=2)+BitArray(uint = (index%limit),length=16)
            Adr_line1 =BitArray(uint=0,length=2) + Adr_line
            Conf_line = BitArray(uint=self.hash_function.get_g()[index],length=2)
            c2 = BitArray(uint=0,length=sym_size+state_size)
            c3 = BitArray(uint=0,length=state_size)
            if self.trans_table[index] != None :
                if self.trans_table[index][0] != 3:
                    c2 = BitArray(bytes=self.trans_table[index][1][0],length=sym_size) + BitArray(bytes=self.trans_table[index][1][1],length=state_size)
                    c3 = BitArray(uint=self.trans_table[index][2],length=state_size)
            Conf_line = Conf_line+c2+c3;
            InFile.write(Adr_line.bin[2:]+'\n')
            InFile.write(Conf_line.bin[2:]+'\n') 
