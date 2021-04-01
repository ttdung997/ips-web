import os
import re
import sys
sys.path.insert(0, '/var/log/core_waf/check_security/')
import helper

check_num = 0
error_list = list()

def check(path):
	# print ''
	# print ' Restrict Override for All Directories '.center(85, '#')
	# print ''
	global check_num
	result = helper.read_file(path)
	obj = re.compile(r'^\s*AllowOverride (.*?)\n',re.MULTILINE).findall(result)
	for i in obj:
		if i != 'None':
			error_list.append('[WARNING] Value of AllowOverride is not set to None')
			check_num += 1
			break
	obj1 = re.compile(r'^\s*AllowOverrideList (?:.*?)\n',re.MULTILINE).findall(result)
	if len(obj1) != 0 :
		error_list.append('[WARNING] AllowOverrideList is exist')
		check_num += 1
	if check_num > 0:
		error_list.insert(0, 16)
	else:
		error_list.insert(0, 0)
	return error_list

	
def set_allowoverride(path):
	result = helper.read_file(path)
	replace = re.sub(r'^\s*AllowOverride (?:.*?)\n','\tAllowOverride None\n',result,flags=re.MULTILINE)
	helper.write_file(path, replace)


def remove_allowoverridelist(path):
	result = helper.read_file(path)
	replace = re.sub(r'AllowOverrideList (?:.*?)\n','\n',result)
	helper.write_file(path, replace)

def fix(path):
	result = helper.read_file(path)
	obj = re.compile(r'^\s*AllowOverride (.*?)\n',re.MULTILINE).findall(result)
	for i in obj:
		if i != 'None':
			set_allowoverride(path)
			break
	obj1 = re.compile(r'^\s*AllowOverrideList (?:.*?)\n',re.MULTILINE).findall(result)
	if len(obj1) != 0 :
		remove_allowoverridelist(path)

# fix('/etc/apache2/apache123.conf')
# check('/etc/apache2/apache123.conf')
# remove_allowoverridelist('/etc/apache2/apache123.conf')
def fix_o():
	fix(helper.config_path)