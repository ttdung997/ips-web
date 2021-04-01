import os
import re
import sys

sys.path.insert(0, '/var/log/core_waf/check_security_mysql/')
import helper
import mysql.connector

error_list = list()


# def check(username, password):
def check(username, password):
    connection = helper.connectToMysql(username,password)
    cursor = connection.cursor()
    flag = True
    if cursor:
        cursor.execute('show variables where variable_name = \'ssl_key\';')
        dir = cursor.fetchone()
        if dir and dir[1]:
            output = os.popen('ls -l <ssl_key Value> | egrep "^-r--------[ \t]*.[ \t]*mysql[ \t]*mysql.*$"').read()
            if not output:
                error_list.append('[WARNING] ssl_key might not have appropriate permissions.')
                error_list.insert(0, 13700)
                flag = False
    if flag:
        error_list.insert(0, 0)
    return error_list

def fix(username, password):
    connection = helper.connectToMysql(username,password)
    cursor = connection.cursor()
    flag = True
    if cursor:
        cursor.execute('show variables where variable_name = \'ssl_key\';')
        dir = cursor.fetchone()
        if dir and dir[1]:
            output = os.popen('ls -l <ssl_key Value> | egrep "^-r--------[ \t]*.[ \t]*mysql[ \t]*mysql.*$"').read()
            if not output:
                os.system('chown mysql:mysql ' + dir[1])
                os.system('chmod 400 ' + dir[1])