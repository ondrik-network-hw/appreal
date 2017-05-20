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
import numpy
import sys
import getopt

import nfa_parser
import wfa_parser
import core_parser
import matrix_wfa

""" Use optimisation during distance computation. If variable is set to zero,
no optimisation is used. If it is set to 1, self-loop optimisation is used
(the product is the first automaton). This setting assume that -a is set
the original automaton, and -b the reduced one. If it is set to 2, pruning
optimisation is used (the product is the second automaton -- reduced one).
"""
OPTIMISATION = 0

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

    parser_nfa = nfa_parser.NFAParser()
    parser_wfa = wfa_parser.WFAParser()

    input_nfa1 = None
    input_nfa2 = None
    pa = None

    try:
        input_nfa1 = parser_nfa.fa_to_nfa(params.input_nfa1)
        input_nfa2 = parser_nfa.fa_to_nfa(params.input_nfa2)
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

    print("Checking whether input NFAs are unambiguous...")
    if input_nfa1.is_unambiguous():
        print("NFA 1 is unambiguous.")
    else:
        print("NFA 1 is not unambiguous, performing disambiguation...")
        input_nfa1 = input_nfa1.get_unambiguous_nfa()
        input_nfa1 = input_nfa1.get_trim_automaton()
        input_nfa1.rename_states()

    if input_nfa2.is_unambiguous():
        print("NFA 2 is unambiguous.")
    else:
        print("NFA 2 is not unambiguous, performing disambiguation...")
        input_nfa2 = input_nfa2.get_unambiguous_nfa()
        input_nfa2 = input_nfa2.get_trim_automaton()
        input_nfa2.rename_states()

    print("Computing product automaton 1...")
    wfa_p1 = pa.product(input_nfa1)
    wfa_p1 = wfa_p1.get_trim_automaton()
    wfa_p1.rename_states()

    print("Computing product automaton 2...")
    wfa_p2 = pa.product(input_nfa2)
    wfa_p2 = wfa_p2.get_trim_automaton()
    wfa_p2.rename_states()

    print("Computing product automaton 3...")
    if OPTIMISATION == 0:
        nfa_a12 = input_nfa1.product(input_nfa2)
    elif OPTIMISATION == 1:
        nfa_a12 = copy.deepcopy(input_nfa1)
    elif OPTIMISATION == 2:
        nfa_a12 = copy.deepcopy(input_nfa2)
    nfa_a12 = nfa_a12.get_trim_automaton()
    nfa_a12.rename_states()
    wfa_p3 = pa.product(nfa_a12)
    wfa_p3 = wfa_p3.get_trim_automaton()
    wfa_p3.rename_states()

    wfa_p1.__class__ = matrix_wfa.MatrixWFA
    wfa_p2.__class__ = matrix_wfa.MatrixWFA
    wfa_p3.__class__ = matrix_wfa.MatrixWFA

    #mtx1 = wfa_p1.get_transition_matrix()
    #ini1 = wfa_p1.get_initial_vector()
    #fin1 = wfa_p1.get_final_vector().transpose()
    mode = None
    if params.iterations is None:
        mode = matrix_wfa.ClosureMode.inverse
    else:
        mode = matrix_wfa.ClosureMode.iterations
    res1 = wfa_p1.compute_language_probability(mode, params.iterations, False)

    res2 = wfa_p2.compute_language_probability(mode, params.iterations, False)
    res3 = wfa_p3.compute_language_probability(mode, params.iterations, False)

    result = res1 + (res2 - 2*res3)
    print("The probabilistic distance of input automata is {0}.".format(result))


if __name__ == "__main__":
    main()
