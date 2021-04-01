import os
import re
import sys
sys.path.insert(0, '/var/log/core_waf/check_security/')
import helper
check_num = 0
error_list = list()

def check():
	# print ''
	# print ' Deny IP Address Based Requests '.center(85, '#')
	# print ''
	global check_num
	f = os.popen('apache2ctl -M 2> /dev/null | grep rewrite')
	result = f.read()[:-1]
	f.close()
	if len(result) == 0:
		error_list.append('[WARNING] Rewrite module is disable')
		check_num += 1
	else:
		result = helper.read_file(helper.config_path)
		rewrite_e = re.compile(r'^\s*RewriteEngine (.*?)\n',re.MULTILINE).findall(result)
		if len(rewrite_e) == 0 or (rewrite_e[0] != 'On' and rewrite_e[0] != 'on'):
			error_list.append('[WARNING] RewriteEngine is not enable')
			check_num += 1
		if len(re.compile(r'RewriteCond %\{HTTP_HOST\} !\^www\\\.example\\\.com \[NC\]\nRewriteCond %\{REQUEST_URI\} !\^\/error \[NC\]\nRewriteRule \^\.\(\.\*\) - \[L,F\]\n',re.DOTALL).findall(result)) == 0:
			error_list.append('[WARNING] Not configure rewrite to disallows request that disallows IP based requests by requiring a HTTP HOST header')
			check_num += 1
	if check_num > 0:
		error_list.insert(0, 28)
	else:
		error_list.insert(0, 0)
	return error_list


def fix():
	f = os.popen('apache2ctl -M 2> /dev/null| grep rewrite')
	result = f.read()[:-1]
	f.close()
	if len(result) == 0:
		os.system('a2enmod rewrite')
		#os.system('service apache2 restart')
	result = helper.read_file(helper.config_path)
	rewrite_e = re.compile(r'^\s*RewriteEngine (.*?)\n',re.MULTILINE).findall(result)
	if len(rewrite_e) == 0:
		replace = result + 'RewriteEngine On\n'
		helper.write_file(helper.config_path, replace)
	if len(rewrite_e) != 0:
		if rewrite_e[0] != 'On' and rewrite_e[0] != 'on':
			replace = re.sub(r'^\s*RewriteEngine (?:.*?)\n','RewriteEngine On\n',result,flags=re.MULTILINE)
			helper.write_file(helper.config_path, replace)
	result = helper.read_file(helper.config_path)
	if len(re.compile(r'RewriteCond %\{HTTP_HOST\} !\^www\\\.example\\\.com \[NC\]\nRewriteCond %\{REQUEST_URI\} !\^\/error \[NC\]\nRewriteRule \^\.\(\.\*\) - \[L,F\]\n',re.DOTALL).findall(result)) == 0:
		replace = result + 'RewriteCond %{HTTP_HOST} !^www\.example\.com [NC]\nRewriteCond %{REQUEST_URI} !^/error [NC]\nRewriteRule ^.(.*) - [L,F]\n'
		helper.write_file(helper.config_path, replace)

def fix_o():
	fix()

# check()
# configure_rewrite_mod()
# fix()
