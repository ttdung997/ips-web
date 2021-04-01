import os
import fileinput
import sys
sys.path.insert(0, '/var/log/core_waf/check_security/')
import helper

error_list = list()

def check(path):
	# print ''
	# print ' Secure Core Dump Directory '.center(85, '#')
	# print ''
	f = os.popen('cat ' + path + ' | grep CoreDumpDirectory')
	result = f.read()
	f.close()
	if len(result) == 0:
		error_list.insert(0, 0)
	else:
		error_list.append('[WARNING] CoreDumpDirectory is configure')
		error_list.insert(0, 7)
	return error_list

def fix_perm_coredumpdirectory():
	os.system('chown -R root ' + check())
	os.system('chgrp -R www-data ' + check())
	os.system('chmod o-rwx ' + check())
	#os.system('service apache2 restart')

def fix(path):
	keyword1 = "CoreDumpDirectory"
	replacement1 = ""
	for line in fileinput.input(path, inplace=True):
	    line = line.rstrip()
	    if keyword1 in line:
	        line = line.replace(line, replacement1)
	    print line


def fix_o():
	fix(helper.config_path)
# check()

