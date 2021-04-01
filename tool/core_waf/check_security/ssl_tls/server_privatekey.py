import os
import re
import sys
sys.path.insert(0, '/var/log/core_waf/check_security/')
import helper
check_num = 0
error_list = list()

def get_dir(path):
	result = helper.read_file(path)
	key = re.findall(r'^\s*SSLCertificateKeyFile (.+)',result,re.MULTILINE)
	tmp = key[0].split('/')
	del tmp[-1]
	a = '/'.join(x for x in tmp)
	return a

def check(path):
	# print ''
	# print " Protect the Server's Private Key ".center(85, '#')
	# print ''
	global check_num
	result = helper.read_file(path)
	cert = re.findall(r'^\s*SSLCertificateFile\s+(.+)',result,re.MULTILINE)
	key = re.findall(r'^\s*SSLCertificateKeyFile (.+)',result,re.MULTILINE)
	if len(cert) == 0 or len(key) == 0:
		error_list.append('[WARNING] SSLCertificateFile or SSLCertificateKeyFile not exsit')
		check_num += 1
	else:
		if  cert[0].split('/')[-2] == key[0].split('/')[-2]:
			error_list.append('[WARNING] Key file and cert file in the same directory')
			check_num += 1
	f = os.popen('ls -la ' + get_dir(path) + ' | grep ".key"')
	result = f.read()
	tmp = result.split('\n')
	for i in range (len(tmp) - 1):
		obj = tmp[i].split()
		if obj[0] != '-r--------' or obj[2] != 'root' or obj[3] != 'root':
			error_list.append('[WARNING] Permission of key file ' + obj[-1])
			check_num += 1
	if check_num > 0:
		error_list.insert(0, 37)
	else:
		error_list.insert(0, 0)
	return error_list


def move_keyfile():
	return 0

def fix(path):
	path_key = get_dir(path)
	f = os.popen("ls "+ path_key + "/ | grep '.key'" )
	result = f.read()
	f.close()
	key = result.split()
	for i in key:
		os.system('chmod 400 ' + path_key + "/" + i)
		os.system('chown root:root ' + path_key + "/" + i)

def fix_o():
	fix(helper.ssl_config)

# check(helper.ssl_config)
# fix(helper.ssl_config)