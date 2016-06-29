###############################################################################
#  example_of_use.py: Example of use module for class PHF_DFA.
#  Copyright (C) 2010 Brno University of Technology, ANT @ FIT
#  Author(s): Milan Dvorak <xdvora66@stud.fit.vutbr.cz>
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

# Import used Netbench modules
from netbench.pattern_match.algorithms.phf_dfa.phf_dfa import PHF_DFA
from netbench.pattern_match.bin.library.bdz import bdz
from netbench.pattern_match.pcre_parser import pcre_parser

"""
    This module demonstrates usage of PHF_DFA class.
"""


# EXAMPLE of use for PHF_DFA class
if __name__ == '__main__':
    print("-------------------------------------------------------------------")
    print("                    Example of use: PHF DFA                        ")
    print("-------------------------------------------------------------------")
    print(" Ruleset: /#include.*>/                                            ")
    print(" Faulty Table: No                                                  ")
    print(" State bits: 10                                                    ")
    print(" Symbol bits: 12                                                   ")
    print(" Fallback State: No                                                ")
    print("-------------------------------------------------------------------")

    # create parser and load RE
    parser = pcre_parser()
    parser.set_text("/#include.*>/")

    # create phf_dfa automaton
    aut = PHF_DFA()
    aut.create_by_parser(parser)

    # redefine default PHF class so table generation won't fail in this script
    # it's not important right now, more about that later
    a = bdz()
    a.set_ratio(2.0)
    aut.set_PHF_class(a)

    # compute dfa and PHF table
    aut.compute()

    # memory used by PHF table
    print "Memory used (Real):", aut.report_memory_real(), "B"
    
    # Print number of symbols, states and transitions
    print "Number of symbols:", aut.get_alpha_num()
    print "Number of states:", aut.get_state_num()
    print "Number of transitions:", aut.get_trans_num()
    
    print("-------------------------------------------------------------------")
    
    # search in string
    print "Search result:", aut.search("#include <stdio.h>")
    
    print("-------------------------------------------------------------------")
    
    print("-------------------------------------------------------------------")
    print("                    Example of use: PHF DFA                        ")
    print("-------------------------------------------------------------------")
    print(" Ruleset: /#include.*>/                                            ")
    print(" Faulty Table: Yes                                                 ")
    print(" Hash bits: 6                                                      ")
    print(" State bits: 10                                                    ")
    print(" Symbol bits: 12                                                   ")
    print(" Fallback State: No                                                ")
    print(" Noncollision transition validation hash: No                       ")
    print("-------------------------------------------------------------------")
    
    # to reduce used memory, we can enable faulty transition table
    aut.enable_faulty_transitions(6)
    aut.compute()
    print "Memory used with faulty transitions (Real):", aut.report_memory_real(), "B"
    print "Faulty search result:", aut.search("#include <stdio.h>")
    
    # Print number of symbols, states and transitions
    print "Number of symbols:", aut.get_alpha_num()
    print "Number of states:", aut.get_state_num()
    print "Number of transitions:", aut.get_trans_num()
    
    print("-------------------------------------------------------------------")
    
    print("-------------------------------------------------------------------")
    print("                    Example of use: PHF DFA                        ")
    print("-------------------------------------------------------------------")
    print(" Ruleset: /#include.*>/                                            ")
    print(" Faulty Table: Yes                                                 ")
    print(" Hash bits: 6                                                      ")
    print(" State bits: 4                                                     ")
    print(" Symbol bits: 4                                                    ")
    print(" Fallback State: No                                                ")
    print(" Noncollision transition validation hash: No                       ")
    print("-------------------------------------------------------------------")
    
    # another way to reduce used memory is to change bits for symbol and state representation
    # NOTE - number of symbols/states must be less than 2**4
    aut.set_table_parameters((4, 4))
    print "Memory used with new parameters (Real):", aut.report_memory_real(), "B"

    # Print number of symbols, states and transitions
    print "Number of symbols:", aut.get_alpha_num()
    print "Number of states:", aut.get_state_num()
    print "Number of transitions:", aut.get_trans_num()
    print("-------------------------------------------------------------------")
    
    print("-------------------------------------------------------------------")
    print("                    Example of use: PHF DFA                        ")
    print("-------------------------------------------------------------------")
    print(" Ruleset: /#include.*>/                                            ")
    print(" Faulty Table: Yes                                                 ")
    print(" Hash bits: 6                                                      ")
    print(" State bits: 4                                                     ")
    print(" Symbol bits: 4                                                    ")
    print(" Fallback State: Yes                                               ")
    print(" Noncollision transition validation hash: No                       ")
    print("-------------------------------------------------------------------")
    
    # we have fully defined automaton, so we can use fallback_state
    aut.enable_fallback_state(warning=False)
    # recompute automaton
    aut.compute()
    # new memory requirements
    print "Memory used with fallback_state (Real):", aut.report_memory_real(), "B"
    print "Number of symbols:", aut.get_alpha_num()
    print "Number of states:", aut.get_state_num()
    print "Number of transitions with fallback_state:", aut.get_trans_num()

    print("-------------------------------------------------------------------")

    print("-------------------------------------------------------------------")
    print("                    Example of use: PHF DFA                        ")
    print("-------------------------------------------------------------------")
    print(" Ruleset: /#include.*>/                                            ")
    print(" Faulty Table: Yes                                                 ")
    print(" Hash bits: 6                                                      ")
    print(" State bits: 4                                                     ")
    print(" Symbol bits: 4                                                    ")
    print(" Fallback State: Yes                                               ")
    print(" Noncollision transition validation hash: Yes                      ")
    
    # we can customize the PHF function, so the table will have less lines
    # note that PHF generation can fail, when table size is too small (get_compute returns False)
    a = bdz() # new PHF class
    a.set_limit(12) # one third of the total PHF table size
                    # we have 35 transitions, so the generation will most certainly fail
    a.set_iteration_limit(8) # number of tries to generate PHF table
    aut.set_PHF_class(a)
    aut.compute()
    i = 12
    while not aut.get_compute(): # until PHF table is generated succesfully,
        i += 1                   # increase its size
        a.set_limit(i)
        aut.set_PHF_class(a)
        aut.compute()
        
    print(" Limit: " + str(i))
    print("-------------------------------------------------------------------")
    
    # Memory usage
    print "Memory used with new PHF:", aut.report_memory_real(), "B"
    
    # Print number of symbols, states and transitions
    print "Number of symbols:", aut.get_alpha_num()
    print "Number of states:", aut.get_state_num()
    print "Number of transitions:", aut.get_trans_num()
    print("-------------------------------------------------------------------")
    
    print("-------------------------------------------------------------------")
    print("                    Example of use: PHF DFA                        ")
    print("-------------------------------------------------------------------")
    print(" Ruleset: /#include.*>/                                            ")
    print(" Faulty Table: No                                                  ")
    print(" State bits: 4                                                     ")
    print(" Symbol bits: 4                                                    ")
    print(" Fallback State: No                                                ")
    print("-------------------------------------------------------------------")
    # if we want to disable faulty transitions and fallback state again:
    aut.disable_faulty_transitions()
    aut.disable_fallback_state()
    # try to compute
    aut.compute()
    #print "Result of compute:", aut.get_compute()
    # compute failed because memory limit on PHF, so let's use default PHF class again
    a = bdz()
    aut.set_PHF_class(a)
    aut.compute()
    #print "Result of compute:", aut.get_compute()
    #print "Number of transitions:", aut.get_trans_num()
    print "Memory used after disabling extensions (Real):", aut.report_memory_real(), "B"
    
    # Print number of symbols, states and transitions
    print "Number of symbols:", aut.get_alpha_num()
    print "Number of states:", aut.get_state_num()
    print "Number of transitions:", aut.get_trans_num()
    print("-------------------------------------------------------------------")
