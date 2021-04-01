import os
import re
import sys

sys.path.insert(0, '/var/log/core_waf/check_security_mysql/')
import helper
error_list = list()


# def check(username, password):
def check(username, password):
    error_list.insert(0, 0)
    return error_list

def fix(username,password):
    return