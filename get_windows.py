# -*- coding: utf-8 -*-
#
# running in windows:
# get all the active window's tittle
#

from win32gui import *

titles = set()

def foo(hwnd,nouse):
    if IsWindow(hwnd) and IsWindowEnabled(hwnd) and IsWindowVisible(hwnd):
        titles.add(GetWindowText(hwnd))

EnumWindows(foo, 0)
lt = [t for t in titles if t]
lt.sort()
for t in lt:
    print t
