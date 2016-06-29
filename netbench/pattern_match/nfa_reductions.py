###############################################################################
#  nfa_reductions.py: Module for PATTERN MATCH - nfa reductions
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

import nfa_data
import b_nfa
import b_state
import copy
from b_nfa import b_nfa
import sym_char
import sym_char_class
import sym_kchar
import b_symbol
import random

class nfa_reductions(b_nfa):
    """ 
        Class for NFA reductions.
    """
    def __init__(self):
        """ 
            Constructor - inits object atributes:
        """
        b_nfa.__init__(self)
       
    def share_prefixes(self):
        """ 
            This method reduce states of NFA by prefix sharing. Only static prefixes are shared.
            
            This method sets _compute to False, and get_compute() will return False until compute() is called.
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

        stack = list()
        stack.append(self._automaton.start)

        while len(stack) > 0:
            state = stack.pop()
            join_states_list = list()
            join_symbol_list = list()
            #join_states_star_list = list()
            for symbol in mapper[state]:
                join_states = set()
                #join_states_star = set()
                #for tstate in mapper[state][symbol]:
                #    pass
                for tstate in mapper[state][symbol]:
                    if len(reverse_mapper[tstate][symbol]) == 1:
                        join_states.add(tstate)
                if len(join_states) > 1:
                    join_states_list.append(join_states)
                    join_symbol_list.append(symbol)
            for i in range(0, len(join_states_list)):
                fstate = join_states_list[i].pop()
                for rstate in join_states_list[i]:
                    # remove from final
                    if rstate in self._automaton.final:
                        self._automaton.final.remove(rstate)
                        self._automaton.final.add(fstate)
                        new_exp = self._automaton.states[fstate].get_regexp_number()
                        new_exp |= self._automaton.states[rstate].get_regexp_number()
                        self._automaton.states[fstate].set_regexp_number(new_exp)
                    # remove from states
                    del self._automaton.states[rstate]
                    # update mapper
                    for symbol in mapper[rstate]:
                        if mapper[fstate].has_key(symbol):
                            mapper[fstate][symbol] |=  mapper[rstate][symbol] - set([rstate])
                        else:
                            mapper[fstate][symbol] =  mapper[rstate][symbol] - set([rstate])
                    # update reverse_mapper
                    for symbol in mapper[rstate]:
                        for tstate in mapper[rstate][symbol]:
                            reverse_mapper[tstate][symbol].add(fstate)
                            reverse_mapper[tstate][symbol].remove(rstate)
                            # update transitions
                            # from rstate to tstate
                            self._automaton.transitions.remove((rstate, symbol, tstate))
                            self._automaton.transitions.add((fstate, symbol, tstate))

                    for sym in reverse_mapper[rstate]:
                        for tst in reverse_mapper[rstate][sym]:
                            self._automaton.transitions.remove((tst, sym, rstate))
                    
                    # remove from mappers
                    del reverse_mapper[rstate]
                    for symbol in mapper[state]:
                        #print "Zpracovavam " + str(symbol)
                        if rstate in mapper[state][symbol]:
                            mapper[state][symbol].remove(rstate)
                            #print "Mazu " + str(symbol)
                    # update transitions
                    # from state to rstate
                    self._automaton.transitions.discard((state, join_symbol_list[i], rstate))
                stack.append(fstate)
        self._compute = False
        
