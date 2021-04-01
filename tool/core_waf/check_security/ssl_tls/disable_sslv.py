import os
import re
import sys
sys.path.insert(0, '/var/log/core_waf/check_security/')
import helper
check_num = 0
error_list = list()

def check(path):
	# print ''
	# print ' Disable the SSL v3.0 Protocol '.center(85, '#')
	# print ''
	global check_num
	result = helper.read_file(path)
	vtconf = re.findall(r'[^#]<VirtualHost (.*?)>(.*?)<\/VirtualHost>',result,re.DOTALL)
	obj = re.findall(r'^\s*SSLProtocol\s+(.+)',result,re.MULTILINE)
	if len(obj) != len(vtconf):
		error_list.append('[WARNING] SSLProtocol directive is not exsit in some VirtualHost')
		check_num += 1
	for i in range (len(obj)):
		if obj[i] != 'TLSv1.1 TLS1.2':
			error_list.append('[WARNING] Disable the TLS v1.0 & v3.0 Protocol')
			check_num += 1
			break
	if check_num > 0:
		error_list.insert(0, 38)
	else:
		error_list.insert(0, 0)
	return error_list

def add_directive(ident,path,content):
	result = helper.read_file(path)
	replace = content + '\tSSLProtocol TLSv1.1 TLS1.2\n'
	replace = re.sub(r'[^#]<VirtualHost '+ ident +r'>.*?<\/VirtualHost>','\t<VirtualHost '+ ident +'>' + replace +'\t</VirtualHost>',result,flags=re.DOTALL)
	helper.write_file(path,replace)

def fix_directive(path):
	result = helper.read_file(path)
	replace = re.sub(r'^\s*SSLProtocol\s+.+','\t\tSSLProtocol TLSv1.1 TLS1.2',result,flags=re.MULTILINE)
	helper.write_file(path, replace)


def fix(path):
	a = list()
	result = helper.read_file(path)
	obj = re.findall(r'^\s*SSLProtocol\s+(.+)',result,re.MULTILINE)
	vtconf = re.findall(r'[^#]<VirtualHost (.*?)>(.*?)<\/VirtualHost>',result,re.DOTALL)
	for i in vtconf:
		a.append(i[0])
	for i in a:
		vtconf = re.findall(r'[^#]<VirtualHost '+ i +r'>(.*?)<\/VirtualHost>',result,re.DOTALL)
		obj2 = re.findall(r'^\s*SSLProtocol\s+(.+)',vtconf[0],re.MULTILINE)
		if len(obj2) == 0:
			add_directive(i,path,vtconf[0])
	for i in range (len(obj)):
		if obj[i] != 'TLSv1.1 TLS1.2':
			fix_directive(path)
			break

def fix_o():
	fix(helper.ssl_config)