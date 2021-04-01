import os
import re
import sys
sys.path.insert(0, '/var/log/core_waf/check_security/')
import helper
check_num = 0
error_list = list()

def check(path):
	# print ''
	# print ' Restrict Options for the Web Root Directory '.center(85, '#')
	# print ''
	global check_num
	result = helper.read_file(path)
	obj = re.compile(r'[^#]<Directory '+helper.get_DocumentRoot()+r'>(.*?)<\/Directory>',re.DOTALL).findall(result)
	if len(obj) != 0:
		obj1 = re.compile(r'^\s*Options (.*?)\n',re.MULTILINE).findall(obj[0])
		if len(obj1) == 0:
			error_list.append('[WARNING] Options directive is not exist')
			check_num += 1
		if obj1[0] != 'None':
			error_list.append('[WARNING] Value of Options is not set to None')
			check_num += 1
	else:
		error_list.append("[WARNING] Can't find web root <Directory> configure <***ko fix tu dong***>")
		check_num += 1
	if check_num > 0:
		error_list.insert(0, 18)
	else:
		error_list.insert(0, 0)
	return error_list

def add_options(path):
	webroot = helper.get_DocumentRoot()
	result = helper.read_file(path)
	obj = re.compile(r'[^#]<Directory '+webroot+r'>(.*?)<\/Directory>',re.DOTALL).findall(result)
	replace = obj[0] + '\tOptions None\n'
	replace1 = re.sub(r'[^#]<Directory '+webroot+r'>(.*?)<\/Directory>','\n<Directory '+webroot+'>'+replace+'</Directory>',result, flags=re.DOTALL)
	helper.write_file(path, replace1)

def set_options(path):
	webroot = helper.get_DocumentRoot()
	result = helper.read_file(path)
	obj = re.compile(r'[^#]<Directory '+webroot+r'>(.*?)<\/Directory>',re.DOTALL).findall(result)
	replace = re.sub(r'^\s*Options (?:.*?)\n','\tOptions None\n',obj[0],flags=re.MULTILINE)
	replace1 = re.sub(r'[^#]<Directory '+webroot+r'>(.*?)<\/Directory>','\n<Directory '+webroot+'>'+replace+'</Directory>',result, flags=re.DOTALL)
	helper.write_file(path, replace1)


def fix(path):
	result = helper.read_file(path)
	obj = re.compile(r'[^#]<Directory '+helper.get_DocumentRoot()+r'>(.*?)<\/Directory>',re.DOTALL).findall(result)
	if len(obj) != 0:
		obj1 = re.compile(r'^\s*Options (.*?)\n',re.MULTILINE).findall(obj[0])
		if len(obj1) == 0:
			add_options(path)
		if obj1[0] != 'None':
			set_options(path)

def fix_o():
	fix(helper.config_path)

