#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import poplib
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
from email import encoders
from configparser import ConfigParser

def guess_charset(msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset

def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


#问题？f.write能write怎样的数据？
def downloaFile(msg,storePath,keyword):
	if (msg.is_multipart()):
		parts = msg.get_payload()
	i = 0
	for part in parts:
		contenttype = part.get_content_type()#获得附件的类型
		content = part.get_payload(decode=True)
		charset = guess_charset(msg)
		if charset:
			content = content.decode(charset)
		filename = part.get_filename() #获得文件的名称
		if filename and contenttype=='application/octet-stream': #附加的格式
			#save
			filename = decode_str(filename)
			if keyword in filename:	
				print(filename)
				print('正在下载附件：%s'%filename)
				f = open('%s\%s'%(storePath,filename),'wb')
				f.write(content)
				f.close()
				print('附件：%s下载完成'%filename)
				i = i + 1
				print('-------------------------------------')
	return i
def getConfig():
    CONFIGFILE = 'config.txt'
    config = ConfigParser()
    config.read(CONFIGFILE,'utf-8')
    storePath = config.get('common','path')
    keyword = config.get('common','keyword')
    beginEmail = int(config.get('email','begin'))
    lenOfEmail = int(config.get('email','len'))
    username = config.get('email','username')
    password = config.get('email','password')
    pop3_server = config.get('email','pop3_server')
    return storePath,keyword,beginEmail,lenOfEmail,username,password,pop3_server

#获取配置参数：
storePath,keyword,beginEmail,lenOfEmail,username,password,pop3_server = getConfig()
# 连接到POP3服务器:
server = poplib.POP3(pop3_server)
# 可以打开或关闭调试信息:
server.set_debuglevel(1)
# 可选:打印POP3服务器的欢迎文字:
print(server.getwelcome().decode('utf-8'))
# 身份认证:
server.user(username)
server.pass_(password)
# stat()返回邮件数量和占用空间:
print('Messages: %s. Size: %s' % server.stat())
# list()返回所有邮件的编号:
resp, mails, octets = server.list()
# 可以查看返回的列表类似[b'1 82923', b'2 2184', ...]
#print(mails)


index = len(mails) #服务器里面的email总数,同时也是最近的一封邮件的位置

# 获取最新一封邮件, 注意索引号从1开始:
i = index - beginEmail + 1#从最近的第beginEmail封邮件开始处理
sumOfEmail = 0
j = 0 #用于记录当前处理到第几封邮件
while i >= 1 and j < lenOfEmail:
    resp, lines, octets = server.retr(i)
    # lines存储了邮件的原始文本的每一行,
    # 可以获得整个邮件的原始文本:
    msg_content = b'\r\n'.join(lines).decode('utf-8')
    # 稍后解析出邮件:
    msg = Parser().parsestr(msg_content)
    #下载附件
    sumOfEmail = sumOfEmail + downloaFile(msg,storePath,keyword)
    i = i - 1
    j = j + 1
# 可以根据邮件索引号直接从服务器删除邮件:
# server.dele(index)
# 关闭连接:
print('下载的文件的总数为%d'%sumOfEmail)
server.quit()


#碰到的问题
#1、在读取配置文件里面的信息的过程中，出现因为编码的问题无法读取   原因：读取的编码和存储的编码不一致，默认情况下是使用gbk编码来读取的
#2、关于 路径的分隔符的问题
#3、fileName的编码的问题