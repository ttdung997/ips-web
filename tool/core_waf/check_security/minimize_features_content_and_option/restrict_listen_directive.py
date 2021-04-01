import os
import re
import sys
sys.path.insert(0, '/var/log/core_waf/check_security/')
import helper
check_num = 0
error_list = list()

def check():
	# print ''
	# print ' Restrict Listen Directive '.center(85, '#')
	# print ''
	global check_num
	result = helper.read_file('/etc/apache2/ports.conf')
	obj = re.compile(r'^\s*Listen (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}):\d+',re.MULTILINE).findall(result)
	obj1 = re.compile(r'^\s*Listen (.+)',re.MULTILINE).findall(result)
	for i in obj:
		if i == '0.0.0.0':
			error_list.append('[WARNING] Detect IP address of all zeros')
			check_num += 1
	if len(obj) != len(obj1):
		error_list.append('[WARNING] Detect listen directive with no IP address specified')
		check_num += 1
		
	if check_num > 0:
		error_list.insert(0, 29)
	else:
		error_list.insert(0, 0)
	# print '[NOTICE] A Listen directive with no IP address specified, or with an IP address of all zeros should not be used'
	error_list.append('[NOTICE] Khong ho tro fix tu dong')
	return error_list
# check()

