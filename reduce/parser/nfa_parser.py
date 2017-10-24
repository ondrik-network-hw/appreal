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

from wfa.core_wfa import Transition
from wfa.nfa import NFA
from parser.core_parser import AutomataParser, AutomataParserException

class NFAParser(AutomataParser):
    """Class for parsing NFAs to inner representation.
    """

    def __init__(self):
        """Constructor.
        """
        super(NFAParser, self).__init__()

    def parse_from_file(self, filename):
        """Generic method for parsing NFA from file (implicitly FA format).

        Return: parsed NFA
        Keyword arguments:
        filename -- name of a file containing representation of an NFA.
        """
        return NFAParser.fa_to_nfa(filename)

    @staticmethod
    def parse_alphabet(line):
        """Parse symbols of alphabet from a string.

        Return: List of symbols = alphabet.
        Keyword arguments:
        line -- string containing space divided symbols.
        """
        alph = set()
        spl = line.split(" ")
        for item in spl:
            if item.strip() != "":
                alph.add(int(item.strip(), 16))
        return alph

    @staticmethod
    def _parse_ba_state(state):
        state = state.replace("[", "").replace("]", "")
        return int(state)

    @staticmethod
    def ba_to_nfa(filename):
        """Parse NFA from BA format (Rabit&Reduce tool). Formely for Buchi automata.
        If fails raise AutomataParserException.

        Return: parsed NFA
        Keyword arguments:
        filename -- name of a file containing representation of an NFA in BA format.
        """
        fhandle = open(filename, 'r')
        transitions = []
        finals = dict()

        try:
            start = NFAParser._parse_ba_state(fhandle.readline())
        except EOFError:
            fhandle.close()
            raise AutomataParserException("Initial state must be specified.")
        except ValueError:
            fhandle.close()
            raise AutomataParserException("States must be nonnegative integers.")

        try:
            for line in fhandle:
                spl = line.split(",")
                if len(spl) == 2:
                    spl2 = spl[1].split("->")
                    if len(spl2) != 2:
                        raise AutomataParserException("Bad input Format")
                    transitions.append(Transition(NFAParser._parse_ba_state(spl2[0]), NFAParser._parse_ba_state(spl2[1]), NFAParser._parse_ba_state(spl[0]), 1.0))
                elif len(spl) == 1:
                    finals[NFAParser._parse_ba_state(spl[0])] = 1.0
                else:
                    raise AutomataParserException("Bad input format.")
        except ValueError:
            fhandle.close()
            raise AutomataParserException("Bad input format.")
        fhandle.close()
        return NFA(transitions, finals, {start: 1.0})

    @staticmethod
    def fa_to_nfa(filename):
        """Parse NFA from FA format (similar to Treba format).
        If fails raise AutomataParserException.

        Return: parsed NFA
        Keyword arguments:
        filename -- name of a file containing representation of an NFA in FA format.
        """
        fhandle = open(filename, 'r')
        transitions = []
        finals = dict()
        chars = set()
        first = True
        alphabet = None

        try:
            start = int(fhandle.readline())
        except EOFError:
            fhandle.close()
            raise AutomataParserException("Initial state must be specified.")
        except ValueError:
            fhandle.close()
            raise AutomataParserException("States must be nonnegative integers.")

        try:
            for line in fhandle:
                if first:
                    if line.startswith(":"):
                        alphabet = NFAParser.parse_alphabet(line[1:])
                        first = False
                        continue
                first = False
                spl = line.split()
                if len(spl) == 3:
                    transitions.append(Transition(int(spl[0]), int(spl[1]), int(spl[2], 16), 1.0))
                    chars.add(int(spl[2], 16))
                elif len(spl) == 1:
                    finals[int(spl[0])] = 1.0
                elif len(spl) == 0:
                    pass
                else:
                    raise AutomataParserException("Bad input format.")
        except ValueError:
            fhandle.close()
            raise AutomataParserException("Bad input format.")

        fhandle.close()
        if alphabet != None:
            if not chars.issubset(alphabet):
                raise AutomataParserException("Transition label is not in given alphabet.")
            alphabet = list(alphabet)
        return NFA(transitions, finals, {start: 1.0}, alphabet)
