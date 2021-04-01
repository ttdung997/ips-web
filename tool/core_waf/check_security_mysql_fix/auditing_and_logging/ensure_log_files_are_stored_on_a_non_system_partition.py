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
    cursor.execute('SELECT @@global.log_bin_basename;')
    if cursor.rowcount > 0:
        for dir in cursor:  # cursor only contains 1 record
            if dir[1]:
                if re.search("(^/\\n|^/var|^/usr)", dir[1]):
                    error_list.append('[WARNING] log_files are stored on System partition')
                    error_list.insert(0, 16200)
                    flag = False
                    break
    if flag:
        error_list.insert(0, 0)
    return error_list

def fix(username, password):
    pass