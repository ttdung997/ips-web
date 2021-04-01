import os
import re
import sys
sys.path.insert(0, '/var/log/core_waf/check_security/')
import helper
error_list = list()

def check(path):
	# print ''
	# print ' Minimize Options for Other Directories '.center(85, '#')
	# print ''
	result = helper.read_file(path)
	obj = re.compile(r'^\s*Options Includes\s*?\n',re.MULTILINE).findall(result)
	if len(obj) != 0:
		error_list.append('[WARNING] Detect Options Includes enable')
		error_list.insert(0, 19)
	else:
		error_list.insert(0, 0)
	return error_list

def fix(path):
	result = helper.read_file(path)
	obj = re.compile(r'^\s*Options Includes\s*?\n',re.MULTILINE).findall(result)
	if len(obj) != 0:
		replace = re.sub(r'^\s*Options Includes\s*?\n','\tOptions None\n',result, flags=re.MULTILINE)
		helper.write_file(path, replace)

def fix_o():
	fix(helper.config_path)
	
# check_options_includes('/etc/apache2/apache123.conf')
# modify_options('/etc/apache2/apache123.conf')
# fix(helper.config_path)
# check(helper.config_path)