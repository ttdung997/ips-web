import winreg

from datetime import datetime,timedelta
import os
import sqlite3
import hashlib
import time
import xml.etree.ElementTree as ET

RES_ERROR = -1
RES_SUCCESS = 0

RES_NO_KEY = 1
RES_LOOKUP_ERR = 2

#DB result code
RES_DB_ERROR = -1
RES_DB_OK = 0
RES_INSERT_SUCC = 1
RES_UPDATE_SUCC = 2
RES_NO_CHANGE = 3
#hash rest code
RES_HASH_ERROR = -1

DEF_WINREG =  {'HKEY_LOCAL_MACHINE': winreg.HKEY_LOCAL_MACHINE, 
                "HKEY_CURRENT_USER": winreg.HKEY_CURRENT_USER, 
                "HKEY_CLASSES_ROOT": winreg.HKEY_CLASSES_ROOT,
                "HKEY_CURRENT_CONFIG": winreg.HKEY_CURRENT_CONFIG,
                "HKEY_DYN_DATA": winreg.HKEY_DYN_DATA,
                "HKEY_PERFORMANCE_DATA": winreg.HKEY_PERFORMANCE_DATA,
                "HKEY_USER": winreg.HKEY_USERS}

REGISTRY_TAG = 'windows_registry'
STS_ADD = 1
STS_UPDATE = 2
STS_DEL = 3

readedValue  = 0
readedKey = 0
unreadKey = 0


#Global variable
currRegistry = {}
dbRegistry = {}
res = {}
#Db connection
conn = None
cur  = None

DEBUG = True
def db_print(str):
    # if __debug__:
    if DEBUG:
        print(str)
###

#return False if hash error
#else retun hexa string hash 1 result
def hash1Str(str):
    try:
        hash_alo = hashlib.sha1()
        hash_alo.update(str.encode())
    except:
        return RES_HASH_ERROR
    return hash_alo.hexdigest()

######## DB function

# return conn or RES_ERROR, err
def get_connect_db(path_db):
    db_print(path_db)
    try:
        conn = sqlite3.connect(path_db)
        return RES_SUCCESS, conn
    except sqlite3.Error as e:
        db_print(e)
        return RES_DB_ERROR
    
#return connection, cursor to db
#if error return ERROR_CODE, err
def connect(dbPath = None):
    if dbPath == None:
        dbPath = r'F:\BKCS\z_More\Host-IPS\Host-IPS\win32\src\test\database\test.db'
    
    retcode, conn = get_connect_db(dbPath)
    if retcode == RES_DB_ERROR:
        return RES_DB_ERROR, conn
    return conn, conn.cursor()

def commit():
    global conn
    try:
        conn.commit()
        return RES_SUCCESS
    except sqlite3.Error as e:
        db_print(e)
        return RES_DB_ERROR

def disconnectDb():
    global conn
    try:
        conn.commit()
        conn.close()
        return RES_SUCCESS
    except sqlite3.Error as e:
        db_print(e)
        return RES_DB_ERROR

#create registry_hash table 
def create_registry_hash():
    global conn, cur
    try:
        cur.execute("CREATE TABLE IF NOT EXISTS registry_hash("
                    "id_registry INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,"
                    "name_registry TEXT(260), "
                    "hash_str TEXT(64),"
                    "last_change INTEGER,"
                    #store 100's nanosec from last update (key) from Jan 1, 1601
                    "status INTEGER)")
                    # 0 no changed
                    # 1 added
                    # 2 modif ied
                    # 3 delete
        return RES_SUCCESS
    except sqlite3.Error as e:
        db_print(e)
        return RES_DB_ERROR

def create_registry_log():
    global conn, cur
    try:
        cur.execute("CREATE TABLE IF NOT EXISTS registry_log("
                    "id_registry INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,"
                    "name_registry TEXT(260), "
                    "last_change INTEGER,"
                    "time_scan TEXT(30),"
                    #store 100's nanosec from last update (key) from Jan 1, 1601
                    "status INTEGER)")
                    # 1 added
                    # 2 modif ied
                    # 3 delete
        return RES_SUCCESS
    except sqlite3.Error as e:
        db_print(e)
        return RES_DB_ERROR

def insert_many_registry_log(record, cur, conn):
    res = RES_DB_ERROR
    if len(record) == 0:
        return RES_SUCCESS
    try:
        cur.executemany("INSERT INTO registry_log " +
                        "VALUES(?, ?, ?, ?, ?)", record) 
        conn.commit()
        res = RES_SUCCESS
    except sqlite3.Error as e:
        db_print(e)
    return res

def select_registry_log():
    global cur
    try:
        cur.execute("SELECT * FROM registry_log ORDER BY time_scan DESC") 

        return cur.fetchall()
    except sqlite3.Error as e:
        db_print(e)
        return []

def delete_log():
    global cur, conn
    try:
        cur.execute("DELETE FROM registry_log") 

        conn.commit()
        return RES_SUCCESS
    except sqlite3.Error as e:
        db_print(e)
        return RES_ERROR
#if success return RES_INSER_SUCC
#ekse return RES_DB_ERROR
def insert_registry_hash(name, hash_str, time, cur):
    res = RES_DB_ERROR
    try:
        cur.execute("INSERT INTO " + "registry_hash " +
                        "VALUES(?, ?, ?, ?, ?, ?)", (None, name, hashStr, time, 0))
        res = RES_INSERT_SUCC
    except sqlite3.Error as e:
        db_print(e)
    return res

#insert many record by records to db
#Return RES_DB_ERROR if error, else return RES_SUCCESS
def insert_many_registry_hash(records, curr, conn):
    res = RES_DB_ERROR
    try:
        cur.executemany("INSERT INTO " + "registry_hash " +
                        "VALUES(?, ?, ?, ?, ?)", records)
        conn.commit()
        res = RES_SUCCESS
    except sqlite3.Error as e:
        db_print(e)
    return res

#update many record by records to db
#Return RES_DB_ERROR if error, else return RES_SUCCESS
def update_many_registry_hash(records, cur, conn):
    res = RES_DB_ERROR
    try:
        cur.executemany("UPDATE  " + "registry_hash "+
                        "SET hash_str = ?, last_change = ?, status = ? WHERE id_registry = ?", records)
        conn.commit()
        res = RES_SUCCESS
    except sqlite3.Error as e:
        db_print(e)
    return res     

#bad perfomnace
def insert_or_update_registry_hash(name, hashStr, time, cur):
    try:
        cur.execute("SELECT id_registry, hash_str " +
                    "FROM registry_hash " +
                    "WHERE name_registry = ?", (name,))
        ret = cur.fetchone()
        if ret is None:
            #Insert
            cur.execute("INSERT INTO " + "registry_hash " +
                        "VALUES(?, ?, ?, ?, ?)", (None, name, hashStr, time, 0))
            res = RES_INSERT_SUCC
        else:
            #Update case
            if hashStr != ret[1]:
                #do update
                cur.execute("UPDATE  " + "registry_hash " +
                            "SET hash_str = ?, last_change = ?, status = ? WHERE id_registry = ?", (hashStr, time, 0, ret[0]))
                res = RES_UPDATE_SUCC
            else:
                res = RES_NO_CHANGE
        # conn.commit()
        # conn.close()  
        return res
    except sqlite3.Error as e:
        db_print("Error %s:" % e.args[0])
        return res


#delete many record by lis id records to db
#Return RES_DB_ERROR if error, else return RES_SUCCESS
def delete_many_registry_hash(records, cur, conn):
    res = RES_DB_ERROR
    try:
        cur.executemany("DELETE FROM  registry_hash "+
                        "WHERE id_registry = ?", records)
        conn.commit()
        res = RES_SUCCESS
    except sqlite3.Error as e:
        db_print(e)
    return res

#Get all registry record by keylist
def queryAll(cur, keyList = []):
    querySt = "SELECT * FROM registry_hash "
    if(len(keyList) >0):
        querySt = querySt + "WHERE "
        i =0
        while i < len(keyList) -1:
            querySt = querySt + "name_registry like \"{}%\" OR ".format(keyList[i])
            i = i+1

        querySt = querySt + "name_registry like \"{}%\"".format(keyList[i])
    db_print(querySt)
    try:
        cur.execute(querySt)
        return cur.fetchall()
    except sqlite3.Error as e:
        db_print(e)
        return []

#Clear tables
def deleteAll():
    global conn, cur
    res = RES_DB_ERROR
    try:
        cur.execute("DELETE from registry_hash")
        conn.commit()
        res = RES_SUCCESS
    except sqlite3.Error as e:
        db_print(e)
    return res


######### reg function

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
            if n == '' or n == " ":
                db_print(name)
            #hash n+t+v as string
            strv = n + str(t) + str(v)
            ret = hash1Str(strv)
            if ret != RES_HASH_ERROR:
                currRegistry[name] = (ret, hkeyInfo[2], 0)
            elif ret == RES_HASH_ERROR or ret == RES_DB_ERROR:
                db_print("Hash error")
                #need to handle?
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
        return RES_SUCCESS
    except EnvironmentError as e:
        db_print(e)
        return RES_LOOKUP_ERR

#conver tupe to dictionary by use name as key
def fromTupeToDic(src):
    if src is None or len(src) ==0:
        return {}
    ret = {}
    for i in range(len(src)):
        tmp = src[i]
        key = tmp[1]
        value = (tmp[0], tmp[2], tmp[3], tmp[4])
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
#Retun RES_SUCCESS if not error
#Else retun RES_ERROR
def doReadReg(keyPath):
    global allKeyNum, readble, unreadable, iSucc, uSucc
    rHkey, path = getHKeyRoot(keyPath)
    if rHkey == None:
        return RES_ERROR
    try:
        hkey = winreg.OpenKey(rHkey, path)
        hkeyInfo = winreg.QueryInfoKey(hkey)
    except WindowsError as e:
        db_print(e)
        return RES_LOOKUP_ERR
    # tryLookupKey(r'HKEY_CURRENT_USER\Software\CocCoc', hkey, cur)
    tryLookupKey(keyPath, hkey)
    db_print("All key: {}  All value {}  All unread {}".format(readedKey, readedValue, unreadKey))



#read config registry key to lookup from xml file
def getRegistryListCfg():
    regPath = os.path.dirname(os.path.abspath(__file__)) + "\\registry.xml"
    db_print(regPath)
    # db_print(os.path.dirname(os.path.abspath(__file__)))
    try:
        ret = []
        tree = ET.parse(regPath)
        root = tree.getroot()
        for child in root:
            if child.tag == REGISTRY_TAG:
                ret.append(child.text)
    except ET.ParseError as e:
        db_print(e)
    return ret

#return RES_SUCCESS or RES_ERROR, connect to DB
def connectDb():
    global conn, cur
    dbPath = regPath = os.path.dirname(os.path.abspath(__file__)) + "\\..\\test\\database\\test.db"
    conn, cur = connect(regPath)
    if(conn == RES_DB_ERROR):
        return conn
    return RES_SUCCESS

#load registry to currRegistry
#Return list key config
def readRegistry():
    global currRegistry
    regKeyList = getRegistryListCfg()
    for key in regKeyList:
        doReadReg(key)
    return regKeyList

#read registry from db to dbRegistry
def loadRegistry(listKey = None):
    global cur, dbRegistry
    if listKey == None:
        res = queryAll(cur)
    else:
        res = queryAll(cur, listKey)
    dbRegistry = fromTupeToDic(res)
    db_print("Db reg: {}".format(len(dbRegistry)))

#check if is key or value
def isKey(s):
    return not ('->' in s)

def insert_log(delList, updateList, insert_list, scan_time):
    global conn, cur
    iList = []
    for reg in delList:
        iList.append((None, reg[1], reg[3]) + (scan_time, STS_DEL))
    ret = insert_many_registry_log(iList, cur, conn)
    if(ret == RES_SUCCESS):
        db_print("Insert log del success")
    db_print(iList)

    del iList
    iList = []
    for reg in updateList:
        iList.append((None, reg[1], reg[3]) + (scan_time, STS_UPDATE))
    ret = insert_many_registry_log(iList, cur, conn)
    if(ret == RES_SUCCESS):
        db_print("Update log update success")
    db_print(iList)

    del iList
    iList = []
    for reg in insert_list:
        iList.append((None, reg[1], reg[3]) + (scan_time, STS_ADD))
    ret = insert_many_registry_log(iList, cur, conn)
    if(ret == RES_SUCCESS):
        db_print("Insert log insert success")
    db_print(iList)



def doCheck():
    time_scan = datetime.now()
    time_scan = time_scan.strftime("%Y-%m-%d %H:%M:%S")
    global cur, conn, readedKey, unreadKey, readedValue
    insertList = []
    updateList = []
    reUpdateList = []
    delIdList = []
    global dbRegistry, currRegistry

    for curName in currRegistry:
        curVal = currRegistry[curName]
        if curName in dbRegistry:
            dbVal = dbRegistry[curName]
            dbCmpVal = (dbVal[1], dbVal[2], dbVal[3])
            if dbCmpVal != curVal:
                
                if isKey(curName) or dbCmpVal[0] != curVal[0]:
                    updateList.append((curVal[0], curVal[1], curVal[2], dbVal[0]))
                    reUpdateList.append((dbVal[0], curName, curVal[0], curVal[1], curVal[2]))
            del dbRegistry[curName]
               
        else:
            insertList.append((None, curName, curVal[0], curVal[1], curVal[2]))
    delList = []
    for dname in dbRegistry:
        dval = dbRegistry[dname]
        delIdList.append((dval[0],))

        delList.append((dval[0] , dname) + dval[1:3])

    del dbRegistry

    dret = delete_many_registry_hash(delIdList, cur, conn)

    uret = update_many_registry_hash(updateList, cur, conn)

    iret = insert_many_registry_hash(insertList, cur, conn)
    del updateList
    updateList = reUpdateList
    insert_log(delList, updateList, insertList, time_scan)
    #data read from windows system
    
   
    sumary = {
            "readed_key_num": readedKey,
            "unread_key_num": unreadKey,
            "readed_value_num": readedValue,
            "update_num": len(updateList),
            "update_status": uret == RES_SUCCESS,
            "insert_num": len(insertList),
            "insert_status": iret == RES_SUCCESS,
            "delete_num": len(delIdList),
            "delete_status": dret == RES_SUCCESS
            }
    if len(updateList) > 10:
        updateList = updateList[:9]
    if len(insertList) > 10:
        insertList = insertList[:9]
    if len(delList) > 10:
        delList = delList[:9]
    detail = {
            "update_list": updateList,
            "insert_list": insertList,
            "delete_list": delList 
            }
    res = {'sumary': sumary, 'detail': detail}
    print(res)
    
#Test function
def test():
    connectDb()
    create_registry_log()
    create_registry_hash()
    # deleteAll()
    # delete_log()
    listKey = readRegistry()
    if(len(listKey) == 0):
        db_print("Nothing to do")
        return 0
    loadRegistry(listKey)
    doCheck()
    print(select_registry_log())
    disconnectDb()


    # listRegistryKey = getRegistryList()
    # doCheckListKey(listRegistryKey)
    # db_print(listRegistryKey)
    # db_print(getHKeyRoot(listRegistryKey[0]))
    #connect to db
    # cur, conn= connect()
    # create_registry_hash(conn, cur)
    # ret= commit(conn)
    # ret = queryAll(cur)
    # ret = fromTupeToDic(ret)
   
    # ret = disconnect(conn)

    # lookupKey('HKEY_LOCAL_MACHINE', conn, cur)
    # db_print(len(dic))
    # lookupKey('HKEY_CURRENT_USER', conn, cur)
    # hkey = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"BCD00000000\Description")
    # db_print(winreg.QueryInfoKey(hkey))

    # create_registry_hash_table()
    # insert_or_update_registry_hash_table('abc', "123", 100000000, 1)

    # db_print(hash1Str(''))
    #disconnect to db
    # disconnect(conn)
    pass
    
#return datime by timeDelta: 100's nanosec from Jan 1, 1601 (Windows file systemS

def getDateTimeReadable(timeDelta):
    timeDeltaMilisec = timeDelta/10
    return datetime(1601, 1, 1) + timedelta(microseconds=timeDeltaMilisec)

if __name__ == "__main__":
    test()
    
    