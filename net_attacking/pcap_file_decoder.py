# -*- coding:utf-8 -*-

#
# A simple script to reading and 
# writing PACP Dump File using EthDecoder.
# by s0nnet

import sys
import getopt
import pcapy
from impacket.ImpactDecoder import EthDecoder
from impacket.ImpactPacket import IP

dev = 'eth0'
decoder = EthDecoder()
input_file = None
dump_file = 'sniffer.pcap'

def write_packet(hdr,data):
    print decoder.decode(data)
    dumper.dump(hdr,data)

def read_packet(hdr,data):
    ether = decoder.decode(data)
    if ether.get_ether_type() == IP.ethertype:
        iphdr = ether.child()
        tcphdr = iphdr.child()
        print iphdr.get_ip_src() + ':' + \
                str(tcphdr.get_th_sport()) + \
                ' -> ' + iphdr.get_ip_dst() + ':' + \
                str(tcphdr.get_th_dport())


def usage():
    print sys.argv[0] + """
    -i <dev>
    -r <input_file>
    -w <output_file>"""
    sys.exit(1)

# Parse parameter
try:
    cmd_opts = 'i:r:w:'
    opts, args = getopt.getopt(sys.argv[1:], cmd_opts)
except getopt.GetoptError:
    usage()

for opt in opts:
    if opt[0] == '-w':
        dump_file = opt[1]
    elif opt[0] == '-i':
        dev = opt[1]
    elif opt[0] == '-r':
        input_file = opt[1]
    else:
        usage()

# Start sniffing and write packet to a pacp dump file
if input_file == None:
    pcap = pcapy.open_live(dev, 1024, 0, 100)
    dumper = pcap.dump_open(dump_file)
    pcap.loop(0, write_packet)

# Read a pacp dump file and print it
else:
    pcap = pcapy.open_offline(input_file)
    pcap.loop(0, read_packet)
