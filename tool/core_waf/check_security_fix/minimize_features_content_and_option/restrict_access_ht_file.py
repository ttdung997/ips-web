import os
import re
import sys
sys.path.insert(0, '/var/log/core_waf/check_security/')
import helper
check_num = 0
error_list = list()

def check(path):
	# print ''
	# print ' Restrict Access to .ht* files '.center(85, '#')
	# print ''
	global check_num
	result = helper.read_file(path)
	obj = re.compile(r'[^#]<FilesMatch "\^\\\.ht">(.*?[^#])<\/FilesMatch>',re.DOTALL).findall(result)
	if len(obj) == 0:
		error_list.append('[WARNING] FilesMatch directive is not present in the apache configuration')
		check_num += 1
	else:
		if obj[0][1:-1] != 'Require all denied':
			error_list.append('[WARNING] FilesMatch directive is not config to restrict access to any file .ht*')
			check_num += 1
			
	if check_num > 0:
		error_list.insert(0, 26)
	else:
		error_list.insert(0, 0)
	return error_list


def fix(path):
	result = helper.read_file(path)
	obj = re.compile(r'[^#]<FilesMatch "\^\\\.ht">(.*?[^#])<\/FilesMatch>',re.DOTALL).findall(result)
	if len(obj) == 0:
		replace = result + '<FilesMatch "^\.ht">\nRequire all denied\n</FilesMatch>\n'
		helper.write_file(path, replace)
	else:
		if obj[0] != 'Require all denied\n':
			replace = re.sub(r'<FilesMatch "\^\\\.ht">(?:.*?[^#])<\/FilesMatch>','',result,flags=re.DOTALL)
			replace1 = replace + '<FilesMatch "^\.ht">\nRequire all denied\n</FilesMatch>\n'
			helper.write_file(path, replace1)

def fix_o():
	fix(helper.config_path)