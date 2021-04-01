import os
import re
import fileinput
import sys
sys.path.insert(0, '/var/log/core_waf/check_security/')
import helper
error_list = list()
check_num = 0

def check_mechanism():
	result_check = list()
	f = os.popen("apache2ctl -t -D DUMP_RUN_CFG 2> /dev/null | grep 'Mutex default'")
	result = f.read()
	f.close()
	obj = re.match( r'Mutex default: dir="(.*)" mechanism=(.*)',result)
	lock_dir = obj.group(1)
	mechanism = obj.group(2)[:-1]
	result_check.append(lock_dir)
	result_check.append(mechanism)
	return result_check

def check():
	# print ''
	# print ' Secure the Lock File '.center(85, '#')
	# print ''
	global check_num
	verify = check_mechanism()[0].find(helper.get_DocumentRoot())
	if verify != -1:
		error_list.append('[WARNING] Lock file directory in the Apache DocumentRoot')
		check_num += 1 
	
	f = os.popen("ls -ld " + check_mechanism()[0])
	result = f.read().split()
	f.close()
	if result[2] != 'root':
		error_list.append('[WARNING] Ownership of lock file directory is not root')
		check_num += 1 
	if result[3] != 'root':
		error_list.append('[WARNING] Group of lock file directory is not root')
		check_num += 1 
	if result[0][8] == 'w':
		error_list.append('[WARNING] Lock file directory can write by other user')
		check_num += 1 

	f = os.popen("df -T " + check_mechanism()[0] + " | tail -n +2 | awk '{print $2}'")
	result = f.read()[:-1]
	if result == 'nfs':
		error_list.append('[WARNING] Lock file directory is NFS mounted file system')
		check_num += 1 

	if check_num > 0:
		error_list.insert(0, 8)
	else:
		error_list.insert(0, 0)
	return error_list


def fix_permission():
	os.system("chown -R root " + check_mechanism()[0])
	os.system("chgrp -R root " + check_mechanism()[0])
	os.system("chmod -R o-w "+ check_mechanism()[0])

def fix_dir():
	keyword1 = "APACHE_LOCK_DIR"
	replacement1 = "export APACHE_LOCK_DIR=/var/lock/apache2$SUFFIX\n"
	keyword2 = "Mutex file:"
	replacement2 = "Mutex file:${APACHE_LOCK_DIR} default\n"
	for line in fileinput.input('/etc/apache2/envvars', inplace=True):
	    line = line.rstrip()
	    if keyword1 in line:
	        line = line.replace(line, replacement1)
	    # print line
	for line in fileinput.input('/etc/apache2/apache2.conf', inplace=True):
	    line = line.rstrip()
	    if keyword2 in line:
	        line = line.replace(line, replacement2)
	    # print line

def fix():
	verify = check_mechanism()[0].find(helper.get_DocumentRoot())
	if verify != -1:
		fix_dir()
	
	f = os.popen("ls -ld " + check_mechanism()[0])
	result = f.read().split()
	f.close()
	if result[2] != 'root' or result[3] != 'root' or result[0][8] == 'w':
		fix_permission()

def fix_o():
	fix()
