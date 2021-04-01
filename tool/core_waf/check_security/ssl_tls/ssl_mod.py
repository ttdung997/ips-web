import os
import sys
sys.path.insert(0, '/var/log/core_waf/check_security/')
import helper
error_list = list()

def check():
	# print ''
	# print ' Install mod_ssl and/or mod_nss '.center(85, '#')
	# print ''
	f = os.popen('apache2ctl -M 2> /dev/null | egrep "ssl|nss"')
	result = f.read()
	f.close()
	if len(result) == 0:
		error_list.append('[WARNING] SSL module disable')
		error_list.insert(0, 36)
	else:
		error_list.insert(0, 0)
	return error_list

def fix():
	os.system('a2enmod ssl > /dev/null')
	#os.system('service apache2 restart')

def fix_o():
	fix()

#print check()
