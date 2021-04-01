import os
import re
import sys
sys.path.insert(0, '/var/log/core_waf/check_security/')
import helper
error_list = list()

def check(path):
	# print ''
	# print ' Restrict Browser Frame Options '.center(85, '#')
	# print ''

	result = helper.read_file(path)
	obj = re.findall(r'(^\s*Header always append X-Frame-Options SAMEORIGIN|Header always append X-Frame-Options DENY)',result, re.MULTILINE)
	if len(obj) == 0:
		error_list.append('[WARNING] Header directive for X-Frame-Options config')
		error_list.insert(0, 30)
	else:
		error_list.insert(0, 0)
	return error_list

def fix(path):
	result = helper.read_file(path)
	obj = re.findall(r'(^\s*Header always append X-Frame-Options SAMEORIGIN|Header always append X-Frame-Options DENY)',result, re.MULTILINE)
	if len(obj) == 0:
		result = helper.read_file(path)
		replace = result + 'Header always append X-Frame-Options SAMEORIGIN\n'
		helper.write_file(path, replace)
	
def fix_o():
	fix(helper.config_path)
