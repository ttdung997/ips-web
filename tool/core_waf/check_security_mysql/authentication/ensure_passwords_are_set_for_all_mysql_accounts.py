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
        cursor.execute('SELECT User,host FROM mysql.user WHERE authentication_string=\'\';')
        dir = cursor.fetchone()  # cursor only contains 1 record
        if dir:
            error_list.append('[WARNING] There might be some users don\'t have passwords.')
            error_list.insert(0, 17300)
            flag = False
    if flag:
        error_list.insert(0, 0)
    return error_list


def fix(username,password):
    pass