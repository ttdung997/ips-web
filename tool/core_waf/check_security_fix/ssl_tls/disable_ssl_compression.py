import os
import re
import sys
sys.path.insert(0, '/var/log/core_waf/check_security/')
import helper
error_list = list()

def check(path):
	# print ''
	# print ' Ensure SSL Compression is not Enabled '.center(85, '#')
	# print ''
	result =helper.read_file(path)
	obj = re.findall(r'^\s*SSLCompression (.+)',result,re.MULTILINE)
	if len(obj) == 0:
		error_list.insert(0, 0)
	else:
		if obj[0] != 'off' and obj[0] != 'Off':
			error_list.append('[WARNING] SSLCompression must be set to off')
			error_list.insert(0, 41)
		else:
			error_list.insert(0, 0)
	return error_list

def fix(path):
	result =helper.read_file(path)
	replace = re.sub(r'^\s*SSLCompression .+','SSLCompression off\n',result,flags=re.MULTILINE)
	helper.write_file(path, replace)

def fix_o():
	fix(helper.ssl_config)
