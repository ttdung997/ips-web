import os
import re
import sys
sys.path.insert(0, '/var/log/core_waf/check_security/')
import helper
error_list = list()

def check():
	# print ''
	# print ' Restrict Group Write Access for the Document Root Directories and Files '.center(85, '#')
	# print ''
	f = os.popen("find -L " + helper.get_DocumentRoot() + " -group www-data -perm /g=w -ls")
	result = f.read()
	f.close()
	if len(result) != 0:
		error_list.append('[WARNING] Detect file or directory in the Apache DocRoot with group write access')
		error_list.insert(0, 12)
	else:
		error_list.insert(0, 0)
	return error_list

def fix():
	os.system("find -L " + helper.get_DocumentRoot() + " -group www-data -perm /g=w -print | xargs chmod g-w 2> /dev/null")
	os.system("service apache2 reload > /dev/null 2> /dev/null")


def fix_o():
	fix()
	
# print helper.get_DocumentRoot()


# check()