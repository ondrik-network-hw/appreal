#!/usr/bin/env python
###############################################################################
#  payload_gen.py: Script for generating packets and flows from pcap file
#  Copyright (C) 2010 Brno University of Technology, ANT @ FIT
#  Author(s): Milan Dvorak <xdvora66@stud.fit.vutbr.cz>
#             Jan Kastil <ikastil@fit.vutbr.cz>
###############################################################################
#
#  LICENSE TERMS
#
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions
#  are met:
#  1. Redistributions of source code must retain the above copyright
#     notice, this list of conditions and the following disclaimer.
#  2. Redistributions in binary form must reproduce the above copyright
#     notice, this list of conditions and the following disclaimer in
#     the documentation and/or other materials provided with the
#     distribution.
#  3. All advertising materials mentioning features or use of this software
#     or firmware must display the following acknowledgement:
#
#       This product includes software developed by the University of
#       Technology, Faculty of Information Technology, Brno and its
#       contributors.
#
#  4. Neither the name of the Company nor the names of its contributors
#     may be used to endorse or promote products derived from this
#     software without specific prior written permission.
#
#  This software or firmware is provided ``as is'', and any express or implied
#  warranties, including, but not limited to, the implied warranties of
#  merchantability and fitness for a particular purpose are disclaimed.
#  In no event shall the company or contributors be liable for any
#  direct, indirect, incidental, special, exemplary, or consequential
#  damages (including, but not limited to, procurement of substitute
#  goods or services; loss of use, data, or profits; or business
#  interruption) however caused and on any theory of liability, whether
#  in contract, strict liability, or tort (including negligence or
#  otherwise) arising in any way out of the use of this software, even
#  if advised of the possibility of such damage.
#
#  $Id$

import sys
import struct
import socket
import os
import shutil
import random
from optparse import OptionParser, OptionGroup
from netbench.common.traffic import Traffic
from netbench.common.packet import Packet
from netbench.pattern_match.b_nfa import b_nfa
from netbench.pattern_match.parser import parser
from netbench.pattern_match import b_symbol

"""
    Script for dividing pcap file into flows and packets. Inputs are pcap file
    and flow file (by simscript.sh).
    Matching strings for given set of regular expressions can be injected into
    packets with giver probability.
"""

count = 1 # simple packet name
FlowNames = dict() # simple flow name
TrailingInjections = dict()

def generate_text(rule):
    """
        From given regular expression (rule) generate corresponding string.
    """
    aut = b_nfa()
    par = parser("pcre_parser")
    par.set_text(rule)
    if not aut.create_by_parser(par):
        return ""
    aut.remove_epsilons()
    aut.search("a")
    state = 0
    string = ""
    while not state in aut._automaton.final:
        trans = aut._mapper[state]
        rnd1 = random.randint(0, len(trans) - 1)
        sym =  aut._automaton.alphabet[list(trans)[rnd1][0]]
        if sym.get_type() == b_symbol.io_mapper["b_Sym_char_class"]:
            chars = sym.charClass
        else:
            chars = sym.char
        state = list(trans)[rnd1][1]
        rnd2 = random.randint(0, len(chars) - 1)
        string += list(chars)[rnd2]
    if 1 not in aut.search(string):
        print "FAIL"
    return string

def injectToPacket(FlowID, data, packetname):
    """
        Insert generated string or any trailing text from previous packet
        in the flow into packet data.
        When ANCHORED is True, insert only in the begining of packet, else
        insert in random position.
        Debugging information about insertion is printed on stdout.
    """
    global rules
    rnd = random.randint(0, len(rules) - 1)
    rule = rules[rnd]
    rule_num = rnd
    rnd = random.randint(0, len(data) - 1)
    if ANCHORED:
        rnd = 0
    text = generate_text(rule)
    over = 0
    if rnd + len(text) >= len(data):
        over = len(data) - rnd
        TrailingInjections[FlowID] = text[over:]
        print "Trailing from packet", packetname
        text = text[:over]
    data = data[:rnd] + text + data[rnd+len(text):]
    print "Inserted rule", rule_num, "into packet", packetname
    return data

def IP2Long(IPstring):
    return struct.unpack('!L',socket.inet_aton(IPstring))[0]

def Flow2FileName(FlowID, TimeStamps, PerPacket=False):
    """
        From given FlowID generate tuple (flowname, packetname)
    """
# old flow name: FlowName=FlowID+"_"+TimeStamps[0]+"|"+TimeStamps[1]
    iter = 2 if PerPacket else 1
    ret = 2*[""]
    for i in range(iter):
        # select correct directory
        if i:
            os.chdir("packets")
        else:
            os.chdir("flows")
        # packet/flow name
        ret[i] = str(count) if i else str(FlowNames[FlowID])
        # ensure maximum number of files in one directory
        if len(ret[i]) > maxfiles:
            dir = ret[i][:-maxfiles]
            ret[i] = dir + "/" + ret[i][-maxfiles:]
        else:
            dir = "0"
            ret[i] = dir + "/" + ret[i]
        # add flowname to packetname
        if i:
            ret[i] += "-" + ret[0].replace("/", "_")
        if not os.path.isdir(dir):
            os.mkdir(dir) # create dir if necessary
        os.chdir("..") # return back
    return ret
    
def writePacket(FlowID, PerPacket, data):
    """
        Write packet to flow file and possibly to single packet file, if
        PerPacket is set. Also match with regular expression is inserted
        with given probability.
    """
    global count # packet counter
    FlowName = Flow2FileName(FlowID, None, PerPacket)
    trail = TrailingInjections[FlowID]
    if trail:
        # insert trailing text
        print "Trailing to packet", FlowName[1]
        data = trail + data[len(trail):]
        TrailingInjections[FlowID] = ""
    else:
        if random.random() < probability:
            # insert generated text
            data = injectToPacket(FlowID, data, FlowName[1])
    # save to file
    iter = 2 if PerPacket else 1
    ret = 2*[""]
    for i in range(iter): 
        dir = "./packets/" if i else "./flows/"
        FileName = dir + FlowName[i]
        FlowFile=open(FileName,"a")
        FlowFile.write(data)
        FlowFile.close
    count += 1 # increment packet counter

def Flow2FlowID(FlowList):
    """
        Convert list with flow information into FlowID.
        Also assign simple flowname (counter) into global dictionary FlowNames.
    """
    global FlowNames
    global TrailingInjections
    if (len(FlowList) < 7):
        return "NONE"
    FlowName="U"
    if FlowList[0] == '6':
        FlowName = "T"
    FlowName=FlowName+hex(IP2Long(FlowList[1]))[2:]
    FlowName=FlowName+hex(IP2Long(FlowList[2]))[2:]
    FlowName=FlowName+hex(int(FlowList[3]))[2:]
    FlowName=FlowName+hex(int(FlowList[4]))[2:]
    FlowNames[FlowName] = FlowNames.get(FlowName, len(FlowNames))
    TrailingInjections[FlowName] = ""
    return FlowName

# parse options
usage = "usage: %prog file.pcap file.flow [options]"
optparser = OptionParser(usage=usage)
optparser.add_option("-O", "--outputdir", dest="outDir", default="tmp", help="output dir for flows and packets")
optparser.add_option("-P", "--PerPacket", dest="PerPacket", action="store_true", default=False,
                  help="enable export of each packet into single file")
optparser.add_option("-M", "--maxfiles", dest="maxfiles", type="int", default="4", help="maximum number of files in each directory")
group = OptionGroup(optparser, "Options for random string generation based on specified regular expressions. "
                            "You must specify both rulesfile and probability or neither!")
group.add_option("-p", "--probability", dest="probability", type="float", default="0", help="probability of string insertion into packet")
group.add_option("-A", "--anchored", dest="ANCHORED", action="store_true", default=False, help="allow insertion only in the beginning of packet")
group.add_option("-r", "--rulesfile", dest="rulesfile", default="", metavar="FILE", help="file with regular expressions")
optparser.add_option_group(group)
(options, args) = optparser.parse_args()

if len(args) != 2:
    optparser.print_usage()
    print "You must specify both file.pcap and file.flow!"
    exit()

# store options
maxfiles, rulesfile, ANCHORED, probability, PerPacket, outDir = options.maxfiles, options.rulesfile, options.ANCHORED, options.probability, options.PerPacket, options.outDir

if (bool(rulesfile) and bool(probability)) != (bool(rulesfile) or bool(probability)):
    print "You must specify both rulesfile and probability or neither!"
    optparser.print_help()
    exit()
if rulesfile:
    rules = open(rulesfile, 'rb').readlines(1)

if outDir[-1] != "/":
    outDir += "/"
# remove and recreate output dir
try:
    shutil.rmtree("./"+outDir)
except OSError:
    pass
os.mkdir("./"+outDir)
os.mkdir("./"+outDir+"/"+"packets")
os.mkdir("./"+outDir+"/"+"flows")
t = Traffic()
#Second argument of the script is a name of the file containng the flows
FlowFileName = args[1]
FlowFile = open(FlowFileName,'r')
Lines = FlowFile.readlines()
#Flows are stored in the lines. Every line contain Flow identification and timestamp of the first and last packet divided by the coma
FlowTable = dict()
for Line in Lines:
    Tmp = Line.split(',')
    if len(Tmp) <7 : continue
    FlowID = Flow2FlowID(Tmp)
    Timestamps = (Tmp[5],Tmp[6].split('\n')[0])
    if not FlowID in FlowTable.keys():
        FlowTable[FlowID] = list()
    FlowTable[FlowID].append(Timestamps)
    if len(FlowTable[FlowID])>1:
        print(Line.split('\n')[0])

if t.set_file(args[0]):
    os.chdir("./"+outDir)
    while 1:
        pckt = Packet()
        if not t.next_packet(pckt): break
        pckt.parse()
        hdr = pckt.get_packet_header()
        if (hdr.get_headers_type() == ['info','ethernet','ipv4','tcp']) or (hdr.get_headers_type() == ['info','ethernet','ipv4','udp']):
            timestamp = hdr.get_header('info').get_field('timestamp')
            protokol = hdr.get_header('ipv4').get_field('protocol')
            SrcIP = str(hdr.get_header('ipv4').get_field('src_addr'))
            DstIP = str(hdr.get_header('ipv4').get_field('dst_addr'))
            if protokol == 6:
                SrcPort = hdr.get_header('tcp').get_field('src_port')
                DstPort = hdr.get_header('tcp').get_field('dst_port')
            else:
                SrcPort = hdr.get_header('udp').get_field('src_port')
                DstPort = hdr.get_header('udp').get_field('dst_port')
            FlowID = 'U'
            if(protokol == 6):
                FlowID = 'T' 
            FlowID = FlowID+hex(IP2Long(SrcIP))[2:]+hex(IP2Long(DstIP))[2:]+hex(SrcPort)[2:-1]+hex(DstPort)[2:-1]
            if not FlowID in FlowTable.keys():
                print("Critical error - packet is not in the flow")
                print(FlowID)
                print(str(protokol)+"|"+SrcIP+"|"+DstIP+"|"+str(SrcPort)+"|"+str(DstPort))
                continue
            TimeSlots = FlowTable[FlowID]
            found = 0
            for TimeStamps in TimeSlots:
                TS1 = float(TimeStamps[0])
                TS2 = float(TimeStamps[1])
                if((timestamp+0.01) >= TS1 and timestamp <= (TS2+0.01)):
                    found = found + 1
                    TSf = TimeStamps
            if found == 0:
                print("Critical error: Packet is outside of the flows time")
                continue
            if found > 1:
                print("Critical error: Packets belongs to several flows")
                continue
            if FlowID[0] == 'U': # UDP
                udp_len=hdr.get_header('udp').get_field('udp_len')
                if udp_len > 8:
                    udp_data = pckt.get_payload('udp')[8:]
                    writePacket(FlowID, PerPacket, udp_data)
            else: # TCP
                iplen = hdr.get_header('ipv4').get_field('total_len')
                iphlen = hdr.get_header('ipv4').get_field('header_len')
                tcp_data = hdr.get_header('tcp').get_field('data_offset')
                payload_size = iplen - 4*iphlen - 4*tcp_data;
                if payload_size > 0:
                    writePacket(FlowID, PerPacket, pckt.get_payload('tcp')[4*tcp_data:])
