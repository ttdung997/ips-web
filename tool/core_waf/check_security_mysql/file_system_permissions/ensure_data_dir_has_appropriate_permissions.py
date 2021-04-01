import os
import re
import sys

sys.path.insert(0, '/var/log/core_waf/check_security_mysql/')
import helper
error_list = list()


# def check(username, password):
def check(username, password):
    output = os.popen('whoami').read()
    connection = helper.connectToMysql(username,password)
    cursor = connection.cursor()
    flag = True
    if cursor:
        cursor.execute('show variables where variable_name = \'datadir\';')
        dir = cursor.fetchone()
        if dir:
            output = os.popen('ls -l ' + dir[1] + "/.. | egrep \"^d[r|w|x]{3}------\s*.\s*mysql\s*mysql\s*\d*.*mysql\"").read()
            if not output:
                error_list.append('[WARNING] Datadir might not have appropriate permissions.')
                error_list.insert(0, 13100)
                flag = False
    if flag:
        error_list.insert(0, 0)
    return error_list

def fix(username,password):
    connection = helper.connectToMysql(username,password)
    cursor = connection.cursor()
    if cursor:
        cursor.execute('show variables where variable_name = \'datadir\';')
        dir = cursor.fetchone()
        if dir and dir[1]:
            output = os.popen('ls -l ' + dir[1] + '/.. | egrep "^d[r|w|x]{3}------\s*.\s*mysql\s*mysql\s*\d*.*mysql"').read()
            if not output:
                os.system('chmod 700 ' + dir[1])
                os.system('chown mysql:mysql ' + dir[1])
    return