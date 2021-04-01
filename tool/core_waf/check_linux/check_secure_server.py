from operating_system_level_configuration import *
from installation_and_planning import *
from file_system_permissions import *
from general import *
from mysql_permission import *
from auditing_and_logging import *
from authentication import *
from network import *
from replication import *

from operator import itemgetter
import imp
import os
import helper
import show_module
import json
from sys import *


list_score = list()
mod_apache = ['dav', 'dav_fs', 'status', 'autoindex', 'proxy', 'userdir', 'info']
principles_permissions_ownership1 = ['check_lock_account', 'check_lock_file', 'check_login_shell', 'check_pid_file', 'document_root_group_write_access', 'group_id_apache', 'group_write_access', 'ownership_apache_dir', 'write_access_apache_dir']
principles_permissions_ownership2 = ['check_scoreboardfile', 'check_user_run_Apache', 'core_dump_directory']
minimize_features_content_and_option1 = ['deny_ip_request', 'remove_cgi_printenv', 'remove_cgi_test_cgi', 'restrict_listen_directive']
minimize_features_content_and_option1_fix = ['deny_ip_request', 'remove_cgi_printenv', 'remove_cgi_test_cgi']
minimize_features_content_and_option2 = ['disable_trace_method', 'limit_http_methods', 'minimize_options_alldir', 'remove_default_html', 'restrict_access_ht_file', 'restrict_browser_frame_options', 'restrict_file_extension', 'restrict_http_protocol_versions', 'restrict_option_rootdir', 'restrict_option_webrootdir']
MODULE_EXTENSIONS = ('.py', '.pyc', '.pyo')

def package_contents(package_name):
    file, pathname, description = imp.find_module(package_name)
    if file:
        raise ImportError('Not a package: %r', package_name)
    # Use a set because some may be both source and compiled.
    a = list(set([os.path.splitext(module)[0]
        for module in os.listdir(pathname)
        if module.endswith(MODULE_EXTENSIONS)]))
    a.remove('__init__')
    return a

def init_config_file():
	vhost_log = helper.read_file('/etc/apache2/conf-available/other-vhosts-access-log.conf')
	security = helper.read_file('/etc/apache2/conf-available/security.conf')
	apache2_conf = helper.read_file('/etc/apache2/apache211.conf')
	apache2_conf_new = apache2_conf + security + vhost_log
	helper.write_file('/etc/apache2/apache211.conf', apache2_conf_new)

#def check(username,password):
def check():
	# for i in mod_apache:
	# 	show_module.check_module(i)
	# show_module.check()
	username = 'root'
	password = 'bkcsstudent'
	for i in package_contents('operating_system_level_configuration'):
		list_score.append(eval(i).check(username, password))
	for i in package_contents('installation_and_planning'):
		list_score.append(eval(i).check(username, password))
	# for i in package_contents('file_system_permissions'):
	# 	list_score.append(eval(i).check(username, password))
	for i in package_contents('general'):
		list_score.append(eval(i).check(username, password))
	for i in package_contents('auditing_and_logging'):
		list_score.append(eval(i).check(username, password))
	for i in package_contents('authentication'):
		list_score.append(eval(i).check(username, password))
	for i in package_contents('network'):
		list_score.append(eval(i).check(username, password))
	for i in package_contents('replication'):
		list_score.append(eval(i).check(username, password))
	##for i in package_contents('apparmor_restrict_apache_proc'):
	##	eval(i).check()

	#for i in package_contents('dos_mitigations'):
	#	list_score.append(eval(i).check(helper.config_path))

	#for i in package_contents('request_limit'):
	#	list_score.append(eval(i).check(helper.config_path))

	#for i in package_contents('information_leakage'):
	#	list_score.append(eval(i).check(helper.config_path))

	#list_score.append(access_log.check(helper.config_path))
	#list_score.append(error_log.check(helper.config_path))
	## apply_applicable_patches.check()
	#list_score.append(mod_security.check())
	#list_score.append(storage_rotation_log.check())

	#ssl_tls = package_contents('ssl_tls')
	#ssl_tls.remove('ssl_mod')
	#for i in ssl_tls:
	#	list_score.append(eval(i).check(helper.ssl_config))
	#list_score.append(ssl_mod.check())


	#for i in principles_permissions_ownership1:
	#	list_score.append(eval(i).check())

	#for i in principles_permissions_ownership2:
	#	list_score.append(eval(i).check(helper.config_path))

	#for i in minimize_features_content_and_option1:
	#	list_score.append(eval(i).check())

	#for i in minimize_features_content_and_option2:
	#	list_score.append(eval(i).check(helper.config_path))
	# print 'Check Done !!!'
	# print sorted(list_score, key=itemgetter(0))
	# print filter(lambda a: a != [0], sorted(list_score, key=itemgetter(0)))
	# print list_score
	print json.dumps(filter(lambda a: a != [0], sorted(list_score, key=itemgetter(0))))

def fix():
	# apache_access_control_fix = package_contents('apache_access_control')
	# apache_access_control_fix.remove('allow_access_web_content')
	# for i in apache_access_control_fix:
	# 	eval(i).fix(helper.config_path)
	#
	# #apparmor_profile.fix()
	#
	# for i in package_contents('dos_mitigations'):
	# 	eval(i).fix(helper.config_path)
	#
	# for i in package_contents('request_limit'):
	# 	eval(i).fix(helper.config_path)
	#
	# for i in package_contents('information_leakage'):
	# 	eval(i).fix(helper.config_path)
	#
	# access_log.fix(helper.config_path)
	# error_log.fix(helper.config_path)
	#
	#
	# ssl_tls_fix = package_contents('ssl_tls')
	# ssl_tls_fix.remove('ssl_mod')
	# for i in ssl_tls_fix:
	# 	eval(i).fix(helper.ssl_config)
	# ssl_mod.fix()
	#
	#
	# for i in principles_permissions_ownership1:
	# 	eval(i).fix()
	#
	# for i in principles_permissions_ownership2:
	# 	eval(i).fix(helper.config_path)
	#
	# for i in minimize_features_content_and_option1_fix:
	# 	eval(i).fix()
	#
	# for i in minimize_features_content_and_option2:
	# 	eval(i).fix(helper.config_path)
	#
	# print 'Fix Done!!!!!'
	username = 'root'
	password = 'bkcsstudent'
	for i in package_contents('operating_system_level_configuration'):
		eval(i).fix(username, password)
	for i in package_contents('installation_and_planning'):
		eval(i).fix(username, password)
	for i in package_contents('file_system_permissions'):
		eval(i).fix(username, password)
	for i in package_contents('general'):
		eval(i).fix(username, password)
	for i in package_contents('auditing_and_logging'):
		eval(i).fix(username, password)
	for i in package_contents('authentication'):
		eval(i).fix(username, password)
	for i in package_contents('network'):
		eval(i).fix(username, password)
	for i in package_contents('replication'):
		eval(i).fix(username, password)

def main():
	# init_config_file()
	if len(argv) == 1:
		print 'Nhap tham so [check] hoac [fix]'
	elif argv[1] == 'fix':
		fix()
	elif argv[1] == 'check':
		check()
	else:
		print 'Nhap lai tham so [check] hoac [fix]'


if __name__ == "__main__":
	main()
