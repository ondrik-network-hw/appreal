###############################################################################
#  example_of_use.py: Module for PATTERN MATCH - example of use for History FA
#                                                variant by J. Suchodol
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
    This module demonstrate usage of history_fa class (variant of History FA \
    by J. Suchodol).
"""

# Import used Netbench modules
from history_fa import history_fa

# EXAMPLE of use for history_fa class
if __name__ == '__main__':
    print("-------------------------------------------------------------------")
    print("        Example of use: History FA variant by J. Suchodol          ")
    print("-------------------------------------------------------------------")
    print(" Ruleset: ../../rules/Snort/http-bots.reg                          ")
    print(" Generated data automaton structure: parse                         ")
    print(" Graphical representation: automat.dot                             ")
    print("-------------------------------------------------------------------")
    
    # Create history_fa object
    his_fa = history_fa()
    
    # Parse ruleset and create the history FA variant by J. Suchodol
    his_fa.compute("../../rules/Snort/http-bots.reg")
    # Save graphical representation of automaton
    his_fa.get_automaton().show("automat.dot")
    # Save history FA structure for later processing
    his_fa.save_to_file("parse")
    # Report amount of used memory - optimal mapping
    print "Utilized memory (optimal mapping):", his_fa.report_memory_optimal(), "B"
    # Report amount of used memory - array mapping
    print "Utilized memory (array mapping):", his_fa.report_memory_naive(), "B"
    
    # Print number of states, transitions and default transitions
    print "Number of states:", his_fa.get_state_num()
    print "Number of transitions:", his_fa.get_trans_num()
    print("-------------------------------------------------------------------")
