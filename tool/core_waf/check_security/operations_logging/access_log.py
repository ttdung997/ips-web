import os
import re
import sys
sys.path.insert(0, '/var/log/core_waf/check_security/')
import helper
check_num = 0
error_list = list()

def check(path):
	# print ''
	# print ' Configure the Access Log '.center(85, '#')
	# print ''
	global check_num
	ck = 1
	result = helper.read_file(path)
	obj = re.compile(r'LogFormat \"\%h \%l \%u \%t \\\"\%r\\\" \%>s \%b \\\"\%\{Referer\}i\\\" \\\"\%\{User-Agent\}i\\\"\" combined',re.MULTILINE).findall(result)
	if len(obj) == 0:
		error_list.append('[WARNING] LogFormat directive has recommended information is not exist')
		check_num += 1
	obj1 = re.compile(r'CustomLog \$\{APACHE_LOG_DIR\}\/access\.log (.+)',re.MULTILINE).findall(result)
	if len(obj1) == 0 :
		error_list.append('[WARNING] CustomLog directive for access log is not exist')
		check_num += 1
	else:
		for i in obj1:
			if i != 'combined':
				ck = 0
				break
		if ck == 0:
			error_list.append("[WARNING] CustomLog directive don't use combined format")
			check_num += 1
	result = helper.read_file(helper.sites_config)
	obj2 = re.compile(r'CustomLog \$\{APACHE_LOG_DIR\}\/access\.log (.+)',re.MULTILINE).findall(result)
	if len(obj2) == 0:
		error_list.append('[WARNING] CustomLog directive for access log is not exist in VirtualHost')
		check_num += 1
	else:
		for i in obj2:
			if i != 'combined':
				ck = 0
				break
		if ck == 0:
			error_list.append("[WARNING] CustomLog directive don't use combined format in VirtualHost")
			check_num += 1
	if check_num > 0:
		error_list.insert(0, 32)
	else:
		error_list.insert(0, 0)
	return error_list

def add_logformat(path):
	result = helper.read_file(path)
	replace = result + 'LogFormat "%h %l %u %t \\\"%r\\\" %>s %b \\\"%{Referer}i\\\" \\\"%{User-Agent}i\\\"" combined\n'
	helper.write_file(path, replace)

def add_customlog(path):
	result = helper.read_file(path)
	obj1 = re.compile(r'CustomLog \$\{APACHE_LOG_DIR\}\/access\.log (.+)',re.MULTILINE).findall(result)
	if len(obj1) == 0:
		if path == helper.config_path:
			replace = result + 'CustomLog ${APACHE_LOG_DIR}/access.log combined\n'
			helper.write_file(path, replace)
		else:
			result = re.sub(r'^\s*<\/VirtualHost>','',result,flags=re.MULTILINE)
			replace = result + '\tCustomLog ${APACHE_LOG_DIR}/access.log combined\n</VirtualHost>\n'
			helper.write_file(path, replace)
	else:
		replace = re.sub(r'CustomLog \$\{APACHE_LOG_DIR\}\/access\.log .+','CustomLog ${APACHE_LOG_DIR}/access.log combined',result,flags=re.MULTILINE)
		helper.write_file(path, replace)


def fix(path):
	ck = 1
	result = helper.read_file(path)
	obj = re.compile(r'LogFormat \"\%h \%l \%u \%t \\\"\%r\\\" \%>s \%b \\\"\%\{Referer\}i\\\" \\\"\%\{User-Agent\}i\\\"\" combined',re.MULTILINE).findall(result)
	if len(obj) == 0:
		add_logformat(path)
	obj1 = re.compile(r'CustomLog \$\{APACHE_LOG_DIR\}\/access\.log (.+)',re.MULTILINE).findall(result)
	if len(obj1) == 0 :
		add_customlog(path)
	else:
		for i in obj1:
			if i != 'combined':
				ck = 0
				break
		if ck == 0:
			add_customlog(path)
	result = helper.read_file(helper.sites_config)
	obj2 = re.compile(r'CustomLog \$\{APACHE_LOG_DIR\}\/access\.log (.+)',re.MULTILINE).findall(result)
	if len(obj2) == 0:
		add_customlog(helper.sites_config)
	else:
		for i in obj2:
			if i != 'combined':
				ck = 0
				break
		if ck == 0:
			add_customlog(helper.sites_config)

def fix_o():
	fix(helper.config_path)