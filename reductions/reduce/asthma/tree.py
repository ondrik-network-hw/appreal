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

class Tree(object):

    def __init__(self, value, transitions=None):
        self.value = value
        self.transitions = transitions
        self.data = None
        self.freq = 0
        self.name = ""
        self.max_freq = 0

    def __str__(self):
        return "{0}: {1}".format(self.name, self.data.name)

    def __repr__(self):
        return self.__str__()
