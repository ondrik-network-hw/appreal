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

import parser.nfa_parser as nfa_parser
import parser.wfa_parser as wfa_parser
import parser.core_parser as core_parser
import wfa.matrix_wfa as matrix_wfa

#import scipy.io

HELP = "Program for computing the product of PA and NFA.\n"\
        "-p aut -- Input probabilistic automaton in Treba format.\n"\
        "-a aut -- NFA in FA format.\n"\
        "-i iters -- Set iterations for matrix closure computation.\n"\
        "-m mode -- Set mode of computing matrix closure (inverse, multiply,"\
            " hotelling).\n"\
        "-d -- Show debug iteration progress.\n"\
        "-h -- Show this text."


class ProductParams(object):
    """Parameters of the application.
    """
    probmat = None
    input_nfa = None
    iterations = 0
    help = False
    debug = False
    mode = matrix_wfa.ClosureMode.inverse

    error = False

    def __init__(self):
        pass

    def handle_params(self, argv):
        """Parse parameters and store them.
        """
        self.error = False
        try:
            opts, _ = getopt.getopt(argv[1:], "p:a:i:hdm:")
        except getopt.GetoptError:
            self.error = True
            return

        for opt, arg in opts:
            if opt == "-p":
                self.probmat = arg
            elif opt == "-a":
                self.input_nfa = arg
            elif opt == "-i" and arg.isdigit():
                self.iterations = int(arg)
            elif opt == "-h":
                self.help = True
            elif opt == "-d":
                self.debug = True
            elif opt == "-m":
                if arg == "inverse":
                    self.mode = matrix_wfa.ClosureMode.inverse
                elif arg == "multiply":
                    self.mode = matrix_wfa.ClosureMode.iterations
                elif arg == "hotelling":
                    self.mode = matrix_wfa.ClosureMode.hotelling_bodewig
                else:
                    self.error = True
            else:
                self.error = True

    def error_occured(self):
        """Check whether the input parameters are well given.

        Return: Bool (True=error)
        """
        if self.help:
            return False
        if self.probmat == None or self.input_nfa == None or self.error:
            return True
        else:
            return False

def main():
    """Main for the product computation.
    """
    params = ProductParams()
    params.handle_params(sys.argv)
    if params.error_occured():
        sys.stderr.write("Wrong program parameters\n")
        sys.exit(1)
    if params.help:
        print HELP
        sys.exit(0)

    input_nfa = None
    proab_aut = None

    try:
        input_nfa = nfa_parser.NFAParser.fa_to_nfa(params.input_nfa)
        proab_aut = wfa_parser.WFAParser.treba_to_wfa(params.probmat)
    except IOError as exc:
        sys.stderr.write("I/O error: {0}\n".format(exc.strerror))
        sys.exit(1)
    except core_parser.AutomataParserException as exc:
        sys.stderr.write("Error during parsing NFA or PA: {0}\n"\
            .format(exc.msg))
        sys.exit(1)

    proab_aut = proab_aut.get_trim_automaton()

    print "Checking whether input NFA is unambiguous..."
    if input_nfa.is_unambiguous():
        print "NFA is unambiguous."
    else:
        print "NFA is not unambiguous, performing unambiguation..."
        input_nfa = input_nfa.get_unambiguous_nfa()

    print "Computing product automaton..."
    wfa_p1 = proab_aut.product(input_nfa)
    wfa_p1 = wfa_p1.get_trim_automaton()
    wfa_p1.rename_states()

    wfa_p1.__class__ = matrix_wfa.MatrixWFA

    ini1 = wfa_p1.get_initial_vector()
    fin1 = wfa_p1.get_final_vector().transpose()
    inv1 = wfa_p1.compute_transition_closure(params.mode, \
        params.iterations, params.debug)
    res1 = (ini1*inv1)*fin1

    #mtx = wfa_p1.get_transition_matrix()
    #scipy.io.savemat('test.mat', {'arr': mtx})

    print "The product closure is {0}.".format(res1[0, 0])


if __name__ == "__main__":
    main()
