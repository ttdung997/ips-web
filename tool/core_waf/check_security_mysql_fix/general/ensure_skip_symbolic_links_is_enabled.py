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
        cursor.execute('SHOW variables LIKE \'have_symlink\';')
        dir = cursor.fetchone()
        if dir and dir[1] != 'DISABLED':
            flag = False
            error_list.append(('[WARNING] skip_symbolic_links feature might be enabled'))
            error_list.insert(0, 14600)
    if flag:
        error_list.insert(0, 0)
    return error_list

def fix(username, password):
    connection = helper.connectToMysql(username,password)
    cursor = connection.cursor()
    flag = True
    if cursor:
        cursor.execute('SHOW variables LIKE \'have_symlink\';')
        dir = cursor.fetchone()
        if dir and dir[1] != 'DISABLED':
            mysqlDefConf = '/etc/mysql/mysql.conf.d/mysqld.cnf'
            helper.fixConfFile(mysqlDefConf,'skip_symbolic_links','YES')
            # with open(mysqlDefConf, 'rb') as f:
            #     configContent = f.read()
            #     f.close()
            #     if configContent:
            #         match = re.search(r'skip_symbolic_links\s*=\s*', configContent, re.MULTILINE)
            #         if match:
            #             helper.updateConfig(mysqlDefConf,{'skip_symbolic_links':'YES'})
            #         else:
            #             helper.appendConfig(mysqlDefConf, configContent + '\n' + 'skip_symbolic_links=YES')