# -*- coding:utf-8 -*-
#
# A tiny tool to report all newly
# connected devices to our network
# with IP and MAC.It can detect if
# ones MAC has changed.

from scapy.all import sniff,ARP
from signal import signal,SIGINT
import sys

arp_watcher_db_file = '/var/cache/arp-watcher.db'
ip_mac = {}

# Save ARP table on shutdown
def sig_int_handler(signum,frame):
    print 'Got SIGINT. Saving ARP database...'
    try:
        f = open(arp_watcher_db_file,'w')
        for (ip,mac) in ip_mac.items():
            f.write(ip + '' + mac + '\n')

        f.close()
        print 'Done.'
    except IOError:
        print 'Cannot write file' + arp_watcher_db_file
        sys.exit(1)


def watch_arp(pkt):
    #Got is-at pkt (ARP response)
    if pkt[ARP].op == 2:
        print pkt[ARP].hwsrc + ' ' + pkt[ARP].psrc

        #Device is now. Remember it.
        if ip_mac.get(pkt[ARP].psrc) == None:
            print 'Found new device' + pkt[ARP].hwsrc + ' ' + pkt[ARP].psrc
            ip_mac[pkt[ARP].psrc] = pkt[ARP].hwsrc



signal(SIGINT,sig_int_handler)

if len(sys.argv) < 2:
    print sys.argv[0] + '<iface>'
    sys.exit(0)


try:
    fh = open(arp_watcher_db_file,'r')
except IOError:
    print 'Cannot read file' + arp_watcher_db_file
    sys.exit(1)


for line in fh:
    line.chomp()
    (ip,mac) = line.split(' ')
    ip_mac[ip] = mac

sniff(prn=watch_arp,filter='arp',iface=sys.argv[1],store=0)
