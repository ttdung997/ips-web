import os
error_list = list()

def check():
	# print ''
	# print ' Lock the Apache User Account '.center(85, '#')
	# print ''
	f = os.popen('passwd -S www-data')
	result = f.read().split()
	if result[1] != 'L':
		error_list.append('[WARNING] Apache user account is not locked')
		error_list.insert(0, 3)
	else:
		error_list.insert(0, 0)
	return error_list

def fix():
	f = os.popen('passwd -S www-data')
	result = f.read().split()
	if result[1] != 'L':
		os.system('passwd -l www-data > /dev/null')
	

def unlock():
	os.system('passwd -u www-data')	


def fix_o():
	fix()