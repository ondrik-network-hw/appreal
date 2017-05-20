#!/usr/bin/env python

###############################################################################
#  Copyright (C) 2010 Brno University of Technology, ANT @ FIT
#  Based on pcre2timbuk.py
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
import sys
import getopt
from netbench.pattern_match import b_automaton
from netbench.pattern_match import nfa_reductions
from netbench.pattern_match import b_dfa
from netbench.pattern_match import parser

def usage():
    print sys.argv[0] + " -h | -i <file> -o <file> [-d <file>] [-S <style>] [-s]"
    print "Parameters:"
    print "-h | --help                   - show this help"
    print "-i <file> | --input <file>    - file with set of PCRE expressions one per line"
    print "-o <file> | --output <file>   - file for resulting automaton encoded in FA format"
    print "-d <file> | --display <file>  - save image of the automaton into this file, graphviz/dot format is used."
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
        else:
            assert False, "unhandled option " + o

    if (input_file == None or output_file == None):
        print "Input file with PCRE patterns and output file for FSM must be specified!"
        sys.exit(1)

    fsm = b_automaton.b_Automaton()
    p = parser.parser("pcre_parser")
    p.load_file(input_file)
    fsm.create_by_parser(p)

    fsm.remove_epsilons()

    print "State num: ", fsm.get_state_num()
    if simple == True:
        fsm.remove_char_classes()
    fsm.save_to_FA_format(output_file)
    if display_file != None:
        fsm.show(display_file, " ")

if __name__ == "__main__":
    main()
