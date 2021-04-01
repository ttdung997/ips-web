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
        cursor.execute('SHOW VARIABLES LIKE \'default_password_lifetime\';')
        dir = cursor.fetchone()  # cursor only contains 1 record
        if dir and dir[1] >= 90:
            error_list.append('[WARNING] default_password_lifetime should be less than or equal to 90')
            error_list.insert(0, 17400)
            flag = False
    if flag:
        error_list.insert(0, 0)
    return error_list

def fix(username,password):
    connection = helper.connectToMysql(username,password)
    cursor = connection.cursor()
    if cursor:
        cursor.execute('SHOW VARIABLES LIKE \'default_password_lifetime\';')
        dir = cursor.fetchone()  # cursor only contains 1 record
        if dir and dir[1] < 90:  # cursor only contains 1 record
            cursor.execute('SET GLOBAL default_password_lifetime=90');
            mysqlDefConf = '/etc/mysql/mysql.conf.d/mysqld.cnf'
            helper.fixConfFile(mysqlDefConf,'default_password_lifetime','90')
            # with open(mysqlDefConf, 'rb') as f:
            #     configContent = f.read()
            #     f.close()
            #     if configContent:
            #         match = re.search(r'default_password_lifetime\s*=\s*', configContent, re.MULTILINE)
            #         if match:
            #             helper.updateConfig(mysqlDefConf, {'default_password_lifetime': '90'})
            #         else:
            #             helper.appendConfig(mysqlDefConf, configContent + '\n' + 'default_password_lifetime = 90')