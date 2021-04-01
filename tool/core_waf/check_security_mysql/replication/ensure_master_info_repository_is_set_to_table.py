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
        cursor.execute('SHOW GLOBAL VARIABLES LIKE \'master_info_repository\';')
        dir = cursor.fetchone()
        if dir and dir[1] == 'FILE':
            flag = False
            error_list.append(('[WARNING] master_info_repository should be save in TABLE instead of FILE'))
            error_list.insert(0, 19300)
    if flag:
        error_list.insert(0, 0)
    return error_list


def fix(username,password):
    connection = helper.connectToMysql(username, password)
    cursor = connection.cursor()
    if cursor:
        cursor.execute('SHOW VARIABLES WHERE Variable_name = \'master_info_repository\';')
        dir = cursor.fetchone()
        if dir and dir[1] == 'FILE':
            mysqlDefConf = '/etc/mysql/mysql.conf.d/mysqld.cnf'
            helper.fixConfFile(mysqlDefConf, 'master_info_repository','TABLE')
            # with open(mysqlDefConf, 'rb') as f:
            #     configContent = f.read()
            #     f.close()
            #     if configContent:
            #         match = re.search(r'master_info_repository\s*=\s*', configContent, re.MULTILINE)
            #         if match:
            #             helper.updateConfig(mysqlDefConf,{'master_info_repository':'TABLE'})
            #         else:
            #             helper.appendConfig(mysqlDefConf, configContent + '\n' + 'master_info_repository=TABLE')