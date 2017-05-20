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

import nfa_parser
import wfa_parser
import core_parser
import core_reduction
import nfa
import matrix_wfa
import selfloop_reduction

SUBFILE = "sub"
WEIGHTFILE = "weight"
PROBFILE = "prob"
CLOSUREMODE = matrix_wfa.ClosureMode.inverse

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

def compute_weights(pa, start, directory, iters=0):
    """Compute weights for all subautomata stored in files. Results are
    stored in a file.

    Keyword arguments:
    start -- Number of the first subautomaton.
    directory -- Directory where subautomata are stored and where the result
        is saved.
    iters -- Max number of iterations (if iterative closure computation is used).
    """
    i = start
    parser_nfa = nfa_parser.NFAParser()

    if not selfloop_reduction.SelfLoopReduction(pa, nfa.NFA()).is_pa_valid():
        raise Exception("Bad input PA")

    while True:
        try:
            aut = parser_nfa.fa_to_nfa("{0}/{1}{2}".format(directory, SUBFILE, i))
            reduction = core_reduction.CoreReduction(pa, aut)

            if reduction.get_nfa().is_unambiguous():
                print("Unambiguous NFA {0}, computing product.".format(i))
                back_prob = reduction.get_states_weight_product(CLOSUREMODE, iters)
            else:
                print("Not unambiguous NFA {0}, computing subautomata.".format(i))
                back_prob = reduction.get_states_weight_subautomaton(CLOSUREMODE, True, iters)

            with open("{0}/{1}{2}".format(directory, WEIGHTFILE, i), 'wb') as f:
                pickle.dump(back_prob, f, pickle.HIGHEST_PROTOCOL)
            for a,b in back_prob.iteritems():
                print(a,b)
            i += 1
        except IOError:
            return

def compute_probabilities(pa, start, directory, iters=0):
    """Compute probabilities for all subautomata stored in files. Results
    are stored in a file.

    Keyword arguments:
    start -- Number of the first subautomaton.
    directory -- Directory where subautomata are stored and where the result
        is saved.
    iters -- Max number of iterations (if iterative closure computation is used).
    """
    i = start
    parser_nfa = nfa_parser.NFAParser()

    while True:
        try:
            aut = parser_nfa.fa_to_nfa("{0}/{1}{2}".format(directory, SUBFILE, i))
            reduction = core_reduction.CoreReduction(pa, aut)

            if reduction.get_nfa().is_unambiguous():
                print("Unambiguous NFA {0}, computing product.".format(i))
                back_prob = reduction.get_finals_prob_product(CLOSUREMODE, iters)
            else:
                print("Not unambiguous NFA {0}, computing subautomata.".format(i))
                back_prob = reduction.get_finals_prob_subautomaton(CLOSUREMODE, True, iters)
            with open("{0}/{1}{2}".format(directory, PROBFILE, i), 'wb') as f:
                pickle.dump(back_prob, f, pickle.HIGHEST_PROTOCOL)
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

    parser_nfa = nfa_parser.NFAParser()
    parser_wfa = wfa_parser.WFAParser()

    print(params.pa)

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

    input_nfa = input_nfa.get_trim_automaton()
    #input_nfa.rename_states()
    input_nfa.__class__ = nfa.NFA

    pa = pa.get_trim_automaton()
    pa.rename_states()
    pa.__class__ = matrix_wfa.MatrixWFA

    try:
        if params.mode == "divide":
            divide_automaton(input_nfa, params.directory)
        elif params.mode == "weight":
            compute_weights(pa, params.start, params.directory, params.iterations)
        elif params.mode == "probability":
            compute_probabilities(pa, params.start, params.directory, params.iterations)
    except Exception as e:
        sys.stderr.write("{0}\n".format(e.message))
        sys.exit(1)


if __name__ == "__main__":
    main()
