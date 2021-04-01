import os
import re
import sys
sys.path.insert(0, '/home/anhthc/do_an/')
import helper


def check():
	print ''
	print ' Ensure Apache AppArmor Profile is in Enforce Mode '.center(85, '#')
	print ''
	a = list()
	f = os.popen('aa-unconfined --paranoid | grep apache2')
	result = '1'
	while result != '':
		result = f.readline()
		a.append(result)
	f.close()
	del a[-2]
	for i in a:
		if 'not confined' in i:
			print '[WARNING] AppArmor profiles is not in enforce mode'
			break



def fix():
	os.system('aa-enforce apache2 > /dev/null')
	a = list()
  	result = '1'
  	f = os.popen("ps -aux | grep apache2 | awk '{print $2}'")
	while result != '':
		result = f.readline()
		a.append(result.strip('\n'))
	f.close()
	del a[-1]
	del a[-1]
	del a[-1]
	for i in a:
		os.system('kill -9 '+ i)
	os.system('service apache2 start > /dev/null')


