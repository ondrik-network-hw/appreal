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

import FAdo.fa
import FAdo.fio
import sys
import getopt

import parser.core_parser as core_parser
import parser.wfa_parser as wfa_parser
import wfa.core_wfa_export as core_wfa_export

import wfa.aux_functions as aux

#from scapy.all import *

#Maximum number of packets for learning.
MAXPACKETS = 25000
#Index of the first considered packet.
STARTPACKET = 0
T0 = 1
ALPHA = 0.0001

HELP = "Program for learning PAs from network traffic (uses tool Treba).\n"\
        "-i pcap -- Input .pcap file.\n"\
        "-p -- Convert learned PA into DOT and PNG format (suffix -Prob.dot, -Prob.png).\n"\
        "-s -- Convert support NFA into DOT and PNG format (suffix -Supp.dot, -Supp.png).\n"\
        "-h -- Show this text."

alphabet = set()

class LearningParams(object):
    """Parameters of the application.
    """
    prob = False
    supp = False
    pcap = None
    help = False

    error = False

    def __init__(self):
        pass

    def handleParams(self, argv):
        """Parse parameters and store them.
        """
        self.error = False
        try:
            opts, _ = getopt.getopt(argv[1:], "i:psdh")
        except getopt.GetoptError:
            self.error = True
            return

        for o, arg in opts:
            if o == "-p":
                self.prob = True
            elif o == "-s":
                self.supp = True
            elif o == "-i":
                self.pcap = arg
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
    """Main for traffic learning.
    """
    params = LearningParams()
    params.handleParams(sys.argv)

    if params.error_occured():
        sys.stderr.write("Wrong program parameters\n")
        sys.exit(1)

    if params.help:
        print(HELP)
        sys.exit(0)

    out_name = "learning/MP" + str(MAXPACKETS)
    reader = PcapReader(params.pcap)

    try:
        dot_prob_file = None
        dot_supp_file = None
        fa_file = None
        obs_file = open("{0}.obs".format(out_name), 'w')

        if params.prob:
            dot_prob_file = open("{0}-Prob.dot".format(out_name), 'w')
        if params.supp:
            dot_supp_file = open("{0}-Supp.dot".format(out_name), 'w')
            fa_file = open("{0}.fa".format(out_name), 'w')
    except IOError as e:
        sys.stderr.write("I/O error: {0}\n".format(e.strerror))
        sys.exit(1)

    print "Max packets: ", MAXPACKETS, " start index: ", STARTPACKET
    print "Parsing .pcap file ... "

    write_obs_file(reader, obs_file)

    if not alphabet_check():
        sys.stderr.write("Alphabet should contain 256 symbols and no gaps.\n")
    else:
        print "Alphabet checked: OK"

    print("Learning probabilistic automaton ...")
    os.system("./learning/treba --train=merge --alpha={0} --prior=0.0 --t0={1} {2}.obs > {3}.fsm".format(ALPHA, T0, out_name, out_name))
    try:
        fa =  wfa_parser.WFAParser.treba_to_wfa("{0}.fsm".format(out_name))
        fa.__class__ = core_wfa_export.CoreWFAExport
    except IOError as e:
        sys.stderr.write("I/O error: {0}\n".format(e.strerror))
        sys.exit(1)
    except core_parser.AutomataParserException as e:
        sys.stderr.write("Error during parsing learned PA: {0}\n".format(e.msg))
        sys.exit(1)

    if fa.all_states_final():
        print "All states finals: OK"
    else:
        print "All states finals: Failed (may cause problems during reduction)"

    handle_dots(params, out_name, fa_file, dot_supp_file, dot_prob_file, fa)


def convert_to_treba_obs(dec):
    """Convert packet payload to Treba observation file format.

    Return: String in Treba observation file format.
    Keyword arguments:
    dec -- String to be converted (Packet payload).
    """
    ret = ""
    for ch in dec:
        ret += str(ord(ch)) + " "
        alphabet.add(ord(ch))
    return ret

def handle_dots(params, out_name, fa_file, dot_supp_file, dot_prob_file, fa):
    """Handle outputs (to DOT, FA format).

    Keyword arguments:
    params -- Parameters of the program (console).
    out_name -- Filename of the result PA.
    fa_file -- Filename of the result PA support.
    dot_supp_file -- Filename of the result PA support converted to DOT.
    dot_prob_file -- Filename of the result PA converted to DOT.
    fa -- Learned PA.
    """
    if params.supp:
        handle_support(out_name, fa_file, dot_supp_file, fa)

    if params.prob:
        handle_prob(params, fa, out_name, dot_prob_file)


def handle_support(out_name, fa_file, dot_supp_file, fa):
    """Handle support of the learned PA.

    Keyword arguments:
    out_name -- Filename of the stored support.
    fa_file -- Filehandler of the fado export.
    dot_supp_file -- Filehandler for the export of the support to DOT format.
    fa -- Learned PA.
    """
    fa_file.write(fa.to_automata_fado_format())
    fa_file.close()

    aut = FAdo.fio.readFromFile("{0}.fa".format(out_name))[0]
    print "States of the support: ", len(aut.States)
    aut_minimal =  aut.minimal()
    print "States of the minimal support: ", len(aut_minimal.States)

    if dot_supp_file is not None:
        print "Convert support to .dot format ..."
        dot_supp_file.write(aut_minimal.dotFormat())
        dot_supp_file.close()
        print "Transforming .dot file to .png image ... "
        os.system("dot -Tpng {0}-Supp.dot -o {1}-Supp.png".format(out_name, out_name))

def handle_prob(params, aut, out_name, dot_prob_file):
    """Handle the output of the PA (saving to a file).

    Keyword arguments:
    parser -- WFA parser.
    out_name -- Filename for storing a PA into a file (FA format).
    dot_prob_file -- Filehandler for the export to the DOT format.
    """
    print "Converting PFA to .dot format ... "
    legend = "#States: {0}\n#Packets: {1}\nAlpha: {2}\nt0: {3}\nFile: {4}".format(len(aut.get_states()), MAXPACKETS, ALPHA, T0, params.pcap)

    dot_prob_file.write(aut.to_dot(True, None, legend))
    dot_prob_file.close()
    print "Transforming .dot file to .png image ... "
    os.system("dot -Tpng {0}-Prob.dot -o {1}-Prob.png".format(out_name, out_name))

def alphabet_check():
    """Check whether the alphabet used for packet payloads contains all 256
    ASCII symbols.

    Return: Bool.
    """
    if len(alphabet) != 256:
        return False
    for i in range(0,256):
        if i not in alphabet:
            return False
    return True

def write_obs_file(reader, out_file):
    """Write packet payloads to Treba observation file.

    Keyword arguments:
    reader -- PCAP reader.
    out_file -- Filehandler of the observation file.
    """
    packet_num = 0
    index = 0
    #ports = [80, 25]
    for p in reader:
        if packet_num < MAXPACKETS:
            if p.getlayer(Raw):
                if index < STARTPACKET:
                    index += 1
                else:
                    # string = p.sprintf("{Raw:%Raw.load%}\n")
                    # if scapy.all.TCP in p and (p[scapy.all.TCP].sport in ports or p[scapy.all.TCP].dport in ports):
                    #     print aux.convertToPritable(p.getlayer(Raw).load)
                    #     print p.sprintf("{Raw:%Raw.load%}\n")
                    #.
                    #print(aux.convert_to_pritable(p.getlayer(Raw).load))
                    #print aux.convert_to_pritable(p.getlayer(Raw).load)
                    out_file.write(convert_to_treba_obs(p.getlayer(Raw).load[0:30]) + "\n")
                    packet_num += 1
        else:
            break

    out_file.close()

if __name__ == "__main__":
    main()
