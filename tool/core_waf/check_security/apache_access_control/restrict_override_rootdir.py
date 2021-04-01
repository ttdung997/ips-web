import os
import re
import sys
sys.path.insert(0, '/var/log/core_waf/check_security/')
import helper

check_num = 0
error_list = list()

def check(path):
	# print ''
	# print ' Restrict Override for the OS Root Directory '.center(85, '#')
	# print ''
	global check_num
	result = helper.read_file(path)
	obj = re.compile(r'[^#]<Directory \/>(.*?)<\/Directory>',re.DOTALL).findall(result)
	if len(obj) != 0:
		if obj[0].find('AllowOverride ') == -1:
			error_list.append('[WARNING] AllowOverride directive is not exist in root directory')
			check_num += 1
		else:
			obj1 = re.compile(r'^\s*AllowOverride (.*?)\n',re.MULTILINE).findall(obj[0])
			if obj1[0] != 'None':
				error_list.append('[WARNING] Value of AllowOverride is not set to None in root directory')
				check_num += 1
		if obj[0].find('AllowOverrideList') != -1:
			error_list.append('[WARNING] AllowOverrideList is exist in root directory')
			check_num += 1
	else:
		error_list.append('[WARNING] RootDirectory is not exist')
		check_num += 1

	if check_num > 0:
		error_list.insert(0, 15)
	else:
		error_list.insert(0, 0)
	return error_list
	

def add_allowoverride(path):
	result = helper.read_file(path)
	obj = re.compile(r'<Directory \/>(.*?)<\/Directory>',re.DOTALL).findall(result)
	replace = obj[0] + '\tAllowOverride None\n'
	replace1 = re.sub(r'<Directory \/>(.*?)<\/Directory>','\n<Directory />'+replace+'</Directory>',result, flags=re.DOTALL)
	helper.write_file(path, replace1)

def remove_allowoverridelist(path):
	result = helper.read_file(path)
	obj = re.compile(r'<Directory \/>(.*?)<\/Directory>',re.DOTALL).findall(result)
	replace = re.sub(r'^\s*AllowOverrideList (?:.*?)\n','\n',obj[0],flags=re.MULTILINE)
	replace1 = re.sub(r'<Directory \/>(.*?)<\/Directory>','\n<Directory />'+replace+'</Directory>',result, flags=re.DOTALL)
	helper.write_file(path, replace1)

def set_allowoverride(path):
	result = helper.read_file(path)
	obj = re.compile(r'<Directory \/>(.*?)<\/Directory>',re.DOTALL).findall(result)
	replace = re.sub(r'^\s*AllowOverride (?:.*?)\n','\tAllowOverride None\n',obj[0],flags=re.MULTILINE)
	replace1 = re.sub(r'<Directory \/>(.*?)<\/Directory>','\n<Directory />'+replace+'</Directory>',result, flags=re.DOTALL)
	helper.write_file(path, replace1)

def fix(path):
	result = helper.read_file(path)
	obj = re.compile(r'[^#]<Directory \/>(.*?)<\/Directory>',re.DOTALL).findall(result)
	if len(obj) != 0:
		if obj[0].find('AllowOverride ') == -1:
			add_allowoverride(path)
		else:
			obj1 = re.compile(r'^\s*AllowOverride (.*?)\n',re.MULTILINE).findall(obj[0])
			if obj1[0] != 'None':
				set_allowoverride(path)
		if obj[0].find('AllowOverrideList') != -1:
			remove_allowoverridelist(path)

def fix_o():
	fix(helper.config_path)

# check_override('/etc/apache2/apache123.conf')
# add_allowoverride('/etc/apache2/apache123.conf')
# remove_allowoverridelist('/etc/apache2/apache123.conf')
# set_allowoverride('/etc/apache2/apache123.conf')