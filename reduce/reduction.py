#!/usr/bin/python

"""
Tool for approximate reductions of finite automata used in network traffic
monitoring.

Copyright (C) 2017  Vojtech Havlena, <xhavle03@stud.fit.vutbr.cz>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 2 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License.
If not, see <http://www.gnu.org/licenses/>.
"""

import sys
import getopt
import pickle

import parser.nfa_parser as nfa_parser
import parser.wfa_parser as wfa_parser
import parser.core_parser as core_parser
import wfa.nfa as nfa
import wfa.nfa_export as nfa_export
import wfa.matrix_wfa as matrix_wfa
import appred.pruning_reduction as pruning
import label.states_weights as states_weights
import appred.selfloop_reduction as selfloop_reduction

#Load probabilities/weights from a file.
LOAD = True
#Folders where the probabilities/weights are stored.
DIRECTORY = "subautomata"
#File name prefix for files containing prob/weights.
FILEWEIGHT = "weight"
FILEPROB = "prob"
FILESELFLOOPS = "sefloops"

#Divide NFA into subautomata.
#DIVIDE = False
RELATIVEEPS = True
INTEGERPROGRAMMING = False
REDUCTION_MODIF = True
APPROX = False
WEIGHT_TYPE = states_weights.LabelType.prob_sigma
#Sparse matrix representation
SPARSE = True

HELP = "Program for reducing NFAs according to a PA.\n"\
        "-p aut -- Input probabilistic automaton in Treba format.\n"\
        "-a aut -- NFA in FA format for reduction.\n"\
        "-i iters -- Use iterative matrix multiplication with iters iterations instead of inverse computation (default).\n"\
        "-h -- Show this text.\n"\
        "-d file -- Convert reduced NFA into DOT format.\n"\
        "-o file -- Output file for storing reduced NFA in FA format.\n"\
        "-t type, --type=type -- Type of a reduction (pr -- the pruning reduction, sl -- the self-loop reduction).\n"\
        "-m mod, --mode=mod -- Mode of a reduction (k -- k-reduction, eps -- epsilon-reduction).\n"\
        "-r val, --restriction=val -- Value of restriction parameter k/eps."


class ReductionParams:
    """Parameters of the application.
    """
    pa = None
    input_nfa = None
    iterations = None
    help = False
    dot = None
    output = "result.fa"
    #Pruning/Self-loop
    red_type = None
    #Restriction parameter
    restriction = None
    error = False
    #Mode -- k/eps reduction
    mode = None

    def __init__(self):
        pass

    def handle_params(self, argv):
        """Parse parameters and store them.
        """
        self.error = False
        try:
            opts, _ = getopt.getopt(argv[1:], "t:r:m:p:a:i:hd:o:", ["type=", "restriction=", "mode="])
        except getopt.GetoptError:
            self.error = True
            return

        for o, arg in opts:
            if o == "-p":
                self.pa = arg
            elif o == "-a":
                self.input_nfa = arg
            elif o == "-i" and arg.isdigit():
                self.iterations = int(arg)
            elif o == "-h":
                self.help = True
            elif o == "-d":
                self.dot = arg
            elif o == "-o":
                self.output = arg
            elif o in ("-t", "--type") and arg in ("pr", "sl"):
                self.red_type = arg
            elif o in ("-r", "--restriction"):
                try:
                    self.restriction = float(arg)
                except ValueError:
                    self.error = True
            elif o in ("-m", "--mode") and (arg in ("k", "eps")):
                self.mode = arg
            else:
                self.error = True

    def error_occured(self):
        """Check whether the input parameters are well given.

        Return: Bool (True=error)
        """
        if self.help:
            return False
        if self.pa == None or self.input_nfa == None or self.red_type == None \
            or self.restriction == None or self.mode == None or self.error:
            return True
        else:
            return False

def load_weights(directory, filename):
    """Load weights/probabilities from file.

    Return: Dictionary of State -> Float (weight/prob)
    """
    ret = dict()
    i = 1
    while True:
        try:
            with open("{0}/{1}{2}".format(directory, filename, i), 'rb') as f:
                ld = pickle.load(f)
                ret.update(ld)
                #print ld
            i += 1
        except IOError:
            return ret


def export_selfloop_states(reduction):
    """Export states where the self-loops were added to file.

    Keyword arguments:
    reduction -- Instance of class for the self-loop reduction.
    """
    with open("{0}/{1}".format(DIRECTORY, FILESELFLOOPS), 'wb') as f:
        pickle.dump(reduction.get_selfloop_states(), f, pickle.HIGHEST_PROTOCOL)

def get_selfloop_reduced_nfa(reduction, mode, restriction):
    """Get a reduced NFA using the self-loop reduction.

    Keyword arguments:
    reduction -- Reduction handler (SelfLoopReduction).
    mode -- Reduction mode.
    restriction -- Reduction restriction.
    """
    reduced_aut = None
    if mode == "eps":
        reduced_aut = reduction.eps_reduction(restriction)
        reduced_aut.__class__ = nfa.NFA
    elif mode == "k":
        if REDUCTION_MODIF:
            reduced_aut = reduction.k_reduction_modif(restriction)
        else:
            reduced_aut = reduction.k_reduction(restriction)
        reduced_aut.__class__ = nfa.NFA
    return reduced_aut

def self_loop_reduction(pa, input_nfa, mode, restriction):
    """The self-loop reduction.

    Return: (NFA, Float) -- (Reduced automaton, error).
    Keyword arguments:
    input_nfa -- NFA for reduction.
    mode -- eps/k reduction
    restriction -- Value of the restriction parameter.
    """
    #pa.set_all_finals()
    reduction = selfloop_reduction.SelfLoopReduction(pa, input_nfa, WEIGHT_TYPE)
    reduction.prepare()
    back_prob = dict()

    if LOAD:
        back_prob_rev = load_weights(DIRECTORY, FILEWEIGHT)
        back_prob = {}
        rename_dict = reduction.get_nfa().get_rename_dict()
        for state, weight in back_prob_rev.iteritems():
            if state == "lang":
                continue
            back_prob[rename_dict[state]] = weight
        reduction.set_labels(back_prob)
        #print reduction.state_labels.get_labels()
    else:
        reduction.compute_labels(APPROX, SPARSE)

    reduced_aut = get_selfloop_reduced_nfa(reduction, mode, restriction)

    err = 0.0
    back_prob = reduction.state_labels.get_labels()
    for state in reduction.get_selfloop_states():
        err += back_prob[state]
    return (reduced_aut, err)

def get_pruning_reduced_nfa(reduction, mode, restriction):
    """Get a reduced NFA using the pruning reduction.

    Keyword arguments:
    reduction -- Reduction handler (PruningReduction).
    mode -- Reduction mode.
    restriction -- Reduction restriction.
    """
    reduced_aut = None
    if mode == "eps":
        if INTEGERPROGRAMMING:
            subautomata = reduction.get_nfa().get_branch_subautomata()
            reduced_aut = reduction.eps_reduction_lp(subautomata, restriction)
        else:
            reduced_aut = reduction.eps_reduction_greedy(restriction)
        reduced_aut.__class__ = nfa.NFA
    elif mode == "k":
        if INTEGERPROGRAMMING:
            subautomata = reduction.get_nfa().get_branch_subautomata()
            if REDUCTION_MODIF:
                reduced_aut = reduction.k_reduction_lp_modif(subautomata, restriction)
            else:
                reduced_aut = reduction.k_reduction_lp(subautomata, restriction)
        else:
            if REDUCTION_MODIF:
                reduced_aut = reduction.k_reduction_greedy(restriction)
            else:
                reduced_aut = reduction.k_reduction(restriction)
        reduced_aut.__class__ = nfa.NFA
    return reduced_aut

def pruning_reduction(pa, input_nfa, mode, restriction):
    """The pruning reduction.

    Return: (NFA, Float) -- (Reduced automaton, error).
    Keyword arguments:
    input_nfa -- NFA for reduction.
    mode -- eps/k reduction
    restriction -- Value of the restriction parameter.
    """
    reduction = pruning.PruningReduction(pa, input_nfa)
    reduction.prepare()

    if LOAD:
        back_prob_rev = load_weights(DIRECTORY, FILEPROB)
        back_prob = {}
        rename_dict = reduction.get_nfa().get_rename_dict()
        for state, weight in back_prob_rev.iteritems():
            back_prob[rename_dict[state]] = weight
        reduction.set_labels(back_prob)
    else:
        reduction.compute_labels(APPROX, SPARSE)

    reduced_aut = get_pruning_reduced_nfa(reduction, mode, restriction)

    err = 0.0
    back_prob = reduction.get_labels()
    for state in reduction.get_removed_finals():
        err += back_prob[state]

    return (reduced_aut, err)

def write_results(params, red_aut):
    """Write the results of the reduction into files.

    Keyword arguments:
    params -- Program parameters.
    red_aut -- Reduced NFA.
    """
    red_aut.__class__ = nfa_export.NFAExport
    try:
        fhandle = open(params.output, 'w')
        fhandle.write(red_aut.to_fa_format(True))
        fhandle.close()
    except IOError as e:
        sys.stderr.write("Error during writing to FA output file: {0}\n".format(e.message))

    if params.dot is not None:
        try:
            fhandle = open(params.dot, 'w')
            fhandle.write(red_aut.to_dot(True))
            fhandle.close()
        except IOError as e:
            sys.stderr.write("Error during writing to DOT output file: {0}\n".format(e.message))

def main():
    """Main for approximate reductions of automata.
    """
    params = ReductionParams()
    params.handle_params(sys.argv)
    if params.error_occured():
        sys.stderr.write("Wrong program parameters\n")
        sys.exit(1)
    if params.help:
        print(HELP)
        sys.exit(0)
    if params.restriction < 0.0 or params.restriction > 1.0:
        sys.stderr.write("Restriction parameter must be in range [0,1].\n")
        sys.exit(1)

    input_nfa = None
    pa = None

    try:
        input_nfa = nfa_parser.NFAParser.fa_to_nfa(params.input_nfa)
        pa =  wfa_parser.WFAParser.treba_to_wfa(params.pa)
    except IOError as e:
        sys.stderr.write("I/O error: {0}\n".format(e.strerror))
        sys.exit(1)
    except core_parser.AutomataParserException as e:
        sys.stderr.write("Error during parsing NFA or WFA: {0}\n".format(e.msg))
        sys.exit(1)

    input_nfa.get_trim_automaton()
    #input_nfa.rename_states()
    input_nfa.__class__ = nfa.NFA

    pa = pa.get_trim_automaton()
    pa.rename_states()
    pa.__class__ = matrix_wfa.MatrixWFA


    if params.red_type == "sl":
        red_aut, err = self_loop_reduction(pa, input_nfa, params.mode, params.restriction)
    else:
        red_aut, err = pruning_reduction(pa, input_nfa, params.mode, params.restriction)

    print "NFA: {0}, PA: {1}".format(params.input_nfa, params.pa)
    print "#States (original): {0}, #States (reduced): {1}".format(len(input_nfa.get_states()), len(red_aut.get_states()))
    print "Mode: {0}, Restriction: {1}, REDUCTION_MODIF: {2}, LOAD: {3}, WEIGHT_TYPE: {4}, SPARSE: {5}, THRESHOLD: {6}".format(params.mode, params.restriction, REDUCTION_MODIF, LOAD, WEIGHT_TYPE, SPARSE, matrix_wfa.THRESHOLD)
    print "The distance upperbound is {0}".format(min(err, 1.0))

    if red_aut is None:
        sys.stderr.write("Error during NFA reduction.\n")
        sys.exit(1)

    write_results(params, red_aut)
    sys.exit(0)

if __name__ == "__main__":
    main()
