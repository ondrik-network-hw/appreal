#!/usr/bin/python

"""
Tool for approximate reductions of finite automata used in network traffic
monitoring.

Author: Vojtech Havlena, <xhavle03@stud.fit.vutbr.cz>
"""

import sys
import getopt
import pickle

import nfa_parser
import wfa_parser
import core_parser
import nfa
import matrix_wfa
import pruning_reduction as pruning
import selfloop_reduction

#Load probabilities/weights from a file.
LOAD = False
#Folders where the probabilities/weights are stored.
DIRECTORY = "subautomata"
#File name prefix for files containing prob/weights.
FILEWEIGHT = "weight"
FILEPROB = "prob"
FILESELFLOOPS = "sefloops"

#Divide NFA into subautomata.
DIVIDE = False
RELATIVEEPS = True
INTEGERPROGRAMMING = False

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

def compute_weight_sub(reduction):
    """Divide NFA to subautomata and compute the weights from these subautomata.

    Return: Numpy.matrix (weight of each state).
    Keyword arguments:
    reduction -- Instance of class for the self-loop reduction.
    """
    subautomata = reduction.get_nfa().get_branch_subautomata()
    i = 1
    back_prob = dict()
    for aut in subautomata:
        red = selfloop_reduction.SelfLoopReduction(reduction.get_pa(), aut)
        if red.get_nfa().is_unambiguous():
            print("Unambiguous NFA {0}, computing product.".format(i))
            ld = red.get_states_weight_product(matrix_wfa.ClosureMode.inverse, True)
        else:
            print("Not unambiguous NFA {0}, computing subautomata.".format(i))
            ld = red.get_states_weight_subautomaton(matrix_wfa.ClosureMode.inverse, True)
        back_prob.update(ld)
        i += 1
    return back_prob

def compute_weight_all(reduction):
    """Compute weights from the whole NFA.

    Return: Numpy.matrix (weight of each state).
    Keyword arguments:
    reduction -- Instance of class for the self-loop reduction.
    """
    if reduction.get_nfa().is_unambiguous():
        print("Input NFA is unambiguous, computing weights by a product.")
        back_prob = reduction.get_states_weight_product(matrix_wfa.ClosureMode.inverse)
        print back_prob
    else:
        print("Input NFA is not unambiguous, computing weights by subautomata.")
        back_prob = reduction.get_states_weight_subautomaton(matrix_wfa.ClosureMode.inverse, True)
        print back_prob
    return back_prob

def self_loop_reduction(pa, input_nfa, mode, restriction):
    """The self-loop reduction.

    Return: (NFA, Float) -- (Reduced automaton, error).
    Keyword arguments:
    input_nfa -- NFA for reduction.
    mode -- eps/k reduction
    restriction -- Value of the restriction parameter.
    """
    reduction = selfloop_reduction.SelfLoopReduction(pa, input_nfa)
    reduction.prepare()
    back_prob = dict()

    if not reduction.is_pa_valid():
        sys.stderr.write("Input PA must be deterministic, and support must be "\
            "the universal automaton.\n")
        return (None,None)

    if LOAD:
        back_prob_rev = load_weights(DIRECTORY, FILEWEIGHT)
        back_prob = {}
        rename_dict = reduction.get_nfa().get_rename_dict()
        for state, weight in back_prob_rev.iteritems():
            back_prob[rename_dict[state]] = weight

        print back_prob
    else:
        if DIVIDE:
            back_prob = compute_weight_sub(reduction)
        else:
            back_prob = compute_weight_all(reduction)

    if mode == "eps":
        reduced_aut = reduction.eps_reduction(back_prob, restriction)
        reduced_aut.__class__ = nfa.NFA
    elif mode == "k":
        reduced_aut = reduction.k_reduction(back_prob, restriction)
        reduced_aut.__class__ = nfa.NFA
    else:
        reduced_aut = None

    err = 0.0
    for state in reduction.get_selfloop_states():
        err += back_prob[state]
    return (reduced_aut, err)

def compute_prob_sub(reduction):
    """Divide NFA to subautomata and compute the probabilities from
    these subautomata.

    Return: Numpy.matrix (probability of each final state).
    Keyword arguments:
    reduction -- Instance of class for the pruning reduction.
    """
    subautomata = reduction.get_nfa().get_branch_subautomata()
    back_prob = dict()
    i = 1
    for aut in subautomata:
        red = pruning.PruningReduction(reduction.get_pa(), aut)
        if red.get_nfa().is_unambiguous():
            print("Unambiguous NFA {0}, computing product.".format(i))
            ld = red.get_finals_prob_product(matrix_wfa.ClosureMode.inverse, True)
        else:
            print("Not unambiguous NFA {0}, computing subautomata.".format(i))
            ld = red.get_finals_prob_subautomaton(matrix_wfa.ClosureMode.inverse, True)
        back_prob.update(ld)
        i += 1
    return back_prob

def compute_prob_all(reduction):
    """Compute probabilities from the whole NFA.

    Return: Numpy.matrix (probability of each final state).
    Keyword arguments:
    reduction -- Instance of class for the pruning reduction.
    """
    if reduction.get_nfa().is_unambiguous():
        print("Input NFA is unambiguous, computing weights by a product.")
        back_prob = reduction.get_finals_prob_product(matrix_wfa.ClosureMode.inverse)
    else:
        print("Input NFA is not unambiguous, computing weights by subautomata.")
        back_prob = reduction.get_finals_prob_subautomaton(matrix_wfa.ClosureMode.inverse, True)
    return back_prob

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
    back_prob = dict()
    subautomata = None

    if LOAD:
        back_prob_rev = load_weights(DIRECTORY, FILEPROB)
        back_prob = {}
        rename_dict = reduction.get_nfa().get_rename_dict()
        for state, weight in back_prob_rev.iteritems():
            back_prob[rename_dict[state]] = weight
    else:
        if DIVIDE:
            back_prob = compute_prob_sub(reduction)
        else:
            back_prob = compute_prob_all(reduction)

    if mode == "eps":
        if INTEGERPROGRAMMING:
            if subautomata is None:
                subautomata = reduction.get_nfa().get_branch_subautomata()
            reduced_aut = reduction.eps_reduction_lp(back_prob, subautomata, restriction)
        else:
            reduced_aut = reduction.eps_reduction(back_prob, restriction)
        reduced_aut.__class__ = nfa.NFA
    elif mode == "k":
        if INTEGERPROGRAMMING:
            if subautomata is None:
                subautomata = reduction.get_nfa().get_branch_subautomata()
            reduced_aut = reduction.k_reduction_lp_modif(back_prob, subautomata, restriction)
        else:
            reduced_aut = reduction.k_reduction(back_prob, restriction)
        reduced_aut.__class__ = nfa.NFA
    else:
        reduced_aut = None

    err = 0.0
    for state in reduction.get_removed_finals():
        err += back_prob[state]

    return (reduced_aut, err)


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

    parser_nfa = nfa_parser.NFAParser()
    parser_wfa = wfa_parser.WFAParser()

    input_nfa = None
    pa = None

    try:
        input_nfa = parser_nfa.fa_to_nfa(params.input_nfa)
        pa = parser_wfa.treba_to_wfa(params.pa)
    except IOError as e:
        sys.stderr.write("I/O error: {0}\n".format(e.strerror))
        sys.exit(1)
    except core_parser.AutomataParserException as e:
        sys.stderr.write("Error during parsing NFA or WFA: {0}\n".format(e.msg))
        sys.exit(1)
    except Exception as e:
        sys.stderr.write("Error during parsing input files: {0}\n".format(e.message))
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

    print "The distance upperbound is {0}".format(err)

    if red_aut is None:
        sys.stderr.write("Error during NFA reduction.\n")
        sys.exit(1)

    try:
        fhandle = open(params.output, 'w')
        fhandle.write(red_aut.to_fa_format(True))
        fhandle.close()
    except IOError as e:
        sys.stderr.write("Error during writing to DOT output file: {0}\n".format(e.message))

    if params.dot is not None:
        try:
            fhandle = open(params.dot, 'w')
            fhandle.write(red_aut.to_dot(True))
            fhandle.close()
        except IOError as e:
            sys.stderr.write("Error during writing to DOT output file: {0}\n".format(e.message))
    sys.exit(0)

if __name__ == "__main__":
    main()
