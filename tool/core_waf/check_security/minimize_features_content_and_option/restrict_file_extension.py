import os
import re
import sys
sys.path.insert(0, '/var/log/core_waf/check_security/')
import helper
error_list = list()


def check(path):
	# print ''
	# print ' Restrict File Extensions '.center(85, '#')
	# print ''
	# f = os.popen("find "+ helper.get_DocumentRoot() +" -type f -name '*.*' | awk -F. '{print $NF }' | sort -u")
	# result = f.read().split('\n')
	# print 'List of existing file extension on the web server:'
	# for i in result:
	# 	print i,
	# print '\n[NOTICE] Review the list of existing file extensions, for appropriate content for the web server, remove those that are inappropriate and add any additional file extensions expected to be added to the web server in the near future.'
	result = helper.read_file(path)
	obj = re.compile(r'[^#]<FilesMatch \"\^\.\*\$\">\n\s*Require all denied\n</FilesMatch>\n',re.DOTALL).findall(result)
	if len(obj) == 0:
		error_list.append("[WARNING] No denies access to all files by default")
		error_list.insert(0, 27)
	else:
		error_list.insert(0, 0)
	return error_list

def fix(path):
	result = helper.read_file(path)
	replace = result + '\n<FilesMatch "^.*$">\n\tRequire all denied\n</FilesMatch>\n'
	helper.write_file(path, replace)


def fix_o():
	fix(helper.config_path)