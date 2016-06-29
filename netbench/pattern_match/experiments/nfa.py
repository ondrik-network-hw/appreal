###############################################################################
#  nfa.py: Compare several NFA based algorithms
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
from netbench.pattern_match.algorithms.clark_nfa import clark_nfa 
from netbench.pattern_match.algorithms.sindhu_prasana_nfa import sindhu_prasana_nfa 
from netbench.pattern_match.algorithms.sourdis_bispo_nfa import sourdis_bispo_nfa 
from netbench.pattern_match.bin.library import padnums
import sys

"""
    This module compare several NFA based algorithms.
"""

# Selected ruleset
ruleset = "../rules/L7/selected.pcre"

def get_clark_wochc(ruleset):
    """
        Generate number of LUTs and FFs for Clark's approach without char 
        classes.
    """
    # Create clark_nfa object
    cn = clark_nfa.clark_nfa(True)
    # Create parser - use default parser
    Test0 = parser.parser("pcre_parser")
    # Load RE file
    Test0.load_file(ruleset)
    # Parse RE and create NFA
    cn.create_by_parser(Test0)
    # Call the compute method
    cn.compute()
    # Get number of used LUTs and FFs
    data = cn.report_logic()
    return ["Clark wo char classes", data[0], data[1]]
    
def get_clark_wchc(ruleset):
    """
        Generate number of LUTs and FFs for Clark's approach with char 
        classes.
    """
    # Create clark_nfa object
    cn = clark_nfa.clark_nfa(False)
    # Create parser - use default parser
    Test0 = parser.parser("pcre_parser")
    # Load RE file
    Test0.load_file(ruleset)
    # Parse RE and create NFA
    cn.create_by_parser(Test0)
    # Call the compute method
    cn.compute()
    # Get number of used LUTs and FFs
    data = cn.report_logic()
    return ["Clark with char classes", data[0], data[1]]

def get_clark_s(ruleset, stride):
    """
        Generate number of LUTs and FFs for strided Clark's approach with char 
        classes.
    """
    # Create clark_nfa object
    cn = clark_nfa.clark_nfa(False, stride)
    # Create parser - use default parser
    Test0 = parser.parser("pcre_parser")
    # Load RE file
    Test0.load_file(ruleset)
    # Parse RE and create NFA
    cn.create_by_parser(Test0)
    # Call the compute method
    cn.compute()
    # Get number of used LUTs and FFs
    data = cn.report_logic()
    return ["Clark with stride ", stride, data[0], data[1]]

def get_sp(ruleset):
    """
        Generate number of LUTs and FFs for Sidhu and Prasana's approach.
    """
    # Create sindhu_prasana_nfa object
    cn = sindhu_prasana_nfa.sindhu_prasana_nfa()
    # Create parser - use default parser
    Test0 = parser.parser()
    # Load RE file
    Test0.load_file(ruleset)
    # Parse RE and create NFA
    cn.create_by_parser(Test0)
    # Call the compute method
    cn.compute()
    # Get number of used LUTs and FFs
    data = cn.report_logic()
    return ["Sidhu Prasana", data[0], data[1]]
    
def get_sp_s(ruleset, stride):
    """
        Generate number of LUTs and FFs for strided Sidhu and Prasana's approach.
    """
    # Create sindhu_prasana_nfa object
    cn = sindhu_prasana_nfa.sindhu_prasana_nfa(stride)
    # Create parser - use default parser
    Test0 = parser.parser()
    # Load RE file
    Test0.load_file(ruleset)
    # Parse RE and create NFA
    cn.create_by_parser(Test0)
    # Call the compute method
    cn.compute()
    # Get number of used LUTs and FFs
    data = cn.report_logic()
    return ["Sidhu Prasana with stride ", stride, data[0], data[1]]
    
def get_sb(ruleset):
    # Create sourdis_bispo_nfa object
    cn = sourdis_bispo_nfa.sourdis_bispo_nfa()
    # Preprocess the REs
    preprocessed = cn.find_pcre_repetitions(ruleset)
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
    return ["Sourdis Bispo", data[0], data[1]]

if __name__ == '__main__':
    print("-------------------------------------------------------------------")
    print("    Comparison of several NFA based pattern matching algorithms    ")
    print("-------------------------------------------------------------------")
    print(" Used algorithms: Clark, Sidhu and Sourdis                         ")
    print(" Ruleset: ../rules/L7/selected.pcre                                ")
    print(" Strided: No                                                       ")
    print("-------------------------------------------------------------------")
    table = [["NFA based algorithm", "LUT", "FF"]]
    # Generate number of LUTs and FFs for Clark's approach without char classes
    table.append(get_clark_wochc(ruleset))
    # Generate number of LUTs and FFs for Clark's approach with char classes
    table.append(get_clark_wchc(ruleset))
    # Generate number of LUTs and FFs for Sidhu and Prasana's approach
    table.append(get_sp(ruleset))
    # Generate number of LUTs and FFs for Sourdis and Bispo's approach
    table.append(get_sb(ruleset))
    # Prety print the table
    padnums.pprint_table(sys.stdout, table)
    
    print("\n")
    print("-------------------------------------------------------------------")
    print("    Comparison of several NFA based pattern matching algorithms    ")
    print("-------------------------------------------------------------------")
    print(" Used algorithms: Clark and Sidhu                                  ")
    print(" Ruleset: ../rules/L7/selected.pcre                                ")
    print(" Strided: Yes - 2 & 4 chars at once                                ")
    print("-------------------------------------------------------------------")
    print("NOTE: Construction of strided automatons may take a long time.\n")
    table = [["NFA based algorithm", "Stride", "LUT", "FF"]]
    for s in [2,4]:
        # Generate number of LUTs and FFs for strided Clark's approach with char 
        # classes
        table.append(get_clark_s(ruleset, s))
        # Generate number of LUTs and FFs for strided Sidhu and Prasana's approach
        table.append(get_sp_s(ruleset, s))
    # Prety print the table
    padnums.pprint_table(sys.stdout, table)
    
    
    
    