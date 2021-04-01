import os

error_list = list()

def check():
	# print ''
	# print ' Give the Apache User Account an Invalid Shell '.center(85, '#')
	# print ''
	with os.popen('grep www-data /etc/passwd') as f:
		for line in f:
			result = line.split(':')
			if result[0] == 'www-data':
				if result[6][:-1] != '/usr/sbin/nologin':
					error_list.append("[WARNING] Login shell is not nologin or invalid shell")
					error_list.insert(0, 2)
				else:
					error_list.insert(0, 0)
			else:
				error_list.insert(0, 0)
	return error_list


def fix():
	os.system('chsh -s /usr/sbin/nologin www-data')

def fix_o():
	fix()