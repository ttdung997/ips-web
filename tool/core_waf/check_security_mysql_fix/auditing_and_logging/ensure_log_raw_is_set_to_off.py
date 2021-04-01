import os
import re
import sys

sys.path.insert(0, '/var/log/core_waf/check_security_mysql/')
import helper
error_list = list()


# def check(username, password):
def check(username, password):
    flag = True
    mysqlDefConf = '/etc/mysql/mysql.conf.d/mysqld.cnf'
    with open(mysqlDefConf, 'rb') as f:
        configContent = f.read()
        f.close()
        if configContent:
            match = re.search(r'log-raw\s*=\s*', configContent, re.MULTILINE)
            if not match:
                error_list.append('[WARNING] log-raw is not present in config file.')
                error_list.insert(0, 16500)
                flag = False
            elif match.group(1) != 'OFF':
                error_list.append('[WARNING] log-raw is set to \'ON\' in config file.')
                error_list.insert(0, 16500)
                flag = False
    if flag:
        error_list.insert(0, 0)
    return error_list

def fix(username,password):
    mysqlDefConf = '/etc/mysql/mysql.conf.d/mysqld.cnf'
    helper.fixConfFile(mysqlDefConf,'log-raw','OFF')
    # with open(mysqlDefConf, 'rb') as f:
    #     configContent = f.read()
    #     f.close()
    #     if configContent:
    #         match = re.search(r'log-raw\s*=\s*(.*)', configContent, re.MULTILINE)
    #         if not match:
    #             helper.appendConfig(mysqlDefConf, configContent + '\n' + 'log-raw = OFF')
    #         elif match.group(1) != 'OFF':
    #             helper.updateConfig(mysqlDefConf, {'log-raw': 'OFF'})