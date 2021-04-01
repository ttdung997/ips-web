import os
import re
import sys
sys.path.insert(0, '/var/log/core_waf/check_security/')
import helper
check_num = 0
error_list = list()

def check(path):
	# print ''
	# print " Set ServerSignature to 'Off' ".center(85, '#')
	# print ''
	global check_num
	result = helper.read_file(path)
	obj = re.compile(r'^\s*ServerSignature (.+)',re.MULTILINE).findall(result)
	if len(obj) == 0:
		error_list.append('[WARNING] ServerSignature directive is not exist')
		check_num += 1
	else:
		if obj[0] != 'Off' and obj[0] != 'off':
			error_list.append('[WARNING] ServerSignature has a value incorrect')
			check_num += 1
	if check_num > 0:
		error_list.insert(0, 45)
	else:
		error_list.insert(0, 0)
	return error_list

def add_directive(path):
	result = helper.read_file(path)
	replace = result + 'ServerSignature Off\n'
	helper.write_file(path, replace)

def set_directive(path):
	result = helper.read_file(path)
	replace = re.sub(r'^\s*ServerSignature (?:.+)','ServerSignature Off\n',result,flags=re.MULTILINE)
	helper.write_file(path, replace)

def fix(path):
	result = helper.read_file(path)
	obj = re.compile(r'^\s*ServerSignature (.+)',re.MULTILINE).findall(result)
	if len(obj) == 0:
		add_directive(path)
	else:
		if obj[0] != 'Off' and obj[0] != 'off':
			set_directive(path)

def fix_o():
	fix(helper.config_path)