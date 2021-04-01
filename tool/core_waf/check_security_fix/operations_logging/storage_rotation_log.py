import os
import re
import sys
sys.path.insert(0, '/var/log/core_waf/check_security/')
import helper
check_num = 0
error_list = list()
directive = ['missingok', 'notifempty', 'sharedscripts', 'rotate', 'compress']

def check():
	# print ''
	# print ' Log Storage and Rotation '.center(85, '#')
	# print ''
	global check_num
	result = helper.read_file('/etc/logrotate.d/apache2')
	obj = re.compile(r'(daily|weekly|monthly|yearly)',re.MULTILINE).findall(result)
	if len(obj) != 0:
		obj1 = re.compile(r'rotate (\d+)',re.MULTILINE).findall(result)
		if obj[0] == 'weekly':
			if obj1[0] < 13:
				error_list.append('[WARNING] Log rotation is configured at least 13 week')
				check_num += 1
		if obj[0] == 'daily':
			if obj1[0] < 100:
				error_list.append('[WARNING] Log rotation is configured at least 100 day')
				check_num += 1
		if obj[0] == 'monthly':
			if obj1[0] < 3:
				error_list.append('[WARNING] Log rotation is configured at least 3 month')
				check_num += 1
		obj2 = re.findall(r'\/var\/log\/apache2\/\*\.log \{(.+)\}',result,re.DOTALL)
		element = obj2[0].split('\n\t')
		# print 'Check logrotate for apache2'
		a = 0
		for i in directive:
			for j in element:
				if i in j:
					a = 1
					break
			if a == 1:
				a = 0
				continue
			else:
				error_list.append('[WARNING] Miss: ' + i)
				check_num += 1
			a = 0
	else:
		error_list.append('[WARNING] Log rotation config fail')
		check_num += 1
	if check_num > 0:
		error_list.insert(0, 33)
	else:
		error_list.insert(0, 0)
	# print '[NOTICE] For each virtual host configured with its own log files ensure that those log files are also included in a similar log rotation'
	error_list.append('[NOTICE] Chuong trinh ko ho tro fix tu dong')
	return error_list
# check()