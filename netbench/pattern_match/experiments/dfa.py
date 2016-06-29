###############################################################################
#  dfa.py: Compare several DFA based algorithms
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

from netbench.pattern_match import parser
from netbench.pattern_match.b_dfa import b_dfa
from netbench.pattern_match.algorithms.delay_dfa.ddfa import DELAY_DFA
from netbench.pattern_match.algorithms.history_counting_fa.history_counting_fa import HistoryCountingFA
from netbench.pattern_match.algorithms.history_fa.history_fa import HistoryFA
from netbench.pattern_match.algorithms.hybrid_fa.hybrid_fa import hybrid_fa
from netbench.pattern_match.algorithms.j_history_fa.history_fa import history_fa
from netbench.pattern_match.algorithms.j_hybrid_fa.j_hybrid_fa import JHybridFA
from netbench.pattern_match.algorithms.phf_dfa.phf_dfa import PHF_DFA
from netbench.pattern_match.bin.library.bdz import bdz
from netbench.pattern_match.bin.library import padnums
import sys

"""
    This module compare several NFA based algorithms.
"""

# Selected ruleset
ruleset = "../rules/Snort/worm.reg"

def get_dfa(ruleset):
    """
        Generate number of states, transitions and consumed memory for DFA.
    """
    # Create parser - use default parser
    po = parser.parser()
    # Parse input file
    po.load_file(ruleset)
    # Create DFA object
    Dfa = DELAY_DFA()
    # Make automaton from RE which was in input file
    Dfa.create_by_parser(po)
    # TODO: propagate
    Dfa.remove_epsilons()
    Dfa.remove_char_classes()
    # Resolve alphabet
    Dfa.resolve_alphabet()
    # Create  DFA
    Dfa.compute()
    # Return experimental results
    return ["DFA", Dfa.get_state_num(), Dfa.get_trans_num(), Dfa.report_memory_optimal(), Dfa.report_memory_naive()]

def get_ddfa(ruleset):
    """
        Generate number of states, transitions and consumed memory for DDFA.
    """
    # Create parser - use default parser
    po = parser.parser()
    # Parse input file
    po.load_file(ruleset)
    # Create Delay  DFA object
    DelayDfa = DELAY_DFA()
    # Make automaton from RE which was in input file
    DelayDfa.create_by_parser(po)
    # Make Delay DFA
    # Resolve alphabet
    DelayDfa.resolve_alphabet()
    # Create Delay DFA
    DelayDfa.compute()
    # Return experimental results
    return ["Delay DFA", DelayDfa.get_state_num(), DelayDfa.get_trans_num(), DelayDfa.report_memory_optimal(), DelayDfa.report_memory_naive()]
    
def get_hcfa(ruleset):
    """
        Generate number of states, transitions and consumed memory for History\
        counting FA.
    """
    # Create parser - use default parser
    po = parser.parser("pcre_parser", True)
    # Parse input file
    po.load_file(ruleset)
    # Create History Counting FA object
    history_counting = HistoryCountingFA()
    # Make automaton from RE which was in input file
    history_counting.create_by_parser(po)
    # Remove epsilons
    history_counting.remove_epsilons()
    # Store the NFA
    NFA = history_counting.get_automaton(True)
    # Replace X{m,n} with X*
    NFA_without_cnt = \
    history_counting._replace_length_restriction_with_a_closure(NFA)
    NFA = history_counting.get_automaton(True)
    # Assingn the automaton with replaced X{m,n} with X*
    history_counting._automaton = NFA_without_cnt
    # Determinise the automaton
    history_counting.determinise(create_table = True)
    # Create History Counting FA
    history_counting.compute(NFA)
    # Return experimental results
    return ["History Counting FA", history_counting.get_state_num(), history_counting.get_trans_num(), history_counting.report_memory_optimal(), history_counting.report_memory_naive()]

def get_hfa(ruleset):
    """
        Generate number of states, transitions and consumed memory for        \
        History FA.
    """
    # Create parser - use default parser
    po = parser.parser()
    # Parse input file
    po.load_file(ruleset)
    # Create History FA object
    history = HistoryFA()
    # Make automaton from RE which was in input file
    history.create_by_parser(po)
    # Remove epsilons
    history.remove_epsilons()
    # Store the NFA
    NFA = history.get_automaton(True)
    # Determinise the automaton
    history.determinise(create_table = True)
    # Create History FA
    history.compute(NFA)
    # Return experimental results
    return ["History FA", history.get_state_num(), history.get_trans_num(), history.report_memory_optimal(), history.report_memory_naive()]

def get_hybfa(ruleset):
    """
        Generate number of states, transitions and consumed memory for        \
        History FA.
    """
    # Create parser - use default parser
    po = parser.parser()
    # Parse input file
    po.load_file(ruleset)    
    # Create Hybrid FA object
    hyb_fa = hybrid_fa()
    # Make automaton from RE which was in input file
    hyb_fa.create_by_parser(po)
    # set parameters for _is_special() function
    hyb_fa.set_max_head_size(-1) # off
    hyb_fa.set_max_tx(-1) # off
    hyb_fa.set_special_min_depth(2)
    # Create Hybrid FA
    hyb_fa.compute()
    # Return experimental results
    return ["Hybrid FA", hyb_fa.get_state_num(), hyb_fa.get_trans_num(), hyb_fa.report_memory_optimal(), hyb_fa.report_memory_naive()]
    
def get_hisfa(ruleset):
    """
        Generate number of states, transitions and consumed memory for        \
        History FA (Suchodol).
    """
    # Create history FA object
    his_fa = history_fa()
    # Create History FA
    his_fa.compute(ruleset)  
    # Return experimental results
    return ["History FA (Suchodol)", his_fa.get_state_num(), his_fa.get_trans_num(), his_fa.report_memory_optimal(), his_fa.report_memory_naive()]
    
def get_hybfas(ruleset):
    """
        Generate number of states, transitions and consumed memory for        \
        History FA (Suchodol).
    """
    # Create parser - use default parser
    po = parser.parser()
    # Create Hybrid FA object
    hyb_fa = JHybridFA()
    # Set parser
    hyb_fa.set_parser(po)
    # Parse input file
    hyb_fa.load_file(ruleset)
    # Create Hybrid FA
    hyb_fa.compute()
    # Return experimental results
    return ["Hybrid FA (Suchodol)", hyb_fa.get_state_num(), hyb_fa.get_trans_num(), hyb_fa.report_memory_optimal(), hyb_fa.report_memory_naive()]

def get_phf(ruleset):
    """
        Generate number of states, transitions and consumed memory for        \
        Perfect hashing DFA.
    """
    # Create parser - use default parser
    po = parser.parser()
    # Parse input file
    po.load_file(ruleset)  
    # create phf_dfa automaton
    aut = PHF_DFA()
    # Make automaton from RE which was in input file
    aut.create_by_parser(po)
    # redefine default PHF class 
    a = bdz()
    a.set_ratio(2.0)
    aut.set_PHF_class(a)
    # compute dfa and PHF table
    aut.compute()
    # Return experimental results
    return ["Perfect Hashing DFA", aut.get_state_num(), aut.get_trans_num(), aut.report_memory_real(), aut.report_memory_real()]
    
# Main
if __name__ == '__main__':
    print("-------------------------------------------------------------------")
    print("    Comparison of several DFA based pattern matching algorithms    ")
    print("-------------------------------------------------------------------")
    print(" Used algorithms: DFA, Delay DFA, History FA, Hybrid FA,           ")
    print("                  History FA (Suchodol), History Counting FA,      ")
    print("                  Hybrid FA (Suchodol), Perfect Hashing DFA        ")
    print(" Ruleset: ../rules/Snort/worm.reg                                  ")
    print("-------------------------------------------------------------------")
    table = [["DFA based algorithm", "States", "Transitions", "Memory (Optimal) [B]", "Memory (Array)[B]"]]
    # Generate number of states, transitions and consumed memory for DFA
    table.append(get_dfa(ruleset))
    # Generate number of states, transitions and consumed memory for DDFA
    table.append(get_ddfa(ruleset))
    # Generate number of states, transitions and consumed memory for History FA.
    table.append(get_hfa(ruleset))
    # Generate number of states, transitions and consumed memory for History counting FA.
    table.append(get_hcfa(ruleset))
    # Generate number of states, transitions and consumed memory for Hybrid FA.
    table.append(get_hybfa(ruleset))
    # Generate number of states, transitions and consumed memory for History FA (Suchodol)
    table.append(get_hisfa(ruleset))
    # Generate number of states, transitions and consumed memory for Hybrid FA (Suchodol).
    #table.append(get_hybfas(ruleset))
    # Generate number of states, transitions and consumed memory for Perfect Hashing DFA.
    table.append(get_phf(ruleset))
    # Pretty print the table
    padnums.pprint_table(sys.stdout, table)
    
