import os
import re
import sys
sys.path.insert(0, '/var/log/core_waf/check_security/')
import helper
check_num = 0
error_list = list()


def check(path):
	# print ''
	# print ' Disable HTTP TRACE Method '.center(85, '#')
	# print ''
	global check_num
	result = helper.read_file(path)
	obj = re.compile(r'^\s*TraceEnable (.*?)\n',re.MULTILINE).findall(result)
	if len(obj) != 0:
		if obj[0] != 'off':
			error_list.append('[WARNING] The Trace method is enable')
			check_num += 1
	else:
		error_list.append("[WARNING] Can't find TraceEnable directive")
		check_num += 1

	if check_num > 0:
		error_list.insert(0, 24)
	else:
		error_list.insert(0, 0)
	return error_list

def fix(path):
	result = helper.read_file(path)
	obj = re.compile(r'^\s*TraceEnable (.*?)\n',re.MULTILINE).findall(result)
	if len(obj) != 0:
		if obj[0] != 'off' or obj[0] != 'Off':
			replace = re.sub(r'^\s*TraceEnable (.*?)\n','TraceEnable off\n',result,flags=re.MULTILINE)
			helper.write_file(path, replace)
	else:
		result = result + '\nTraceEnable off\n'
		helper.write_file(path, result)

def fix_o():
	fix(helper.config_path)
# fix()
# check()
