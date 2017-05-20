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

import numpy
import core_wfa

class ClosureMode(object):
    """Implemented methods for computing the closure.
    """
    inverse = 1
    iterations = 2 #Iterative matrix multiplication.
    hotelling_bodewig = 3

class MatrixWFAException(Exception):
    """Exception for invalid operations and errors during computing.
    """
    def __init__(self, msg):
        super(MatrixWFAException, self).__init__()
        self.msg = msg

    def __str__(self):
        return self.msg

class MatrixWFA(core_wfa.CoreWFA):
    """Class for matrix operations with WFAs involving matrix operations.
    """
    def __init__(self, transitions=None, finals=None, start=0, alphabet=None):
        super(MatrixWFA, self).__init__(transitions, finals, start, alphabet)

    def are_states_compatible(self):
        """Check whether the states of the WFA are compatible with matrix
        operations (states are labeled with consequtive numbers from 0 to n-1).

        Return: Bool
        """
        states = super(MatrixWFA, self).get_states()
        initial = False
        for i in range(0, len(states)):
            found = False
            if super(MatrixWFA, self).get_start() == i:
                initial = True
            for state in states:
                if state == i:
                    found = True
                    break
            if not found:
                return False

        for state, _ in super(MatrixWFA, self).get_finals().iteritems():
            found = False
            for i in range(0, len(states)):
                if state == i:
                    found = True
                    break
            if not found:
                return False

        return initial

    def get_transition_matrix(self):
        """Get a transition matrix corresponding to the WFA.

        Return: Numpy.matrix (transition matrix)
        """
        if not self.are_states_compatible():
            raise MatrixWFAException("States must be renamed to the set {0,...,n}")

        num_states = len(super(MatrixWFA, self).get_states())
        mtx = numpy.matrix(numpy.empty((num_states,num_states,)))
        mtx[:] = 0.0

        for transition in super(MatrixWFA, self).get_transitions():
            mtx[transition.src, transition.dest] \
                = mtx[transition.src, transition.dest] + transition.weight

        return mtx

    def get_final_vector(self):
        """Get a vector with final weights corresponding to the WFA.

        Return: Numpy.matrix (final vector).
        """
        if not self.are_states_compatible():
            raise MatrixWFAException("States must be renamed to the set {0,...,n}")

        num_states = len(super(MatrixWFA, self).get_states())
        mtx = numpy.matrix(numpy.empty((num_states,)))
        mtx[:] = 0.0

        for state, weight in super(MatrixWFA, self).get_finals().iteritems():
            mtx[0, state] = weight
        return mtx

    def get_final_ones(self):
        """Get a vector with items 1.0 corresponding to final states (other
        states are set to 0).

        Return: Numpy.matrix (final states are set to one).
        """
        if not self.are_states_compatible():
            raise MatrixWFAException("States must be renamed to the set {0,...,n}")

        num_states = len(super(MatrixWFA, self).get_states())
        mtx = numpy.matrix(numpy.empty((num_states,)))
        mtx[:] = 0.0

        for state, weight in super(MatrixWFA, self).get_finals().iteritems():
            if weight > 0.0:
                mtx[0, state] = 1.0
            else:
                mtx[0, state] = 0.0
        return mtx

    def get_initial_vector(self):
        """Get a vector of initial weights.

        Return: Numpy.matrix (of initial weights).
        """
        if not self.are_states_compatible():
            raise MatrixWFAException("States must be renamed to the set {0,...,n}")

        num_states = len(super(MatrixWFA, self).get_states())
        mtx = numpy.matrix(numpy.empty((num_states,)))
        mtx[:] = 0.0
        mtx[0, super(MatrixWFA, self).get_start()] = 1.0
        return mtx

    def compute_transition_closure(self, closure_mode, iterations=0, debug=False):
        """Compute transition closure by a specified method (assume that the
        conditions for given method are met).

        Return: Numpy.matrxi (transition closure).
        Keyword arguments:
        closure_mode -- Method for computing the transition closure (ClosureMode).
        iterations -- Maximum number of iteration (in the case of iterative methods).
        debug -- Show debug info.
        """
        if len(super(MatrixWFA, self).get_states()) == 0:
            return None

        transition_matrix = self.get_transition_matrix()
        identity = numpy.matrix(numpy.identity(len(transition_matrix)))
        result = numpy.matrix(numpy.empty(len(transition_matrix)))

        if debug:
            eig, _ = numpy.linalg.eig(transition_matrix)
            print "Eigenvalue: ", max(abs(eig))

        if closure_mode == ClosureMode.inverse:
            result = (identity - transition_matrix).getI()
        elif closure_mode == ClosureMode.iterations:
            all_mult = identity
            result = identity
            for i in range(iterations):
                if debug:
                    print "Iteration: {0}".format(i)
                all_mult = all_mult * transition_matrix
                result = result + all_mult
        elif closure_mode == ClosureMode.hotelling_bodewig:
            vn = identity
            mtx = identity - transition_matrix
            for i in range(iterations):
                if debug:
                    print "Iteration: {0}".format(i)
                vn = vn*(2*identity - mtx*vn)
            result = vn
        return result

    def compute_language_probability(self, closure_mode, iterations=0, debug=False):
        """Compute the total probability of the WFA.

        Return: String (DOF format)
        Keyword arguments:
        closure_mode -- Method for computing the transition closure (ClosureMode).
        iterations -- Maximum number of iteration (in the case of iterative methods).
        debug -- Show debug info.
        """
        if len(super(MatrixWFA, self).get_states()) == 0:
            return 0.0
        ini = self.get_initial_vector()
        fin = self.get_final_vector().transpose()
        closure = self.compute_transition_closure(closure_mode, iterations, debug)
        return ((ini*closure)*fin)[0,0]

    def compute_language_weight(self, closure_mode, iterations=0, debug=False):
        """Compute the total weight of the WFA.

        Return: String (DOF format)
        Keyword arguments:
        closure_mode -- Method for computing the transition closure (ClosureMode).
        iterations -- Maximum number of iteration (in the case of iterative methods).
        debug -- Show debug info.
        """
        if len(super(MatrixWFA, self).get_states()) == 0:
            return 0.0
        ini = self.get_initial_vector()
        fin = self.get_final_ones().transpose()
        closure = self.compute_transition_closure(closure_mode, iterations, debug)
        return ((ini*closure)*fin)[0,0]
