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
import scapy.all

import asthma.fpta as fpta
import asthma.core_asthma as core_asthma
import asthma.predicates as predicates

import wfa.aux_functions as aux

MAXPACKETS = 25000
OMEGA = 1000
STARTPACKET = 0

def main():

    reader = PcapReader(sys.argv[1])
    tree, num = create_fpta(reader)

    # tree = fpta.FPTA()
    # tree.add_string("aba")
    # tree.add_string("abb")
    # tree.add_string("abc")
    # tree.add_string("aca")
    # tree.add_string("ada")

    tree.set_flat_transitions()

    pred = construct_predicates()

    learning_handler = core_asthma.Asthma(tree, pred)
    learning_handler.learn_pa(OMEGA, True, True)
    learned_pa = learning_handler.get_pa()

    sys.stderr.write("#States: {0}\n".format(len(learned_pa.get_states())))

    convert_to_dot(learned_pa, pred, sys.argv[1], sys.argv[2], num)


def construct_predicates():
    alphabet = frozenset(range(0, 256))
    pred = predicates.Predicates([predicates.PredicateItem("empty", frozenset()), predicates.PredicateItem("all", alphabet)])
    return pred

def convert_to_dot(learned_pa, pred, pcap, res_file, num):
    learned_pa.rename_states()
    state_label = {}
    for old, new in learned_pa.get_rename_dict().iteritems():
        state_label[new] = "{0}".format(old.data.name)

    predicates_list = str()
    for pr in pred:
        predicates_list += pr.name + ", "
    legend = "#States: {0}\n#Packets: {1}\nOmega: {2}\nPredicates: {3}\nFile: {4}".format(len(learned_pa.get_states()), num, OMEGA, predicates_list, pcap)

    try:
        fl = open("{0}.fa".format(res_file), 'w')
        fl.write(learned_pa.to_fa_format())
        fl.close()

        fl = open("{0}.dot".format(res_file), 'w')
        fl.write(learned_pa.to_dot(True, state_label, legend))
        fl.close()
    except IOError as e:
        sys.stderr.write("I/O error: {0}\n".format(e.strerror))
        sys.exit(1)


def create_fpta(reader):
    """Write packet payloads to Treba observation file.

    Keyword arguments:
    reader -- PCAP reader.
    out_file -- Filehandler of the observation file.
    """
    tree = fpta.FPTA()
    packet_num = 0
    index = 0
    ports = [25]
    for p in reader:
        if packet_num < MAXPACKETS:
            if p.getlayer(Raw):
                if index < STARTPACKET:
                    index += 1
                else:
                    # string = p.sprintf("{Raw:%Raw.load%}\n")
                    #if scapy.all.TCP in p and (p[scapy.all.TCP].sport in ports or p[scapy.all.TCP].dport in ports):
                        #     print aux.convertToPritable(p.getlayer(Raw).load)
                        #     print p.sprintf("{Raw:%Raw.load%}\n")
                        #.
                    payload = p.getlayer(Raw).load[0:30]
                    # if payload[0] == 'C':
                    #     sys.stderr.write("{0} {1}\n".format(packet_num, aux.convert_to_pritable(payload)))
                    tree.add_string(payload)
                    packet_num += 1
                    #    sys.stderr.write("{0}\n".format(packet_num))
                        #print packet_num

        else:
            break

    return (tree, packet_num)


if __name__ == "__main__":
    main()
