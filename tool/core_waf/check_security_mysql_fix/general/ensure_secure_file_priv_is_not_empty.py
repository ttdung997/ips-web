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
        cursor.execute('SHOW GLOBAL VARIABLES WHERE Variable_name = \'secure_file_priv\' AND Value<>\'\';')
        dir = cursor.fetchone()
        if dir and not dir[1]:
                error_list.append('[WARNING] secure_file_priv might be deactivated')
                error_list.insert(0, 14800)
                flag = False
    if flag:
        error_list.insert(0, 0)
    return error_list

def fix(username, password):
    connection = helper.connectToMysql(username,password)
    cursor = connection.cursor()
    flag = True
    if cursor:
        cursor.execute('SHOW GLOBAL VARIABLES WHERE Variable_name = \'secure_file_priv\' AND Value<>\'\';')
        for dir in cursor:  # cursor only contains 1 record
            if not dir[1]:
                mysqlDefConf = '/etc/mysql/mysql.conf.d/mysqld.cnf'
                helper.fixConfFile(mysqlDefConf,'secure_file_priv','/var/lib/mysql-files/')
                # with open(mysqlDefConf, 'rb') as f:
                #     configContent = f.read()
                #     f.close()
                #     if configContent:
                #         match = re.search(r'secure_file_priv\s*=\s*', configContent, re.MULTILINE)
                #         if match:
                #             helper.updateConfig(mysqlDefConf, {'secure_file_priv': '/var/lib/mysql-files/'})
                #         else:
                #             helper.appendConfig(mysqlDefConf, configContent + '\n' + 'secure_file_priv=/var/lib/mysql-files/')