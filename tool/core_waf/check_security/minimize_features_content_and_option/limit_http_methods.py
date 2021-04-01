import os
import re
import sys
sys.path.insert(0, '/var/log/core_waf/check_security/')
import helper
check_num = 0
error_list = list()

def check(path):
	# print ''
	# print ' Limit HTTP Request Methods '.center(85, '#')
	# print ''
	global check_num
	result = helper.read_file(path)
	obj = re.compile(r'<Directory \/\w(?:.*?)>(?:.*?[^#])<\/Directory>', re.DOTALL).findall(result)
	for i in obj:
		method = re.compile(r'^\s*<LimitExcept (.*?)>', re.MULTILINE).findall(i)
		if len(method) == 0:
			error_list.append('[WARNING] No LimitExcept on HTTP methods')
			check_num += 1
		else:
			if 'GET' not in method[0] or 'POST' not in method[0] or 'OPTIONS' not in method[0] or len(method[0].split()) > 3:
				error_list.append('[WARNING] Detect <LimitExcept> include HTTP methods outside GET,POST,OPTIONS')
				check_num += 1
	if check_num > 0:
		error_list.insert(0, 23)
	else:
		error_list.insert(0, 0)
	return error_list


def set_limit_except(path):
	list_path = list()
	result = helper.read_file(path)
	obj = re.compile(r'[^#]<Directory \/\w(?:.*?)>(?:.*?)<\/Directory>', re.DOTALL).findall(result)
	for i in obj:
		method = re.compile(r'^\s*<LimitExcept (.*?)>', re.MULTILINE).findall(i)
		if len(method) == 0:
			continue
		obj1 = re.compile(r'<LimitExcept (?:.*?)>(.*?)<\/LimitExcept>', re.DOTALL).findall(i)
		obj2 = re.compile(r'^\s*Require all denied',re.MULTILINE).findall(obj1[0])
		if 'GET' not in method[0] or 'POST' not in method[0] or 'OPTIONS' not in method[0] or len(method[0].split()) > 3 or len(obj2) == 0:
			path_re = re.compile(r'<Directory \/(.*?)>(?:.*?[^#])<\/Directory>', re.DOTALL).findall(i)
			list_path.append(path_re[0])
	for i in list_path:
		result = helper.read_file(path)
		obj = re.compile(r'[^#]<Directory \/' + i + r'>(.*?)<\/Directory>', re.DOTALL).findall(result)
		obj1 = re.compile(r'<LimitExcept (?:.*?)>(.*?)<\/LimitExcept>', re.DOTALL).findall(obj[0])
		obj2 = re.compile(r'^\s*Require all denied',re.MULTILINE).findall(obj1[0])
		if len(obj2) == 0:
			replace2 = obj1[0] + '\tRequire all denied\n\t'
			replace3 = re.sub(r'<LimitExcept (?:.*?)>(.*?)<\/LimitExcept>', '<LimitExcept GET POST OPTIONS>' + replace2 + '</LimitExcept>', obj[0], flags=re.DOTALL)
			replace1 = re.sub(r'[^#]<Directory \/' + i + r'>(?:.*?)<\/Directory>','\n<Directory /' + i +'>'+ replace3 +'</Directory>',result,flags=re.DOTALL)
			helper.write_file(path, replace1)
		else:
			replace = re.sub(r'<LimitExcept (?:.*?)>','<LimitExcept GET POST OPTIONS>', obj[0])
			replace1 = re.sub(r'[^#]<Directory \/' + i + r'>(?:.*?)<\/Directory>','\n<Directory /' + i +'>'+ replace +'</Directory>',result,flags=re.DOTALL)
			helper.write_file(path, replace1)


def add_limit_except(path):
	list_path = list()
	result = helper.read_file(path)
	obj = re.compile(r'[^#]<Directory \/\w(?:.*?)>(?:.*?)<\/Directory>', re.DOTALL).findall(result)
	for i in obj:
		if '<LimitExcept ' not in i or len(re.compile(r'^\s*<LimitExcept (.*?)>', re.MULTILINE).findall(i)) == 0:
			path_re = re.compile(r'[^#]<Directory \/(.*?)>(?:.*?)<\/Directory>', re.DOTALL).findall(i)
			list_path.append(path_re[0])
	for i in list_path:
		result = helper.read_file(path)
		obj = re.compile(r'[^#]<Directory \/' + i + r'>(.*?)<\/Directory>', re.DOTALL).findall(result)
		replace = obj[0] + '\t<LimitExcept GET POST OPTIONS>\n\t\tRequire all denied\n\t</LimitExcept>\n'
		replace1 = replace1 = re.sub(r'<Directory \/' + i + r'>(?:.*?[^#])<\/Directory>','\n<Directory /' + i +'>'+ replace +'</Directory>',result,flags=re.DOTALL)
		helper.write_file(path, replace1)

def fix(path):
	result = helper.read_file(path)
	obj = re.compile(r'[^#]<Directory \/\w(?:.*?)>(?:.*?)<\/Directory>', re.DOTALL).findall(result)
	for i in obj:
		method = re.compile(r'^\s*<LimitExcept (.*?)>', re.MULTILINE).findall(i)
		if len(method) == 0:
			add_limit_except(path)
		else:
			if 'GET' not in method[0] or 'POST' not in method[0] or 'OPTIONS' not in method[0] or len(method[0].split()) > 3:
				set_limit_except(path)

def fix_o():
	fix(helper.config_path)

# set_limit_except()
# add_limit_except()
# check_limit_except()
# fix(helper.config_path)
# check()
