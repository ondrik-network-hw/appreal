###############################################################################
#  example_of_use.py: Module for PATTERN MATCH - example of use for Hybrid FA 
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
    This module demonstrate usage of hybrid_fa class.
"""

# Import used Netbench modules
from hybrid_fa import hybrid_fa
from netbench.pattern_match.pcre_parser import pcre_parser

# EXAMPLE of use for hybrid_fa class
if __name__ == '__main__':
    print("-------------------------------------------------------------------")
    print("                   Example of use: Hybrid FA                       ")
    print("-------------------------------------------------------------------")
    print(" Ruleset: ../../rules/Snort/web-cgi.rules.pcre                     ")
    print(" Head size: Off                                                    ")
    print(" Max thresholds count: Off                                         ")
    print(" minimal depth: 2                                                  ")
    print("-------------------------------------------------------------------")
    
    # Create PCRE parser object
    parser = pcre_parser()

    # Try to process rules from ../../rules/Snort/web-cgi.rules.pcre
    parser.load_file("../../rules/Snort/web-cgi.rules.pcre") # load rules from file

    #parser.set_text("/abcd/") # set rules from string

    # Create hybrid_fa object
    hyb_fa = hybrid_fa()
    # Parse the ruleset
    hyb_fa.create_by_parser(parser)

    # set parameters for _is_special() function
    # Head size if off, max thresholds count is off, minimal depth is 2."
    hyb_fa.set_max_head_size(-1) # off
    hyb_fa.set_max_tx(-1) # off
    hyb_fa.set_special_min_depth(2)
    
    # Create the Hybrid FA
    hyb_fa.compute() # run the approach

    # Report amount of used memory - optimal mapping
    print "Utilized memory (optimal mapping):", hyb_fa.report_memory_optimal(), "B"
    # Report amount of used memory - array mapping
    print "Utilized memory (array mapping):", hyb_fa.report_memory_naive(), "B"
    
    # Print number of states and transitions
    print "Number of states:", hyb_fa.get_state_num()
    print "Number of transitions:", hyb_fa.get_trans_num()
    
    print("-------------------------------------------------------------------")
    
    # Look up some dangerous inputs. Zero means no match, one means match.
    print "Look up some dangerous inputs. Zero means no match, one match:\n" + str(hyb_fa.search("/awstats.pl?---configdir=| /calendar-admin.pl /db4web_c.exe/aaaa:  /itemid=123f  /ShellExample.cgi?aaaaa*"))
    
    # Save automaton into file in DOT format
    #hyb_fa.show("automaton.dot")

    print("-------------------------------------------------------------------")