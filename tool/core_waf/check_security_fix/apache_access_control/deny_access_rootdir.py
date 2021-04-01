import os
import re
import sys
sys.path.insert(0, '/var/log/core_waf/check_security/')
import helper
check_num = 0
error_list = list()

def check(path):
	# print ''
	# print ' Deny Access to OS Root Directory '.center(85, '#')
	# print ''
	global check_num
	result = helper.read_file(path)
	obj = re.compile(r'[^#]<Directory \/>(.*?)<\/Directory>',re.DOTALL).findall(result)
	if len(obj) != 0:
		if obj[0].find('Allow ') != -1 or obj[0].find('Order ') != -1 or obj[0].find('Deny ') != -1:
			error_list.append('[WARNING] Using the deprecated Order/Deny/Allow method	in OS Root Directory')
			check_num += 1
		
		value = re.compile(r'^\s*Require (.*?)\n',re.MULTILINE).findall(obj[0])
		if len(value) != 0:
			if value[0] != 'all denied':
				error_list.append('[WARNING] Value of Require method is not all denied in Root Directory')
				check_num += 1
		else:
			error_list.append('[WARNING] Require directive is not exist in Root Directory')
			check_num += 1
	else:
		error_list.append('[WARNING] RootDirectory is not exist')
		check_num += 1

	if check_num > 0:
		error_list.insert(0, 13)
	else:
		error_list.insert(0, 0)
	return error_list

def fix_require_value(path):
	result = helper.read_file(path)
	obj = re.compile(r'<Directory \/>(.*?)<\/Directory>',re.DOTALL).findall(result)
	replace = re.sub(r'^\s*Require (.*?)\n','\tRequire all denied\n',obj[0],flags=re.MULTILINE)
	replace1 = re.sub(r'<Directory \/>(.*?)<\/Directory>','\n<Directory />'+replace+'</Directory>',result, flags=re.DOTALL)
	helper.write_file(path, replace1)

def delete_allow_order_deny_method(path):
	result = helper.read_file(path)
	obj = re.compile(r'<Directory \/>(.*?)<\/Directory>',re.DOTALL).findall(result)
	value = re.compile(r'^\s*(Allow|Order|Deny) (.*?)\n',re.MULTILINE).findall(obj[0])
	if value != '':
		replace = re.sub(r'^\s*(Allow|Order|Deny) (.*?)\n','\n',obj[0],flags=re.MULTILINE)
		replace1 = re.sub(r'<Directory \/>(.*?)<\/Directory>','\n<Directory />'+replace+'</Directory>',result, flags=re.DOTALL)
	helper.write_file(path, replace1)

def add_require_directive(path):
	result = helper.read_file(path)
	obj = re.compile(r'<Directory \/>(.*?)<\/Directory>',re.DOTALL).findall(result)
	replace = obj[0] + '\tRequire all denied\n'
	replace1 = re.sub(r'<Directory \/>(.*?)<\/Directory>','\n<Directory />'+replace+'</Directory>',result, flags=re.DOTALL)
	helper.write_file(path, replace1)

def fix(path):
	result = helper.read_file(path)
	obj = re.compile(r'[^#]<Directory \/>(.*?)<\/Directory>',re.DOTALL).findall(result)
	if len(obj) != 0:
		if obj[0].find('Allow ') != -1 or obj[0].find('Order ') != -1 or obj[0].find('Deny ') != -1:
			delete_allow_order_deny_method(path)
		
		value = re.compile(r'^\s*Require (.*?)\n',re.MULTILINE).findall(obj[0])
		if len(value) != 0:
			if value[0] != 'all denied':
				fix_require_value(path)
		else:
			add_require_directive(path)

def fix_o():
	fix(helper.config_path)
# print get_file_config()
# check_access('/etc/apache2/apache123.conf')
# add_require_directive('/etc/apache2/apache123.conf')
# delete_allow_order_deny_method('/etc/apache2/apache123.conf')
# fix_require_value('/etc/apache2/apache123.conf')