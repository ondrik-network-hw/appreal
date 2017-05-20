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

def convert_to_pritable(dec, dot=False):
    """Convert string containing also non-printable characters to printable hexa
    number. Inspired by the Netbench tool.

    Return: Input string with replaced nonprintable symbols with their hexa numbers.
    Keyword arguments:
    dec -- Input string.
    dot -- Use the result for converting to dot format.
    """
    esc_str = str()
    for ch in dec:
        if (ord(ch) > 127) or (ord(ch) < 30):
            esc_str = esc_str + "\\" + hex(ord(ch))
        elif ch == '\'':
            esc_str += "\\" + hex(ord(ch))
        elif ch== '\\' and dot:
            esc_str += "\\\\"
        elif ch == '\\' and not dot:
            esc_str += "\\"
        elif ch == '"':
            esc_str += "\\" + hex(ord(ch))
        else:
            esc_str = esc_str + ch
    return esc_str

def get_related(relation, item):
    """Get all items that are in relation with item.

    Return: List of all related items.
    Keyword arguments:
    relation -- Binary relation (a set of pairs).
    item -- Find items related with item.
    """
    ret = []
    for first, second in list(relation):
        if second == item:
            ret.append(first)
    return ret


def list_powerset(lst):
    """The powerset of the list lst.

    Return: Power list.
    Keyword arguments:
    lst -- pattern (list) for the power list.
    """
    result = [[]]
    for x in lst:
        result.extend([subset + [x] for subset in result])
    return result

def merge_equivalence_classes(eq_class, item1, item2):
    """Merge two equivalence classes given by item1 and item2.

    Return: Modified equivalence class by merging classes
        containing item1 and item2.
    Keyword arguments:
    eq_class -- The set of equivalence classes.
    item1, item2 -- The items specifying classes to merge.
    """
    set1 = None
    set2 = None
    for part in list(eq_class):
        if item1 in part:
            set1 = part
        if item2 in part:
            set2 = part

    if set1 == None or set2 == None:
        return eq_class

    eq_class.discard(set1)
    eq_class.discard(set2)
    eq_class.add(set1 | set2)

    return eq_class
