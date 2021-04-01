import os
import re
import sys
sys.path.insert(0, '/home/anhthc/do_an/')
import helper


def check():
	print ''
	print ' Enable the AppArmor Framework '.center(85, '#')
	print ''
	f = os.popen("aa-status --enabled && echo Enabled")
	result = f.read()
	f.close()
	if 'command not found' in result:
		print '[WARNING] AppArmor package is not installed'
	if len(result) == 0:
		print '[WARNING] AppArmor is not Enabled'

def install_apparmor():
	os.system('apt-get install apparmor > /home/anhthc/do_an/log_apparmor1 2> /home/anhthc/do_an/log_apparmor2')
	result = helper.read_file('/home/anhthc/do_an/log_apparmor2')
	if len(result) == 0:
		print 'Install AppArmor done!'
	os.system('apt-get install libapache2-mod-apparmor > /home/anhthc/do_an/log_apparmor3 2> /home/anhthc/do_an/log_apparmor4')
	result = helper.read_file('/home/anhthc/do_an/log_apparmor4')
	if len(result) == 0:
		print 'Install libapache2-mod-apparmor done!'
	os.system('/etc/init.d/apparmor start > /dev/null')
