import os
import re
import sys
sys.path.insert(0, '/home/anhthc/do_an/')
import helper

error_list = list()


# def check(username, password):
def check(username, password):
    output = os.popen('sudo systemctl status mysql').read()
    match = re.search(r'\(([^\)].*); [e,d]',output,re.MULTILINE)
    flag = True
    if match:
        mysqlScript = match.group(1)
        with open(mysqlScript, 'rb') as f:
            configContent = f.read()
            if configContent:
                match = re.search(r'ExecStart=(.*)',configContent,re.MULTILINE)
                if match:
                    startupCommand = match.group(1)
                    match = re.search('--allow-suspicious-udfs',startupCommand)
                    if match:
                        flag = False
                        error_list.append(('[WARNING] allow-suspicious-udfs option might be added in startup Mysql command'))
                        error_list.insert(0, 14300)
    if flag:
        error_list.insert(0,0)
    return error_list

def fix(username, password):
    output = os.popen('sudo systemctl status mysql').read()
    match = re.search(r'\(([^\)].*); [e,d]',output,re.MULTILINE)
    if match:
        mysqlScript = match.group(1)
        with open(mysqlScript, 'rb') as f:
            configContent = f.read()
            f.close()
            if configContent:
                match = re.search(r'ExecStart=(.*)',configContent,re.MULTILINE)
                if match:
                    startupCommand = match.group(1)
                    match = re.search('--allow-suspicious-udfs',startupCommand)
                    if match:
                        helper.updateConfig(mysqlScript,{'ExecStart':'/usr/sbin/mysqld'})