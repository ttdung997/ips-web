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
    cursor.execute('SELECT @@global.sql_mode;')
    rows = cursor.fetchall()
    if cursor.rowcount > 0:
        for dir in rows:  # cursor only contains 1 record
            if dir[0]:
                globalSetting = dir[0]
                break
    cursor.execute('SELECT @@session.sql_mode;')
    rows = cursor.fetchall()
    if cursor.rowcount > 0:
        for dir in rows:
            if dir[0]:
                sessionSetting = dir[0]
    if globalSetting and sessionSetting:
        if not re.search("NO_AUTO_CREATE_USER", globalSetting) or not re.search("NO_AUTO_CREATE_USER", sessionSetting):
            error_list.append('[WARNING] NO_AUTO_CREAT_USER might be activated')
            error_list.insert(0, 17200)
            flag = False
    if flag:
        error_list.insert(0, 0)
    return error_list

def fix(username,password):
    connection = helper.connectToMysql(username, password)
    cursor = connection.cursor()
    flag = True
    row_count = cursor.execute('SELECT @@global.sql_mode;')
    dir = cursor.fetchone()  # cursor only contains 1 record
    if dir and dir[0]:
        globalSetting = dir[0]
        if not re.search("NO_AUTO_CREATE_USER", globalSetting):
            newSetting = globalSetting + ',NO_AUTO_CREATE_USER'
            mysqlDefConf = '/etc/mysql/mysql.conf.d/mysqld.cnf'
            with open(mysqlDefConf, 'rb') as f:
                configContent = f.read()
                f.close()
                if configContent:
                    match = re.search(r'sql_mode\s*=\s*', configContent, re.MULTILINE)
                    if not match:
                        helper.appendConfig(mysqlDefConf, configContent + '\n' + 'sql_mode = ' + newSetting)
                    else:
                        helper.updateConfig(mysqlDefConf, {'sql_mode': newSetting})