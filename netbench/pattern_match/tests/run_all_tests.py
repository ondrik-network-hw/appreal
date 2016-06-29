import unittest
from netbench.pattern_match.tests.test_b_automaton import test_b_Automaton
from netbench.pattern_match.tests.test_b_dfa import test_b_dfa
from netbench.pattern_match.tests.test_b_state import test_b_State
from netbench.pattern_match.tests.test_b_symbol import test_b_Symbol
from netbench.pattern_match.tests.test_coloured_state import test_ColouredState
from netbench.pattern_match.tests.test_def_symbols import test_DEF_SYMBOLS
from netbench.pattern_match.tests.test_nfa_data import test_nfa_data
from netbench.pattern_match.tests.test_nfa_parser import test_nfa_parser
from netbench.pattern_match.tests.test_pcre_parser import test_pcre_parser
from netbench.pattern_match.tests.test_sym_cnt_constr import test_b_Sym_cnt_constr
from netbench.pattern_match.tests.test_sym_char import test_b_Sym_char
from netbench.pattern_match.tests.test_sym_char_class import test_b_Sym_char_class
from netbench.pattern_match.tests.test_sym_kchar import test_b_Sym_kchar
from netbench.pattern_match.tests.test_sym_string import test_b_Sym_string
from netbench.pattern_match.algorithms.clark_nfa.test_clark_nfa import test_clark_nfa
from netbench.pattern_match.algorithms.delay_dfa.test_ddfa import test_ddfa
from netbench.pattern_match.algorithms.history_counting_fa.test_history_counting_fa import test_HistoryCountingFA
from netbench.pattern_match.algorithms.history_fa.test_history_fa import test_HistoryFA
from netbench.pattern_match.algorithms.hybrid_fa.test_hybrid_fa import test_hybrid_fa
from netbench.pattern_match.algorithms.j_history_fa.test_history_fa import test_history_fa as test_j_history_fa
from netbench.pattern_match.algorithms.j_hybrid_fa.test_j_hybrid_fa import test_JHybridFA
from netbench.pattern_match.algorithms.experimental.nfa_split.test_nfa_split import test_nfa_split
from netbench.pattern_match.algorithms.phf_dfa.test_phf_dfa import test_PHF_DFA
from netbench.pattern_match.algorithms.sindhu_prasana_nfa.test_sindhu_prasana_nfa import test_sindhu_prasana_nfa
from netbench.pattern_match.algorithms.sourdis_bispo_nfa.test_sourdis_bispo_nfa import test_sourdis_bispo_nfa
class run_all_tests(unittest.TestCase):
    """Run all tests."""

    def test_b_Automaton(self):
        """test_b_Automaton"""
        suite = unittest.TestLoader().loadTestsFromTestCase(test_b_Automaton)
        unittest.TextTestRunner(verbosity=0).run(suite)

    def test_b_dfa(self):
        """testt_b_dfa"""
        suite = unittest.TestLoader().loadTestsFromTestCase(test_b_dfa)
        unittest.TextTestRunner(verbosity=1).run(suite)

    def test_b_State(self):
        """test_b_State"""
        suite = unittest.TestLoader().loadTestsFromTestCase(test_b_State)
        unittest.TextTestRunner(verbosity=1).run(suite)

    def test_b_Symbol(self):
        """test_b_Symbol"""
        suite = unittest.TestLoader().loadTestsFromTestCase(test_b_Symbol)
        unittest.TextTestRunner(verbosity=1).run(suite)

    def test_ColouredState(self):
        """test_ColouredState"""
        suite = unittest.TestLoader().loadTestsFromTestCase(test_ColouredState)
        unittest.TextTestRunner(verbosity=1).run(suite)

    def test_DEF_SYMBOLS(self):
        """test_DEF_SYMBOLS"""
        suite = unittest.TestLoader().loadTestsFromTestCase(test_DEF_SYMBOLS)
        unittest.TextTestRunner(verbosity=1).run(suite)

    def test_nfa_data(self):
        """nfa_data"""
        suite = unittest.TestLoader().loadTestsFromTestCase(test_nfa_data)
        unittest.TextTestRunner(verbosity=1).run(suite)

    def test_nfa_parser(self):
        """nfa_parser"""
        suite = unittest.TestLoader().loadTestsFromTestCase(test_nfa_parser)
        unittest.TextTestRunner(verbosity=1).run(suite)

    def test_pcre_parser(self):
        """pcre_parser"""
        suite = unittest.TestLoader().loadTestsFromTestCase(test_pcre_parser)
        unittest.TextTestRunner(verbosity=1).run(suite)

    def test_b_Sym_cnt_constr(self):
        """b_Sym_cnt_constr"""
        suite = unittest.TestLoader().loadTestsFromTestCase(test_b_Sym_cnt_constr)
        unittest.TextTestRunner(verbosity=1).run(suite)

    def test_b_Sym_char(self):
        """b_Sym_char"""
        suite = unittest.TestLoader().loadTestsFromTestCase(test_b_Sym_char)
        unittest.TextTestRunner(verbosity=1).run(suite)

    def test_b_Sym_char_class(self):
        """b_Sym_char_class"""
        suite = unittest.TestLoader().loadTestsFromTestCase(test_b_Sym_char_class)
        unittest.TextTestRunner(verbosity=1).run(suite)

    def test_b_Sym_kchar(self):
        """b_Sym_kchar"""
        suite = unittest.TestLoader().loadTestsFromTestCase(test_b_Sym_kchar)
        unittest.TextTestRunner(verbosity=1).run(suite)

    def test_b_Sym_string(self):
        """b_Sym_string"""
        suite = unittest.TestLoader().loadTestsFromTestCase(test_b_Sym_string)
        unittest.TextTestRunner(verbosity=1).run(suite)
        
    def test_clark_nfa(self):
        """clark_nfa"""
        suite = unittest.TestLoader().loadTestsFromTestCase(test_clark_nfa)
        unittest.TextTestRunner(verbosity=1).run(suite)
        
    def test_delay_dfa(self):
        """delay_dfa"""
        suite = unittest.TestLoader().loadTestsFromTestCase(test_ddfa)
        unittest.TextTestRunner(verbosity=1).run(suite)
    
    def test_history_fa(self):
        """history_fa"""
        suite = unittest.TestLoader().loadTestsFromTestCase(test_HistoryFA)
        unittest.TextTestRunner(verbosity=1).run(suite)
    
    def test_history_counting_fa(self):
        """history_counting_fa"""
        suite = unittest.TestLoader().loadTestsFromTestCase(test_HistoryCountingFA)
        unittest.TextTestRunner(verbosity=1).run(suite)
    
    def test_hybrid_fa(self):
        """hybrid_fa"""
        suite = unittest.TestLoader().loadTestsFromTestCase(test_hybrid_fa)
        unittest.TextTestRunner(verbosity=1).run(suite)
    
    def test_j_history_fa(self):
        """j_history_fa"""
        suite = unittest.TestLoader().loadTestsFromTestCase(test_j_history_fa)
        unittest.TextTestRunner(verbosity=1).run(suite)
        
    def test_j_hybrid_fa(self):
        """j_hybrid_fa"""
        suite = unittest.TestLoader().loadTestsFromTestCase(test_JHybridFA)
        unittest.TextTestRunner(verbosity=1).run(suite)
        
    def test_nfa_split(self):
        """nfa_split"""
        suite = unittest.TestLoader().loadTestsFromTestCase(test_nfa_split)
        unittest.TextTestRunner(verbosity=1).run(suite)
        
    def test_phf_dfa(self):
        """phf_dfa"""
        suite = unittest.TestLoader().loadTestsFromTestCase(test_PHF_DFA)
        unittest.TextTestRunner(verbosity=1).run(suite)
        
    def test_sindhu_prasana_nfa(self):
        """sindhu_prasana_nfa"""
        suite = unittest.TestLoader().loadTestsFromTestCase(test_sindhu_prasana_nfa)
        unittest.TextTestRunner(verbosity=1).run(suite)
        
    def test_sourdis_bispo_nfa(self):
        """sourdis_bispo_nfa"""
        suite = unittest.TestLoader().loadTestsFromTestCase(test_sourdis_bispo_nfa)
        unittest.TextTestRunner(verbosity=1).run(suite)


if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(run_all_tests)
    unittest.TextTestRunner(verbosity=1).run(suite)

