import os
import re
import sys
sys.path.insert(0, '/var/log/core_waf/check_security/')
import helper
check_num = 0
error_list = list()

def check(path):
	# print ''
	# print ' Set KeepAliveTimeout Low to Mitigate Denial of Service '.center(85, '#')
	# print ''
	global check_num
	result = helper.read_file(path)
	obj = re.findall(r'^\s*KeepAliveTimeout (.+)',result,re.MULTILINE)
	if len(obj) == 0:
		error_list.append('[WARNING] KeepAliveTimeout directive is not exsit')
		check_num += 1
	else:
		if int(obj[0]) > 15:
			error_list.append('[WARNING] KeepAliveTimeout too long')
			check_num += 1
	if check_num > 0:
		error_list.insert(0, 49)
	else:
		error_list.insert(0, 0)
	return error_list

def add_directive(path):
	result = helper.read_file(path)
	replace = result + 'KeepAliveTimeout 10\n'
	helper.write_file(path, replace)

def fix_directive(path):
	result = helper.read_file(path)
	replace = re.sub(r'^\s*KeepAliveTimeout .+','KeepAliveTimeout 10\n',result,flags=re.MULTILINE)
	helper.write_file(path, replace)

def fix(path):
	result = helper.read_file(path)
	obj = re.findall(r'^\s*KeepAliveTimeout (.+)',result,re.MULTILINE)
	if len(obj) == 0:
		add_directive(path)
	else:
		if int(obj[0]) > 15:
			fix_directive(path)

# fix(helper.config_path)
# check(helper.config_path)
def fix_o():
	fix(helper.config_path)