###############################################################################
#  test_history_fa.py: Test module for History FA
#  Copyright (C) 2011 Brno University of Technology, ANT @ FIT
#  Author(s): Jaroslav Suchodol <xsucho04@stud.fit.vutbr.cz>
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
#  This software or firmware is provided ``as is, and any express or implied
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

from netbench.pattern_match.algorithms.j_history_fa.history_fa import history_fa
from netbench.pattern_match.nfa_data import nfa_data
from netbench.pattern_match import aux_func
import unittest
import os

class test_history_fa(unittest.TestCase):
    """
        Test module for History FA.
    """

    def test_compute(self):
        """compute()"""
        # Method compute(input_file_name):
        # Check the correctness of the logical machine output over
        # self.assertTrue on individual automaton items + focus on the
        # properties of H-FA (transitions, flags, counters)

        # 1) /abcd/ ; test with an expression that does not use properties
        # of History FA
        his_fa = history_fa()
        his_fa.compute(aux_func.getPatternMatchDir() + "/algorithms/j_history_fa/test_data/his_fa_1.RE")
        copy = his_fa.get_automaton(False)
        result = nfa_data().load_from_file(
            aux_func.getPatternMatchDir() + "/algorithms/j_history_fa/test_data/his_fa_1.nfa_data")

        self.assertTrue(sorted(copy.states.keys()) ==
            sorted(result.states.keys()))
        self.assertTrue(copy.alphabet == result.alphabet)
        self.assertTrue(copy.start == result.start)
        self.assertTrue(copy.final == result.final)
        self.assertTrue(copy.transitions == result.transitions)
        self.assertTrue(copy.Flags == result.Flags)

        # 2) /ab.*cd/ ; test with an expression that contain .*
        his_fa = history_fa()
        his_fa.compute(aux_func.getPatternMatchDir() + "/algorithms/j_history_fa/test_data/his_fa_2.RE")
        copy = his_fa.get_automaton(False)
        result = nfa_data().load_from_file(
            aux_func.getPatternMatchDir() + "/algorithms/j_history_fa/test_data/his_fa_2.nfa_data")

        self.assertTrue(sorted(copy.states.keys()) ==
            sorted(result.states.keys()))
        self.assertTrue(copy.alphabet == result.alphabet)
        self.assertTrue(copy.start == result.start)
        self.assertTrue(copy.final == result.final)
        self.assertTrue(copy.transitions == result.transitions)
        self.assertTrue(copy.Flags == result.Flags)
        
        # 3) /ab[^1234]*cd|efg/; test with an expression containing one
        # alternation [^1234]*, the second is not        
        his_fa = history_fa()
        his_fa.compute(aux_func.getPatternMatchDir() + "/algorithms/j_history_fa/test_data/his_fa_3.RE")
        copy = his_fa.get_automaton(False)
        result = nfa_data().load_from_file(
            aux_func.getPatternMatchDir() + "/algorithms/j_history_fa/test_data/his_fa_3.nfa_data")

        self.assertTrue(sorted(copy.states.keys()) ==
            sorted(result.states.keys()))
        self.assertTrue(copy.alphabet == result.alphabet)
        self.assertTrue(copy.start == result.start)
        self.assertTrue(copy.final == result.final)
        self.assertTrue(copy.transitions == result.transitions)
        self.assertTrue(copy.Flags == result.Flags)

    def test_save_to_file(self):
        """save_to_file()"""
        
        his_fa = history_fa()
        his_fa.compute(aux_func.getPatternMatchDir() + "/algorithms/j_history_fa/test_data/his_fa_1.RE")
        his_fa.save_to_file(aux_func.getPatternMatchDir() + "/algorithms/j_history_fa/test_data/save.dat")
        self.assertTrue(os.path.exists(aux_func.getPatternMatchDir() + "/algorithms/j_history_fa/test_data/save.dat") == True)
        f = open(aux_func.getPatternMatchDir() + "/algorithms/j_history_fa/test_data/save.tmpl","r");
        tmpl_content = f.read()
        f.close()
        f = open(aux_func.getPatternMatchDir() + "/algorithms/j_history_fa/test_data/save.dat","r");
        save_content = f.read()
        f.close()
        self.assertTrue(tmpl_content == save_content)
        aux_func.getstatusoutput("rm -f " + aux_func.getPatternMatchDir() + "/algorithms/j_history_fa/test_data/save.dat", None)
        
    def test_report_memory_optimal(self):
        """report_memory_optimal()"""

        his_fa = history_fa()
        his_fa.compute(aux_func.getPatternMatchDir() + "/algorithms/j_history_fa/test_data/his_fa_1.RE")

        self.assertTrue(his_fa.report_memory_optimal() == 13)

    def test_report_memory_naive(self):
        """report_memory_naive()"""

        his_fa = history_fa()
        his_fa.compute(aux_func.getPatternMatchDir() + "/algorithms/j_history_fa/test_data/his_fa_1.RE")

        self.assertTrue(his_fa.report_memory_naive() == 40)

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(test_history_fa)
    unittest.TextTestRunner(verbosity=2).run(suite)
