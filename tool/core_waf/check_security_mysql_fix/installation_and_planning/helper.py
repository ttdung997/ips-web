import os
import re
import mysql.connector
from os import fsync

config_path = '/etc/apache2/apache211.conf'
# config_path = '/etc/mysql/mysql.conf'
envvars = '/etc/apache2/envvars'
sites_config = '/etc/apache2/sites-available/000-default.conf'
ssl_config = '/etc/apache2/sites-available/default-ssl.conf'
core_path = '/var/log/core_waf/check_security/'


def read_file(file):
    f = open(file, 'r')
    result = f.read()
    f.close()
    return result


def write_file(file, content):
    f = open(file, 'w')
    f.write(content)
    f.close()


def get_DocumentRoot():
    f = os.popen("apache2ctl -t -D DUMP_RUN_CFG 2> /dev/null | grep 'Main DocumentRoot'")
    DocumentRoot = f.read()
    f.close()
    obj = re.match(r'Main DocumentRoot: "(.*)"', DocumentRoot)
    DocumentRoot = obj.group(1)
    return DocumentRoot


def get_apache_dir():
    apache_dir = list()
    with os.popen("find / -type d -name apache2 2> /dev/null") as f:
        for line in f:
            result = line
            result2 = result.split('/')
            if result2[-1][:-1] == 'apache2':
                apache_dir.append(result[:-1])
    return apache_dir


def get_file_config():
    path = list()
    with os.popen("find /etc/apache2/ -path /etc/apache2/mods-available -prune -o -type f -name *.conf -print") as f:
        for line in f:
            path.append(line)
        return path

# print read_file('/etc/apache2/apache123.conf')
def connectToMysql(username, password):
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user=username,
            passwd=password
        )
        return connection
    except:
        print ('database connection error')

def updateConfig(filename,dict):

    RE = '(('+'|'.join(dict.keys())+')\s*=)[^\r\n]*?(\r?\n|\r)'
    pat = re.compile(RE)

    def replace(mat,dic = dict ):
        return dic[mat.group(2)].join(mat.group(1,3))

    with open(filename,'rb') as f:
        content = f.read()
        f.close()

    with open(filename,'wb') as f:
        f.write(pat.sub(replace,content))
        f.close()

def appendConfig(filename, content):
    with open(filename, 'wb') as f:
        f.write(content)
        f.close()

def fixConfFile(fileName,key, value):
    with open(fileName, 'rb') as f:
        configContent = f.read()
        f.close()
        if configContent:
            match = re.search(r''+key+'\s*=\s*(.*)', configContent, re.MULTILINE)
            if not match:
                appendConfig(fileName, configContent + '\n' + key + ' = ' + value)
            else:
                updateConfig(fileName, { key : value})
