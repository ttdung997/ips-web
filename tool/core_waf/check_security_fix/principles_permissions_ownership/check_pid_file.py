import os
import re
import fileinput
import sys
sys.path.insert(0, '/var/log/core_waf/check_security/')
import helper

error_list = list()
check_num = 0

def get_dir_pidfile():
	global check_num
	f = os.popen("apache2ctl -t -D DUMP_RUN_CFG 2> /dev/null | grep 'PidFile'")
	result = f.read()
	f.close()
	obj = re.match( r'PidFile: "(.*)"',result)
	pidfile_dir = obj.group(1)
	file_name = pidfile_dir.split('/')[-1]
	pidfile_dir = pidfile_dir[:pidfile_dir.rfind('/' + file_name)]
	return pidfile_dir

def check():
	# print ''
	# print ' Secure the Pid File '.center(85, '#')
	# print ''
	global check_num
	verify = get_dir_pidfile().find(helper.get_DocumentRoot())
	if verify != -1:
		error_list.append('[WARNING] Pid file directory in the Apache DocumentRoot')
		check_num += 1 

	f = os.popen("ls -ld " + get_dir_pidfile())
	result = f.read().split()
	f.close()
	if result[2] != 'root':
		error_list.append('[WARNING] Ownership of pid file directory is not root')
		check_num += 1 
	if result[3] != 'root':
		error_list.append('[WARNING] Group of pid file directory is not root')
		check_num += 1 
	if result[0][8] == 'w':
		error_list.append('[WARNING] Pid file directory can write by other user')
		check_num += 1 

	if check_num > 0:
		error_list.insert(0, 9)
	else:
		error_list.insert(0, 0)
	return error_list

	

def fix_permission():
	os.system("chown -R root " + get_dir_pidfile())
	os.system("chgrp -R root " + get_dir_pidfile())
	os.system("chmod -R o-w "+ get_dir_pidfile())


def fix_dir():
	keyword1 = "APACHE_PID_FILE"
	replacement1 = "export APACHE_PID_FILE=/var/run/apache2/apache2$SUFFIX.pid\n"
	keyword2 = "PidFile:"
	replacement2 = "PidFile ${APACHE_PID_FILE}\n"
	for line in fileinput.input('/etc/apache2/envvars', inplace=True):
	    line = line.rstrip()
	    if keyword1 in line:
	        line = line.replace(line, replacement1)
	    print line
	for line in fileinput.input('/etc/apache2/apache2.conf', inplace=True):
	    line = line.rstrip()
	    if keyword2 in line:
	        line = line.replace(line, replacement2)
	    print line

def fix():
	verify = get_dir_pidfile().find(helper.get_DocumentRoot())
	if verify != -1:
		fix_dir()

	f = os.popen("ls -ld " + get_dir_pidfile())
	result = f.read().split()
	f.close()
	if result[2] != 'root' or result[3] != 'root' or result[0][8] == 'w':
		fix_permission()

def fix_o():
	fix()