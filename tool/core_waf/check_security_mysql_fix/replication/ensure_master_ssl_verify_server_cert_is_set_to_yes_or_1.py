import os
import re
import sys

sys.path.insert(0, '/var/log/core_waf/check_security_mysql/')
import helper
error_list = list()


# def check(username, password):
def check(username, password):
    connection = helper.connectToMysql(username,password)
    cursor = connection.cursor()
    flag = True
    if cursor:
        cursor.execute('select ssl_verify_server_cert from mysql.slave_master_info;')
        dir = cursor.fetchone()
        if not dir:
            flag = False
            error_list.append('[WARNING] slave_master_info feature might not be activated.')
            error_list.insert(0, 19200)
        elif (dir[1] != '1'):
            flag = False
            error_list.append('[WARNING] the slave should verify master certificate.')
            error_list.insert(0,19200)
    if flag:
        error_list.insert(0, 0)
    return error_list

def fix(username,password):
    return