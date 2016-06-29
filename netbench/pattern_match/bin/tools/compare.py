#! /usr/bin/env python
###############################################################################
#  compare.py: Script for comparing matching results of PHF_DFA and PCRE
#  Copyright (C) 2012 Brno University of Technology, ANT @ FIT
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
from netbench.pattern_match.library.bitstring import BitStream, BitArray
from netbench.pattern_match.library.jenkins import jenkins_compress
from netbench.pattern_match.library.bdz import bdz
from netbench.pattern_match.nfa_data import nfa_data
from netbench.pattern_match.b_nfa import b_nfa

import sys, subprocess
import os
import copy
import cProfile
from pprint import pprint
from optparse import OptionParser, OptionGroup

"""
    Script for comparing search results of PCRE library (pcregrep) and faulty  \
    algorithm, DFA with PHF and faulty transition table in this case.          \
    Inputs are file with regular expressions and input directory with flows    \
    and/or packets. Result is number of false negatives, false positives and   \
    computed values of precision, recall and F-measure.
"""

def parse_rule(pcre_rule):
    """
        Return tuple of regular expressions (without '/') and PCRE parameters  \
        transformed into pcregrep arguments.
    """
    end = pcre_rule.rfind('/')
    rule = pcre_rule[1:end] # regexp between slashes
    options = pcre_rule[end+1:-1] # options without '/' and '\n'
    params = ""
    count = 0
    if 'm' in options:
        params += ' -M'
        count += 1
    if 's' in options:
        params += ' -S'
        count += 1
    if 'i' in options:
        params += ' -i'
        count += 1
    if count != len(options):
        print >> sys.stderr, "UNKNOWN option in ", options

    return (rule, params)

def compare_results(results):
    """
        Compare results of PCRE, PHF_DFA and possibly also PCRE per packet.    \
        Number of total packets, errors and hits is returned.
    """
    count = 0 # total number of packets
    hits = 0  # hits - number of matched packets
    fp = 0
    fn = 0
    fp2 = 0 # false positives
    fn2 = 0 # false negatives
    ppp = 0 # per pacpet fp
    ppn = 0 # per packet fn
    for key, res in results.iteritems():
        count += 1
        hits += sum(res[1])
        if res[0] == res[1]:
            text = "OK "
        elif sum(res[0]) > sum(res[1]):
            fp += 1
            text = "FP "
        elif sum(res[0]) < sum(res[1]):
            fn += 1
            text = "FN "
        else:
            text = "WTF "
        for a,b in zip(res[0], res[1]):
            if a > b:
                fp2 += 1
            if b > a:
                fn2 += 1
        for a,b in zip(res[1], res[2]):
            if a > b:
                ppp += 1
            if b > a:
                ppn += 1
        if DEBUG > 1:
            print text,
            print key + str(res)
    return(hits, fp2, fn2, count, ppp, ppn)

def test():
    """
        Run searching using pcregrep and PHF_DFA. Prints out the results.
    """
    # parse options
    usage = "usage: %prog rules.pcre pcap_dir/ [options]"
    optparser = OptionParser(usage=usage)
    optparser.add_option("-O", "--outputfile", dest="resultfile", help="output file for results, default is stdout")
    optparser.add_option("-P", "--PerPacket", dest="PerPacket", action="store_true", default=False,
                      help="compare nonfaulty matching for flows and packets, faulty algorithm is used only with flows")
    optparser.add_option("-s", "--showprogress", dest="progress", action="store_true", default=False,
                      help="show progress of computation")
    optparser.add_option("-C", "--count", dest="maxiter", type="int", default="1", help="number of test iterations")
    optparser.add_option("-F", "--faulty", dest="FAULTY", type="int", default="0", help="number of bits for compress hash, default is 0 (no faulty transitions)")
    optparser.add_option("-D", "--debuglevel", dest="DEBUG", type="int", default="0", help="debug output level (0-2)")
    optparser.add_option("-S", "--savefile", dest="savefile", default="", metavar="FILE", help="save nfa_data in FILE")
    optparser.add_option("-L", "--loadfile", dest="autfile", default="", metavar="FILE", help="load nfa_data from FILE")
    optparser.add_option("-N", "--nonfaulty", dest="NonFaulty", action="store_true", default=False,
                      help="try to generate PHF table without collisions, therefore ensure nonfaulty matching. Experimental code. "
                            "May take a long time with small compress hash output.")
    (options, args) = optparser.parse_args()

    global FAULTY, DEBUG
    if len(args) != 2:
       print "You must specify rules.pcre and pcap_dir/"
       optparser.print_usage()
       exit(1)
    rulesfile, inputdir = args
    PerPacket, resultfile,  maxiter, autfile, savefile, FAULTY, DEBUG = options.PerPacket, options.resultfile, options.maxiter, options.autfile, options.savefile, options.FAULTY, options.DEBUG
    progress = options.progress
    NonFaulty = options.NonFaulty
    
    if inputdir[-1] == "/":
        inputdir = inputdir[:-1] # remove '/' from the end
    rules = open(rulesfile, 'rb')
    if PerPacket:
        packetdir = inputdir + "/packets"
        inputdir = inputdir + "/flows"
    if resultfile:
        sys.stdout = open(resultfile, 'a')
    totalhits, totalfp, totalfn = (0, 0, 0)
    iter = 0    
    while iter != maxiter:
        if progress:
            print >>sys.stderr, "\r", ' '*80, '\r',"pcregrep",
        if not iter:
            # prepare pcregrep
            p = subprocess.Popen("cd pcre-8.20/ && make pcregrep", shell=True, stdout=subprocess.PIPE)
            p.wait()
            results = dict()
        file_list = list()
        rule_count = len(open(rulesfile).readlines())
        for root, dirs, files in os.walk(inputdir):
            for i in files:
                i = os.path.join(root, i)
                file_list.append(i)
                if not iter:
                    results[i] = [rule_count*[0],rule_count*[0],rule_count*[0]]
                else:
                    results[i][0] = rule_count*[0]
        #results = init_results
        rule_num = 0
        grep_reg_exp = "grep_reg_exp." + str(os.getpid())
        for rule in rules:
            if not iter:
                if DEBUG:
                    print rule,
                (grep_rule, grep_params) = parse_rule(rule)
                f = open(grep_reg_exp, 'w')
                f.write(grep_rule)
                f.close()
                p = subprocess.Popen("pcre-8.20/pcregrep --buffer-size 50000 --color=auto -N ANYCRLF" + grep_params + " -r -l -f " + grep_reg_exp + " " + inputdir, shell=True, stdout=subprocess.PIPE)
                p.wait()
                for out in p.stdout:
                    item = out.split()[0]
                    results[item][1][rule_num] = 1
                if PerPacket:
                    p = subprocess.Popen("pcre-8.20/pcregrep --buffer-size 50000 --color=auto -N ANYCRLF" + grep_params + " -r -l -f " + grep_reg_exp + " " + packetdir, shell=True, stdout=subprocess.PIPE)
                    p.wait()
                    for out in p.stdout:
                        item =  inputdir + "/" + out.split()[0].split("-")[1].replace("_", "/")
                        results[item][2][rule_num] = 1

            rule_num += 1
        try:
            os.remove(grep_reg_exp)
        except:
            pass
        if progress:
            print >>sys.stderr, "\r", ' '*80, '\r', "create automaton",
        #aut = b_Automaton()
        aut = PHF_DFA()
        if autfile:
            aut.create_from_nfa_data(nfa_data().load_from_file(autfile))
        else:
            par = parser("pcre_parser")
            #par.set_text(rule)
            par.load_file(rulesfile)
            aut.create_by_parser(par)
            if DEBUG:
                aut.show("NFA.dot")
            #aut.remove_epsilons()
            if progress:
                print >>sys.stderr, "\r", ' '*80, '\r', "resolve alphabet",
            aut.resolve_alphabet()
            if progress:
                print >>sys.stderr, "\r", ' '*80, '\r', "determinise",
            aut.determinise()
            if progress:
                print >>sys.stderr, "\r", ' '*80, '\r', "minimise",
            aut.minimise()
            if DEBUG:
                aut.show("DFA.dot")
            if savefile:
                aut._automaton.save_to_file(savefile)
        aut._automaton1 = aut._automaton
        aut.set_table_parameters((20,10))
        if DEBUG > 1:
            print "Without fallback state:"
            print "Symbols:", len(aut._automaton.alphabet)
            print "States:", len(aut._automaton.states)
            print "Transitions:", aut.get_trans_num(), float(aut.get_trans_num()) / (aut.get_state_num() * aut.get_alpha_num()) * 100, "%"
        if isinstance(aut, PHF_DFA):
            if progress:
                print >>sys.stderr, "\r", ' '*80, '\r', "generate PHF",
            if aut.get_trans_num() == (aut.get_state_num() * aut.get_alpha_num()):
                aut.enable_fallback_state(warning=False)
            if FAULTY:
                aut.enable_faulty_transitions(FAULTY)
                if NonFaulty:
                    aut.enable_faulty_check()
            aut.compute()
            if DEBUG:
                print "Fallback state:", aut.fallback_state
                print "Symbols:", len(aut._automaton.alphabet)
                print "States:", len(aut._automaton.states)
                print "Transitions:", aut.get_trans_num(), float(aut.get_trans_num()) / (aut.get_state_num() * aut.get_alpha_num()) * 100, "%"
        count = 1
        all = len(file_list)
        if progress:
            print >> sys.stderr, '\r' + 80*' ' + '\r',
        for f in file_list:
            # progress
            if progress:
                print >> sys.stderr, '\r',
                print >> sys.stderr, str(iter+1)+'/'+str(maxiter)+ ":", count, '/', all,
#                sys.stderr.flush()
            count += 1
            data = open(f, 'rb').read()
            results[f][0] = aut.search(data)
        if progress:
            print >>sys.stderr, "\r", ' '*80, '\r', "compare results",
        if isinstance(aut, PHF_DFA) and DEBUG:
            if DEBUG > 1:
                print "List of collisions:"
                print aut.collisions
                for tran, i in aut.collisions.iteritems():
                    #print tran, i
                    print  BitArray(bytes=tran[0], length=aut.symbol_bits).uint, BitArray(bytes=tran[1], length=aut.state_bits).uint, i
                    print "SYM:", aut._automaton.alphabet[BitArray(bytes=tran[0], length=aut.symbol_bits).uint]
            print "Bad transitions:", aut.bad_transitions
            print "Collisions:", len(aut.collisions)
            print "Compress bits:", aut.compress_bits
        stats = compare_results(results)
        stats = list(stats)
        if stats[0] == 0:
            print "Zero hits, cannot compute F-measure!"
            stats[0] = 1
        if DEBUG:
            print "Total number of searched packets/flows:", stats[3]
        print "Hits:", stats[0]
        totalhits += stats[0]
        totalfp += stats[1]
        totalfn += stats[2]
        precis = float(stats[0])/(stats[1]+stats[0])
        recall = float(stats[0])/(stats[0]+stats[2])
        fmeas = 2* precis * recall / (precis + recall)
        print "False positives:", stats[1], precis*100, "%"
        print "False negatives:", stats[2], recall*100, "%"
        print "F-measure:", fmeas*100, "%"
        if PerPacket:
            print "Per packet errors:", stats[4], stats[5]
        print '-'*80
        iter += 1
    print "Total stats:"
    precis = float(totalhits)/(totalfp + totalhits)
    recall = float(totalhits)/(totalfn + totalhits)
    fmeas = 2* precis * recall / (precis + recall)
    print "Hits:", totalhits
    print "False positives:", totalfp, precis*100, "%"
    print "False negatives:", totalfn, recall*100, "%"
    print "F-measure:", fmeas*100, "%"
    print "_"*80

if __name__ == '__main__':
#    cProfile.run('test()')
    test()
