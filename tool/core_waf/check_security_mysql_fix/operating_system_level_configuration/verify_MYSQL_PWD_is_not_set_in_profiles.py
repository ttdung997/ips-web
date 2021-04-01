import os
import re
import sys

sys.path.insert(0, '/var/log/core_waf/check_security/')
import helper

check_num = 0
error_list = list()


def check(username,password):
    flag = True
    for file in ['bashrc', 'profile', 'bash_profile']:
        output = os.popen('grep -s MYSQL_PWD /home/*/.' + file).read()
        if output:
            error_list.append('[WARNING] MYSQL_PWD is set in ' + file)
            error_list.insert(0, 11600)
            flag = False
            break
    if flag:
        error_list.insert(0,0)
    return error_list

def fix(username, password):
    pass

def fix_o():
    fix(helper.config_path)
