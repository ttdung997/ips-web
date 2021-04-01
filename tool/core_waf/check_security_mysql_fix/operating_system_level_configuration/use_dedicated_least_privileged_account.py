import os
import re
import sys
sys.path.insert(0, '/var/log/core_waf/check_security_mysql/')
import helper
error_list = list()

def check(username, password):
	output = os.popen('ps -ef | egrep "^mysql.*$"').read()
	if not output:
		error_list.append('[WARNING] A dedicated least privileged account should be set up for MySQL')
		error_list.insert(0,11200)
	else:
		error_list.insert(0,0)
	return error_list

def fix(username, password):
    pass

def fix_o():
    fix(helper.config_path)

