import sqlite3
from win32.src.integrity.integrity_msg import *
import os
# Defile path of database
PATH_DB_INTEGRITY = os.path.dirname(os.path.abspath(__file__)) + "\\integrity.db"


DEBUG = False
#debug print
def db_print(s):
    if DEBUG == True:
        print(s)

# return conn or None
def get_connect_db(path_db):
    conn = None
    try:
        conn = sqlite3.connect(path_db)
    except sqlite3.Error as e:
        db_print("Error %s:" % e.args[0])
    return conn


# Check version sqlite3
def sqlite3_version():
    try:
        conn = get_connect_db(PATH_DB_INTEGRITY)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT SQLITE_VERSION()")

            data = cur.fetchone()
            db_print("SQLite version: %s" % data)
    except sqlite3.Error as e:
        db_print("Error %s:" % e.args[0])


# Create database integrity
def create_integrity_db():
    try:
        conn = get_connect_db(PATH_DB_INTEGRITY)
        with conn:
            cur = conn.cursor()
            # Create table storage hash string for file
            cur.execute("CREATE TABLE IF NOT EXISTS hash_file("
                        "id_file INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "
                        "path_file TEXT(260), "
                        "hash_str TEXT(64))")
            db_print(SUCCESS_CREATE_DB_MSG + "hash_file.db")
            # Create table storage hash string for registry
            cur.execute("CREATE TABLE IF NOT EXISTS hash_registry("
                        "id_registry INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "
                        "name_registry TEXT(260), "
                        "hash_str TEXT(64), "
                        "last_change INTEGER)")

            db_print(SUCCESS_CREATE_DB_MSG + "hash_registry.db")
            # Create table storage list file check integrity
            cur.execute("CREATE TABLE IF NOT EXISTS syscheck_object("
                        "id_obj	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "
                        "type INTEGER, " #0 file 1 dir 2 registry
                        "path TEXT(260), "
                        "state INTEGER DEFAULT 0, " #state == 0 new add, 1 added
                        "ignore INTEGER DEFAULT 0)") 

            db_print(SUCCESS_CREATE_DB_MSG + "syscheck.db")
            cur.execute("CREATE TABLE IF NOT EXISTS alert_integrity("
                        "id	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "
                        "time TEXT, "
                        "state TEXT, "
                        "path_object TEXT(260))")
            conn.commit()
            return SUCCESS_CODE
    except sqlite3.Error as e:
        db_print(e)
        return ERROR_CODE

def remove_hash_file():
    try:
        conn = get_connect_db(PATH_DB_INTEGRITY)
        with conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM hash_file ")
            conn.commit()
            return SUCCESS_CODE
    except sqlite3.Error as e:
        # print("Error %s:" % e.args[0])
        db_print(ERROR_QUERY_DB)
        return ERROR_CODE

def remove_hash_registry():
    try:
        conn = get_connect_db(PATH_DB_INTEGRITY)
        with conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM hash_registry ")
            conn.commit()
            return SUCCESS_CODE
    except sqlite3.Error as e:
        # print("Error %s:" % e.args[0])
        db_print(ERROR_QUERY_DB)
        return ERROR_CODE

def remove_hash_syscheck_object():
    try:
        conn = get_connect_db(PATH_DB_INTEGRITY)
        with conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM syscheck_object ")
            conn.commit()
            return SUCCESS_CODE
    except sqlite3.Error as e:
        # print("Error %s:" % e.args[0])
        db_print(ERROR_QUERY_DB)
        return ERROR_CODE

def remove_alert_integrity():
    try:
        conn = get_connect_db(PATH_DB_INTEGRITY)
        with conn:
            cur = conn.cursor()
            
            cur.execute("DELETE FROM alert_integrity ")
            conn.commit()
            return SUCCESS_CODE
    except sqlite3.Error as e:
        # print("Error %s:" % e.args[0])
        db_print(ERROR_QUERY_DB)
        return ERROR_CODE


# Get hash record from database
def get_hash_record_db(type_obj, path_obj):
    try:
        conn = get_connect_db(PATH_DB_INTEGRITY)
        with conn:
            cur = conn.cursor()
            if type_obj == FILE_TYPE:
                cur.execute("SELECT id_file, path_file, hash_str " +
                            "FROM hash_file " +
                            "WHERE path_file = ?", (path_obj, ))
            if type_obj == REGISTRY_TYPE:
                cur.execute("SELECT id_registry, name_registry, hash_str, last_change " +
                            "FROM hash_registry " +
                            "WHERE name_registry = ?", (path_obj,))
            return cur.fetchone()
    except sqlite3.Error as e:
        # print("Error %s:" % e.args[0])
        db_print(ERROR_QUERY_DB)
        return ERROR_CODE

def insert_hash_to_db(type_obj, path_obj, hash_str):
    try:
        conn = get_connect_db(PATH_DB_INTEGRITY)
        with conn:
            cur = conn.cursor()
            if type_obj == FILE_TYPE:
                cur.execute("INSERT INTO " + "hash_file " +
                            "VALUES(?, ?, ?)", (None, path_obj, hash_str, ))
            # if type_obj == REGISTRY_TYPE:
            #     cur.execute("INSERT INTO " + "hash_registry " +
            #                 "VALUES(?, ?, ?)", (None, path_obj, hash_str, None, ))
                conn.commit()
            return SUCCESS_CODE
    except sqlite3.Error as e:
        # print("Error %s:" % e.args[0])
        db_print(ERROR_QUERY_DB)
        return ERROR_CODE


def update_hash_by_id(type_obj, id_obj, hash_str):
    try:
        conn = get_connect_db(PATH_DB_INTEGRITY)
        with conn:
            cur = conn.cursor()
            if type_obj == FILE_TYPE:
                cur.execute("UPDATE " + "hash_file SET hash_str = ? WHERE id_file = ?", (hash_str, id_obj))
            if type_obj == REGISTRY_TYPE:
                cur.execute("UPDATE " + "hash_registry SET hash_str = ? WHERE id_registry = ?", (hash_str, id_obj))
            conn.commit()
            return SUCCESS_CODE
    except sqlite3.Error as e:
        # print("Error %s:" % e.args[0])
        db_print(ERROR_QUERY_DB)
        return ERROR_CODE


def insert_integrity_object_to_db(type_obj, path, state, ignore):
    try:
        conn = get_connect_db(PATH_DB_INTEGRITY)
        with conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO " + "syscheck_object " +
                        "VALUES(?, ?, ?, ?)", (None, type_obj, path, state, ignore))
            conn.commit()
            return SUCCESS_CODE
    except sqlite3.Error as e:
        # print("Error %s:" % e.args[0])
        db_print(ERROR_QUERY_DB)
        return ERROR_CODE

def insert_integrity_alert(time, state, path_object):
    try:
        conn = get_connect_db(PATH_DB_INTEGRITY)
        with conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO " + "alert_integrity " +
                        "VALUES(?, ?, ?, ?)", (None, time, state, path_object))
            conn.commit()
            return SUCCESS_CODE
    except sqlite3.Error as e:
        # print("Error %s:" % e.args[0])
        db_print(ERROR_QUERY_DB)
        return ERROR_CODE

#insert or update
#Return SUCCESS_CODE or ERROR_CODE
def insert_or_update_sys_check(path, type):
    try:
        conn = get_connect_db(PATH_DB_INTEGRITY)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT * " +
                        "FROM syscheck_object " +
                        "WHERE path = ?", (path,))
            res = cur.fetchone()
            
            if res is None: 
                cur.execute("INSERT INTO syscheck_object " +
                            "VALUES(?, ?, ?, ?, ?)", (None, type, path, 0, 0))
                conn.commit()
                db_print('insert a record to syscheck_object')
            elif res[1]!= type:
                cur.execute("UPDATE syscheck_object " +
                            "SET type = ?, state = ? WHERE id_obj = ?", (type, 0, res[0]))
                conn.commit()
                db_print('update a record to syscheck_object')
        return SUCCESS_CODE
    except sqlite3.Error as e:
        db_print(e)
        return ERROR_CODE

def update_first_add_sts(checkId):
    try:
        conn = get_connect_db(PATH_DB_INTEGRITY)
        with conn:
            cur = conn.cursor()
            cur.execute("UPDATE syscheck_object " +
                        "SET state = ? WHERE id_obj = ?", (1, checkId))
            conn.commit()
            db_print('update a record to syscheck_object')
        return SUCCESS_CODE
    except sqlite3.Error as e:
        db_print(e)
        return ERROR_CODE


#Remove sys check record by path_type
def remove_sys_check(path, type):
    try:
        conn = get_connect_db(PATH_DB_INTEGRITY)
        with conn:
            cur = conn.cursor()
            cur.execute("DELETE " +
                        "FROM syscheck_object " +
                        "WHERE path = ? AND type = ?", (path, type))
            if(cur.rowcount >0):
                db_print("remove {} record(s)".format(cur.rowcount))
            conn.commit()
        return SUCCESS_CODE
    except sqlite3.Error as e:
        db_print(e)
        return ERROR_CODE

def get_sys_check_object(path, type):
    try:
        conn = get_connect_db(PATH_DB_INTEGRITY)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT * " +
                        "FROM syscheck_object WHERE type = ? AND path = ?", (type, path))
            return cur.fetchone()
        return SUCCESS_CODE
    except sqlite3.Error as e:
        db_print(e)
        return ERROR_CODE


def del_hash_by_id(type_obj, id_obj):
    try:
        conn = get_connect_db(PATH_DB_INTEGRITY)
        with conn:
            cur = conn.cursor()
            if type_obj == FILE_TYPE:
                cur.execute("DELETE FROM hash_file WHERE id_file = ?", (id_obj, ))
            if type_obj == REGISTRY_TYPE:
                cur.execute("DELETE FROM hash_registry WHERE id_registry = ?", (id_obj, ))
            conn.commit()
            return SUCCESS_CODE
    except sqlite3.Error:
        print(ERROR_QUERY_DB)
        return ERROR_CODE


def get_list_sys_check():
    try:
        conn = get_connect_db(PATH_DB_INTEGRITY)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT * " +
                        "FROM syscheck_object ")
            return cur.fetchall()
        return SUCCESS_CODE
    except sqlite3.Error as e:
        db_print(e)
        return ERROR_CODE

def get_list_alert():
    try:
        conn = get_connect_db(PATH_DB_INTEGRITY)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM " + "alert_integrity ORDER BY time DESC")
            return cur.fetchall()
    except sqlite3.Error as e:
        db_print(ERROR_QUERY_DB)
        return ERROR_CODE

def db_get_last_alert_id():
    try:
        conn = get_connect_db(PATH_DB_INTEGRITY)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT id FROM " + "alert_integrity ORDER BY id DESC LIMIT 1")
            return cur.fetchone()
    except sqlite3.Error as e:
        db_print(ERROR_QUERY_DB)
        return ERROR_CODE

#get alert list with id gather than id
def get_list_alert_from_id(id):
    try:
        conn = get_connect_db(PATH_DB_INTEGRITY)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM " + "alert_integrity where id > ? ORDER BY time DESC", (id, ))
            return cur.fetchall()
    except sqlite3.Error as e:
        db_print(ERROR_QUERY_DB)
        return ERROR_CODE

def get_list_hash_file():
    try:
        conn = get_connect_db(PATH_DB_INTEGRITY)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM " + "hash_file")
            return cur.fetchall()
    except sqlite3.Error as e:
        db_print(ERROR_QUERY_DB)
        return ERROR_CODE


def get_list_hash_registry():
    try:
        conn = get_connect_db(PATH_DB_INTEGRITY)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM " + "hash_registry")
            return cur.fetchall()
    except sqlite3.Error as e:
        db_print(ERROR_QUERY_DB)
        return ERROR_CODE

def get_list_file_from_curr_dir_db(path_dir):
    try:
        conn = get_connect_db(PATH_DB_INTEGRITY)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT id_file, path_file, hash_str FROM hash_file WHERE path_file LIKE ? "
                        "AND path_file NOT LIKE ?", (path_dir, path_dir + "\\%", ))
            return cur.fetchall()
    except sqlite3.Error as e:
        db_print("Error %s:" % e.args[0])
        db_print(ERROR_QUERY_DB)
        return ERROR_CODE

def get_list_file_from_curr_dir_db_and_child(path_dir):
    try:
        conn = get_connect_db(PATH_DB_INTEGRITY)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT id_file, path_file, hash_str FROM hash_file WHERE path_file LIKE ?", (path_dir +"\\%",))
            return cur.fetchall()
    except sqlite3.Error as e:
        db_print("Error %s:" % e.args[0])
        db_print(ERROR_QUERY_DB)
        return ERROR_CODE



#REGISTRY

def insert_many_registry_log(record):
    res = ERROR_CODE
    if len(record) == 0:
        return SUCCESS_CODE
    try:
        conn = get_connect_db(PATH_DB_INTEGRITY)
        with conn:
            cur = conn.cursor()
            cur.executemany("INSERT INTO alert_integrity " +
                            "VALUES(?, ?, ?, ?)", record) 
            conn.commit()
            res = SUCCESS_CODE
    except sqlite3.Error as e:
        db_print(e)
    return res

#if success return SUCCESS_CODE
#ekse return ERROR_CODE
def insert_registry_hash(name, hash_str, time, cur):
    res = ERROR_CODE
    try:
        conn = get_connect_db(PATH_DB_INTEGRITY)
        with conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO " + "registry_hash " +
                            "VALUES(?, ?, ?, ?, ?)", (None, name, hash_str, time, 0))
            conn.commit()
            res = SUCCESS_CODE
    except sqlite3.Error as e:
        db_print(e)
    return res

#insert many record by records to db
#Return ERROR_CODE if error, else return SUCCESS_CODE
def insert_many_registry_hash(records):
    res = ERROR_CODE
    try:
        conn = get_connect_db(PATH_DB_INTEGRITY)
        with conn:
            cur = conn.cursor()
            cur.executemany("INSERT INTO " + "hash_registry " +
                            "VALUES(?, ?, ?, ?)", records)
            conn.commit()
            res = SUCCESS_CODE
    except sqlite3.Error as e:
        db_print(e)
    return res

#update many record by records to db
#Return ERROR_CODE if error, else return SUCCESS_CODE
def update_many_registry_hash(records):
    res = ERROR_CODE
    try:
        conn = get_connect_db(PATH_DB_INTEGRITY)
        with conn:
            cur = conn.cursor()
            cur.executemany("UPDATE  " + "hash_registry "+
                            "SET hash_str = ?, last_change = ? WHERE id_registry = ?", records) 
            conn.commit()
            res = SUCCESS_CODE
    except sqlite3.Error as e:
        db_print(e)
    return res     


#delete many record by lis id records to db
#Return ERROR_CODE if error, else return SUCCESS_CODE
def delete_many_registry_hash(records):
    res = ERROR_CODE
    try:
        conn = get_connect_db(PATH_DB_INTEGRITY)
        with conn:
            cur = conn.cursor()
            cur.executemany("DELETE FROM  hash_registry "+
                            "WHERE id_registry = ?", records)
            conn.commit()
            res = SUCCESS_CODE   
    except sqlite3.Error as e:
        db_print(e)
    return res

#Get all registry record by keylist
def get_registry_by_key_list(keyList = []):
    querySt = "SELECT * FROM hash_registry "
    if(len(keyList) >0):
        querySt = querySt + "WHERE "
        i =0
        while i < len(keyList) -1:
            querySt = querySt + "name_registry like \"{}%\" OR ".format(keyList[i])
            i = i+1

        querySt = querySt + "name_registry like \"{}%\"".format(keyList[i])

    try:
        conn = get_connect_db(PATH_DB_INTEGRITY)
        with conn:
            cur = conn.cursor()
            cur.execute(querySt)
            return cur.fetchall()
    except sqlite3.Error as e:
        db_print(e)
        return []

def deleteDb():
    try:
        conn = get_connect_db(PATH_DB_INTEGRITY)
        with conn:
            cur = conn.cursor()
            cur.execute("DROP TABLE IF EXISTS hash_file")
            cur.execute("DROP TABLE IF EXISTS hash_registry")
            cur.execute("DROP TABLE IF EXISTS syscheck_object")
            cur.execute("DROP TABLE IF EXISTS alert_integrity")
            conn.commit()
            return SUCCESS_CODE
    except sqlite3.Error as e:
        db_print(e)
        return ERROR_CODE


def resetDb():
    deleteDb()
    create_integrity_db()


def test():
    # resetDb()
    # create_integrity_db()
    # remove_sys_check('C:\\Users\\Cu Lee\\Desktop\\test.txt')
    # db_print(get_list_sys_check())
    pass

if __name__ == '__main__':
    test()