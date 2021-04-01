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
        cursor.execute('SHOW variables LIKE \'log_error\';')
        for dir in cursor:  # cursor only contains 1 record
            if not dir[1]:
                error_list.append('[WARNING] log_error path is empty.')
                error_list.insert(0, 16100)
                flag = False
                break
    if flag:
        error_list.insert(0, 0)
    return error_list


def fix(username,password):
    connection = helper.connectToMysql(username,password)
    cursor = connection.cursor()
    if cursor:
        cursor.execute('SHOW variables LIKE \'log_error\';')
        dir = cursor.fetchone()
        if not dir[1]:
            mysqlDefConf = '/etc/mysql/mysql.conf.d/mysqld.cnf'
            helper.fixConfFile(mysqlDefConf,'log-error','/var/log/mysql/error.log')
            # with open(mysqlDefConf, 'rb') as f:
            #     configContent = f.read()
            #     f.close()
            #     if configContent:
            #         match = re.search(r'log-error\s*=\s*(.*)', configContent, re.MULTILINE)
            #         if match:
            #             helper.updateConfig(mysqlDefConf, {'log-error': '/var/log/mysql/error.log'})
            #         else:
            #             helper.appendConfig(mysqlDefConf, configContent + '\n' + 'log-error = /var/log/mysql/error.log')