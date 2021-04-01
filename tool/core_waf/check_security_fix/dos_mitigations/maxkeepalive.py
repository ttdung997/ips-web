import os
import re
import sys
sys.path.insert(0, '/var/log/core_waf/check_security/')
import helper
check_num = 0
error_list = list()

def check(path):
	# print ''
	# print ' Set MaxKeepAliveRequests to 100 or greater '.center(85, '#')
	# print ''
	global check_num
	result = helper.read_file(path)
	obj = re.findall(r'^\s*MaxKeepAliveRequests (.+)',result,re.MULTILINE)
	if len(obj) == 0:
		error_list.append('[WARNING] MaxKeepAliveRequests directive is not exsit')
		check_num += 1
	else:
		if int(obj[0]) < 100:
			error_list.append('[WARNING] MaxKeepAliveRequests too short')
			check_num += 1
	if check_num > 0:
		error_list.insert(0, 48)
	else:
		error_list.insert(0, 0)
	return error_list

def add_directive(path):
	result = helper.read_file(path)
	replace = result + 'MaxKeepAliveRequests 100\n'
	helper.write_file(path, replace)

def fix_directive(path):
	result = helper.read_file(path)
	replace = re.sub(r'^\s*MaxKeepAliveRequests .+','MaxKeepAliveRequests 100\n',result,flags=re.MULTILINE)
	helper.write_file(path, replace)

def fix(path):
	result = helper.read_file(path)
	obj = re.findall(r'^\s*MaxKeepAliveRequests (.+)',result,re.MULTILINE)
	if len(obj) == 0:
		add_directive(path)
	else:
		if int(obj[0]) < 100:
			fix_directive(path)

# fix(helper.config_path)
# check(helper.config_path)
def fix_o():
	fix(helper.config_path)