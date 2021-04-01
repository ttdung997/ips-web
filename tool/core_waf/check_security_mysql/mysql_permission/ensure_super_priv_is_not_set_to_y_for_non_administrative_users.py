import os
import re
import sys

sys.path.insert(0, '/var/log/core_waf/check_security_mysql/')
import helper

error_list = list()

# def check(username, password):
def check(username, password):
    output = os.popen('grep -e "^mysql -u" /home/*/.bash_history').read()
    match = re.findall(r'^mysql -u ?(.+) ?-p ?(.+)$',output,re.MULTILINE)
    if match:
        error_list.append(('[WARNING] Database password might be visible in the command line history'))
        error_list.insert(0, 12300)
    else:
        error_list.insert(0, 0)
    return error_list


def fix(username, password):
    pass
