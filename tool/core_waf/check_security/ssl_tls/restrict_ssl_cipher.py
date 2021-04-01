import os
import re
import sys
sys.path.insert(0, '/var/log/core_waf/check_security/')
import helper
check_num = 0
error_list = list()

def check(path):
	# print ''
	# print ' Restrict Weak SSL Ciphers '.center(85, '#')
	# print ''
	global check_num
	result = helper.read_file(path)
	vtconf = re.findall(r'[^#]<VirtualHost (.*?)>(.*?)<\/VirtualHost>',result,re.DOTALL)
	sslhonor = re.findall(r'^\s*SSLHonorCipherOrder (.+)',result,re.MULTILINE)
	sslcipher = re.findall(r'^\s*SSLCipherSuite (.+)',result,re.MULTILINE)
	if len(vtconf) != len(sslcipher) or len(vtconf) != len(sslhonor):
		error_list.append('[WARNING] SSLHonorCipherOrder or SSLCipherSuite is not exsit in some VirtualHost')
		check_num += 1
	for i in sslhonor:
		if i != 'On' and i != 'on':
			error_list.append('[WARNING] Config SSLHonorCipherOrder')
			check_num += 1
			break
	for i in sslcipher:
		if i != 'ALL:!EXP:!NULL:!ADH:!LOW:!SSLv2:!SSLv3:!MD5:!RC4':
			error_list.append('[WARNING] Config SSLCipherSuite')
			check_num += 1
			break
	if check_num > 0:
		error_list.insert(0, 39)
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
	replace = re.sub(r'^\s*SSLHonorCipherOrder .+','\t\tSSLHonorCipherOrder On',result,flags=re.MULTILINE)
	replace = re.sub(r'^\s*SSLCipherSuite .+','\t\tSSLCipherSuite ALL:!EXP:!NULL:!ADH:!LOW:!SSLv2:!SSLv3:!MD5:!RC4',replace,flags=re.MULTILINE)
	helper.write_file(path, replace)

def fix(path):
	a = list()
	result = helper.read_file(path)
	vtconf = re.findall(r'[^#]<VirtualHost (.*?)>(.*?)<\/VirtualHost>',result,re.DOTALL)
	for i in vtconf:
		a.append(i[0])
	for i in a:
		vtconf = re.findall(r'[^#]<VirtualHost '+ i +r'>(.*?)<\/VirtualHost>',result,re.DOTALL)
		sslhonor = re.findall(r'^\s*SSLHonorCipherOrder (.+)',vtconf[0],re.MULTILINE)
		sslcipher = re.findall(r'^\s*SSLCipherSuite (.+)',vtconf[0],re.MULTILINE)
		if len(sslhonor) == 0:
			add_directive(i,path,'\tSSLHonorCipherOrder On\n')
		if len(sslcipher) == 0:
			add_directive(i,path,'\tSSLCipherSuite ALL:!EXP:!NULL:!ADH:!LOW:!SSLv2:!SSLv3:!MD5:!RC4\n')
	result = helper.read_file(path)
	sslhonor = re.findall(r'^\s*SSLHonorCipherOrder (.+)',result,re.MULTILINE)
	sslcipher = re.findall(r'^\s*SSLCipherSuite (.+)',result,re.MULTILINE)
	for i in sslhonor:
		if i != 'On' and i != 'on':
			fix_directory(path)
			break
	for i in sslcipher:
		if i != 'ALL:!EXP:!NULL:!ADH:!LOW:!SSLv2:!SSLv3:!MD5:!RC4':
			fix_directory(path)
			break

def fix_o():
	fix(helper.ssl_config)
