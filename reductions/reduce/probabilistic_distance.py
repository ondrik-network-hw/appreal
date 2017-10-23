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

import copy
import sys
import getopt
import pickle

import parser.nfa_parser as nfa_parser
import parser.wfa_parser as wfa_parser
import parser.core_parser as core_parser
import wfa.matrix_wfa as matrix_wfa
import wfa.nfa as nfa
import wfa.matrix_wfa_export as matrix_wfa_export

import label.states_weights as states_weights

""" Use optimisation during distance computation. If variable is set to zero,
no optimisation is used. If it is set to 1, self-loop optimisation is used
(the product is the first automaton). This setting assume that -a is set
the original automaton, and -b the reduced one. If it is set to 2, pruning
optimisation is used (the product is the second automaton -- reduced one).
"""
OPTIMISATION = 1

LOAD = False

DIRECTORY = "subautomata"
#File name prefix for files containing prob/weights.
FILEWEIGHT = "weight"
FILEPROB = "prob"
FILESELFLOOPS = "sefloops"

#Sparse matrix representation
SPARSE = True



CLOSUREMODE = matrix_wfa.ClosureMode.inverse
ITERATIONS = 100
APPROXIMATE = False
WEIGHT_TYPE = states_weights.LabelType.prob_sigma
#Sparse matrix representation

HELP = "Program for computing the probabilistic distance between languages.\n"\
        "-p aut -- Input probabilistic automaton in Treba format.\n"\
        "-a aut -- First NFA in FA format.\n"\
        "-b aut -- Second NFA in FA format.\n"\
        "-i iters -- Use iterative matrix multiplication with iters iterations instead of inverse computation (default).\n"\
        "-h -- Show this text."


class DistanceParams:
    """Parameters of the application.
    """
    #Probabilistic automaton0
    pa = None
    #Two input NFAs
    input_nfa1 = None
    input_nfa2 = None
    #Number of iterations
    iterations = None
    help = False

    #Bad parameters
    error = False

    def __init__(self):
        pass

    def handle_params(self, argv):
        """Parse parameters and store them.
        """
        self.error = False
        try:
            opts, _ = getopt.getopt(argv[1:], "p:a:b:i:h")
        except getopt.GetoptError:
            self.error = True
            return

        for o, arg in opts:
            if o == "-p":
                self.pa = arg
            elif o == "-a":
                self.input_nfa1 = arg
            elif o == "-b":
                self.input_nfa2 = arg
            elif o == "-i" and arg.isdigit():
                self.iterations = int(arg)
            elif o == "-h":
                self.help = True
            else:
                self.error = True

    def error_occured(self):
        """Check whether the input parameters are well given.

        Return: Bool (True=error)
        """
        if self.help:
            return False
        if self.pa == None or self.input_nfa1 == None \
            or self.input_nfa2 == None or self.error:
            return True
        else:
            return False

def prepare_nfas(input_nfa1, input_nfa2):
    """Prepare input NFAs for the distance computation. Includes disambiguation,
    trimming and renaming states.

    Keyword arguments:
    input_nfa1 -- NFA 1
    input_nfa2 -- NFA 2
    """
    if OPTIMISATION != 1 or (not LOAD):
        print("Checking whether input NFAs are unambiguous...")
        if input_nfa1.is_unambiguous():
            print("NFA 1 is unambiguous.")
        else:
            print("NFA 1 is not unambiguous, performing disambiguation...")
            input_nfa1 = input_nfa1.get_dfa()
            input_nfa1.rename_states()
            input_nfa1 = input_nfa1.get_trim_automaton()
            input_nfa1.__class__ = nfa.NFA
            input_nfa1 = input_nfa1.get_minimal_dfa_hopcroft()
            input_nfa1.rename_states()

    if input_nfa2.is_unambiguous():
        print("NFA 2 is unambiguous.")
    else:
        print("NFA 2 is not unambiguous, performing disambiguation...")
        input_nfa2 = input_nfa2.get_dfa()
        input_nfa2.rename_states()
        input_nfa2 = input_nfa2.get_trim_automaton()
        input_nfa2.__class__ = nfa.NFA
        input_nfa2 = input_nfa2.get_minimal_dfa_hopcroft()
        #input_nfa2.rename_states()

    return input_nfa1, input_nfa2

def compute_products(pa, input_nfa1, input_nfa2):
    """Compute automata products for the distance computation. Optimizations
    for the product coputation are considered.

    Return: (MatrixWFA a, MatrixWFA b, MatrixWFA c) where a = prod(pa, input_nfa1),
    b = prod(pa, input_nfa2), c = prod(pa, prod(input_nfa1, input_nfa2))
    Keyword arguments:
    pa -- Probabilistic automaton
    input_nfa1 -- NFA 1
    input_nfa2 -- NFA 2
    """
    print("Computing product automaton 1...")
    wfa_p1 = pa.product(input_nfa1)
    wfa_p1 = wfa_p1.get_trim_automaton()
    wfa_p1.rename_states()
    wfa_p1.__class__ = matrix_wfa_export.MatrixWFAExport

    print("Computing product automaton 2...")
    wfa_p2 = pa.product(input_nfa2)
    wfa_p2 = wfa_p2.get_trim_automaton()
    wfa_p2.rename_states()

    print("Computing product automaton 3...")
    if OPTIMISATION == 0:
        nfa_a12 = input_nfa1.product(input_nfa2)
        nfa_a12 = nfa_a12.get_trim_automaton()
        nfa_a12.rename_states()
        wfa_p3 = pa.product(nfa_a12)
        wfa_p3 = wfa_p3.get_trim_automaton()
        wfa_p3.rename_states()
    elif OPTIMISATION == 1:
        #nfa_a12 = copy.deepcopy(input_nfa1)
        wfa_p3 = wfa_p1
    elif OPTIMISATION == 2:
        #nfa_a12 = copy.deepcopy(input_nfa2)
        wfa_p3 = wfa_p2

    wfa_p1.__class__ = matrix_wfa.MatrixWFA
    wfa_p2.__class__ = matrix_wfa.MatrixWFA
    wfa_p3.__class__ = matrix_wfa.MatrixWFA

    return wfa_p1, wfa_p2, wfa_p3

def main():
    """Main for computing the probabilistic distance.
    """
    params = DistanceParams()
    params.handle_params(sys.argv)
    if params.error_occured():
        sys.stderr.write("Wrong program parameters\n")
        sys.exit(1)
    if params.help:
        print(HELP)
        sys.exit(0)

    input_nfa1 = None
    input_nfa2 = None
    pa = None

    try:
        input_nfa1 = nfa_parser.NFAParser.fa_to_nfa(params.input_nfa1)
        input_nfa2 = nfa_parser.NFAParser.fa_to_nfa(params.input_nfa2)
        pa =  wfa_parser.WFAParser.treba_to_wfa(params.pa)
        pa = pa.get_trim_automaton()
        pa.rename_states()
    except IOError as e:
        sys.stderr.write("I/O error: {0}\n".format(e.strerror))
        sys.exit(1)
    except core_parser.AutomataParserException as e:
        sys.stderr.write("Error during parsing NFA or WFA: {0}\n".format(e.msg))
        sys.exit(1)

    #input_nfa1 = input_nfa1.get_trim_automaton()
    input_nfa1.__class__ = nfa.NFA

    prep_nfa1, prep_nfa2 = prepare_nfas(input_nfa1, input_nfa2)
    wfa_p1, wfa_p2, wfa_p3 = compute_products(pa, prep_nfa1, prep_nfa2)

    mode = None
    if params.iterations is None:
        mode = matrix_wfa.ClosureMode.inverse
    else:
        mode = matrix_wfa.ClosureMode.iterations

    if LOAD:
        with open("{0}/{1}{2}".format(DIRECTORY, FILEWEIGHT, 1), 'rb') as f:
            ld = pickle.load(f)
            res1 = ld["lang"]
    else:
        res1 = wfa_p1.compute_language_probability(mode, SPARSE, params.iterations, False)

    res2 = wfa_p2.compute_language_probability(mode, SPARSE, params.iterations, False)
    if OPTIMISATION == 1:
        res3 = res1
    elif OPTIMISATION == 2:
        res3 = res2
    else:
        res3 = wfa_p3.compute_language_probability(mode, SPARSE, params.iterations, False)

    result = res1 + res2 - 2*res3
    # if OPTIMISATION == 1:
    #     result = res2 - res1
    # else:
    #     result = res1 + res2 - 2*res3
    # print res1, res2, res3
    print("The probabilistic distance of input automata is {0}.".format(result))


if __name__ == "__main__":
    main()
