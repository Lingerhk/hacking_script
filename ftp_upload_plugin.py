# -*- coding: utf8 -*- 

import os
import time
import string
import random
import socket
import win32api
import win32con
import base64
from ftplib import FTP

userID = ' '
username = 'test'
password =  'test'
host = '192.168.194.6'
path = './media'
remotepath = '/'
client_keys = ['01TW5JKD','02YUW8B3','03W49GHK']

	
def get_new_name():
	now_time = time.strftime("%Y%m%d",time.localtime())
	chars = string.digits + string.letters
	gen_str = ''.join(random.sample(chars,5))
	new_name = now_time + gen_str + userID +'.mp4'
	return(new_name)
	
def rename_file():
	print '\n'
	for file in os.listdir(path):
		if os.path.isfile(os.path.join(path,file)) == True:
			os.rename(os.path.join(path,file),os.path.join(path,get_new_name()))
			print '%s ==> %s\n' % (file,get_new_name())
			log = open('log.txt','a+')
			action = time.strftime('%Y%m%d %H:%M:%S  ', time.localtime()) + file +' '+ get_new_name()
			log.write(action+'\n')
			log.close()		
	
def uploading():
	for file in os.listdir(path):
		try:
			f = FTP(host)
			f.login(username,password)
			f.cwd(remotepath)
			fd = open(os.path.join(path,file),'rb')
			print u'正在上传：',
			print file
			f.storbinary('STOR %s' % os.path.basename(file),fd)
			fd.close()
			f.quit()
			
		except:
			print '%s' % file
			print u'上传失败！'
	print u'\n视频已全部上传完成！\n'
	print u'按任意键退出!'
	raw_input('') 
	
	
def upload_file():
	try:
		dirs = os.listdir('media')
		print '-'* 50
		print u'已在media文件夹下读取到以下文件:'
		print '-'* 50
		for file in dirs:
			print file+'\n'
		print '-'* 50
		print u'是否全部上传（y/n）?'
		ch = raw_input(' ')
		try:
			if (ch == 'y' or ch == 'Y'):
				rename_file()
				uploading()	
		except:
			print u'已取消上传！'
		
	except :
		print u'无法读取当前的media文件夹，请先创建media文件夹再将视频文件放入其中!'
		s = os.getcwd()
		print u'当前路径为'+s+'\n\n'
		time.sleep(5)

def list_file():
	try:
		f = FTP(host)
		f.login(username,password)
		f.cwd(remotepath)
		print '-'* 50
		print u'服务器文件列表：'
		print '-'* 50
		files = f.dir()
		print files
		print '-'* 50
		f.quit()
		print u'\n按任意键退出!'
		raw_input('') 
	except:
		print u'服务器文件列表获取失败！'
	
def read_reg():
	try:
		subkey = 'SOFTWARE\Microsoft\Windows\CurrentVersion'
		key = win32api.RegOpenKeyEx(win32con.HKEY_LOCAL_MACHINE,subkey,0,win32con.KEY_READ)
		string = win32api.RegQueryValueEx(key,'ftp_client')
		return True
	except:
		return False
		
def add_reg(client_key):
	print 'client_key = %s' % client_key
	try:
		subkey = 'SOFTWARE\Microsoft\Windows\CurrentVersion'
		key = win32api.RegOpenKeyEx(win32con.HKEY_LOCAL_MACHINE,subkey,0,win32con.KEY_ALL_ACCESS)
		win32api.RegSetValueEx(key,'ftp_client',0,win32con.REG_SZ,client_key)
		return True
	except:
		print u'权限不许可，请以管理员权限运行！'
		return False

def running():
	print '\n'+'-'*50
	print u'  1.上传视频文件\n  2.服务器文件列表\n'
	ch = raw_input('==> ')
	try:
		if (ch == '1'):
			upload_file()
		elif(ch == '2'):
			list_file()
		else:
			print u'输入错误！\n'
	except:
		print u'初始化失败！'
		
def get_key():
	global userID
	print u'此上传插件尚未激活，请输入激活密钥:'
	client_key = raw_input('>>>')
	if client_key in client_keys:
		if add_reg(client_key):
			print u'此上传插件已激活！\n'
			userID = client_key[:2]
			print userID
			running()
	else:
		print u'激活失败，请输入正确的密钥！'
	
def login_client():
	if read_reg():
		running()
	else:
		get_key()

if __name__ == '__main__':

	login_client()
	time.sleep(3)

	