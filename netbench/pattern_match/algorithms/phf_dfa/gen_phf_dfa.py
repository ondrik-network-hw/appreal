from netbench.pattern_match import sym_char, sym_char_class
from netbench.pattern_match import pcre_parser
from netbench.pattern_match.b_automaton import b_Automaton
from netbench.pattern_match.nfa_data import nfa_data
#from netbench.pattern_match.b_dfa import b_dfa
from phf_dfa import PHF_DFA
import sys


def ProcessRule(parser):
    f = open("out.out","a")
    N_Automaton = b_Automaton()
    N_Automaton.create_from_nfa_data(parser.get_nfa())
    N_Automaton.get_automaton().Show("test_NFA.dot")
    print("Automata joined")
    D_Automaton = PHF_DFA()
    D_Automaton.create_from_nfa_data(N_Automaton.get_automaton())
    print("Determinising...")
    D_Automaton.resolve_alphabet()
   # D_Automaton.removeCharClasses()
   # D_Automaton.reduce_alphabet()
    D_Automaton.determinise(states_limit = 10000)
    print("Minimising...")
    D_Automaton.minimise()   #Co to vlastne vypisuje?
    D_Automaton.get_automaton().Show("test_min_dfa.dot")
    stride0 = str(D_Automaton.get_state_num())+"/"+str(D_Automaton.get_trans_num())+"|"
    f.write(stride0)
    D_Automaton.stride_2()
    stride2 = str(D_Automaton.get_state_num())+"/"+str(D_Automaton.get_trans_num())+"|"
    f.write(stride2)
    D_Automaton.stride_2()
    stride4 = str(D_Automaton.get_state_num())+"/"+str(D_Automaton.get_trans_num())+"|"
    f.write(stride4)
    #D_Automaton.stride_2()
    #stride8 = str(D_Automaton.get_state_num())+"/"+str(D_Automaton.get_trans_num())+"|"
    #f.write(stride8)
    f.write("\n")
    f.close()
   # D_Automaton.set_table_parameters((5,13))
   # if(D_Automaton.generate_PHF_table() == False):
   #    print("Failed")
   #    exit()
#    D_Automaton.search("ahojdfgffskf sdfgsdfgs dfg jkgsdgcjgfsdfg admin_root=php")
   # D_Automaton.search(Data)
 # except Exception:
 #    print("GENERATED EXCEPTION")
    #D_Automaton.printConfFile("/home/galloth/configuration");
    print("")

FileName= "../../rules/Moduly/web-php.rules.pcre"
#FileName= "../../rules/Moduly/together.pcre"
#FileName="ahoj.pcre"
parser = pcre_parser.pcre_parser()
parser.load_file(FileName)
i=0;

DataFileName = "data.tmp"
DataFile=open(DataFileName,"rb")
Data = DataFile.read()

#while(i<1):
ProcessRule(parser)
while (parser.next_line()):
    i = i+1
    print("Rule: ",i);
    ProcessRule(parser)
