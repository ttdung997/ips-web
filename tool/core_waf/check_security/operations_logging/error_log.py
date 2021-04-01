import os
import re
import sys
sys.path.insert(0, '/var/log/core_waf/check_security/')
import helper
check_num = 0
error_list = list()

def check(path):
	# print ''
	# print ' Configure the Error Log '.center(85, '#')
	# print ''
	global check_num
	result = helper.read_file(path)
	obj = re.compile(r'^\s*LogLevel (.+)',re.MULTILINE).findall(result)
	if len(obj) != 0:
		for i in obj:
			if i != 'notice core:info':
				error_list.append('[WARNING] LogLevel directive value')
				check_num += 1
				break
	else:
		error_list.append('[WARNING] LogLevel directive is not exist')
		check_num += 1
	obj1 = re.compile(r'^\s*ErrorLog (.+)',re.MULTILINE).findall(result)
	if len(obj1) != 0:
		for i in obj1:
			if i != '${APACHE_LOG_DIR}/error.log':
				error_list.append('[WARNING] ErrorLog directive in apache2 configuration')
				check_num += 1
				break
	else:
		error_list.append('[WARNING] ErrorLog directive is not exist')
		check_num += 1
	result = helper.read_file(helper.envvars)
	obj2 = re.compile(r'^\s*export APACHE_LOG_DIR=(.+)',re.MULTILINE).findall(result)
	if len(obj2) != 0:
		for i in obj2:
			if i != '/var/log/apache2$SUFFIX':
				error_list.append('[WARNING] APACHE_LOG_DIR configure')
				check_num += 1
				break
	else:
		error_list.append('[WARNING] APACHE_LOG_DIR is not exist in envvars')
		check_num += 1
	result = helper.read_file(helper.sites_config)
	obj3 = re.compile(r'^\s*ErrorLog (.+)',re.MULTILINE).findall(result)
	if len(obj3) != 0:
		for i in obj3:
			if i != '${APACHE_LOG_DIR}/error.log':
				error_list.append('[WARNING] ErrorLog configure in virtual host')
				check_num += 1
				break
	else:
		error_list.append('[WARNING] ErrorLog directive is not exist in VirtualHost')
		check_num += 1
	if check_num > 0:
		error_list.insert(0, 31)
	else:
		error_list.insert(0, 0)
	return error_list

def add_LogLevel_config(path):
	result = helper.read_file(path)
	result = re.sub(r'^\s*LogLevel (.+)','',result,flags=re.MULTILINE)
	replace = result + 'LogLevel notice core:info\n'
	helper.write_file(path, replace)

def add_ErrorLog_config(path):
	if path == helper.config_path:
		result = helper.read_file(path)
		result = re.sub(r'^\s*ErrorLog (.+)','',result,flags=re.MULTILINE)
		replace = result + 'ErrorLog ${APACHE_LOG_DIR}/error.log\n'
		helper.write_file(path, replace)
	else:
		result = helper.read_file(path)
		result = re.sub(r'^\s*ErrorLog (.+)','',result,flags=re.MULTILINE)
		result = re.sub(r'^\s*<\/VirtualHost>','',result,flags=re.MULTILINE)
		replace = result + '\tErrorLog ${APACHE_LOG_DIR}/error.log\n</VirtualHost>\n'
		helper.write_file(path, replace)

def set_LogLevel_config(path):
	result = helper.read_file(path)
	result = re.sub(r'^\s*LogLevel (.+)','LogLevel notice core:info\n',result,flags=re.MULTILINE)
	helper.write_file(path, result)

def set_ErrorLog_config(path):
	result = helper.read_file(path)
	result = re.sub(r'^\s*ErrorLog (.+)','ErrorLog ${APACHE_LOG_DIR}/error.log\n',result,flags=re.MULTILINE)
	helper.write_file(path, result)

def add_logdir_config():
	result = helper.read_file(helper.envvars)
	result = re.sub(r'^\s*export APACHE_LOG_DIR=(.+)','',result,flags=re.MULTILINE)
	replace = result + 'export APACHE_LOG_DIR=/var/log/apache2$SUFFIX'
	helper.write_file(helper.envvars, replace)

def set_logdir_config():
	result = helper.read_file(helper.envvars)
	result = re.sub(r'^\s*export APACHE_LOG_DIR=(.+)','export APACHE_LOG_DIR=/var/log/apache2$SUFFIX',result,flags=re.MULTILINE)
	helper.write_file(helper.envvars, result)

def fix(path):
	result = helper.read_file(path)
	obj = re.compile(r'^\s*LogLevel (.+)',re.MULTILINE).findall(result)
	if len(obj) > 1 or len(obj) == 0:
		add_LogLevel_config()
	else:
		if obj[0] != 'notice core:info':
			set_LogLevel_config(path)

	obj1 = re.compile(r'^\s*ErrorLog (.+)',re.MULTILINE).findall(result)
	if len(obj1) > 1 or len(obj1) == 0:
		add_ErrorLog_config(path)
	else:
		if obj1[0] != '${APACHE_LOG_DIR}/error.log':
			set_ErrorLog_config(path)
	result = helper.read_file(helper.envvars)
	obj2 = re.compile(r'^\s*export APACHE_LOG_DIR=(.+)',re.MULTILINE).findall(result)
	if len(obj2) > 1 or len(obj2) == 0:
		add_logdir_config()
	else:
		if obj2[0] != '/var/log/apache2$SUFFIX':
			add_logdir_config()
	result = helper.read_file(helper.sites_config)
	obj3 = re.compile(r'^\s*ErrorLog (.+)',re.MULTILINE).findall(result)
	if len(obj3) > 1 or len(obj3) == 0:
		add_ErrorLog_config(helper.sites_config)
	else:
		if obj3[0] != '${APACHE_LOG_DIR}/error.log':
			set_ErrorLog_config(helper.sites_config)


def fix_o():
	fix(helper.config_path)