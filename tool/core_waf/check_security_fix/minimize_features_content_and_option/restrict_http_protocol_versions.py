import os
import re
import sys
sys.path.insert(0, '/var/log/core_waf/check_security/')
import helper
check_num = 0
error_list = list()

def check(path):
	# print ''
	# print ' Restrict HTTP Protocol Versions '.center(85, '#')
	# print ''
	global check_num
	f = os.popen('apache2ctl -M 2> /dev/null | grep rewrite')
	result = f.read()[:-1]
	f.close()
	if len(result) == 0:
		error_list.append('[WARNING] Rewrite module is disable')
	else:
		result = helper.read_file(path)
		rewrite_e = re.compile(r'^\s*RewriteEngine (.*?)\n',re.MULTILINE).findall(result)
		if len(rewrite_e) == 0 or (rewrite_e[0] != 'On' and rewrite_e[0] != 'on'):
			error_list.append('[WARNING] RewriteEngine is not enable')
			check_num += 1
		if len(re.compile(r'RewriteCond %\{THE_REQUEST\} !HTTP\/1\\\.1\$\nRewriteRule \.\* - \[F\]\nRewriteOptions Inherit\n',re.DOTALL).findall(result)) == 0:
			error_list.append('[WARNING] Misconfigure Rewrite to disallows request that do not include the HTTP /1.1 header')
			check_num += 1
	if check_num > 0:
		error_list.insert(0, 25)
	else:
		error_list.insert(0, 0)
	return error_list

def fix(path):
	f = os.popen('apache2ctl -M 2> /dev/null | grep rewrite')
	result = f.read()[:-1]
	f.close()
	if len(result) == 0:
		os.system('a2enmod rewrite > /dev/null')
		#os.system('service apache2 restart > /dev/null')
	result = helper.read_file(path)
	rewrite_e = re.compile(r'^\s*RewriteEngine (.*?)\n',re.MULTILINE).findall(result)
	if len(rewrite_e) == 0:
		replace = result + '\nRewriteEngine On\n'
		helper.write_file(path, replace)
	if len(rewrite_e) != 0:
		if rewrite_e[0] != 'On' and rewrite_e[0] != 'on':
			replace = re.sub(r'^\s*RewriteEngine (?:.*?)\n','RewriteEngine On\n',result,flags=re.MULTILINE)
			helper.write_file(path, replace)
	result = helper.read_file(path)
	if len(re.compile(r'RewriteCond %\{THE_REQUEST\} !HTTP\/1\\\.1\$\nRewriteRule \.\* - \[F\]\nRewriteOptions Inherit\n',re.DOTALL).findall(result)) == 0:
		replace = result + 'RewriteCond %{THE_REQUEST} !HTTP/1\.1$\nRewriteRule .* - [F]\nRewriteOptions Inherit\n'
		helper.write_file(path, replace)

def fix_o():
	fix(helper.config_path)
# check(helper.config_path)
# fix(helper.config_path)
