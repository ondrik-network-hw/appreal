###############################################################################
#  example_of_use.py: Module for PATTERN MATCH - example of use for Delay DFA
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
    This module demonstrate usage of DELAY_DFA class.
"""

# Import used Netbench modules
from ddfa import DELAY_DFA
from netbench.pattern_match import pcre_parser
from netbench.pattern_match.b_dfa import b_dfa

# Import general Netbench modules
import os

# way to file with Regular Expresions
FileName = "../../rules/Snort/http-bots.reg"
    
# EXAMPLE of use for Delay_DFA class
if __name__ == '__main__':
    print("-------------------------------------------------------------------")
    print("                Example of use: Delay DFA                          ")
    print("-------------------------------------------------------------------")
    print(" Ruleset: " + FileName)
    print(" Diameter bound: Unlimited                                         ")
    print(" Generated data automaton structure: parse                         ")
    print(" Graphical representation: automat.dot                             ")
    print("-------------------------------------------------------------------")
    
    # Parse input file
    parser = pcre_parser.pcre_parser()
    parser.load_file(FileName)

    # Create delay dfa object
    DelayDfa = DELAY_DFA()
    # Make automat from RE which was in input file
    DelayDfa.create_by_parser(parser)

    # Make Delay DFA
    # Resolve alphabet -> alphabet will be deterministic
    DelayDfa.resolve_alphabet()
    # Set diameter bound to 0 - unbounded (value bigger than 0 sets diameter 
    # bound to this value).
    DelayDfa.set_bound(0)
    # Create Delay DFA
    DelayDfa.compute()
    # Save Delay DFA structure for later processing
    DelayDfa.SaveToFile("parse")
    # Report amount of used memory - optimal mapping
    print "Utilized memory (optimal mapping):", DelayDfa.report_memory_optimal(), "B"
    # Report amount of used memory - array mapping
    print "Utilized memory (array mapping):", DelayDfa.report_memory_naive(), "B"
    # Save graphical representation of automaton
    DelayDfa._automaton.show("automat.dot")
    # Print number of states, transitions and default transitions
    print "Number of states:", DelayDfa.get_state_num()
    print "Number of transitions:", DelayDfa.get_trans_num()
    print "Number of default transitions:", DelayDfa.get_default_trans_num()
    print("-------------------------------------------------------------------")
