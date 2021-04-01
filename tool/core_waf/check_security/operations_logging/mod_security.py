import os
import re
import sys
sys.path.insert(0, '/var/log/core_waf/check_security/')
import helper
error_list = list()

def check():
	# print ''
	# print ' Check install modsecurity '.center(85, '#')
	# print ''
	f = os.popen('apache2ctl -M 2> /dev/null | grep security')
	result = f.read()
	f.close()
	if len(result) == 0:
		error_list.append('[WARNING] Modsecurity is not install in apache server')
		error_list.insert(0, 34)
	else:
		error_list.insert(0, 0)
	error_list.append('[NOTICE] See https://www.modsecurity.org/download.html for detail')
	return error_list

# check()