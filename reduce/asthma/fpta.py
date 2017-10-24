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

import asthma.tree as tree
import wfa.core_wfa_export as core_wfa_export
import wfa.core_wfa as core_wfa

class FPTA(core_wfa_export.CoreWFAExport):

    def __init__(self):
        super(FPTA, self).__init__()
        self._nodes = {}
        self._edges = []
        self._root = tree.Tree(0, {})
        self._nodes[self._root] = 0
        self.set_starts({self._root: 1.0})

    def _create_path(self, root, pref, string):
        if len(string) == 0:
            root.value += 1
            root.freq += 1
            self._nodes[root] += 1
            return

        new = tree.Tree(0, {})
        new.name = pref

        self._nodes[new] = 0
        trans = core_wfa.Transition(root, new, ord(string[0]), 1)
        root.transitions[ord(string[0])] = trans
        root.freq += 1

        self._edges.append(trans)
        self._create_path(new, pref + string[1:2], string[1:])

    def add_string(self, string):
        act = self._root

        for i in range(len(string)):
            try:
                trans = act.transitions[ord(string[i])]
                trans.weight += 1
                act.freq += 1
                act = trans.dest
            except KeyError:
                self._create_path(act, string[0:i+1], string[i:])
                act = None
                break
        if act != None:
            act.value += 1
            act.freq += 1
            self._nodes[act] += 1

        self.set_finals(self._nodes)
        self.set_transitions(self._edges)

    def _set_flat_transitions(self, node):
        tmp = node.transitions.values()
        node.transitions = tmp
        for trans in node.transitions:
            self._set_flat_transitions(trans.dest)

    def set_flat_transitions(self):
        self._set_flat_transitions(self._root)
