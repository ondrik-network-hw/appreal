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
from scapy.utils import os

import sys
import getopt

import core_parser
import nfa_parser as parser
import aux_functions as aux

import scapy.all

#from scapy.all import *

#Maximum number of considered packets
MAXPACKETS = 1000000
#Filter packets by a substring
SUBSTRING = True
#Filter packets by ports.
PORTS = None #for instance [80, 25]

HELP = "Program for network traffic filtering captured in .pcap file (print statistics or matched payload on stdout).\n"\
        "-p file -- Input .pcap file.\n"\
        "-n aut -- NFA for payload match.\n"\
        "-s string -- String for payload match (in printable format).\n"\
        "-c count -- Max scanned packets from input file.\n"\
        "-o -- Print matched packets on stdout.\n"\
        "-h -- Show this text."

class FilterParams:
    """Parameters of the application.
    """
    pcap = None
    input_nfa = None
    input_string = None
    count = None
    show = False
    help = False

    error = False

    def __init__(self):
        pass

    def handle_params(self, argv):
        """Parse parameters and store them.
        """
        self.error = False
        try:
            opts, _ = getopt.getopt(argv[1:], "p:n:s:c:oh")
        except getopt.GetoptError:
            self.error = True
            return

        for o, arg in opts:
            if o == "-p":
                self.pcap = arg
            elif o == "-n":
                self.input_nfa = arg
            elif o == "-s":
                self.input_string = arg
            elif o == "-c" and arg.isdigit():
                self.count = int(arg)
            elif o == "-o":
                self.show = True
            elif o == "-h":
                self.help = True
            else:
                self.error = True

    def error_occured(self):
        """Check whether the input parameters are well given.

        Return: Bool (True=error)
        """
        if self.help:
            return False
        if self.pcap == None or self.error:
            return True
        else:
            return False

def main():
    """Main for the packet fitering.
    """
    params = FilterParams()
    params.handle_params(sys.argv)
    if params.error_occured():
        sys.stderr.write("Wrong program parameters\n")
        sys.exit(1)
    if params.help:
        print(HELP)
        sys.exit(0)

    nfa_parser = parser.NFAParser()

    input_nfa = None
    input_string = params.input_string
    reader = None

    try:
        if params.input_nfa != None:
            input_nfa = nfa_parser.fa_to_nfa(params.input_nfa)
        reader = PcapReader(params.pcap)
    except IOError as e:
        sys.stderr.write("I/O error: {0}\n".format(e.strerror))
        sys.exit(1)
    except core_parser.AutomataParserException as e:
        sys.stderr.write("Error during parsing NFA: {0}\n".format(e.msg))
        sys.exit(1)
    except Exception as e:
        sys.stderr.write("Error during parsing input files: {0}\n".format(e.message))
        sys.exit(1)


    if params.count == None:
        max_packets = MAXPACKETS
    else:
        max_packets = params.count

    ca,cr,ia,sa = filter_packets(input_nfa, input_string, reader, max_packets, params.show)

    print("Input NFA accepted: {0}".format(ia))
    print("String accepted: {0}".format(sa))
    print("Packets: {0}, Raw packets: {1}".format(ca, cr))

    return 0


def filter_packets(nfa, match_string, reader, max_packets, show):
    """Filter packets stored in PCAP file.

    Return: (Int, Int, Int, Int) (number of all packets (incuding empty),
        number of nonepty packets, number of packets accepted by the input NFA,
        number of packets mathed by a string).
    Keyword arguments:
    nfa -- Input NFA.
    match_string -- String pattern.
    reader -- PCAP reader.
    max_packets -- Maximum number of considered packets.
    show -- Show matched/accepted packets.
    """
    counter_all = 0
    counter_real = 0
    input_accept = 0
    string_accept = 0

    for p in reader:
        if counter_all >= max_packets:
            break

        if p.getlayer(Raw):
            if PORTS is not None:
                if not (scapy.all.TCP in p and (p[scapy.all.TCP].sport in PORTS\
                    or p[scapy.all.TCP].dport in PORTS)):
                    continue

            string = p.getlayer(Raw).load
            printable = aux.convert_to_pritable(string)
            acc = 0

            if nfa is not None:
                if nfa.accept_word(string, False):
                    input_accept += 1
                    acc += 1
            if match_string is not None:
                if not SUBSTRING and printable.startswith(match_string):
                    string_accept += 1
                    acc += 1
                elif SUBSTRING and (match_string in printable):
                    string_accept += 1
                    acc += 1

            if show and acc > 0:
                print(printable)
            counter_real += 1

        counter_all += 1

    return (counter_all, counter_real, input_accept, string_accept)

if __name__ == "__main__":
    main()
