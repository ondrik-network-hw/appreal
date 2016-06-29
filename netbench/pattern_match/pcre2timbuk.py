#!/usr/bin/env python

import sys
import getopt
from netbench.pattern_match import b_automaton
from netbench.pattern_match import parser

def usage():
    print sys.argv[0] + " -h | -i <file> -o <file> [-d <file>] [-S <style>] [-s]"
    print "Parameters:"
    print "-h | --help                   - show this help"
    print "-i <file> | --input <file>    - file with set of PCRE expressions one per line"
    print "-o <file> | --output <file>   - file for resulting automaton encoded in Timbuk format"
    print "-d <file> | --display <file>  - save image of the automaton into this file, graphviz/dot format is used."
    print "-S <style> | --style <style>  - create nondeterministic automaton of specified type <style>:"
    print "                                  nfa - nodeterministic finite automaton"
    print "                                   pa - nodeterministic position (glushkov) automaton"
    print "                                  dpa - nondeterministic dual position (glushkov) automaton"
    print "                                  Defaut value is nfa."
    print "-s                            - Use simple mode. In simple mode only automata with "
    print "                                character symbols are supported and the symbols are "
    print "                                encoded as trasition labels in format 'sXX', where "
    print "                                XX is hexadecimal value of input symbol. If simple "
    print "                                mode is disabled, the any supported automata symbol "
    print "                                can be used and its label is created by its function"
    print "                                export_symbol(). Simple mode can not be used with "
    print "                                automata styles pa or dpa as current implementation "
    print "                                does not support pa or dpa without character classes."
    print "                                Actually it can be used but the automaton doesn't conform"
    print "                                to specification of pa or dpa."

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:d:si:S:", ["help", "output=", "display=", "simple", "input=", "style="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err)
        usage()
        sys.exit(1)
    output_file = None
    input_file = None
    display_file = None
    simple = False
    fsm_style = "nfa"
    for o, a in opts:
        if o == "-s":
            simple = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-o", "--output"):
            output_file = a
        elif o in ("-i", "--input"):
            input_file = a
        elif o in ("-d", "--display"):
            display_file = a
        elif o in ("-S", "--style"):
            fsm_style = a.lower()
        else:
            assert False, "unhandled option " + o
    
    if (input_file == None or output_file == None):
        print "Input file with PCRE patterns and output file for FSM must be specified!"
        sys.exit(1)

    fsm = b_automaton.b_Automaton()
    p = parser.parser("pcre_parser")
    p.load_file(input_file)
    fsm.create_by_parser(p)
    
    if fsm_style == "nfa":
        fsm.remove_epsilons()
    elif fsm_style == "pa":
        fsm.thompson2glushkov()
    elif fsm_style == "dpa":
        fsm.thompson2reverse_glushkov()
    else:
        print "Unsupported automaton type: " + fsm_style
        print "Supported automata styles are: nfa, pa, dpa"
        print "See " + sys.argv[0] + " -h for details"
        sys.exit(1)
        
    if simple == True:
        fsm.remove_char_classes()
    fsm.save_to_timbuk(output_file, simple)
    if display_file != None:
        fsm.show(display_file, " ")

if __name__ == "__main__":
    main()
