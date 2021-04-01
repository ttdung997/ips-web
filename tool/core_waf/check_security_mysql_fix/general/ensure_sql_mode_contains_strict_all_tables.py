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
        cursor.execute('SHOW VARIABLES LIKE \'sql_mode\';')
        dir = cursor.fetchone()
        if dir and dir[1]:
                match = re.search('STRICT_ALL_TABLES',dir[1])
                if not match:
                    error_list.append(('[WARNING] STRICT_ALL_TABLES feature might be disabled'))
                    error_list.insert(0, 14900)
    if flag:
        error_list.insert(0, 0)
    return error_list

def fix(username,password):
    connection = helper.connectToMysql(username, password)
    cursor = connection.cursor()
    flag = True
    if cursor:
        cursor.execute('SHOW VARIABLES LIKE \'sql_mode\';')
        dir = cursor.fetchone()
        if dir and dir[1]:
            match = re.search('STRICT_ALL_TABLES', dir[1])
            if not match:
                mysqlDefConf = '/etc/mysql/mysql.conf.d/mysqld.cnf'
                helper.fixConfFile(mysqlDefConf,'sql_mode', dir[1]+',STRICT_ALL_TABLES')
                # with open(mysqlDefConf, 'rb') as f:
                #     configContent = f.read()
                #     f.close()
                #     if configContent:
                #         match = re.search(r'sql_mode\s*=\s*(.*)', configContent, re.MULTILINE)
                #         if match:
                #             helper.updateConfig(mysqlDefConf, {'sql_mode': dir[1]+',STRICT_ALL_TABLES'})
                #         else:
                #             helper.appendConfig(mysqlDefConf, configContent + '\n' + 'sql_mode='+dir[1]+',STRICT_ALL_TABLES')