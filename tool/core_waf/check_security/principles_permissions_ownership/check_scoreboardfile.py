import os
import fileinput
import sys
sys.path.insert(0, '/var/log/core_waf/check_security/')
import helper
error_list = list()
check_num = 0

def get_scoreboardFile(path):
	global check_num
	f = os.popen('cat ' + path + ' | grep ScoreBoardFile')
	result = f.read()
	f.close()
	if len(result) == 0:
		# print '[OK] ScoreBoardFile is not configure'
		return 0
	else:
		error_list.append('[WARNING] ScoreBoardFile is configure')
		check_num += 1
		return result.split()[1]

def check_nfs(path):
	global check_num
	f = os.popen("df -T " + get_scoreboardFile(path) + " | tail -n +2 | awk '{print $2}'")
	result = f.read()[:-1]
	if result == 'nfs':
		error_list.append('[WARNING] ScoreBoardFile directory is NFS mounted file system')
		check_num += 1
def check(path):
	# print ''
	# print ' Secure the ScoreBoard File '.center(85, '#')
	# print ''
	global check_num
	if get_scoreboardFile(path) != 0:
		check_nfs(path)
	if check_num > 0:
		error_list.insert(0, 10)
	else:
		error_list.insert(0, 0)
	return error_list

def fix_perm_scoreboardFile():
	os.system('chown -R root ' + get_scoreboardFile())
	os.system('chgrp -R www-data ' + get_scoreboardFile())
	os.system('chmod o-rwx ' + get_scoreboardFile())
	#os.system('service apache2 restart')

def remove_scoreboardFile(path):
	keyword1 = "ScoreBoardFile"
	replacement1 = ""
	for line in fileinput.input(path, inplace=True):
	    line = line.rstrip()
	    if keyword1 in line:
	        line = line.replace(line, replacement1)
	    print line

def fix(path):
	f = os.popen('cat ' + path + ' | grep ScoreBoardFile')
	result = f.read()
	f.close()
	if len(result) != 0:
		remove_scoreboardFile(path)

def fix_o():
	fix(helper.config_path)
