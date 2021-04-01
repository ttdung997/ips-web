import os
import re
import sys
sys.path.insert(0, '/home/anhthc/do_an/')
import helper

error_list = list()


# def check(username, password):
def check(username, password):
    mysqlDefConf = '/etc/mysql/mysql.conf.d/mysqld.cnf'
    flag = True
    with open(mysqlDefConf, 'rb') as f:
        configContent = f.read()
        f.close()
        if configContent:
            match = re.search(r'skip-grant-tables\s=\s', configContent, re.MULTILINE)
            if match:
                if match.group(1) != 'FALSE':
                    flag = False
                    error_list.append('[WARNING] skip-grant-tables option might be enabled in mysql config file')
                    error_list.insert(0, 14500)
    if flag:
        error_list.insert(0, 0)
    return error_list

def fix(username,password):
    mysqlDefConf = '/etc/mysql/mysql.conf.d/mysqld.cnf'
    helper.fixConfFile(mysqlDefConf,'skip-grant-tables','FALSE')
    # with open(mysqlDefConf, 'rb') as f:
    #     configContent = f.read()
    #     f.close()
    #     if configContent:
    #         match = re.search(r'skip-grant-tables\s*=\s*(.*)', configContent, re.MULTILINE)
    #         if match:
    #             if match.group(1) != 'FALSE':
    #                 helper.updateConfig(mysqlDefConf, {'skip-grant-tables': 'FALSE'})
    #         else:
    #             helper.appendConfig(mysqlDefConf, configContent + '\n' + 'skip-grant-tables = FALSE')
