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
import wfa.matrix_wfa as matrix_wfa
import label.state_labels as state_labels
import abc

class CoreReduction(object):
    """Base class for operations used for NFA reductions.
    """

    __metaclass__ = abc.ABCMeta

    def __init__(self, pa, i_nfa):
        """Set input PA and NFA.

        Keyword arguments:
        pa -- PA as an input for a reduction
        nfa -- NFA as an input for a reduction
        """
        self.pa = pa
        self.pa.__class__ = matrix_wfa.MatrixWFA
        self.nfa = i_nfa
        self.nfa.__class__ = nfa.NFA
        self.state_labels = state_labels.StateLabels(pa, i_nfa)


    def get_nfa(self):
        """Get a stored NFA (input for a reduction). Return NFA.
        """
        return self.nfa

    def get_pa(self):
        """Get a stored PA (input for a reduction). Return MatrixWFA.
        """
        return self.pa

    def prepare(self):
        """Make a preparation for reduction (trimming input automata,
        rename their states). Return void.
        """
        self.pa = self.pa.get_trim_automaton()
        self.pa.rename_states()
        self.pa.__class__ = matrix_wfa.MatrixWFA

        self.nfa = self.nfa.get_trim_automaton()
        self.nfa.rename_states()
        self.nfa.__class__ = nfa.NFA
        #self.state_labels.prepare()

    def get_labels(self):
        """Get state labels (necessary for the reduction).

        Return: Dict: State -> Float
        """
        return self.state_labels.get_labels()

    def set_labels(self, lab):
        """Set state labels used for the reduction.

        Keyword arguments:
        lab -- New state labels, Dict: State -> Float
        """
        self.state_labels.set_labels(lab)

    @abc.abstractmethod
    def compute_labels(self, approx, sparse=False):
        """Compute state labels (abstract method).

        Keyword arguments:
        approx -- Compute the state labels approximately (Bool).
        """
        return
