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

#import wfa.core_wfa as core_wfa
import wfa.matrix_wfa as matrix_wfa
import wfa.core_wfa_export as core_wfa_export
#import wfa.aux_functions as aux

class MatrixWFAExport(matrix_wfa.MatrixWFA, core_wfa_export.CoreWFAExport):

    def __init__(self, transitions=None, finals=None, start=None, alphabet=None):
        super(MatrixWFAExport, self).__init__(transitions, finals, start, alphabet)
