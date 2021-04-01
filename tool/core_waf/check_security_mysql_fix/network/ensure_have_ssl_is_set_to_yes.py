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
        cursor.execute('SHOW variables WHERE variable_name = \'have_ssl\';')
        dir = cursor.fetchone()  # cursor only contains 1 record
        if dir and dir[1] != 'YES':
            error_list.append('[WARNING] have_ssl might not be set')
            error_list.insert(0, 18100)
            flag = False
    if flag:
        error_list.insert(0, 0)
    return error_list

def fix(username,password):
    pass

