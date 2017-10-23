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

import wfa.nfa as nfa
import wfa.core_wfa_export as core_wfa_export
import wfa.aux_functions as aux

class NFAExport(nfa.NFA, core_wfa_export.CoreWFAExport):

    def __init__(self, transitions=None, finals=None, start=None, alphabet=None):
        super(NFAExport, self).__init__(transitions, finals, start, alphabet)

    def to_dot(self, replace_alphabet=True, state_label=None, legend=None):
        """Convert NFA to dot format (for graphical visualization). Use
        aggregation of transitions between same states.

        Return: String
        Keyword arguments:
        replace_alphabet -- if true the aggregated transition labeled by the
            whole alphabel is replaced with ^[]
        state_label -- label of each state (shown inside of the state)
        """
        dot = str()
        dot += "digraph \" Automat \" {\n    rankdir=LR;\n"
        if legend is not None:
            dot += "{{ rank = LR\n Legend [shape=none, margin=0, label=\"{0}\"] }}\n".format(legend)
        dot += "node [shape = doublecircle];\n"

        if len(super(NFAExport, self).get_finals()) > 0:
            for state, _ in super(NFAExport, self).get_finals().iteritems():
                if state_label == None:
                    dot += "\"" + str(state) + "\"" + " [label=\"" \
                        + str(state) + "\"]"
                else:
                    dot += "\"" + str(state) + "\"" + " [label=\"" \
                        + str(state) + ", " \
                        + "{:.2e}".format(state_label[state]) + "\"]"
                dot += ";\n"

        dot += "node [shape = circle];\n"
        if state_label != None:
            for state in super(NFAExport, self).get_states():
                if state not in super(NFAExport, self).get_finals():
                    dot += "\"" + str(state) + "\"" + " [label=\"" \
                        + str(state) + ", " \
                        + "{:.2e}".format(state_label[state]) + "\"]"
                    dot += ";\n"
        else:
            for state in self.get_states():
                if state not in super(NFAExport, self).get_finals():
                    dot += "\"" + str(state) + "\"" + " [label=\"" \
                        + str(state) + "\"]"
                    dot += ";\n"

        dot += "node [shape = circle];\n"
        for (src, dest), res in super(NFAExport, self).get_aggregated_transitions().items():
            dot += "\"" + str(src) + "\""
            dot += " -> "
            dot += "\"" + str(dest) + "\""
            dot += " [ label = \"" + self._format_label(res[0], replace_alphabet)
            dot += "\" ];\n"

        dot += "}"
        return dot

    def to_fa_format(self, alphabet=False):
        """Converts automaton to FA format.

        Return: String (NFA in FA format)
        Keyword arguments:
        alphabet -- whether show explicitly symbols from alphabet.
        """

        if len(super(NFAExport, self).get_starts()) != 1:
            raise nfa.NFAOperationException("Only to an NFA with a single initial state can be converted to the FA format.")

        fa = str()
        fa += str(super(NFAExport, self).get_starts().keys()[0])+"\n"
        if alphabet:
            fa += ":"
            for sym in self.get_alphabet():
                fa += hex(sym) + " "
            fa += "\n"
        for transition in self._transitions:
            fa += "{0} {1} {2}\n".format(transition.src, transition.dest,\
                hex(transition.symbol))
        for final, _ in self._finals.iteritems():
            fa += "{0}\n".format(final)

        return fa

    def _format_label(self, sym, replace_alphabet=True):
        """Format label for dot converting (btw. this method perform
        aggregation of transitions for better clarity).

        Return: String (formatted label)
        Keyword arguments:
        sym -- list of symbols
        replace_alphabet -- replace transition labeled with the whole
            alphabel with ^[]
        """
        max_symbols = core_wfa_export.SYMBOLS
        sym_str = str()
        if (set(sym) == set(self.get_alphabet())) and replace_alphabet:
            return "^[]"
        for char in sorted(sym):
            if max_symbols > 0:
                sym_str += aux.convert_to_pritable(chr(char), True)
                max_symbols = max_symbols - 1
            else:
                sym_str += "... {0}".format(len(sym))
                break
        return "[" + sym_str + "]"

    def to_timbuk(self):
        """Convert NFA to Timbuk format (only NFA with single initial state
        can be converted to the Timbuk format).

        Return: String (NFA in Timbuk format)
        """
        if len(super(NFAExport, self).get_starts()) != 1:
            raise nfa.NFAOperationException("Only NFA with a single initial state can be converted to the Timbuk format.")

        timbuk = str()
        timbuk += "Ops "
        for sym in super(NFAExport, self).get_alphabet():
            timbuk += "a{0}:1 ".format(sym)
        timbuk += "x:0\n\n"
        timbuk += "Automaton A1\nStates "
        for state in super(NFAExport, self).get_states():
            timbuk += "q{0} ".format(state)
        timbuk += "\nFinal States "

        for final, _ in super(NFAExport, self).get_finals().iteritems():
            timbuk += "q{0} ".format(final)
        timbuk += "\nTransitions\n"

        timbuk += "x -> q{0}\n".format(super(NFAExport, self).get_starts().keys()[0])
        for transition in super(NFAExport, self).get_transitions():
            timbuk += "a{0}(q{1}) -> q{2}\n".format(transition.symbol, transition.src, transition.dest)

        return timbuk

    def to_vtf(self):
        """Convert NFA to VTF format (VATA library format).

        Return: String (NFA in VTF format)
        """
        vtf = str()
        vtf += "@NFA\n"
        vtf += "%Name A1\n%Initial "
        for state, _ in super(NFAExport, self).get_starts().iteritems():
            vtf += "q{0} ".format(state)

        vtf += "\n%Final "
        for final, _ in super(NFAExport, self).get_finals().iteritems():
            vtf += "q{0} ".format(final)
        vtf += "\n"

        for transition in super(NFAExport, self).get_transitions():
            vtf += "q{0} {1} q{2}\n".format(transition.src, transition.symbol, transition.dest)

        return vtf

    def to_ba(self):
        """Convert NFA to BA format (format of the Rabit&Reduce tool).

        Return: string (BA format).
        """
        if len(super(NFAExport, self).get_starts()) != 1:
            raise nfa.NFAOperationException("Only NFA with a single initial state can be converted to the Timbuk format.")

        ba = str()
        for state, _ in super(NFAExport, self).get_starts().iteritems():
            ba += "q{0}\n".format(state)

        for transition in super(NFAExport, self).get_transitions():
            ba += "{0},q{1}->q{2}\n".format(transition.symbol, transition.src, transition.dest)

        for final, _ in super(NFAExport, self).get_finals().iteritems():
            ba += "q{0}\n".format(final)

        return ba

    def to_msfm(self, preprocess=False):
        """Convert NFA to MSFM format.

        Return: string (MSFM format).
        Keyword arguments:
        preprocess -- Bool, Remove self-loops from final states?
        """

        if len(super(NFAExport, self).get_starts()) != 1:
            raise nfa.NFAOperationException("Only NFA with a single initial state can be converted to the MSFM format.")

        if preprocess:
            self.remove_final_selfloops()

        msfm = str()
        msfm += "{0}\n".format(len(self.get_states()))
        msfm += "{0}\n".format(len(self.get_transitions()))
        msfm += "{0}".format(self.get_starts().keys()[0])

        alph_dict = {}
        i = 0
        for symbol in self.get_alphabet():
            alph_dict[symbol] = i
            i += 1

        for transition in self.get_transitions():
            msfm += "\n{0}|{1}|{2}|0".format(transition.src, alph_dict[transition.symbol], transition.dest)

        msfm += "\n######################################################################################\n"
        msfm += "{0}\n".format(len(self.get_finals()))
        for state, _ in self.get_finals().iteritems():
            msfm += "{0},".format(state)
        msfm += "\n######################################################################################\n"

        msfm += "{0}".format(len(alph_dict))
        for symbol, index in alph_dict.iteritems():
            msfm += "\n{0}:{1}|".format(index, hex(symbol))

        return msfm
