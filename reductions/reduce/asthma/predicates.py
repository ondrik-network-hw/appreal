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

import collections

PredicateItem = collections.namedtuple('PredicateItem', ['name', 'symbols'])

class PredicateException(Exception):
    def __init__(self, msg):
        super(PredicateException, self).__init__()
        self.msg = msg

    def __str__(self):
        return self.msg


class Predicates(object):

    def __init__(self, predicates):
        self._predicates = predicates
        self._top = PredicateItem("T", None)

    def __iter__(self):
        return iter(self._predicates)

    def add_predicate(self, predicate_item):
        self._predicates.append(predicate_item)

    def get_top(self):
        return self._top

    def get_top_pred(self):
        if len(self._predicates) == 0:
            raise PredicateException("Predicates must contain at least one predicate.")
        return self._predicates[-1]

    def get_bottom_pred(self):
        if len(self._predicates) == 0:
            raise PredicateException("Predicates must contain at least one predicate.")
        return self._predicates[0]

    def _least_predicate_set(self, set1, set2):
        if (set1 is None) or (set2 is None):
            return self._top
        for pred in self._predicates:
            if (set1.union(set2)) <= pred.symbols:
                return pred

        raise PredicateException("There is no least predicate {0}, {1}.".format(set1, set2))

    def least_predicate_contains(self, pred, contains):
        return self._least_predicate_set(pred.symbols, contains)

    def least_predicate(self, pred1, pred2):
        return self._least_predicate_set(pred1.symbols, pred2.symbols)
