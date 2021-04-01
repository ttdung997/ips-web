import re
import os

config_path = '/etc/apache2/apache211.conf'
envvars = '/etc/apache2/envvars'
sites_config = '/etc/apache2/sites-available/000-default.conf'
ssl_config = '/etc/apache2/sites-available/default-ssl.conf'
core_path = '/var/log/core_waf/check_security/'

def read_file(file):
	f = open(file,'r')
	result = f.read()
	f.close()
	return result
def write_file(file,content):
	f = open(file,'w')
	f.write(content)
	f.close()

def get_DocumentRoot():
	f = os.popen("apache2ctl -t -D DUMP_RUN_CFG 2> /dev/null | grep 'Main DocumentRoot'")
	DocumentRoot = f.read()
	f.close()
	obj = re.match(r'Main DocumentRoot: "(.*)"', DocumentRoot)
	DocumentRoot = obj.group(1)
	return DocumentRoot

def get_apache_dir():
	apache_dir = list()
	with os.popen("find / -type d -name apache2 2> /dev/null") as f:
		for line in f:
			result = line
			result2 = result.split('/')
			if result2[-1][:-1] == 'apache2':
				apache_dir.append(result[:-1]) 
	return apache_dir

def get_file_config():
	path = list()
	with os.popen("find /etc/apache2/ -path /etc/apache2/mods-available -prune -o -type f -name *.conf -print") as f:
		for line in f:
			path.append(line)
		return path

# print read_file('/etc/apache2/apache123.conf')
