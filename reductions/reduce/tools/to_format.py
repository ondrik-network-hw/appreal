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

import nfa_parser
import core_parser
import nfa

HELP = "Program for converting NFAs.\n"\
        "-i file -- Input NFA file.\n"\
        "-f format (fa, ba, timbuk) -- Input NFA format (default FA format).\n"\
        "-o file -- Output NFA file.\n"\
        "-t format (fa, ba, timbuk, fado, dot) -- Output NFA format.\n"\
        "-h -- Show this text."

class FormatParams:
    """Parameters of the application.
    """
    input_aut = None
    output_aut = "aut.out"
    help = False
    input_format = "fa"
    output_format = "timbuk"
    error = False

    def __init__(self):
        pass

    def handle_params(self, argv):
        """Parse parameters and store them.
        """
        self.error = False
        try:
            opts, _ = getopt.getopt(argv[1:], "i:o:f:t:h")
        except getopt.GetoptError:
            self.error = True
            return

        for o, arg in opts:
            if o == "-i":
                self.input_aut = arg
            elif o == "-o":
                self.output_aut = arg
            elif o == "-h":
                self.help = True
            elif o == "-f" and arg in ("fa", "fado", "timbuk"):
                self.input_format = arg
            elif o == "-t" and arg in ("fa", "ba", "dot", "fado", "timbuk"):
                self.output_format = arg
            else:
                self.error = True

    def error_occured(self):
        """Check whether the input parameters are well given.

        Return: Bool (True=error)
        """
        if self.help:
            return False
        if self.input_aut == None or self.error:
            return True
        else:
            return False

def main():
    """Main for converting automata.
    """
    params = FormatParams()
    params.handle_params(sys.argv)
    if params.error_occured():
        sys.stderr.write("Wrong program parameters\n")
        sys.exit(1)
    if params.help:
        print(HELP)
        sys.exit(0)

    parser_nfa = nfa_parser.NFAParser()

    input_nfa = import_nfa(parser_nfa, params.input_aut, params.input_format)
    input_nfa.__class__ = nfa.NFA
    export_nfa(input_nfa, params.output_aut, params.output_format)


def import_nfa(parser, input_file, input_format):
    input_nfa = None
    try:
        if input_format == "fa":
            input_nfa = parser.fa_to_nfa(input_file)
        elif input_format == "ba":
            input_nfa = parser.ba_to_nfa(input_file)
        #TODO: import from Timbuk format
    except IOError as e:
        sys.stderr.write("I/O error: {0}\n".format(e.strerror))
        sys.exit(1)
    except core_parser.AutomataParserException as e:
        sys.stderr.write("Error during parsing the input NFA: {0}\n".format(e.msg))
        sys.exit(1)
    except Exception as e:
        sys.stderr.write("Error during parsing input files: {0}\n".format(e.message))
        sys.exit(1)
    return input_nfa


def export_nfa(input_nfa, out_file, format_aut):
    try:
        fhandle = open(out_file, 'w')
        if format_aut == "fa":
            fhandle.write(input_nfa.to_fa_format())
        elif format_aut == "ba":
            #TODO: Implement export to BA format
            pass
        elif format_aut == "fado":
            fhandle.write(input_nfa.to_automata_fado_format())
        elif format_aut == "dot":
            fhandle.write(input_nfa.to_dot())
        else:
            fhandle.write(input_nfa.to_timbuk())
        fhandle.close()
    except IOError as e:
        sys.stderr.write("I/O error: {0}\n".format(e.strerror))
        sys.exit(1)
    except nfa.NFAOperationException as e:
        sys.stderr.write("Converting error: {0}\n".format(e.strerror))
        sys.exit(1)


if __name__ == "__main__":
    main()
