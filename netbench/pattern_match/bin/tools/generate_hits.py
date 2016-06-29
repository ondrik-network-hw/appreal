#! /usr/bin/env python
###############################################################################
#  generate_hits.py: Experimental script for generating strings from RE
#  Copyright (C) 2010 Brno University of Technology, ANT @ FIT
#  Author(s): Milan Dvorak <xdvora66@stud.fit.vutbr.cz>
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

from netbench.pattern_match.b_automaton import b_Automaton
from netbench.pattern_match.parser import parser
from netbench.pattern_match.pcre_parser import pcre_parser
from netbench.pattern_match.b_dfa import b_dfa
from netbench.pattern_match.algorithms.phf_dfa.phf_dfa import PHF_DFA
import sys, subprocess
from netbench.pattern_match.library.bitstring import BitStream, BitArray
from netbench.pattern_match.library.jenkins import jenkins_compress
from netbench.pattern_match.library.bdz import bdz
from netbench.pattern_match.nfa_data import nfa_data
from netbench.pattern_match.b_nfa import b_nfa
from netbench.pattern_match import b_symbol

import os
import random
import copy
import cProfile
from pprint import pprint

"""
    Experimental script for generating strings from given regular expressions.
    Rules are randomly selected from file as first parameter.
    Number of generated strings is specified as second parameter.
    Output format for one string is as follows:
    Rule: N
    generated_text
    -------------------------------------------------------------------------
"""

def generate_text(rule):
    aut = b_nfa()
    par = parser("pcre_parser")
    par.set_text(rule)
    if not aut.create_by_parser(par):
        return ""
    aut.remove_epsilons()
    aut.search("a")
    state = 0
    string = ""
    while not state in aut._automaton.final:
        trans = aut._mapper[state]
        rnd1 = random.randint(0, len(trans) - 1)
        sym =  aut._automaton.alphabet[list(trans)[rnd1][0]]
        if sym.get_type() == b_symbol.io_mapper["b_Sym_char_class"]:
            chars = sym.charClass
        else:
            chars = sym.char
        state = list(trans)[rnd1][1] 
        rnd2 = random.randint(0, len(chars) - 1)
        string += list(chars)[rnd2]
    if 1 not in aut.search(string):
        print "FAIL"
    return string

if len(sys.argv) != 3 or '-h' in sys.argv:
    print "./generate_hits.py rules.txt count"
    exit()
rules = open(sys.argv[1], 'rb').readlines(1)
i = 0
count = int(sys.argv[2])
while i < count:
    i += 1
    rnd = random.randint(0, len(rules) - 1)
    rule = rules[rnd]
    rule_num = rnd
    text = generate_text(rule)
    print "Rule:", rule_num
    print text
    print '-' * 80
