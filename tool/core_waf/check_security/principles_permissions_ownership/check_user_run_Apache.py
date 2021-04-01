import os
import re

check_num = 0
error_list = list()

def check_user_and_group_directive(path):
	global check_num
	fu = os.popen("grep -i '^User' " + path)
	fg = os.popen("grep -i '^Group' " + path)
	user = fu.read()
	group = fg.read()
	if len(user) == 0 or user[0] == "#":
		error_list.append("[WARNING] User directives not in Apache configuration")
		check_num += 1
	if len(group) == 0 or group[0] == "#":
		error_list.append("[WARNING] Group directives not in Apache configuration")
		check_num += 1

def check_UID():
	global check_num
	fuid_min = os.popen("grep '^UID_MIN' /etc/login.defs")
	fuid = os.popen("id www-data")
	
	matchObj_uidmin = re.match(r'UID_MIN\s*(\d*)',fuid_min.read())
	matchObj_uid = re.match(r'uid=(\d*).* gid=(\d*).* groups=(\d*).*',fuid.read())

	UID_MIN = matchObj_uidmin.group(1)
	uid = matchObj_uid.group(1)
	gid = matchObj_uid.group(2)
	groups = matchObj_uid.group(3)
	if int (uid) > int (UID_MIN):
		error_list.append("[WARNING] UID Apache is incorrect")
		check_num += 1

def check_username():
	global check_num
	fuser_name = os.popen("ps -uax | grep apache2 | grep -v '^root'")
	if fuser_name.read().split()[0] != "www-data":
		error_list.append("[WARNING] User Apache is incorrect")
		check_num += 1

def check(path):
	# print ''
	# print ' Run the Apache Web Server as a non-root user '.center(85, '#')
	# print ''
	global check_num
	check_user_and_group_directive(path)
	check_UID()
	check_username()
	if check_num > 0:
		error_list.insert(0, 1)
	else:
		error_list.insert(0, 0)
	return error_list


def add_user_and_group():
	os.system("groupadd -r www-data > /dev/null 2> /dev/null")
	os.system("useradd www-data -r -g www-data -d /var/www -s /sbin/nologin > /dev/null 2> /dev/null")

def cf_apache_user_and_group(path):
	f = open(path,'a+')
	f.write("User www-data\nGroup www-data")
	f.close()
	#os.system('service apache2 restart > /dev/null 2> /dev/null')

def fix(path):
	add_user_and_group()
	fu = os.popen("grep -i '^User' " + path)
	fg = os.popen("grep -i '^Group' " + path)
	user = fu.read()
	group = fg.read()
	if len(user) == 0 or user[0] == "#" or len(group) == 0 or group[0] == "#":
		cf_apache_user_and_group(path)

def fix_o():
	fix(helper.config_path)

# print check('/etc/apache2/apache211.conf')
