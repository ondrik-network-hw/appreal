###############################################################################
#  b_nfa.py: Module for PATTERN MATCH - base NFA implementation
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

import nfa_data
import b_automaton 
import b_state
import copy
import math


class b_nfa(b_automaton.b_Automaton):
    """ 
        A base class for NFA automata.
    """
    def __init__(self):
        """
            Object constructor.
        """
        b_automaton.b_Automaton.__init__(self)
        
    def report_memory_optimal(self):
        """
            Report consumed memory in bytes. Optimal mapping algorithm is used \
            (with oracle). Basic algorithm for this variant of mapping is:     \
            M = \|transitions\| * ceil(log(\|states\|, 2)+1 / 8)
            
            :returns: Returns number of bytes.
            :rtype: int
        """
        tr_len = len(self._automaton.transitions)
        st_len = len(self._automaton.states)
        return int(tr_len * math.ceil(math.log(st_len, 2)+1 / 8));
    
    def report_memory_naive(self):
        """
            Report consumed memory in bytes. Naive mapping algorithm is used \
            (2D array). Basic algorithm for this variant of mapping is:      \
            M = \|states\| * \|alphabet\| * ceil(log(\|states\| + 1, 2) / 8) \
             + cnt * ceil(log(\|states\| + 1, 2) / 8) where cnt is number of \
             nondeterministic transitions.
            
            :returns: Returns number of bytes.
            :rtype: int
        """
        st_len = len(self._automaton.states)
        al_len = len(self._automaton.alphabet)
        
        mapper = dict()
        for state in self._automaton.states:
            mapper[state] = dict()
        for transition in self._automaton.transitions:
            if mapper[transition[0]].has_key(transition[1]) == True:
                mapper[transition[0]][transition[1]].add(transition[2])
            else:
                mapper[transition[0]][transition[1]] = set()
                mapper[transition[0]][transition[1]].add(transition[2])
        cnt = 0
        for state in mapper:
            for symbol in mapper[state].keys():
                if len(mapper[state][symbol]) > 1:
                    cnt +=  len(mapper[state][symbol])
                    
        cell = (math.ceil(math.log(st_len + 1, 2)+ 1 / 8))
        
        return int(st_len * al_len * cell + cnt * cell);
 
    # The class will contain optimisitions of NFA. One method = one
    # optimisation

###############################################################################
# End of File b_nfa.py                                                        #
###############################################################################