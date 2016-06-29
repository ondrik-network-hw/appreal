###############################################################################
#  example_of_use.py: Module for PATTERN MATCH - example of use for Clark's NFA
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

from netbench.pattern_match import parser
from netbench.pattern_match.algorithms.clark_nfa import clark_nfa 

"""
    This module demonstrate usage of clark_nfa class in various settings.
"""

if __name__ == '__main__':
    # Clark mapping method without suppotr for char classes
    print("-------------------------------------------------------------------")
    print("                     Example of use: Clark NFA                     ")
    print("-------------------------------------------------------------------")
    print(" Ruleset: ../../rules/L7/selected.pcre                             ")
    print(" Character Classes: No                                             ")
    print(" Strided: No                                                       ")
    print(" Genereated VHDL output: clark_nfa_impl_wochc.vhd                  ")
    print("-------------------------------------------------------------------")
    # Create clark_nfa object
    cn = clark_nfa.clark_nfa(True)
    # Create parser - use default parser
    Test0 = parser.parser("pcre_parser")
    # Load RE file
    Test0.load_file("../../rules/L7/selected.pcre")
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
    f = open("clark_nfa_impl_wochc.vhd", "w")
    # Get VHDL code and write the code
    f.write(cn.get_HDL())
    # Close file
    f.close()
    
    
    # Clark mapping method with support for char classes
    print("-------------------------------------------------------------------")
    print("                     Example of use: Clark NFA                     ")
    print("-------------------------------------------------------------------")
    print(" Ruleset: ../../rules/L7/selected.pcre                             ")
    print(" Character Classes: Yes                                            ")
    print(" Strided: No                                                       ")
    print(" Genereated VHDL output: clark_nfa_impl_wchc.vhd                   ")
    print("-------------------------------------------------------------------")
    # Create clark_nfa object
    cn = clark_nfa.clark_nfa(False)
    # Create parser - use default parser
    Test0 = parser.parser("pcre_parser")
    # Load RE file
    Test0.load_file("../../rules/L7/selected.pcre")
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
    f = open("clark_nfa_impl_wchc.vhd", "w")
    # Get VHDL code and write the code
    f.write(cn.get_HDL())
    # Close file
    f.close()
    
    
    # Clark mapping method for strided automaton with stride 2
    print("-------------------------------------------------------------------")
    print("                     Example of use: Clark NFA                     ")
    print("-------------------------------------------------------------------")
    print(" Ruleset: ../../rules/L7/selected.pcre                             ")
    print(" Character Classes: Yes                                            ")
    print(" Strided: Yes [2]                                                  ")
    print(" Genereated VHDL output: clark_nfa_impl_strided.vhd                ")
    print("-------------------------------------------------------------------")
    # Create clark_nfa object
    cn = clark_nfa.clark_nfa(False, 2)
    # Create parser - use default parser
    Test0 = parser.parser("pcre_parser")
    # Load RE file
    Test0.load_file("../../rules/L7/selected.pcre")
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
    f = open("clark_nfa_impl_strided.vhd", "w")
    # Get VHDL code and write the code
    f.write(cn.get_HDL())
    # Close file
    f.close()
