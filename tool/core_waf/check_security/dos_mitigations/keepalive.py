import os
import re
import sys
sys.path.insert(0, '/var/log/core_waf/check_security/')
import helper
check_num = 0
error_list = list()

def check(path):
	# print ''
	# print ' Set the KeepAlive directive to On '.center(85, '#')
	# print ''
	global check_num
	result = helper.read_file(path)
	obj = re.findall(r'^\s*KeepAlive (.+)',result,re.MULTILINE)
	if len(obj) == 0:
		error_list.append('[WARNING] KeepAlive directive is not exsit')
		check_num += 1
	else:
		if obj[0] != 'On' and obj[0] != 'on':
			error_list.append('[WARNING] KeepAlive disable')
			check_num += 1
	if check_num > 0:
		error_list.insert(0, 47)
	else:
		error_list.insert(0, 0)
	return error_list

def add_directive(path):
	result = helper.read_file(path)
	replace = result + 'KeepAlive On\n'
	helper.write_file(path, replace)

def fix_directive(path):
	result = helper.read_file(path)
	replace = re.sub(r'^\s*KeepAlive .+','KeepAlive On\n',result,flags=re.MULTILINE)
	helper.write_file(path, replace)

def fix(path):
	result = helper.read_file(path)
	obj = re.findall(r'^\s*KeepAlive (.+)',result,re.MULTILINE)
	if len(obj) == 0:
		add_directive(path)
	else:
		if obj[0] != 'On' and obj[0] != 'on':
			fix_directive(path)

# fix(helper.config_path)
# check(helper.config_path)
def fix_o():
	fix(helper.config_path)