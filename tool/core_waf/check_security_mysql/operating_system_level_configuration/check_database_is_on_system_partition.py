import os
import re
import sys
sys.path.insert(0, '/var/log/core_waf/check_security_mysql/')
import helper
import mysql.connector
error_list = list()

# def check(username, password):
def check(username,password):
    connection = helper.connectToMysql(username,password)
    cursor = connection.cursor()
    cursor.execute('show variables where variable_name = \'datadir\'')
    rows = cursor.fetchall()
    flag = True
    if cursor.rowcount > 0:
        for dir in rows: #cursor only contains 1 record
            defaultMysqlDir = dir[1]
            output = os.popen('df - h '+ defaultMysqlDir).read()
            if re.search("(/\\n$|/var.*$|/usr.*$)",output):
                flag = False
                error_list.append('[WARNING] Database is on System partition')
                error_list.insert(0,11100)
                break
    if flag:
        error_list.insert(0, 0)
    return error_list

def fix(username,password):
    pass