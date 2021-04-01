import os
import re
import sys
sys.path.insert(0, '/var/log/core_waf/check_security/')
import helper
error_list = list()

def check(path):
	# print ''
	# print ' Allow Appropriate Access to Web Content '.center(85, '#')
	# print ''
	result = helper.read_file(path)
	obj = re.compile(r'[^#]<Directory \/>(?:.*?)<\/Directory>',re.DOTALL).findall(result)
	if len(obj) != 1:
		error_list.append('[WARNING] Number of DocumentRoot in apache config more than one')
		error_list.insert(0, 14)
	else:
		error_list.insert(0, 0)
	error_list.append('[NOTICE] Ensure that the Order/Deny/Allow directives are NOT used for the all directory')
	error_list.append('[NOTICE] Ensure the Require directives have values that are appropriate for the purposes of the directory')
	return error_list

