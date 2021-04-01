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
        cursor.execute('SHOW VARIABLES WHERE Variable_name = \'local_infile\';')
        dir = cursor.fetchone()
        if dir and dir[1] == 'ON':
            flag = False
            error_list.append(('[WARNING] local_infile feature might be activated'))
            error_list.insert(0, 14400)
    if flag:
        error_list.insert(0, 0)
    return error_list


def fix(username,password):
    connection = helper.connectToMysql(username, password)
    cursor = connection.cursor()
    if cursor:
        cursor.execute('SHOW VARIABLES WHERE Variable_name = \'local_infile\';')
        dir = cursor.fetchone()
        if dir and  dir[1] == 'ON':
            mysqlDefConf = '/etc/mysql/mysql.conf.d/mysqld.cnf'
            helper.fixConfFile(mysqlDefConf,'local-infile','0')
            # with open(mysqlDefConf, 'rb') as f:
            #     configContent = f.read()
            #     f.close()
            #     if configContent:
            #         match = re.search(r'local-infile\s*=\s*', configContent, re.MULTILINE)
            #         if match:
            #             helper.updateConfig(mysqlDefConf,{'local-infile':'0'})
            #         else:
            #             helper.appendConfig(mysqlDefConf, configContent + '\n' + 'local-infile=0')