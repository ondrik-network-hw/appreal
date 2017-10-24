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
import label.states_weights as states_weights
import label.states_probabilities as states_probabilities

SUBFILE = "sub"
WEIGHTFILE = "weight"
PROBFILE = "prob"
CLOSUREMODE = matrix_wfa.ClosureMode.inverse
ITERATIONS = 100
APPROXIMATE = False
WEIGHT_TYPE = states_weights.LabelType.prob_sigma
#Sparse matrix representation
SPARSE = True

HELP = "Program for dividing NFA into subautomata, and computing state weights and probabilities.\n"\
        "-p aut -- Input probabilistic automaton in Treba format.\n"\
        "-a aut -- First NFA in FA format.\n"\
        "-i iters -- Use iterative matrix multiplication with iters iterations instead of inverse computation (default).\n"\
        "-h -- Show this text.\n"\
        "-d dir -- Directory for storing subautomata.\n"\
        "-m mode -- Computing mode (divide, weight, probability).\n"\
        "-s start -- Start computing from start-th subautomaton."


class SubautomatonWeightParams:
    """Parameters of the application.
    """
    pa = None
    input_nfa = None
    iterations = None
    help = False
    directory = "subautomata"
    start = 1
    error = False
    mode = None

    def __init__(self):
        pass

    def handle_params(self, argv):
        """Parse parameters and store them.
        """
        self.error = False
        try:
            opts, _ = getopt.getopt(argv[1:], "p:a:i:d:m:s:h")
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
                self.directory = arg
            elif o == "-m" and arg in ("divide", "weight", "probability"):
                self.mode = arg
            elif o == "-s" and arg.isdigit():
                self.start = int(arg)
            else:
                self.error = True

    def error_occured(self):
        """Check whether the input parameters are well given.

        Return: Bool (True=error)
        """
        if self.help:
            return False
        if self.pa == None or self.input_nfa == None \
            or self.mode == None or self.error:
            return True
        else:
            return False

def divide_automaton(input_nfa, directory):
    """Divide NFA into subautomata.

    Keyword arguments:
    input_nfa -- NFA for division.
    directory -- Directory where the divided subautomata are stored.
    """
    i = 1
    substates = 0
    subautomata = input_nfa.get_branch_subautomata()
    try:
        for automaton in subautomata:
            automaton.__class__ = nfa_export.NFAExport
            substates += len(automaton.get_states())
            fhandle = open("{0}/{1}{2}".format(directory, SUBFILE, i), 'w')
            fhandle.write(automaton.to_fa_format())
            fhandle.close()
            i += 1
    except IOError as e:
        sys.stderr.write("I/O error: {0}\n".format(e.strerror))
        sys.exit(1)

    print("Original automaton states: {0}".format(len(input_nfa.get_states())))
    print("Subautomata states sum: {0}".format(substates))

def save_weights(pa, input_nfa, start, directory, approx=False):
    """Compute weights for all subautomata stored in files. Results are
    stored in a file.

    Keyword arguments:
    start -- Number of the first subautomaton.
    directory -- Directory where subautomata are stored and where the result
        is saved.
    iters -- Max number of iterations (if iterative closure computation is used).
    """
    i = start

    #all_labels = states_weights.StatesWeights(pa, input_nfa, WEIGHT_TYPE)
    # all_labels.prepare()
    lang = 0.0

    while True:
        try:
            aut = nfa_parser.NFAParser.fa_to_nfa("{0}/{1}{2}".format(directory, SUBFILE, i))
            labels = states_weights.StatesWeights(pa, aut, WEIGHT_TYPE)
            labels.prepare()

            # if i == 1:
            #     print "Computing language probability"
            #     lang = all_labels.get_nfa_prob(CLOSUREMODE, SPARSE, ITERATIONS)

            print "Processing automaton {0}".format(i)
            labels.compute_weights(approx, SPARSE)


            #labels.get_labels()["lang"] = lang
            #print labels.get_labels()

            with open("{0}/{1}{2}".format(directory, WEIGHTFILE, i), 'wb') as f:
                pickle.dump(labels.get_labels(), f, pickle.HIGHEST_PROTOCOL)

            i += 1
        except IOError:
            return

def save_probabilities(pa, start, directory):
    """Compute probabilities for all subautomata stored in files. Results
    are stored in a file.

    Keyword arguments:
    start -- Number of the first subautomaton.
    directory -- Directory where subautomata are stored and where the result
        is saved.
    iters -- Max number of iterations (if iterative closure computation is used).
    """
    i = start

    while True:
        try:
            aut = nfa_parser.NFAParser.fa_to_nfa("{0}/{1}{2}".format(directory, SUBFILE, i))
            labels = states_probabilities.StatesProbabilities(pa, aut)
            labels.prepare()

            print "Processing automaton {0}".format(i)
            labels.compute_probs(SPARSE)

            #print labels.get_labels()

            with open("{0}/{1}{2}".format(directory, PROBFILE, i), 'wb') as f:
                pickle.dump(labels.get_labels(), f, pickle.HIGHEST_PROTOCOL)
            i += 1
        except IOError:
            return

def main():
    """Main for subautoata computing.
    """
    params = SubautomatonWeightParams()
    params.handle_params(sys.argv)
    if params.error_occured():
        sys.stderr.write("Wrong program parameters\n")
        sys.exit(1)
    if params.help:
        print(HELP)
        sys.exit(0)

    #print(params.pa)

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

    input_nfa = input_nfa.get_trim_automaton()
    #input_nfa.rename_states()
    input_nfa.__class__ = nfa.NFA

    #pa = pa.get_trim_automaton()
    #pa.rename_states()
    pa.__class__ = matrix_wfa.MatrixWFA

    if params.mode == "divide":
        divide_automaton(input_nfa, params.directory)
    elif params.mode == "weight":
        save_weights(pa, input_nfa, params.start, params.directory, APPROXIMATE)
    elif params.mode == "probability":
        save_probabilities(pa, params.start, params.directory)


if __name__ == "__main__":
    main()
    sys.stdout.flush()
