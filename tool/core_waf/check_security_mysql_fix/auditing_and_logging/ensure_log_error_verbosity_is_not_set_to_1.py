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
        cursor.execute('SHOW GLOBAL VARIABLES LIKE \'log_error_verbosity\';')
        dir = cursor.fetchone()
        if dir and dir[1]:
            # cursor only contains 1 record
            if dir[1] != 2 and dir[1] !=3:
                error_list.append('[WARNING] log_error_verbosity should be 2 or 3.')
                error_list.insert(0, 16300)
                flag = False
    if flag:
        error_list.insert(0, 0)
    return error_list

def fix(username,password):
    connection = helper.connectToMysql(username, password)
    cursor = connection.cursor()
    if cursor:
        cursor.execute('SHOW GLOBAL VARIABLES LIKE \'log_error_verbosity\';')
        dir = cursor.fetchone()
        if dir and dir[1] != 2 and dir[1] !=3:
            mysqlDefConf = '/etc/mysql/mysql.conf.d/mysqld.cnf'
            helper.fixConfFile(mysqlDefConf,'log-error_verbosity','2')
            # with open(mysqlDefConf, 'rb') as f:
            #     configContent = f.read()
            #     f.close()
            #     if configContent:
            #         match = re.search(r'log-error_verbosity\s*=\s*(.*)', configContent, re.MULTILINE)
            #         if match:
            #             helper.updateConfig(mysqlDefConf, {'log-error_verbosity': '2'})
            #         else:
            #             helper.appendConfig(mysqlDefConf, configContent + '\n' + 'log-error_verbosity = 2')