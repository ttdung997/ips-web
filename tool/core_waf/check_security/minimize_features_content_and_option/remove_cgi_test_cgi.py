import os
import re
import sys
sys.path.insert(0, '/var/log/core_waf/check_security/')
import helper
error_list = list()

def check():
	# print ''
	# print ' Remove Default CGI Content test-cgi '.center(85, '#')
	# print ''
	result = helper.read_file('/etc/apache2/conf-available/serve-cgi-bin.conf')
	obj = re.compile(r'^\s*(?:ScriptAlias|ScriptAliasMatch|ScriptInterpreterSource) \/cgi-bin\/ (.*?)\n', re.MULTILINE).findall(result)
	if obj[0] != 0:
		f = os.popen('find '+obj[0]+' -name test-cgi')
		find_result = f.read()
		f.close()
		if len(find_result) != 0:
			error_list.append('[WARNING] Detect the test-cgi default CGI in cgi-bin directory')
			error_list.insert(0, 22)
		else:
			error_list.insert(0, 0)
	return error_list


def get_cgi_bin_dir():
	result = helper.read_file('/etc/apache2/conf-available/serve-cgi-bin.conf')
	obj = re.compile(r'^\s*(?:ScriptAlias|ScriptAliasMatch|ScriptInterpreterSource) \/cgi-bin\/ (.*?)\n', re.MULTILINE).findall(result)
	f = os.popen('find '+obj[0]+' -name test-cgi')
	find_result = f.read()
	f.close()
	return find_result



def fix():
	result = helper.read_file('/etc/apache2/conf-available/serve-cgi-bin.conf')
	obj = re.compile(r'^\s*(?:ScriptAlias|ScriptAliasMatch|ScriptInterpreterSource) \/cgi-bin\/ (.*?)\n', re.MULTILINE).findall(result)
	if obj[0] != 0:
		f = os.popen('find '+obj[0]+' -name test-cgi')
		find_result = f.read()
		f.close()
		if len(find_result) != 0:
			os.system('rm -r '+get_cgi_bin_dir()[:-1])

def fix_o():
	fix()
# print get_cgi_bin_dir()
# remove_cgi_test_cgi()