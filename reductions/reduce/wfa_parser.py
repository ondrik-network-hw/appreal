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

from core_wfa import CoreWFA, Transition
from core_parser import AutomataParser, AutomataParserException
import aux_functions as aux

class WFAParser(AutomataParser):
    """Class for parsing WFAs.
    """
    def __init__(self):
        super(WFAParser, self).__init__()
        self.table = dict()

    def parse_from_file(self, filename):
        """Generic method for parsing NFA from file (implicitly Treba format).

        Return: parsed NFA
        Keyword arguments:
        filename -- name of a file containing representation of an NFA.
        """
        return self.treba_to_wfa(filename)

    def treba_to_wfa(self, filename):
        """Parse NFA from Treba format.
        If fails raise AutomataParserException.

        Return: parsed NFA
        Keyword arguments:
        filename -- name of a file containing representation of an NFA in BA format.
        use_table -- Obsolote, do not use
        """
        fhandle = open(filename, 'r')
        inv_table = None
        transitions = []
        finals = dict()

        #if use_table and self.table != None:
        #    inv_table = {v: k for k, v in self.table.iteritems()}

        try:
            for line in fhandle:
                spl = line.split()
                if len(spl) == 4:
                    if inv_table != None: #Obsolete -- do not use
                        transitions.append(Transition(int(spl[0]), int(spl[1]), aux.convert_to_pritable(inv_table[int(spl[2])]), float(spl[3])))
                    else:
                        weight = float(spl[3])
                        if weight > 0.0:
                            transitions.append(Transition(int(spl[0]), int(spl[1]), int(spl[2]), weight))
                        else:
                            print("Warning: transition with zero probability is ignored.")
                elif len(spl) == 2:
                    weight = float(spl[1])
                    if weight > 0.0:
                        finals[int(spl[0])] = weight
                    else:
                        print("Warning: final state with zero probability is ignored.")
                else:
                    raise AutomataParserException("Bad WFA input format.")
        except ValueError:
            fhandle.close()
            raise AutomataParserException("Bad WFA input format.")
        fhandle.close()
        return CoreWFA(transitions, finals, {0: 1.0})
