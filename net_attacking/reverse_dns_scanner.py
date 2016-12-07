# -*- coding:utf-8 -*-

# 
#
#
#
#

import sys
import socket
from random import randint

if len(sys.argv) < 2:
    print sys.argv[0] + "<start_ip>-<end_ip>"
    sys.exit(1)

def get_ips(start_ip, end_ip):
    ips = []
    tmp = []

    for i in start_ip.split('.'):
        tmp.append("%02X" % long(i))

    start_dec = long(''.join(tmp), 16)
    tmp = []

    for i in end_ip.split('.'):
        tmp.append("%02X" % long(i))

    end_dec = long(''.join(tmp), 16)


    while(start_dec < end_dec + 1):
        bytes = []
        bytes.append(str(int(start_dec / 16777216)))
        rem = start_dec % 16777216
        bytes.append(str(int(rem / 65535)))
        rem = rem % 65535
        bytes.append(str(int(rem / 256)))
        rem = rem % 256
        bytes.append(str(rem))
        ips.append(".".join(bytes))
        start_dec += 1

    return ips

def dns_reverse_lookup(start_ip, end_ip):
    ips = get_ips(start_ip, end_ip)

    while len(ips) > 0:
        i = randint(0, len(ips) - 1)
        lookup_ip = str(ips[i])

        try:
            print lookup_ip + ": " + \
            str(socket.gethostbyaddr(lookup_ip)[0])
        except (socket.herror, socket.error):
            pass

        del ips[i]

start_ip, end_ip = sys.argv[1].split('-')
dns_reverse_lookup(start_ip,end_ip)
