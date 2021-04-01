import os
import re
import sys
sys.path.insert(0, '/var/log/core_waf/check_security/')
import helper
check_num = 0
error_list = list()

def check(path):
	# print ''
	# print ' Enable HTTP Strict Transport Security '.center(85, '#')
	# print ''
	global check_num
	result = helper.read_file(path)
	vtconf = re.findall(r'[^#]<VirtualHost (.*?)>(.*?)<\/VirtualHost>',result,re.DOTALL)
	header = re.findall(r'^\s*Header (.+)',result,re.MULTILINE)
	if len(vtconf) != len(header):
		error_list.append('[WARNING] Header directive is not exsit in some VirtualHost')
		check_num += 1
	for i in header:
		if i != 'always set Strict-Transport-Security "max-age=600"':
			error_list.append('[WARNING] Config Header to enable HSTS')
			check_num += 1
			break
	if check_num > 0:
		error_list.insert(0, 43)
	else:
		error_list.insert(0, 0)
	return error_list

def add_directive(ident,path,direct):
	result = helper.read_file(path)
	vtconf = re.findall(r'[^#]<VirtualHost '+ ident +r'>(.*?)<\/VirtualHost>',result,re.DOTALL)
	replace = vtconf[0] + direct
	replace = re.sub(r'[^#]<VirtualHost '+ ident +r'>.*?<\/VirtualHost>','\t<VirtualHost '+ ident +'>' + replace +'\t</VirtualHost>',result,flags=re.DOTALL)
	helper.write_file(path,replace)


def fix_directory(path):
	result = helper.read_file(path)
	replace = re.sub(r'^\s*Header .+','\t\tHeader always set Strict-Transport-Security "max-age=600"',result,flags=re.MULTILINE)
	helper.write_file(path, replace)

def fix(path):
	a = list()
	result = helper.read_file(path)
	vtconf = re.findall(r'[^#]<VirtualHost (.*?)>(.*?)<\/VirtualHost>',result,re.DOTALL)
	for i in vtconf:
		a.append(i[0])
	for i in a:
		vtconf = re.findall(r'[^#]<VirtualHost '+ i +r'>(.*?)<\/VirtualHost>',result,re.DOTALL)
		header = re.findall(r'^\s*Header (.+)',vtconf[0],re.MULTILINE)
		if len(header) == 0:
			add_directive(i,path,'\tHeader always set Strict-Transport-Security "max-age=600"\n')
	result = helper.read_file(path)
	header = re.findall(r'^\s*Header (.+)',result,re.MULTILINE)
	for i in header:
		if i != 'always set Strict-Transport-Security "max-age=600"':
			fix_directory(path)
			break

def fix_o():
	fix(helper.ssl_config)
