#!/usr/bin/python

import sys
import os
import socket
import urllib
from random import randint

# Often used proxy ports
proxy_ports = [3128, 8080, 8181, 8000, 1080, 80]

# URL we try to fetch
get_host = "www.google.com"
socket.setdefaulttimeout(3)

# get a list of ips from start / stop ip
def get_ips(start_ip, stop_ip):
    ips = []
    tmp = []

    for i in start_ip.split('.'):
        tmp.append("%02X" % long(i))

    start_dec = long(''.join(tmp), 16)
    tmp = []

    for i in stop_ip.split('.'):
        tmp.append("%02X" % long(i))

    stop_dec = long(''.join(tmp), 16)

    while(start_dec < stop_dec + 1):
        bytes = []
        bytes.append(str(int(start_dec / 16777216)))
        rem = start_dec % 16777216
        bytes.append(str(int(rem / 65536)))
        rem = rem % 65536
        bytes.append(str(int(rem / 256)))
        rem = rem % 256
        bytes.append(str(rem))
        ips.append(".".join(bytes))
        start_dec += 1

    return ips


# try to connect to the proxy and fetch an url
def proxy_scan(ip):
    # for every proxy port
    for port in proxy_ports:
        try:
            # try to connect to the proxy on that port
            s = socket.socket(socket.AF_INET,
                              socket.SOCK_STREAM)
            s.connect((ip, port))
            print ip + ":" + str(port) + " OPEN"

            # try to fetch the url
            print "GET " + get_host + " HTTP/1.0\n"
            s.send("GET " + get_host + " HTTP/1.0\r\n")
            s.send("\r\n")

            # get and print response
            while 1:
                data = s.recv(1024)

                if not data:
                    break

                print data

            s.close()
        except socket.error:
            print ip + ":" + str(port) + " Connection refused"

# parsing parameter
if len(sys.argv) < 2:
    print sys.argv[0] + ": <start_ip-stop_ip>"
    sys.exit(1)
else:
    if len(sys.argv) == 3:
        get_host = sys.argv[2]

    if sys.argv[1].find('-') > 0:
        start_ip, stop_ip = sys.argv[1].split("-")
        ips = get_ips(start_ip, stop_ip)

        while len(ips) > 0:
            i = randint(0, len(ips) - 1)
            lookup_ip = str(ips[i])
            del ips[i]
            proxy_scan(lookup_ip)
    else:
        proxy_scan(sys.argv[1])
