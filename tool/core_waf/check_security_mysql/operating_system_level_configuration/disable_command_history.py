import os
import re
import sys

sys.path.insert(0, '/var/log/core_waf/check_security_mysql/')
import helper

check_num = 0
error_list = list()


def check(username,password):
    flag = True
    output = os.popen('find /home -name ".mysql_history"').read().splitlines()
    for dir in output:
        mysql_history_location = os.popen('ls -l ' + dir).read()
        if not (re.search("\/dev\/null$", mysql_history_location)):
            error_list.append('[WARNING] Command history should be disabled!')
            error_list.insert(0, 11300)
            flag = False
            break
    if flag:
        error_list.insert(0, 0)
    return error_list

def fix(username,password):
    output = os.popen('find /home -name ".mysql_history"').read().splitlines()
    for dir in output:
        mysql_history_location = os.popen('ls -l ' + dir).read()
        if not (re.search(r'\/dev\/null\n$', mysql_history_location)):
            os.system('rm ' + dir)
            # username_search = re.search('/home/(.*)/\.mysql_history',mysql_history_location)
            # if username_search:
            #     username = username_search.group(1)
            os.system('ln -s /dev/null ' + dir)

def fix_o():
    fix(helper.config_path)
