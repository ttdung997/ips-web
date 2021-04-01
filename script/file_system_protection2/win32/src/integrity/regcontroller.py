import winreg
from datetime import datetime,timedelta
import os
import sqlite3
import hashlib
import time
from win32.src.database.sqlite3_func import *
from win32.src.integrity.integrity_msg import *
import xml.etree.ElementTree as ET

DEF_WINREG =  {
                'HKEY_LOCAL_MACHINE': winreg.HKEY_LOCAL_MACHINE, 
                "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER, 
                "HKEY_CLASSES_ROOT": winreg.HKEY_CLASSES_ROOT,
                "HKEY_CURRENT_CONFIG": winreg.HKEY_CURRENT_CONFIG,
                "HKEY_DYN_DATA": winreg.HKEY_DYN_DATA,
                "HKEY_PERFORMANCE_DATA": winreg.HKEY_PERFORMANCE_DATA,
                "HKEY_USER": winreg.HKEY_USERS
            }

readedValue  = 0
readedKey = 0
unreadKey = 0


#Global variable
currRegistry = {}
dbRegistry = {}
res = {}

DEBUG = False
# def db_print(str):
#     # if __debug__:
#     if DEBUG:
#         print(str)
###

#return False if hash error
#else retun hexa string hash 1 result
def hash1Str(str):
    try:
        hash_alo = hashlib.sha1()
        hash_alo.update(str.encode())
    except:
        return ERROR_CODE
    return hash_alo.hexdigest()


#loopkup key store in currRegistry
def tryLookupKey(path, hkey):
    global readedValue, unreadKey, readedKey, currRegistry
    readedKey = readedKey +1
    try:
        hkeyInfo = winreg.QueryInfoKey(hkey)
        currRegistry[path] = (hash1Str(''), hkeyInfo[2], 0)
        #read value in key
        for i in range (hkeyInfo[1]):
            n, v, t = winreg.EnumValue(hkey, i)
            name = path + '->' + n

            #hash n+t+v as string
            strv = n + str(t) + str(v)
            ret = hash1Str(strv)
            if ret != ERROR_CODE:
                currRegistry[name] = (ret, hkeyInfo[2])
            readedValue = readedValue + 1

        # lookup sub key
        for i in range(hkeyInfo[0]):
            subKeyName = winreg.EnumKey(hkey, i)
            try:
                subKey = winreg.OpenKey(hkey, subKeyName, access= winreg.KEY_READ | winreg.KEY_WOW64_32KEY)
            except:     
                try:
                    subKey = winreg.OpenKey(hkey, subKeyName, access= winreg.KEY_READ | winreg.KEY_WOW64_64KEY)
                except:
                    unreadKey = unreadKey + 1
                continue

            tryLookupKey(path + '\\' + subKeyName, subKey)
        return SUCCESS_CODE
    except EnvironmentError as e:
        db_print(e)
        return ERROR_CODE

#conver tupe to dictionary by use name as key
def fromTupeToDic(src):
    if src is None or len(src) ==0:
        return {}
    ret = {}
    for i in range(len(src)):
        tmp = src[i]
        key = tmp[1]
        value = (tmp[0], tmp[2], tmp[3])
        ret[key] = value
    return ret


#return rootHkey, pathToKey such as winreg.HKEY_LOCAL_MACHINE, bla bla  and path to key from rootHkey
#if not found return None, ''
def getHKeyRoot(hkeyStr):
    spl = hkeyStr.split("\\", 1)
    if spl is None or len(spl) == 0:
        return None, ''
    pathKey = ''
    if len(spl) == 2:
        pathKey = spl[1]
    rkey = spl[0]
    rHkey = None
    
    if rkey in DEF_WINREG:
        rHkey = DEF_WINREG[rkey]
    return rHkey, pathKey

#Do read with one keyPath, and all of key it contain
#Retun SUCCESS_CODE if not error
#Else retun ERROR_CODE
def doReadReg(keyPath):
    global readedKey, readedValue, unreadKey
    rHkey, path = getHKeyRoot(keyPath)

    if rHkey == None:
        return ERROR_CODE
    try:
        hkey = winreg.OpenKey(rHkey, path)
        hkeyInfo = winreg.QueryInfoKey(hkey)
    except WindowsError as e:
        db_print(e)
        return ERROR_CODE
    tryLookupKey(keyPath, hkey)
    # db_print("All key: {}  All value {}  All unread {}".format(readedKey, readedValue, unreadKey))


#load registry to currRegistry
#Return list key config
def readRegistry(regKeyList):
    for key in regKeyList:
        doReadReg(key)


#load registry stored in db
#read registry from db to dbRegistry
def loadRegistry(listKey = None):
    global cur, dbRegistry
    res = get_registry_by_key_list(listKey)
    if res == ERROR_CODE:
        res = []
    dbRegistry = fromTupeToDic(res)
    # db_print("Db reg: {}".format(len(dbRegistry)))

#check if is key or value
def isKey(s):
    return not ('->' in s)

def insert_log(delList, updateList, insert_list, scan_time):
    # db: id, time, status, path
    iList = []
    for reg in delList:
        if(isKey(reg[1])):
            iList.append((None, scan_time) + (KEY_DEL, reg[1]))
        else:
            iList.append((None, scan_time) + (VALUE_DEL, reg[1]))

    ret = insert_many_registry_log(iList)
    # if(ret == SUCCESS_CODE):
    #     # db_print("Insert log del success")
    # db_print(iList)

    del iList
    iList = []
    for reg in updateList:
        iList.append((None, scan_time, VALUE_CHANGE, reg[1]))
    ret = insert_many_registry_log(iList)
    # if(ret == SUCCESS_CODE):
    #     db_print("Update log update success")
    # db_print(iList)

    del iList
    iList = []
    for reg in insert_list:
        if isKey(reg[1]):
            iList.append((None, scan_time, KEY_ADD, reg[1]))
        else:
            iList.append((None, scan_time, VALUE_ADD, reg[1]))

    ret = insert_many_registry_log(iList)
    # if(ret == SUCCESS_CODE):
    #     db_print("Insert log insert success")
    # db_print(iList)

def getDateTimeReadable(timeDelta):
    timeDeltaMilisec = timeDelta/10
    return datetime(1601, 1, 1) + timedelta(microseconds=timeDeltaMilisec)

def doCheck(time_scan, insert_alert = True):
    global eadedKey, unreadKey, readedValue
    insertList = []
    updateList = []
    reUpdateList = []
    delIdList = []
    global dbRegistry, currRegistry
    # {name : (hash_str, last_change)}
    for curName in currRegistry:
        curVal = currRegistry[curName]
        if curName in dbRegistry:
            dbVal = dbRegistry[curName]
            dbCmpVal = (dbVal[1], dbVal[2])
            if dbCmpVal != curVal:
                
                if isKey(curName):
                    updateList.append((curVal[0], curVal[1], dbVal[0]))
                elif dbCmpVal[0] != curVal[0]:
                    #(hash_str, name_registry, last_change, id_registry)s
                    updateList.append((curVal[0], curVal[1], dbVal[0]))
                    reUpdateList.append((dbVal[0], curName, curVal[0], curVal[1]))
            del dbRegistry[curName]
               
        else:
            insertList.append((None, curName, curVal[0], curVal[1]))
    delList = []
    for dname in dbRegistry:
        dval = dbRegistry[dname]
        delIdList.append((dval[0],))

        delList.append((dval[0] , dname) + dval[1:3])

    del dbRegistry

    dret = delete_many_registry_hash(delIdList)

    uret = update_many_registry_hash(updateList)

    iret = insert_many_registry_hash(insertList)

    del updateList
    updateList = reUpdateList
    if insert_alert:
        insert_log(delList, updateList, insertList, time_scan)
    #data read from windows system
    
    sumary = {
            "readed_key_num": readedKey,
            "unread_key_num": unreadKey,
            "readed_value_num": readedValue,
            "update_num": len(updateList),
            "update_status": uret == SUCCESS_CODE,
            "insert_num": len(insertList),
            "insert_status": iret == SUCCESS_CODE,
            "delete_num": len(delIdList),
            "delete_status": dret == SUCCESS_CODE
            }
    # if len(updateList) > 10:
    #     updateList = updateList[:9]
    # if len(insertList) > 10:
    #     insertList = insertList[:9]
    # if len(delList) > 10:
    #     delList = delList[:9]
    # detail = {
    #         "update_list": updateList,
    #         "insert_list": insertList,
    #         "delete_list": delList 
    #         }
    # res = {'sumary': sumary, 'detail': detail}
    return sumary

def doReset():
    global readedValue, readedKey, unreadKey, currRegistry, dbRegistry
    readedValue  = 0
    readedKey = 0
    unreadKey = 0
    currRegistry = {}
    dbRegistry = {}

#Test function
def scanRegistryKey(keyPath, scan_time):
    doReset()
    listKey = [keyPath]
    
    if len(keyPath) == 0:
        db_print("Nothing to do")
        return SUCCESS_CODE

    readRegistry(listKey)
    loadRegistry(listKey)
    checkObj = get_sys_check_object(keyPath, REGISTRY_TYPE)
    print(checkObj)
    if checkObj is None:
        return ERROR_CODE
    insert_alert = checkObj[3] != 0
    ret = doCheck(scan_time, insert_alert)
    
    if ret != ERROR_CODE and insert_alert == False:
        update_first_add_sts(checkObj[0])
    return ret

if __name__ == "__main__":
    pass
    
    