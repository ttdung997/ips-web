import os
import re
import sys

sys.path.insert(0, '/var/log/core_waf/check_security_mysql/')
import helper

error_list = list()

# def check(username, password):
def check(username, password):
    flag = True
    output = os.popen('grep -e "^mysql -u" /home/*/.bash_history').read()
    if output:
        match = re.findall(r'^mysql -u ?(.+) ?-p ?(.+)$',output,re.MULTILINE)
        if match:
            flag = False
            error_list.append(('[WARNING] Database password might be visible in the command line history'))
            error_list.insert(0, 12300)
    if flag:
        error_list.insert(0, 0)
    return error_list


def fix(username, password):
    pass
