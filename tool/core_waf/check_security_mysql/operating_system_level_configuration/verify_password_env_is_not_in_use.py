import os
import re
import sys
sys.path.insert(0, '/var/log/core_waf/check_security/')
import helper

check_num = 0
error_list = list()

def check(username,password):
	output = os.popen('grep -s MYSQL_PWD /proc/*/environ').read()
	if output:
		error_list.append('[WARNING] MYSQL_PWD Environment is in used')
		error_list.insert(0,11400)
	else:
		error_list.insert(0,0)
	return error_list

def fix(username, password):
	pass

def fix_o():
	fix(helper.config_path)