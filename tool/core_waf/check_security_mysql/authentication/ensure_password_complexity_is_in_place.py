import os
import re
import sys
sys.path.insert(0, '/home/anhthc/do_an/')
import helper

error_list = list()

def checkLength(configDict):
    return 'validate_password_length' in configDict and configDict['validate_password_length'] >= 14

def checkMixedCase(configDict):
    return 'validate_password_mixed_case_count' in configDict and configDict['validate_password_mixed_case_count'] > 0

def checkNumberCount(configDict):
    return 'validate_password_number_count' in configDict and configDict['validate_password_number_count'] > 0

def checkCharCount(configDict):
    return 'validate_password_special_char_count' in configDict and configDict['validate_password_special_char_count'] > 0

def checkPolicy(configDict):
    return 'validate_password_policy' in configDict and (configDict['validate_password_policy'] == 'MEDIUM' or configDict['validate_password_policy'] == 'STRONG')

def isPasswordStrongEnough(configDict):
    return checkLength(configDict) and checkMixedCase(configDict) and checkNumberCount(configDict) and checkCharCount(configDict) and checkPolicy(configDict)

# def check(username, password):
def check(username, password):
    connection = helper.connectToMysql(username,password)
    cursor = connection.cursor()
    flag = True
    if cursor:
        cursor.execute('SHOW VARIABLES LIKE \'validate_password%\';')
        config = dict()
        rows = cursor.fetchall()
        if cursor.rowcount > 0:
            flag = False
            for dir in rows:
                config[dir[0]] = dir[1]
                if isPasswordStrongEnough(config):
                    error_list.insert(0, 0)
                else:
                    error_list.append('[WARNING] Password is not strong enough.')
                    error_list.insert(0, 17500)
    if flag:
        error_list.append('[WARNING] Validate plugin is not activated')
        error_list.insert(0, 17500)
    return error_list

def fixPlugin():
    fixPluginLoad()
    fixValidatePassword()
    fixLength()
    fixMixedCase()
    fixNumberCount()
    fixCharCount()
    fixPolicy()

def fixStrength(configDict):
    fixPluginLoad()
    fixValidatePassword()
    if not checkLength(configDict):
        fixLength()
    if not checkMixedCase(configDict):
        fixMixedCase()
    if not checkNumberCount(configDict):
        fixNumberCount()
    if not checkCharCount(configDict):
        fixCharCount()
    if not checkPolicy(configDict):
        fixPolicy()

def fixPluginLoad():
    mysqlDefConf = '/etc/mysql/mysql.conf.d/mysqld.cnf'
    with open(mysqlDefConf, 'rb') as f:
        configContent = f.read()
        f.close()
        if configContent:
            match = re.search(r'plugin-load\s*=\s*validate_password.so', configContent, re.MULTILINE)
            if not match:
                helper.appendConfig(mysqlDefConf, configContent + '\nplugin-load = validate_password.so')

def fixConfFile(key, value):
    mysqlDefConf = '/etc/mysql/mysql.conf.d/mysqld.cnf'
    with open(mysqlDefConf, 'rb') as f:
        configContent = f.read()
        f.close()
        if configContent:
            match = re.search(r''+key+'\s*=\s*(.*)', configContent, re.MULTILINE)
            if not match:
                helper.appendConfig(mysqlDefConf, configContent + '\n' + key + ' = ' + value)
            else:
                helper.updateConfig(mysqlDefConf, { key : value})

def fixValidatePassword():
    fixConfFile('validate-password','FORCE_PLUS_PERMANENT')

def fixLength():
    fixConfFile('validate_password_length','14')

def fixMixedCase():
    fixConfFile('validate_password_mixed_case_count','1')

def fixNumberCount():
    fixConfFile('validate_password_number_count','1')

def fixCharCount():
    fixConfFile('validate_password_special_char_count','1')

def fixPolicy():
    fixConfFile('validate_password_policy','MEDIUM')

def fix(username, password):
    connection = helper.connectToMysql(username,password)
    cursor = connection.cursor()
    flag = True
    if cursor:
        cursor.execute('SHOW VARIABLES LIKE \'validate_password%\';')
        config = dict()
        rows = cursor.fetchall()
        if cursor.rowcount > 0:
            flag = False
            for dir in rows:
                config[dir[0]] = dir[1]
            fixStrength(config)
    if flag:
        fixPlugin()