###############################################################################
#  test_clark_nfa.py: Module for PATTERN MATCH - test implementation of Clark's
#                     NFA, Modelsim is necessary for this test
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

# Import general modules
import copy
import re
import unittest
import os
# Import Netbench modules
from netbench.pattern_match import parser
from netbench.pattern_match.algorithms.clark_nfa import clark_nfa 
from netbench.pattern_match import aux_func

"""
    This module test clark_nfa class in various settings.
"""

def load_file(name):
    """
        Open file specified by name and split content acording to "%$%".
        
        :param name: Name of the file.
        :type name: string
        :returns: Loaded and splited content of the file.
        :rtype: list(string)
    """
    # Open VHDL template file and load the template
    f = open(name, "rb");
    blob = f.read()
    # Split the file
    tmp = re.split("%\$%", blob)
    # Close the opened file
    f.close()
    
    return tmp

def save_file(name, content):
    """
        Save the content stored in parameter content into file named by \
        parameter name.
        
        :param name: Name of the file.
        :type name: string
        
        :param content: Content to write.
        :type content: string
    """
    # Open file
    f = open(name, "w")
    # Write the content into the file
    f.write(content)
    # Close file
    f.close()

def create_simulation(alg):
    """
        Creates simulation files from templates for object specified by alg  \
        parameter.
        
        :param alg: Object representing pattern matching algorithm.
        :type alg: b_ptrn_match
    """
    # Get base directory
    base = aux_func.getPatternMatchDir() + "/vhdl/tests/"
    # Get test directory 
    tdir = aux_func.getPatternMatchDir() + "/algorithms/clark_nfa/test/"
    # wrapper.vhd
    content = load_file(base + "wrapper.vhd")
    result = content[0] + "CLARK_NFA" + content[1]
    save_file(tdir + "wrapper.vhd", result)
    
    # testbench.vhd
    content = load_file(base + "testbench.vhd")
    result = content[0] + str(32) + content[1] + str(alg.width) + content[2] + str(alg._fStateNum) + content[3];
    save_file(tdir + "testbench.vhd", result)
    
    # Modules.tcl
    content = load_file(base + "Modules.tcl")
    result = content[0] + aux_func.getPatternMatchDir() + content[1] + "" + content[2] + "test.vhd" + content[3];
    save_file(tdir + "Modules.tcl", result)
    
    # test.vhd
    save_file(tdir + "test.vhd", alg.get_HDL())
    
def run_simulation(test):
    """
        Runs the simulation and compare the results.
        
        :param test: Object representing the test.
        :type alg: test_clark_nfa
        
        :returns: True when simulation is OK, False otherwise.
        :rtype: boolean
    """
    # Get test directory 
    tdir = aux_func.getPatternMatchDir() + "/algorithms/clark_nfa/test/"
    # Run Modelsim
    work_path = os.getcwd()
    res = aux_func.getstatusoutput("cd " + tdir + "; vsim -c -do " + tdir + "testbench.do; cd " + work_path, "")
    # Check the output and print the stdout and stderr
    if res[0] != 0:
        print "STDOUT:"
        print res[0]
        print "STDERR:"
        print res[1]
    # Test if run was OK
    test.assertTrue(res[0] == 0)
    # Load expected file
    exp = load_file(tdir + "tests/expected.txt")
    # Load results from simulation
    sim = load_file(tdir + "tests/monitor.txt")
    
    test.assertTrue(exp[0] == sim[0])
    
class test_clark_nfa(unittest.TestCase):
    """
        A base test class for Clark NFA.
    """
    
    def test_wchc(self):
        """
            Tests the algorithm when character classes are used.
        """
        # Get test directory 
        tdir = aux_func.getPatternMatchDir() + "/algorithms/clark_nfa/test/"
        # Create clark_nfa object
        cn = clark_nfa.clark_nfa(False)
        # Create parser - use default parser
        Test0 = parser.parser("pcre_parser")
        # Load RE file
        Test0.load_file(tdir + "tests/test.pcre")
        # Parse RE and create NFA
        cn.create_by_parser(Test0)
        # Call the compute method
        cn.compute()
        # Create the simulation
        create_simulation(cn)
        # run the simulation
        run_simulation(self)
    
    def test_wochc(self):
        """
            Tests the algorithm without character classes.
        """
        # Get test directory 
        tdir = aux_func.getPatternMatchDir() + "/algorithms/clark_nfa/test/"
        # Create clark_nfa object
        cn = clark_nfa.clark_nfa(True)
        # Create parser - use default parser
        Test0 = parser.parser("pcre_parser")
        # Load RE file
        Test0.load_file(tdir + "tests/test.pcre")
        # Parse RE and create NFA
        cn.create_by_parser(Test0)
        # Call the compute method
        cn.compute()
        # Create the simulation
        create_simulation(cn)
        # run the simulation
        run_simulation(self)
        
    def test_strided(self):
        """
            Tests the algorithm with stride = 2.
        """
        # Get test directory 
        tdir = aux_func.getPatternMatchDir() + "/algorithms/clark_nfa/test/"
        # Create clark_nfa object
        cn = clark_nfa.clark_nfa(False, 2)
        # Create parser - use default parser
        Test0 = parser.parser("pcre_parser")
        # Load RE file
        Test0.load_file(tdir + "tests/test.pcre")
        # Parse RE and create NFA
        cn.create_by_parser(Test0)
        # Call the compute method
        cn.compute()
        # Create the simulation
        create_simulation(cn)
        # run the simulation
        run_simulation(self)
    
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_clark_nfa)
    unittest.TextTestRunner(verbosity=2).run(suite)
    
    
