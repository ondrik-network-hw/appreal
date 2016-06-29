from netbench.pattern_match import sym_char, sym_char_class
from netbench.pattern_match import pcre_parser
from netbench.pattern_match.b_automaton import b_Automaton
from netbench.pattern_match.nfa_data import nfa_data
#from netbench.pattern_match.b_dfa import b_dfa
from phf_dfa import PHF_DFA

#FileName= "../../rules/Moduly/web-client.rules.pcre"
FileName= "../../rules/Moduly/web-php.rules.pcre"
parser = pcre_parser.pcre_parser()
parser.load_file(FileName)

print("Joining...")
N_Automaton = b_Automaton()
N_Automaton.create_from_nfa_data(parser.get_nfa())

#while (parser.next_line()):
#   N_Automaton.join(parser.get_nfa())

N_Automaton.get_automaton().Show("test_NFA.dot")
print("Automata joined")
D_Automaton = PHF_DFA()
D_Automaton.create_from_nfa_data(N_Automaton.get_automaton())
print("Determinising...")
D_Automaton.determinise(states_limit = 10000)
print("Minimising...")
D_Automaton.minimise()   #Co to vlastne vypisuje?
D_Automaton.get_automaton().Show("test_min_dfa.dot")

D_Automaton.get_automaton().SaveToFile("temp_automaton")

print("striding...")
D_Automaton.reduce_alphabet()
D_Automaton.stride_2()
D_Automaton.get_automaton().Show("test_multi_dfa.dot")
print("generating PHF...")
D_Automaton.generate_PHF_table()

D_Automaton1 = PHF_DFA()
Temp = nfa_data()
Temp = Temp.LoadFromFile("temp_automaton")
D_Automaton1.create_from_nfa_data(Temp)
D_Automaton1.reduce_alphabet()
D_Automaton1.stride_2()
D_Automaton1.get_automaton().Show("test_multi_dfa.dot")
print("generating PHF...")
D_Automaton1.generate_PHF_table()

