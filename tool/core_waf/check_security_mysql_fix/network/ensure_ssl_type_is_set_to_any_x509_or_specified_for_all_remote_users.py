import os
import re
import sys
sys.path.insert(0, '/home/anhthc/do_an/')
import helper

error_list = list()

def checkType(row):
    if row[1]:
        type = row[1]
        return type == 'ANY' or type == 'X509' or type == 'SPECIFIED'
    else:
        return False


# def check(username, password):
def check(username, password):
    connection = helper.connectToMysql(username,password)
    cursor = connection.cursor()
    flag = True
    if cursor:
        cursor.execute('SELECT user, host, ssl_type FROM mysql.user WHERE NOT HOST IN (\'::1\', \'127.0.0.1\', \'localhost\');')
        rows = cursor.fetchall()
        if rows:
            for row in rows:
                if checkType(row):
                    error_list.append('[WARNING] ssl type might not be set for some users.')
                    error_list.insert(0, 18200)
                    flag = False
                    break
    if flag:
        error_list.insert(0, 0)
    return error_list

def fix(username,password):
    pass
