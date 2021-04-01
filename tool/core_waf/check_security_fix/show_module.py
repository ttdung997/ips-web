import os
def show_current_module():
	print '---auth* modules----'
	os.system("apache2ctl -M 2> /dev/null > /dev/null | egrep 'auth._'")
	print '---LDAP modules-----'
	f = os.popen("apache2ctl -M 2> /dev/null > /dev/null | egrep 'ldap'")
	result = f.read()
	if len(result) == 0:
		print '[WARNING] LDAP modules disable'
	else:
		print result

def check():
	f = os.popen("apache2ctl -M 2> /dev/null | egrep 'log_config'")
	result = f.read()
	if len(result) == 0:
		print '[WARNING] log_config_module disable'
	else:
		print '[OK] log_config_module enable'


def check_module(module_name):
	f = os.popen("apache2ctl -M 2> /dev/null > /dev/null | egrep '"+ module_name +"'")
	result = f.read()
	if len(result) == 0:
		print '[OK] '+module_name+'_module disable'
	else:
		print '[WARNING] Module: '+ result[:-1] +' enable'

def disable_module(module_name):
	f = open('/etc/apache2/mods-available/'+module_name+'.load','r')
	result = f.read()
	f.close()
	f = open('/etc/apache2/mods-available/'+module_name+'.load','w')
	result = '#'+result
	f.write(result)
	f.close()
	os.system('service apache2 restart 2> /dev/null > /dev/null')


# check_module('log_config')
# check_module('info')
# show_current_module()
# disable_module('autoindex')
