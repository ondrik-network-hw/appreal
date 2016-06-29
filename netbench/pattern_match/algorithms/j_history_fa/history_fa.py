############################################################################
#  history_fa.py: Module for PATTERN MATCH algorithm History Finite Automat
#  Copyright (C) 2010 Brno University of Technology, ANT @ FIT
#  Author(s): Jaroslav Suchodol
############################################################################
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
#  This software or firmware is provided ``as is'', and any express or
#  implied warranties, including, but not limited to, the implied warranties
#  of merchantability and fitness for a particular purpose are disclaimed.
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

"""Module for pattern match: History based Finite Automaton algorithm."""

# Based on: "Curing Regular Expressions Matching Algorithms from Insomnia,
# Amnesia, and Acalculia", ISBN: 978-1-59593-945-6
# URL: http://portal.acm.org/citation.cfm?id=1323574&dl=GUIDE,

# Useful methods (like get_state_num()) may not be overload.

from netbench.pattern_match import sym_char
from netbench.pattern_match.parser import parser
from netbench.pattern_match.b_dfa import b_dfa
import os
import re
import tempfile
import sys
import math

class history_fa(b_dfa):
    """
        Class for History based Finite Automaton.
    """

    def __init__(self):
        """
            Construct basic items.
        """

        b_dfa.__init__(self)

    def compute(self, file_name):
        """
            Fuction for make History based FA from RE in file_name.

            :param file_name: Name of input file
            :type file_name: string
        """
        self._make_his_fa(file_name)
        self._compute = True

    def report_memory_optimal(self):
        """
            Report consumed memory in bytes. Optimal mapping algorithm is used \
            (with oracle). Basic algorithm for this variant of mapping is:     \
            M = \|transitions\| * ceil(log(\|states\|, 2) / 8).
            For History is: basic + Mem(Flags) + (Tran*Flags*2).
            
            :returns: Returns number of bytes.
            :rtype: int
        """
        tr_len = len(self._automaton.transitions)
        st_len = len(self._automaton.states)
        return int(tr_len * math.ceil(math.log(st_len, 2) / 8)) + \
            (self.flag_c / 8) + (tr_len*(self.flag_c)*3/8);
    
    def report_memory_naive(self):
        """
            Report consumed memory in bytes. Naive mapping algorithm is used \
            (2D array). Basic algorithm for this variant of mapping is:      \
            M = \|states\| * \|alphabet\| * ceil(log(\|states\| + 1, 2) / 8)
            For History is: basic + Mem(Flags) + (State * Sym * Flags * 2)
            
            :returns: Returns number of bytes.
            :rtype: int
        """
        st_len = len(self._automaton.states)
        al_len = len(self._automaton.alphabet)
        return int(st_len * al_len * math.ceil(math.log(st_len + 1, 2) / 8)) +\
            (self.flag_c / 8) + (st_len*al_len*self.flag_c*3/8);

    def _make_his_fa(self, file_name):
        """
            Fuction for make History based FA from RE in FileName.

            :param file_name: Name of input file
            :type file_name: string
        """

    # Discover before part, according .* or .{m} like pattern,
    # and change .{m} to .* like.
        b = []    # keys for closure states
        cl = []   # closure NFA states
        cn = []   # counters for counting constraint
        cn_i = [] # counters index
        fr = open(file_name, "r")
        tmp = tempfile.NamedTemporaryFile(delete=False)
        for line in fr.readlines():
            # remove '\n' from end of line
            line = line.rsplit('\n', 1)[0]
            pattern = re.compile(r"""
            (?<=[^/])[.](?=[*])   # for like .*
            (?![^[]*?\])          # because of .* not in [.*]
            |
            \[\^
            .*?                   # for like [^abc]*
            (?<!\\)\](?=[*])
            (?![^[]*?\])
            |
            [.](?=[{])            # for like .{15}
            (?![^[]*?\])
            |
            .(?=[{])              # for like a{15}
            (?![^[]*?\])
            |
            \[\^?                 # for like [abc]{15} or [^abc]{15}
            .*?
            (?<!\\)\](?=[{])
            (?![^[]*?\])
            """, re.X)
            # split line to before (split[0]) and after (split[1]) part
            split = re.split(pattern, line, maxsplit=1)
            # remove .* from begin of pattern
            if split[0].find(".*") != -1:
                split[0] = '/' + split[0][split[0].find(".*") + 2:]
            # line contain .* or .{m} like pattern
            if len(split) == 2:
                b.append(split[0][1:])
                cl.append([])
                if split[1][0] == '{':
                    cn.append(int(split[1][1:split[1].find('}', 1)]))
                    cn_i.append(len(cn) - 1)
                    # replace .{m} like to .* like
                    line = line[:line.find(split[1])] + '*' + \
                    split[1][split[1].find('}') + 1:]
                else :
                    cn.append(-1)
            # append line to tmp file
            tmp.write(line + '\n')
        fr.close()
        tmp.close()
    # Make DFA.
        # Parse input file
        par = parser("pcre_parser")
        par.load_file(tmp.name)
        # Make automat from RE which was in input file
        self.create_by_parser(par)
        # Make Deterministic FA
        self.determinise(True)
        # remove temporary file
        os.unlink(tmp.name)
    # Adjustment _state_representation list.
        m = list(min(self._state_representation[1:]))
        r = self._state_representation
        for i in range(0, len(r)):
            for x in m:
                if x in r[i]:
                    r[i].remove(x)
            r[i] = list(r[i])
    # Discover closure state.
        a = self._automaton
        cur_state = a.start
        # sort transitions
        sort = {} # sorted transitions
        for s in range(0, len(a.states)):
            sort[s] = []
        for t in a.transitions:
            sort[t[0]].append(t[1:])
        for i in range(0, len(b)):
            for c in b[i]:
                for t in sort[cur_state]:
                    prev_state = cur_state
                    # single character
                    if isinstance(a.alphabet[t[0]], sym_char.b_Sym_char):
                        if a.alphabet[t[0]].char == c:
                            cur_state = t[-1]
                            # skip other transitions
                            break
                    # character range
                    else :
                        if c in a.alphabet[t[0]].charClass:
                            cur_state = t[-1]
                            # skip other transitions
                            break
            # remove closure transition
            a.transitions.remove((prev_state, t[0], t[1]))
            cl[i] = r[cur_state][-1] + 1
            # append closure history transition
            if cn[i] == -1:
                a.transitions.add((prev_state, t[0], t[1], '|',
                -2, i))
            else :
                # counting constraint
                a.transitions.add((prev_state, t[0], t[1], '|',
                -2, i, cn[i], cn_i.index(i)))
            cur_state = a.start
    # Discover fading states and their overlap states.
        f = []    # fading states (DFA)
        f_d = {}  # fading states in dictionary, key is string before
        o = []    # overlap states according fading states (DFA)
        for i in range(0, len(b)):
            f_d[b[i]] = []
            c_s = cl[i]   # c_s is closure states (NFA)
            for j in range(0, len(r)):
                if c_s in r[j]:
                    over = list(r[j])
                    for s in cl:
                        if s in over:
                            over.remove(s)
                    # append only states which have overlap state
                    if over in r:
                        if j not in f:
                            f.append(j)
                            f_d[b[i]].append(j)
                            # append overlap DFA state
                            o.append(r.index(over))
    # Remove fading states.
        for s in f:
            del a.states[s]
        # delete deleted states from finite states
        for s in list(a.final):
            if s in f:
                a.final.remove(s)
        # change numbering for states
        a_s = sorted(a.states.keys()) # aux. states
        tmp = {}
        for k in a_s:
            tmp[a_s.index(k)] = a.states[k]
        a.states = tmp
        # change numbering for final states
        tmp = set()
        for s in a.final:
            tmp.add(a_s.index(s))
        a.final = tmp
        # change numbering for start state
        a.start = a_s.index(a.start)
    # Change fading transitions.
        # transition is tuple of 3 numbers plus history properties
        # like: (S, A, D)
        # S is source state
        # A is alphabet (transition char)
        # D is destination state
        # like: (S, A, D, -2, f_i, '|', -4, f_i)
        # -2 is flag which is needed for execution transition
        # f_i is flag index
        # '|' separating needed properties for execution tran. of properties
        # which will be set after tran. finished
        # -4 flag which will be set after tran. finish
        # f_i is flag index
        # flags: -2 = set, -3 = must be set, -4 = reset, -5 = must be reset
        #c_s_D = []  # closure state DFA !
        #print "cl:",cl
        #print "r:",r
        #for c_s_N in cl:
            #print "c_s_N:",c_s_N
            #c_s_D.append(r.index([c_s_N]))
        aux = set()
        d = {}    # transitions for pruning process
        tmp = []  # helpful list for pruning process
        tmp_t = []  # helpful list for pruning process
        for t in a.transitions:
            t = list(t)
            # destination state is fading state
            if t[2] in f:
                # source state is fading state
                if t[0] in f:
                    # this transition only if is set flag (=)
                    # append must be set flag
                    for i in range(0, len(b)):
                        if t[0] in f_d[b[i]]:
                            t.append(-3)
                            t.append(i)
                            if cn[i] != -1:
                                # append counting constraint counter 0
                                t.append(0)
                                t.append(cn_i.index(i))
                    t.append('|')
                    # change to overlap state
                    t[0] = o[f.index(t[0])]
                # source state is non fading
                else :
                    if '|' not in t:
                        t.append('|')
                    # append set flag
                    for i in range(0, len(b)):
                        if t[2] in f_d[b[i]]:
                            t.append(-2)
                            t.append(i)
                            if cn[i] != -1:
                                # append counting constraint set counter
                                t.append(cn[i])
                                t.append(cn_i.index(i))
                # change des. state to overlap state
                t[2] = o[f.index(t[2])]
            # source state is fading state
            elif t[0] in f:
                # append must be set flag
                for i in range(0, len(b)):
                    if t[0] in f_d[b[i]]:
                        t.append(-3)
                        t.append(i)
                        if cn[i] != -1:
                            # append counting constraint counter 0
                            t.append(0)
                            t.append(cn_i.index(i))
                t.append('|')
                # destination state is non-fading state
                # reset flag
                for i in range(0, len(b)):
                    if t[0] in f_d[b[i]]:
                        t.append(-4)
                        t.append(i)
                        if cn[i] != -1:
                            # append counting constraint reset counter
                            t.append(0)
                            t.append(cn_i.index(i))
                # change to overlap state
                t[0] = o[f.index(t[0])]
            # change numbering
            t[0] = a_s.index(t[0])
            t[2] = a_s.index(t[2])
            aux.add(tuple(t))
            # for pruning process
            if len(t) == 3:
                t_a = t + ['|']
            else :
                t_a = t[0:3] + t[t.index('|'):]
            t_a = tuple(t_a)
            if t_a in tmp:
                # select similarly transitions
                if not d.has_key(t_a):
                    d[t_a] = [tmp_t[tmp.index(t_a)]]
                if t not in d[t_a]:
                    d[t_a].append(t)
            else :
                tmp.append(t_a)
                tmp_t.append(t)
        a.transitions = aux
    # Pruning process (remove similarly transitions).
        for key in d.keys():
            # exist transition without condition
            if list(key[0:3]) in d[key]:
                # keep only this transition
                d[key].remove(list(key[0:3]))
                for t in d[key]:
                    a.transitions.remove(tuple(t))
            else :
                # find set and remove all her subset
                c = []    # auxiliary, conditions for tran.
                c_l = []  # auxiliary, conditions length
                tran = [] # auxiliary, original tran.
                for t in d[key]:
                    aux = []
                    for i in range(3, t.index('|'), 2):
                        aux += [tuple(t[i:i+2])]
                    c.append(aux)
                    c_l.append(len(aux))
                    tran.append(tuple(t))
                while len(c) != 0:
                    s = c[c_l.index(min(c_l))]  # set
                    for t_c in list(c):
                        flag = 1
                        for x in s:
                            if x not in t_c:
                                flag = 0
                                break
                        # tran. fall into this set
                        if flag and s != t_c:
                            # remove subset tran.
                            del c_l[c.index(t_c)]
                            a.transitions.remove(tran[c.index(t_c)])
                            c.remove(t_c)
                    # remove set (only from c)
                    del c_l[c.index(s)]
                    c.remove(s)
    # Append must be reset flag.
        c = {}  # tran. which have must be set flag
        c_i = {}# indexes of flags
        n = {}  # tran. which have not must be set flag
        for s in range(0, len(a.states)):
            c[s] = []
            c_i[s] = []
            n[s] = []
        for t in a.transitions:
            added = False
            t = list(t)
            # must be set tran.
            if len(t) > 3 and (t.index('|') - 3) > 0:
                tmp = []
                for i in range(3, t.index('|'), 2):
                    if t[i] == -3:
                        tmp.append(t[i+1])
                if tmp != []:
                    if tuple(t) not in c[t[0]]:
                        c[t[0]].append(tuple(t))
                        c_i[t[0]].append(tmp)
                    added = True
            # not must be set tran.
            if not added:
                if tuple(t) not in n[t[0]]:
                    n[t[0]].append(tuple(t))
        for s in range(0, len(a.states)):
            for t in c[s]:
                # discover tran. char
                if isinstance(a.alphabet[t[1]], sym_char.b_Sym_char):
                    chars = list(a.alphabet[t[1]].char)
                else :
                    chars = list(a.alphabet[t[1]].charClass)
                for t_n in list(n[s]):
                    if isinstance(a.alphabet[t_n[1]], sym_char.b_Sym_char):
                        chars_n = list(a.alphabet[t_n[1]].char)
                    else :
                        chars_n = list(a.alphabet[t_n[1]].charClass)
                    for char in chars_n:
                        if char in chars:
                            # remove bad tran.
                            a.transitions.remove(t_n)
                            n[s].remove(t_n)
                            # append must be reset flag
                            t_n = list(t_n)
                            if '|'  not in t_n:
                                for i in c_i[s][c[s].index(t)]:
                                    t_n.append('-5')
                                    t_n.append(i)
                                t_n.append('|')
                            else :
                                for i in c_i[s][c[s].index(t)]:
                                    t_n.insert(3, '-5')
                                    t_n.insert(4, i)
                            a.transitions.add(tuple(t_n))
                            break
    # Count of flags and counters.
        self.flag_c = len(b)
        self.ctr_c = len(cn_i)
        self.cn_i = cn_i
    # Add automat flag.
        a.Flags["History FA"] = True

    def save_to_file(self, file_name):
        """
            Make file which represent the History automat.
            This file will be input into algorithm written in C language.

            :param file_name: Name of output file
            :type file_name: string
        """

        a = self._automaton
        fw = open(file_name, 'w')

        # write COUNT OF STATES
        fw.write(str(len(a.states)) + '\n')
        # write START STATE
        fw.write(str(a.start) + '\n')
        # write TRANSITIONS
        sort = {} # sorted transitions
        for s in range(0, len(a.states)):
            sort[s] = []
        for t in a.transitions:
            sort[t[0]].append(t[1:])
        for s in range(0, len(a.states)):
            fw.write("t_c: " + str(len(sort[s])) + '\n')
            for t in sort[s]:
                if isinstance(a.alphabet[t[0]], sym_char.b_Sym_char):
                    fw.write("c_c: 1, d: " + str(t[1]) + '\n')
                    fw.write(str(ord(a.alphabet[t[0]].char)) + "|\n")
                else :
                    fw.write("c_c: " + \
                    str(len(a.alphabet[t[0]].charClass)) + \
                    ", d: " + str(t[1]) + '\n')
                    chars = ""
                    for c in a.alphabet[t[0]].charClass:
                        chars += str(ord(c)) + '|'
                    fw.write(chars + '\n')
                # conditions for transition
                if len(t) == 2:
                    fw.write("n_c: 0, a_c: 0\n")
                else :
                    fw.write("n_c: " + str((t.index('|') - 2) / 2) + ", a_c: " \
                            + str((len(t) - t.index('|')) / 2) + "\n")
                    # write needed conditions
                    for i in range(2, t.index('|'), 2):
                        fw.write(str(t[i]) + "->" + str(t[i+1]) + '|')
                    fw.write('\n')
                    # write after part
                    for i in range(t.index('|') + 1, len(t), 2):
                        fw.write(str(t[i]) + "->" + str(t[i+1]) + '|')
                    fw.write('\n')
        # write FINAL STATES
        final = ""
        for s in a.final:
            final += str(s) + '|'
        fw.write(str(len(a.final)) + '\n' + final + '\n')
        # write count of flags and counters
        fw.write("flags: " + str(self.flag_c) + '\n')
        fw.write("counters: " + str(self.ctr_c) + '\n')
        f_i = ""
        for i in self.cn_i:
            f_i += str(i) + '|'
        fw.write(f_i + '\n')


