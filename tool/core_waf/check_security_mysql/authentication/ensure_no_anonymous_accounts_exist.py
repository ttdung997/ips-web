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
        cursor.execute('SELECT user,host FROM mysql.user WHERE user = \'\';')
        dir = cursor.fetchone()
        if dir:
            error_list.append('[WARNING] There might be some anonymous users.')
            error_list.insert(0, 17700)
            flag = False
    if flag:
        error_list.insert(0, 0)
    return error_list

def fix(username,password):
    pass
