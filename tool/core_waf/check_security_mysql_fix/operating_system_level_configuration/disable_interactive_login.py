import os
import re
import sys
sys.path.insert(0, '/var/log/core_waf/check_security/')
import helper

check_num = 0
error_list = list()

def check(username, password):
	output = os.popen('getent passwd mysql | egrep "^.*[\/bin\/false|\/sbin\/nologin]$"').read()
	if not output:
		error_list.append('[WARNING] MySQL Interactive Login is not disabled')
		error_list.insert(0,11500)
	else:
		error_list.insert(0,0)
	return error_list

def fix(username, password):
	output = os.system('usermod -s /bin/false')

def fix_o():
	fix(helper.config_path)