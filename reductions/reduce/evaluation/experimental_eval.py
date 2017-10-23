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

from scapy.all import PcapReader, Raw

import sys
import getopt

import parser.core_parser as core_parser
import parser.nfa_parser as parser

#Maximum number of considerated packets
MAXPACKETS = 1

class EvalParams(object):
    """Parameters of the application.
    """
    pcap = None
    input_nfa = None
    reduced_nfa = None
    count = None

    error = False

    def __init__(self):
        pass

    def handle_params(self, argv):
        """Parse parameters and store them.
        """
        self.error = False
        try:
            opts, _ = getopt.getopt(argv[1:], "p:r:i:c:")
        except getopt.GetoptError:
            self.error = True
            return

        for opt, arg in opts:
            if opt == "-p":
                self.pcap = arg
            elif opt == "-r":
                self.reduced_nfa = arg
            elif opt == "-i":
                self.input_nfa = arg
            elif opt == "-c" and arg.isdigit():
                self.count = int(arg)
            else:
                self.error = True

    def error_occured(self):
        """Check whether the input parameters are well given.

        Return: Bool (True=error)
        """
        if self.pcap == None or self.input_nfa == None \
            or self.reduced_nfa == None or self.error:
            return True
        else:
            return False

def main():
    """Main for experimental evaluation.
    """
    params = EvalParams()
    params.handle_params(sys.argv)
    if params.error_occured():
        sys.stderr.write("Wrong program parameters\n")
        sys.exit(1)

    input_nfa = None
    reduced_nfa = None
    reader = None

    try:
        input_nfa = parser.NFAParser.fa_to_nfa(params.input_nfa)
        reduced_nfa = parser.NFAParser.fa_to_nfa(params.reduced_nfa)
        reader = PcapReader(params.pcap)
    except IOError as exc:
        sys.stderr.write("I/O error: {0}\n".format(exc.strerror))
        sys.exit(1)
    except core_parser.AutomataParserException as exc:
        sys.stderr.write("Error during parsing NFA: {0}\n".format(exc.msg))
        sys.exit(1)

    if params.count == None:
        max_packets = MAXPACKETS
    else:
        max_packets = params.count

    #print reduced_nfa.accept_word("530 L")
    #return 0

    c_all, c_real, in_acc, red_acc, err = compare_automata(reader,\
        input_nfa, reduced_nfa, max_packets)

    print "Input NFA accepted: {0}".format(in_acc)
    print "Reduced NFA accepted: {0}".format(red_acc)
    print "Misclassified: {0}, error: {1}".format(err, float(err)/c_all)
    print "Packets: {0}, Raw packets: {1}".format(c_all, c_real)

    return 0

def compare_automata(reader, input_nfa, reduced_nfa, max_packets):
    """Compare two automata according to an input traffic.

    Return (Int, Int, Int, Int, Int) (number of all packets (incuding empty),
        number of nonepty packets, number of packets accepted by the input NFA,
        number of packets accepted by the reduced NFA, number of misclassified
        packets).
    Keyword arguments:
    reader -- PCAP reader.
    input_nfa -- Input NFA.
    reduced_nfa -- Reduced NFA.
    max_packets -- Maximum number of considered packets.
    """
    counter_all = 0
    counter_real = 0
    input_accept = 0
    reduced_accept = 0
    misclassified = 0
    acc = 0
    input_tr_dict = input_nfa.get_dictionary_transitions()
    red_tr_dict = reduced_nfa.get_dictionary_transitions()
    #total = 0
    for packet in reader:
        if counter_all >= max_packets:
            break

        if packet.getlayer(Raw):
            string = packet.getlayer(Raw).load
        else:
            string = ""

        acc = 0

        if input_nfa.accept_word(string, False, input_tr_dict):
            acc += 1
            input_accept += 1
        if reduced_nfa.accept_word(string, False, red_tr_dict):
            acc += 1
            reduced_accept += 1

        if acc == 1:
            misclassified += 1

        counter_real += 1
        counter_all += 1

    return (counter_all, counter_real, input_accept,\
        reduced_accept, misclassified)

if __name__ == "__main__":
    main()
