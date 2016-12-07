# -*- coding:utf-8 -*-

#
# A simple networking data packets
# sniff script using the famous PCAP library.
# Request:
#    pip install impacket pacpy
# by s0nnet. 
#


import sys
import getopt
import pcapy
from impacket.ImpactDecoder import EthDecoder


dev = 'eth0'
filter = 'arp'
decoder = EthDecoder()

# This function wills be called for every packet
# and just print it
def handle_packet(hdr,data):
    print decoder.decode(data)


def usage():
    print sys.argv[0] + ' -i <dev> -f <pcap_filter>'
    sys.exit(1)

# Parsing parameter
try:
    cmd_opts = 'f:i:'
    opts,args = getopt.getopt(sys.argv[1:], cmd_opts)
except getopt.GetoptError:
    usage()


for opt in opts:
    if opt[0] == '-f':
        filter = opt[1]
    elif opt[0] == '-i':
        dev = opt[1]
    else:
        usage()

# Open device in promisc mode
pcap = pcapy.open_live(dev, 1024, 0, 100) # dev,buffer,mode,timeout

# Set pcap filter
pcap.setfilter(filter)

# Start sniffing
pcap.loop(0, handle_packet)
