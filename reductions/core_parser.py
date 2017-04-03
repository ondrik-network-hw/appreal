#!/usr/bin/python

"""
Tool for approximate reductions of finite automata used in network traffic
monitoring.

Author: Vojtech Havlena, <xhavle03@stud.fit.vutbr.cz>
"""

import abc

class AutomataParserException(Exception):
    """Exception used when an error during parsing is occured.
    """
    def __init__(self, msg):
        super(AutomataParserException, self).__init__()
        self.msg = msg

    def __str__(self):
        return self.msg


class AutomataParser(object):
    """Base class for parsing automata (WFA, NFA).
    """
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        pass

    @abc.abstractmethod
    def parse_from_file(self, filename):
        return
