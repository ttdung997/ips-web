import os
import re
import sys
sys.path.insert(0, '/var/log/core_waf/check_security/')
import helper
check_num = 0
error_list = list()

def check(path):
	# print ''
	# print ' Set Timeout Limits for Request Headers and Body'.center(85, '#')
	# print ''
	global check_num
	f = os.popen("apache2ctl -M 2> /dev/null | grep reqtimeout ")
	result = f.read()
	f.close()
	if len(result) == 0:
		error_list.append('[WARNING] mod_requesttimeout disable')
		check_num += 1
	result = helper.read_file(path)
	obj = re.findall(r'^\s*RequestReadTimeout (.+)',result,re.MULTILINE)
	if len(obj) == 0:
		error_list.append('[WARNING] RequestReadTimeout directive is not exsit')
		check_num += 1
	else:
		if obj[0] != 'header=20-40,MinRate=500 body=20,MinRate=500':
			error_list.append('[WARNING] RequestReadTimeout value')
			check_num += 1
	if check_num > 0:
		error_list.insert(0, 50)
	else:
		error_list.insert(0, 0)
	return error_list

def enable_req_timeout_mod():
	os.system("a2enmod reqtimeout > /dev/null 2> /dev/null")
	#os.system("service apache2 restart > /dev/null 2> /dev/null")

def add_directive(path):
	result = helper.read_file(path)
	replace = result + 'RequestReadTimeout header=20-40,MinRate=500 body=20,MinRate=500\n'
	helper.write_file(path, replace)

def fix_directive(path):
	result = helper.read_file(path)
	replace = re.sub(r'^\s*RequestReadTimeout .+','RequestReadTimeout header=20-40,MinRate=500 body=20,MinRate=500\n',result,flags=re.MULTILINE)
	helper.write_file(path,replace)

def fix(path):
	f = os.popen("apache2ctl -M 2> /dev/null | grep requesttimeout")
	result = f.read()
	f.close()
	if len(result) == 0:
		enable_req_timeout_mod()
	result = helper.read_file(path)
	obj = re.findall(r'^\s*RequestReadTimeout (.+)',result,re.MULTILINE)
	if len(obj) == 0:
		add_directive(path)
	else:
		if obj[0] != 'header=20-40,MinRate=500 body=20,MinRate=500':
			fix_directive(path)
# fix(helper.config_path)
# check(helper.config_path)
def fix_o():
	fix(helper.config_path)