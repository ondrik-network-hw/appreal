###############################################################################
#  example_of_use.py: Module for PATTERN MATCH - example of use for
#                     Sourdis's NFA
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

# Import used Netbench modules
from netbench.pattern_match import parser
from netbench.pattern_match.algorithms.sourdis_bispo_nfa import sourdis_bispo_nfa 

"""
    This module demonstrate usage of sourdis_bispo_nfa class.
"""

if __name__ == '__main__':
    # Clark mapping method without suppotr for char classes
    print("-------------------------------------------------------------------")
    print("                             Sourdis NFA                           ")
    print("-------------------------------------------------------------------")
    print(" Ruleset: ../../rules/L7/selected.pcre                             ")
    print(" Genereated VHDL output: sourdis_nfa_impl.vhd                      ")
    print("-------------------------------------------------------------------")
    # Create sourdis_bispo_nfa object
    cn = sourdis_bispo_nfa.sourdis_bispo_nfa()
    # Preprocess the REs
    preprocessed = cn.find_pcre_repetitions("../../rules/L7/selected.pcre")
    # Create parser - use default parser
    Test0 = parser.parser("pcre_parser")
    # Load REs
    Test0.set_text(preprocessed)

    # Parse RE and create NFA
    cn.create_by_parser(Test0)
    
    # Call the compute method
    cn.compute()
    
    # Get number of used LUTs and FFs
    data = cn.report_logic()
    print(" Used LUTs estimation: " + str(data[0]))
    print(" Used FFs estimation: " + str(data[1]))
    print("-------------------------------------------------------------------")
    # Save implementation
    # Open file
    f = open("sourdis_nfa_impl.vhd", "w")
    # Get VHDL code and write the code
    f.write(cn.get_HDL())
    # Close file
    f.close()
