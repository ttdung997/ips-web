import os
import re
import sys
sys.path.insert(0, '/home/anhthc/do_an/')
import helper

error_list = list()


# def check(username, password):
def check(username, password):
    connection = helper.connectToMysql(username,password)
    cursor = connection.cursor()
    flag = True
    if cursor:
        cursor.execute('show variables where variable_name = \'plugin_dir\';')
        dir = cursor.fetchone()
        if dir and dir[1]:
            output = os.popen('ls -l ' + dir[1] + '/.. | egrep "^drwxr[-w]xr[-w]x[ \t]*[0-9][ \t]*mysql[ \t]*mysql.*plugin.*$"').read()
            if not output:
                error_list.append('[WARNING] Datadir might not have appropriate permissions.')
                error_list.insert(0, 13800)
                flag = False
    if flag:
        error_list.insert(0, 0)
    return error_list

def fix(username,password):
    connection = helper.connectToMysql(username,password)
    cursor = connection.cursor()
    if cursor:
        cursor.execute('show variables where variable_name = \'plugin_dir\';')
        dir = cursor.fetchone()
        if dir and dir[1]:
            output = os.popen('ls -l ' + dir[1] + '/.. | egrep "^drwxr[-w]xr[-w]x[ \t]*[0-9][ \t]*mysql[ \t]*mysql.*plugin.*$"').read()
            if not output:
                os.system('chmod 755 ' + dir[1])
                os.system('chown mysql:mysql ' + dir[1])
    return
