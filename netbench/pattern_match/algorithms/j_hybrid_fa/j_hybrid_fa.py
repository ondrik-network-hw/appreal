############################################################################
#  j_hybrid_fa.py: Module for PATTERN MATCH algorithm Hybrid Finite Automat
#  Copyright (C) 2012 Brno University of Technology, ANT @ FIT
#  Author(s): Milan Pala, <xpalam00@stud.fit.vutbr.cz>
#             Jaroslav Suchodol, <xsucho04@stud.fit.vutbr.cz>
############################################################################
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
#  This software or firmware is provided ``as is'', and any express or
#  implied warranties, including, but not limited to, the implied warranties
#  of merchantability and fitness for a particular purpose are disclaimed.
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

"""Module for pattern match: algorithm for Hybrid Finite Automat."""

from netbench.pattern_match import sym_char
from netbench.pattern_match.nfa_parser import nfa_parser
from netbench.pattern_match.b_dfa import b_dfa
from netbench.pattern_match.b_nfa import b_nfa
from netbench.pattern_match.nfa_data import nfa_data
from netbench.pattern_match.b_automaton import b_Automaton
from netbench.pattern_match.pattern_exceptions import empty_automaton_exception
from netbench.pattern_match.pattern_exceptions import general_not_implemented
from netbench.pattern_match.pattern_exceptions import unknown_parser
import os
import re
import math
import sys

class JHybridFA(b_Automaton):
    """
        Class for Hybrid Finite Automat.

        Hybrid automaton is saved in:
         - self.dfa            - Head DFA part of Hybrid FA
         - self.nfas           - Tails NFA parts of Hybrid FA
         - self.tran_aut       - List of border states
                
        Indexes in self.tran_aut reffer to
        self.nfas list for particular NFA tails.
        
        Based on:
            "A hybrid finite automaton for practical deep packet inspection"
            ISBN: 978-1-59593-770-4
            URL: http://portal.acm.org/citation.cfm?id=1364656
        
        Approach split each input regular expression to DFA prefix and
        NFA suffix by blow up pattern. It is the pattern where autmaton
        reachs much more states than before. For example pattern:
        /ab[a-z]*cd/ has blow up pattern [a-z]* and it will be split into
        /ab/ pattern to DFA part and /[a-z]*.cd/ pattern to be set into
        NFA tail.
        DFA part is determinised as usual and than are joined NFA tails.
        
        Approach works with input text file and split input patterns - not
        input NFA.
        This idea comes from Jaroslav Suchodol <xsucho04@stud.fit.vutbr.cz>
    """

    def __init__(self):
        """
            Constructor - inits object atributes:
            dfa            - Head DFA part of Hybrid FA
            nfas           - Tails NFA parts of Hybrid FA
            tran_aut       - List of border states
            
            Index in self.tran_aut reffer to
            self.nfas list for particular NFA tails.
        """
        b_Automaton.__init__(self)
        self.dfa = b_dfa()
        self.nfas = dict()
        self.tran_aut = dict()

        self._patterns = [] # compiled pattern to finding blow up

        self._nfaEpsFree = b_nfa()
        
        self._init_blowup_expresion()

    def create_by_parser(self, parser):
        """
            This function is used to create automaton from set of regular expressions.

            This method is forbidden because approach work with input text file. \
            Set parser instance by set_parser() method and input file with \
            regular expressions by load_file().

            :param nfa_parser_class: An instation of nfa_parser class.
            :type nfa_parser_class: nfa_parser
            :returns: False if creation of automaton failed or True if creation was successful.
            :rtype: boolean

            This method sets _compute to False, and get_compute() will return False until compute() is called.
            
            :raises: general_not_implemented()
        """
        raise general_not_implemented("Use set_parser() instead or see example_of_use.py.")
        
    def create_from_nfa_data(self):
        """
            Create automaton from nfa_data object.

            This method is forbidden because approach work with input text file. \
            Set parser instance by set_parser() method and input file with \
            regular expressions by load_file().

            :param nfa: nfa_data object, from which automaton is created.
            :type nfa: nfa_data
            :param safe: If True perform deep copy, otherwise set reference. Default value is True.
            :type safe: boolean

            This method sets _compute to False, and get_compute() will return False until compute() is called.
            
            :raises: general_not_implemented()
        """
        raise general_not_implemented("Use set_parser() instead or see example_of_use.py.")
    
    def load_file(self, file_name):
        """
            Set path to file with regular expression.
            
            :param file_name: Path to file with regular expression
            :type file_name: string
        """
        self._file_name = file_name
    
    def set_parser(self, parser_instance):
        """
            Set parser instance to be used in approach.
            
            :param parser_instance: Parser instance to be used in approach.
            :type parser_instance: nfa_parser
        """
        if(not isinstance(parser_instance, nfa_parser)):
            raise unknown_parser(parser_instance)
        else:
            self._parser = parser_instance

    def _init_blowup_expresion(self):
        """
            Compile patterns of blow up patterns in input regular expression.
            To add new blow up pattern, create new RE bellow and add to
            list of blow up patterns.
        """
        # dot star
        pattern_dotstar = re.compile(r"""
            \.\*     
        """, re.X)
        # dot counting constrain
        pattern_dotcc = re.compile(r"""
            \.\{[0-9,]+\}
        """, re.X)
        # char class  counting constrain
        pattern_charclasscc = re.compile(r"""
            (?<!\\)\[[^\]]+]\{[0-9,]+\}     
        """, re.X)
        # char class star
        pattern_charclassstar = re.compile(r"""
            (?<!\\)\[[^\]]+]\*     
        """, re.X)
        
        self._patterns.append(pattern_dotstar)
        self._patterns.append(pattern_dotcc)
        self._patterns.append(pattern_charclasscc)
        self._patterns.append(pattern_charclassstar)    

    def _find_first_occurence_of_blowup(self, expression):
        """
            Find first occurence of blow up pattern in RE and return it.
            
            :returns: Position of occurence.
            :rtype: int
        """
        first_occurence = None
        for pattern in self._patterns:
            ser = re.finditer(pattern, expression)
            for m in ser:
                if first_occurence is None or first_occurence > m.start():
                    first_occurence = m.start()
        return first_occurence

    def _split_expresion(self, expression):
        """
            Split each expression in safe DFA part and NFA part.
            
            :rtype: tupple
        """
        ocurrence = self._find_first_occurence_of_blowup(expression)
        
        if ocurrence is None: # RE does not have blow up pattern
            return (expression, "")
        elif ocurrence is 1: # blow up is on start of RE
            return ("", expression)
        else: # spli RE into two parts
            a = expression[0:ocurrence]
            a += expression[expression.rindex("/"):len(expression)]
            
            b = "/"
            b += expression[ocurrence:len(expression)]
            
            return (a,b)

    def compute(self):
        """
            Computes Hybrid automaton.
        """
        b_Automaton.compute(self)
        self._compute = False

        # save input NFA automaton
        self._nfaEpsFree = b_nfa()
        parserInstance = self._parser
        parserInstance.load_file(self._file_name)
        self._nfaEpsFree.create_by_parser(parserInstance)
        self._nfaEpsFree.remove_epsilons()

        fr = open(self._file_name, "r")
        
        # split input REs into DFA and NFA parts
        # RE can have blow up on start, then is not DFA part
        # RE can have not blow up, then is not NFA part
        dfa_patterns = "" # dfa patterns are set into parser
        nfa_patterns = [] # each nfa pattern is set to parser
        # create mapping beetween number of input RE and number of
        # RE in DFA patterns and NFA patterns
        re_to_nfa = dict()
        re_to_dfa = dict()
        nfa_to_re = dict()
        dfa_to_re = dict()
        nfa_i = 0
        dfa_i = 0
        i = 0
        for line in fr.readlines():
            (a, b) = self._split_expresion(line.rstrip("\n"))
            if a is not "":
                re_to_dfa[i] = dfa_i
                dfa_to_re[dfa_i] = i
                dfa_i+=1
                dfa_patterns += a+"\n"
            if b is not "":
                nfa_patterns.append(b)
                re_to_nfa[i] = nfa_i
                nfa_to_re[nfa_i] = i
                nfa_i+=1
            i+=1
        dfa_patterns = dfa_patterns[:-1] # delete last new line
        
        # compute DFA head part
        self.dfa = b_dfa()
        self.dfa.set_multilanguage(self.get_multilanguage())
        parserInstance = self._parser
        parserInstance.set_text(dfa_patterns)
        self.dfa.create_by_parser(parserInstance)
        self.dfa.compute()
        self.dfa.get_automaton(False).Flags["Hybrid FA - DFA part"] = True

        # compute NFA tails
        for key in range(0, len(nfa_patterns)):
            nfa = b_nfa()
            parserInstance = self._parser
            parserInstance.set_text(nfa_patterns[key])
            nfa.create_by_parser(parserInstance)
            nfa.remove_epsilons()
            nfa.compute()
            nfa.get_automaton(False).Flags["Hybrid FA - one NFA part"] = True
            # update RE number in finals states
            for state in nfa.get_automaton(False).states:
                if nfa.get_automaton(False).states[state].is_final():
                    new_regexp_number = set()
                    new_regexp_number.add(nfa_to_re[key])
                    nfa.get_automaton(False).states[state].set_regexp_number(new_regexp_number)
            self.nfas[len(self.nfas)] = nfa
            
        # update RE number in finals states or map border state to NFA
        for state in self.dfa.get_automaton().states:
            if self.dfa.get_automaton().states[state].is_final() == True:
                new_regexp_numbers = set()
                for re_number in self.dfa.get_automaton(False).states[state].get_regexp_number():
                    if re_to_nfa.has_key(dfa_to_re[re_number]):
                        self.tran_aut[re_to_nfa[dfa_to_re[re_number]]] = state
                    else:
                        new_regexp_numbers.add(dfa_to_re[re_number])
                self.dfa.get_automaton(False).states[state].set_regexp_number(new_regexp_numbers)

        # add RE having blow up pattern on start
        new_tran_aut = dict()
        for nfa in nfa_to_re:
            if self.tran_aut.has_key(nfa) is False:
                new_tran_aut[nfa] = self.dfa.get_automaton(False).start
            else:
                new_tran_aut[nfa] = self.tran_aut[nfa]
        self.tran_aut = new_tran_aut

        self._compute = True

    def search(self, input_string):
        """
            Function will find patterns in the given string.

            :param input_string: Input string.
            :param input_string: string
            :returns: Bitmap of matched regular expressions.
            :rtype: list(int)
        """
        # Create mapping between reg. exp. number and coresponding final states.
        sameFinal = dict()
        for fstate in self._nfaEpsFree._automaton.final:
            rnums = self._nfaEpsFree._automaton.states[fstate].get_regexp_number()
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
        self._bitmap = [0] * rules

        self._search(self.dfa, input_string)
        
        return self._bitmap

    def _search(self, nfa, input_string, in_dfa = True):
        """
            Function will find patterns in the given string in given automaton.
        """
        # Stack of states. State is list (tupple) consisting of state and unprocessed part of input string.
        Stack = list()
        # Set of actual states.
        ActState = set()

        # Create start state.
        ActState.add((nfa._automaton.start, input_string))
        # Add start state to stack.0
        Stack.append(ActState)

        borders = dict()
        for i in range(0, len(self.tran_aut)):
            borders.setdefault(self.tran_aut[i], set()).add(i)

        # If needed create mapping between states and outgoing transitions.
        _mapper = dict()
        for transition in nfa._automaton.transitions:
            if _mapper.has_key(transition[0]) == True:
                _mapper[transition[0]].add((transition[1], transition[2]))
            else:
                _mapper[transition[0]] = set()
                _mapper[transition[0]].add((transition[1], transition[2]))

        # Until stack is empty, search
        while len(Stack) != 0:
            # Pop state from stack.
            ActState = Stack.pop()
            newActState = set()
            # Create new state. Accept char if possible and add state to new state.
            for state in ActState:
                if _mapper.has_key(state[0]):
                    for transition in _mapper[state[0]]:
                        try:
                            res = nfa._automaton.alphabet[transition[0]].accept(state[1])
                        except:
                            pass
                        else:
                            newActState.add((transition[1],res))
                # If in final state, set coresponding bitmap field to 1.
                if nfa._automaton.states[state[0]].is_final() == True:
                    for rnum in nfa._automaton.states[state[0]].get_regexp_number():
                        self._bitmap[rnum] = 1
                # Try to find in NFA tail if current state is a border one
                if in_dfa is True and borders.has_key(state[0]):
                    for nfaIndex in borders[state[0]]:
                        self._search(self.nfas[nfaIndex], state[1], False)
            # If possible add new state to stack.
            if len(newActState) > 0:
                Stack.append(newActState)

    def report_memory_naive(self):
        """
            Report consumed memory in bytes. Read documentaion in b_dfa
            and b_nfa methods for more information.
            
            :returns: Returns number of bytes.
            :rtype: int
        """
        size = self.dfa.report_memory_naive()
        for i in range(0, len(self.nfas)):
            size += self.nfas[i].report_memory_naive()
        size += len(self.nfas)*math.ceil(math.log(sys.maxint)/8)
        return int(size)
        
    def report_memory_optimal(self):
        """
            Report consumed memory in bytes. Read documentaion in b_dfa
            and b_nfa methods for more information.
            
            :returns: Returns number of bytes.
            :rtype: int
        """
        size = self.dfa.report_memory_optimal()
        for i in range(0, len(self.nfas)):
            size += self.nfas[i].report_memory_optimal()
        size += len(self.nfas)*math.ceil(math.log(sys.maxint)/8)
        return int(size)

    def get_automaton(self):
        """
            DFA head of automaton is save in self.dfa, NFA tails are in self.nfas.
            Read instruction in __init__ method.
            
            :raises: empty_automaton_exception()
        """
        raise empty_automaton_exception()

    def show(self, file_name):
        """
            Print states, alphabet, start, transitions, final, Flags of DFA
            part and NFA parts. And save graphviz dot file, representing
            graphical structure of nfa_data.

            :param file_name: Name of output DOT file
            :type file_name: string
        """

    # Display DFA part.
        print '*' * 80
        print "*** HYBRID FA - DFA part ***"
        print "STATES:", self.dfa.get_automaton(False).states, '\n'
        print "ALPHABET:", self.dfa.get_automaton(False).alphabet, '\n'
        print "START STATE:", self.dfa.get_automaton(False).start, '\n'
        print "TRANSITIONS:", self.dfa.get_automaton(False).transitions, '\n'
        print "FINAL STATES:", self.dfa.get_automaton(False).final, '\n'
        print "FLAGS OF AUTOMAT:", self.dfa.get_automaton(False).Flags
        print '*' * 80, '\n'
        self.dfa._automaton.show(os.path.splitext(file_name)[0] + "_DFA" + os.path.splitext(file_name)[1])
    # Display NFA parts.
        for i in range(0, len(self.nfas)):
            print '*' * 80
            print "*** HYBRID FA - NFA part which joining to",
            print "STATES:", self.nfas[i].get_automaton(False).states, '\n'
            print "ALPHABET:", self.nfas[i].get_automaton(False).alphabet, '\n'
            print "START STATE:", self.nfas[i].get_automaton(False).start, '\n'
            print "TRANSITIONS:", self.nfas[i].get_automaton(False).transitions, '\n'
            print "FINAL STATES:", self.nfas[i].get_automaton(False).final, '\n'
            print "FLAGS OF AUTOMAT:", self.nfas[i].get_automaton(False).Flags
            print '*' * 80, '\n'
            self.nfas[i]._automaton.show(os.path.splitext(file_name)[0] + "_NFA_" + str(i) + os.path.splitext(file_name)[1])

    def save_to_file(self, file_name):
        """
            DFA head of automaton is save in self.dfa, NFA tails are in self.nfas.
            Read instruction in __init__ method.
            
            :raises: empty_automaton_exception()
        """
        raise empty_automaton_exception()

    def get_state_num(self):
        """
            Return number of states in Hybrid automaton.

            :returns: Number of states in Hybrid automaton
            :rtype: int
        """

        number_states = 0
        for i in range(0, len(self.nfas)):
            number_states += len(self.nfas[i].get_automaton(False).states)
        number_states += len(self.dfa.get_automaton(False).states)
        return number_states

    def get_trans_num(self):
        """
            Return number of transitions in Hybrid automaton.

            :returns: Number of transitions in Hybrid automaton
            :rtype: int
        """

        number_tran = 0
        for i in range(0, len(self.nfas)):
            number_tran += len(self.nfas[i].get_automaton(False).transitions)
        number_tran += len(self.dfa.get_automaton(False).transitions)
        return number_tran
