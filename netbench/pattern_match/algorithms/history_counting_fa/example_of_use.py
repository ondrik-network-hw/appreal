###############################################################################
#  example_of_use.py: Module for PATTERN MATCH - example of use for History 
#                                                Counting FA
#  Copyright (C) 2012 Brno University of Technology, ANT @ FIT
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

"""
    This module demonstrate usage of HistoryCountingFA class.
"""

# Import used Netbench modules
from history_counting_fa import HistoryCountingFA
from netbench.pattern_match.pcre_parser import pcre_parser

# EXAMPLE of use for HistoryCountingFA class
if __name__ == '__main__':
    print("-------------------------------------------------------------------")
    print("             Example of use: History Counting FA                   ")
    print("-------------------------------------------------------------------")
    print(" Ruleset: /ab.{3}cd/                                               ")
    print(" Graphical representation: automaton.dot                           ")
    print("                           history_counting.dot                    ")
    print("-------------------------------------------------------------------")
    
    # Create PCRE parser object and set create PCRE counting constraint symbols
    par = pcre_parser(create_cnt_constr = True)
    # Set the ruleset
    par.set_text("/ab.{3}cd/")
    
    # Create HistoryCountingFA object
    history_counting = HistoryCountingFA()
    # Parse the ruleset
    history_counting.create_by_parser(par)
    # Remove epsilons
    history_counting.remove_epsilons()
    # Get copy of NFA part
    NFA = history_counting.get_automaton(True)
    # Replace counting constraint symbols with .*
    NFA_without_cnt = \
        history_counting._replace_length_restriction_with_a_closure(NFA)
    # Get copy of NFA part
    NFA = history_counting.get_automaton(True)
    # Set the NFA_without_cnt as automaton for the HistoryCountingFA object
    history_counting._automaton = NFA_without_cnt
    # Determinise the automaton with replaced counting constraint symbols.
    # Record corespondance between DFA states and NFA states
    history_counting.determinise(create_table = True)
    # Create the History Counting FA from deterministic automaton with replaced
    # counting constraint symbols and original NFA with  counting constraint 
    # symbols.
    history_counting.compute(NFA)

    #print history_counting.search("ab bccd")
    #print history_counting.search("ab bce c")
    
    # Save graphical representation of automatons
    # Original NFA
    history_counting.show("automaton.dot")
    # History Counting FA
    history_counting._show("history_counting.dot")

    # Report amount of used memory - optimal mapping
    print "Utilized memory (optimal mapping):", history_counting.report_memory_optimal(), "B"
    # Report amount of used memory - array mapping
    print "Utilized memory (array mapping):", history_counting.report_memory_naive(), "B"
    
    # Print number of states and transitions
    print "Number of states:", history_counting.get_state_num()
    print "Number of transitions:", history_counting.get_trans_num()
    
    print("-------------------------------------------------------------------")
