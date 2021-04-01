import os
import re
import sys
sys.path.insert(0, '/var/log/core_waf/check_security/')
import helper
check_num = 0
error_list = list()

def check(path):
	# print ''
	# print ' Remove Default HTML Content '.center(85, '#')
	# print ''
	global check_num
	result = helper.read_file(path)
	f = os.popen('find '+helper.get_DocumentRoot()+'/index.html 2> /dev/null')
	default_index = f.read()[:-1]
	if len(default_index) != 0:
		error_list.append('[WARNING] Detect default index.html in DocumentRoot')
		check_num += 1
	# print '[NOTICE] Ensure the Apache User Manual content is not installed by checking the configuration file for manual location directive'
	obj = re.compile(r'[^#]<Location \/server-status>(.*?)<\/Location>',re.DOTALL).findall(result)
	if len(obj) != 0:
		error_list.append('[WARNING] Detect server-status handler configuration')
		check_num += 1
	obj1 = re.compile(r'[^#]<Location \/server-info>(.*?)<\/Location>',re.DOTALL).findall(result)
	if len(obj1) != 0:
		error_list.append('[WARNING] Detect server-info handler configuration')
		check_num += 1
	obj2 = re.compile(r'[^#]<Location \/perl-status>(.*?)<\/Location>',re.DOTALL).findall(result)
	if len(obj2) != 0:
		error_list.append('[WARNING] Detect perl-status handler configuration')
		check_num += 1

	if check_num > 0:
		error_list.insert(0, 20)
	else:
		error_list.insert(0, 0)
	return error_list

def remove_default_index():
	os.system('rm '+helper.get_DocumentRoot()+'/index.html')

def remove_handler_config(path,string):
	result = helper.read_file(path)
	li = list()
	obj = re.compile(r'<Location \/'+string+r'>(?:.*?)<\/Location>',re.DOTALL).findall(result)
	li = obj[0].split('\n')
	# print li
	for i in range (len(li)):
		li[i] = li[i].replace(li[i],'#'+li[i]) 
	a = '\n'.join(x for x in li)
	# print a
	replace = re.sub(r'<Location \/'+string+r'>(?:.*?)<\/Location>',a,result,flags=re.DOTALL)
	helper.write_file(path, replace)

def fix(path):
	result = helper.read_file(path)
	f = os.popen('find '+helper.get_DocumentRoot()+'/index.html 2> /dev/null')
	default_index = f.read()[:-1]
	if len(default_index) != 0:
		remove_default_index()
	obj = re.compile(r'[^#]<Location \/server-status>(.*?)<\/Location>',re.DOTALL).findall(result)
	if len(obj) != 0:
		remove_handler_config(path, 'server-status')
	obj1 = re.compile(r'[^#]<Location \/server-info>(.*?)<\/Location>',re.DOTALL).findall(result)
	if len(obj1) != 0:
		remove_handler_config(path, 'server-info')
	obj2 = re.compile(r'[^#]<Location \/perl-status>(.*?)<\/Location>',re.DOTALL).findall(result)
	if len(obj2) != 0:
		remove_handler_config(path, 'perl-status')

def fix_o():
	fix(helper.config_path)

