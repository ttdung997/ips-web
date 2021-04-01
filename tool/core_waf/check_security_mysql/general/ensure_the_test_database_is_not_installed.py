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
        cursor.execute('SHOW DATABASES LIKE \'test\';')
        dir = cursor.fetchone()
        if dir:
            error_list.append('[WARNING] \'test\' database might be installed.')
            error_list.insert(0, 14200)
            flag = False
    if flag:
        error_list.insert(0, 0)
    return error_list

def fix(username, password):
    connection = helper.connectToMysql(username, password)
    cursor = connection.cursor()
    if cursor:
        cursor.execute('SHOW DATABASES LIKE \'test\';')
        dir = cursor.fetchone()
        if dir and dir[1]:
            cursor.execute('DROP DATABASE "test";')