#!/usr/bin/env python
# coding=utf-8
#
#  A client online remind script.
#  When a client was online,this script 
#  will show who he is with an linux system box
#


import os
import time
import urllib

ON_URL = 'http://xxxx.sinaapp.com/online_ok.txt'

def get_msg(box_msg):
    
    list = box_msg.split('@')
    userID = list[0]
    on_time = int(list[1].replace(':',''))
    lo_time = int(time.strftime('%H%M',time.localtime()))

    cmd = "notify-send '%s在%s上线了'" % (userID,list[1].strip('\n'))


    if (lo_time-2 < on_time) and (lo_time+2 > on_time):
        os.system(cmd)

if __name__=='__main__':

    while True:
        try:
            box_msg  = urllib.urlopen(ON_URL).read()
            get_msg(box_msg)

        except:
            time.sleep(100)
        time.sleep(20)
