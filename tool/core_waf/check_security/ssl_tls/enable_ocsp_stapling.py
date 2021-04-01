import os
import re
import sys
sys.path.insert(0, '/var/log/core_waf/check_security/')
import helper
check_num = 0
error_list = list()

def check(path):
	# print ''
	# print ' Enable OCSP Stapling '.center(85, '#')
	# print ''
	global check_num
	result = helper.read_file(path)
	vtconf = re.findall(r'[^#]<VirtualHost (.*?)>(.*?)<\/VirtualHost>',result,re.DOTALL)
	ssltap = re.findall(r'^\s*SSLStaplingCache (.+)',result,re.MULTILINE)
	ssluse = re.findall(r'^\s*SSLUseStapling (.+)',result,re.MULTILINE)
	if len(vtconf) != len(ssltap) or len(vtconf) != len(ssluse):
		error_list.append('[WARNING] SSLStaplingCache or SSLUseStapling is not exsit in some VirtualHost')
		check_num += 1
	for i in ssluse:
		if i != 'on' and i != 'On':
			error_list.append('[WARNING] Config SSLUseStapling')
			check_num += 1
			break
	for i in ssltap:
		if i != 'shmcb:logs/ssl_staple_cache(512000)' and i != 'dbm:logs/ssl_staple_cache.db' and i != 'dc:UNIX:logs/ssl_staple_socket':
			error_list.append('[WARNING] Config SSLStaplingCache')
			check_num += 1
			break
	if check_num > 0:
		error_list.insert(0, 42)
	else:
		error_list.insert(0, 0)
	return error_list

def add_directive(ident,path,direct):
	result = helper.read_file(path)
	vtconf = re.findall(r'[^#]<VirtualHost '+ ident +r'>(.*?)<\/VirtualHost>',result,re.DOTALL)
	replace = vtconf[0] + direct
	replace = re.sub(r'[^#]<VirtualHost '+ ident +r'>.*?<\/VirtualHost>','\t<VirtualHost '+ ident +'>' + replace +'\t</VirtualHost>',result,flags=re.DOTALL)
	helper.write_file(path,replace)


def fix_directory(path):
	result = helper.read_file(path)
	replace = re.sub(r'^\s*SSLUseStapling .+','\t\tSSLUseStapling On',result,flags=re.MULTILINE)
	replace = re.sub(r'^\s*SSLStaplingCache .+','\t\tSSLStaplingCache dc:UNIX:logs/ssl_staple_socket',replace,flags=re.MULTILINE)
	helper.write_file(path, replace)

def fix(path):
	a = list()
	result = helper.read_file(path)
	vtconf = re.findall(r'[^#]<VirtualHost (.*?)>(.*?)<\/VirtualHost>',result,re.DOTALL)
	for i in vtconf:
		a.append(i[0])
	for i in a:
		vtconf = re.findall(r'[^#]<VirtualHost '+ i +r'>(.*?)<\/VirtualHost>',result,re.DOTALL)
		ssluse = re.findall(r'^\s*SSLUseStapling (.+)',vtconf[0],re.MULTILINE)
		ssltap = re.findall(r'^\s*SSLStaplingCache (.+)',vtconf[0],re.MULTILINE)
		if len(ssluse) == 0:
			add_directive(i,path,'\tSSLUseStapling On\n')
		if len(ssltap) == 0:
			add_directive(i,path,'\tSSLStaplingCache dc:UNIX:logs/ssl_staple_socket\n')
	result = helper.read_file(path)
	ssluse = re.findall(r'^\s*SSLUseStapling (.+)',result,re.MULTILINE)
	ssltap = re.findall(r'^\s*SSLStaplingCache (.+)',result,re.MULTILINE)
	for i in ssluse:
		if i != 'On' and i != 'on':
			fix_directory(path)
			break
	for i in ssltap:
		if i != 'dc:UNIX:logs/ssl_staple_socket':
			fix_directory(path)
			break

def fix_o():
	fix(helper.ssl_config)