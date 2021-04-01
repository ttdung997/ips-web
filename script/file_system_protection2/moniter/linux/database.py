import sqlite3
import os
# Defile path of database
PATH_DB_MONITER = os.path.dirname(os.path.abspath(__file__)) + "/moniter.db"
ERROR_CODE = -1
SUCCESS_CODE = 0
SUCCESS_CREATE_DB_MSG = "Create table success"
ERROR_QUERY_DB = "Query error"

DEBUG = True
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
        conn = get_connect_db(PATH_DB_MONITER)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT SQLITE_VERSION()")

            data = cur.fetchone()
            db_print("SQLite version: %s" % data)
    except sqlite3.Error as e:
        db_print("Error %s:" % e.args[0])


# Create database integrity
def create_moniter_db():
    try:
        conn = get_connect_db(PATH_DB_MONITER)
        with conn:
            cur = conn.cursor()
            # Create table storage hash string for file
            cur.execute("CREATE TABLE IF NOT EXISTS moniter_file("
                        "id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "
                        "path TEXT(260), "
                        "c_time TEXT, "
                        "m_time TEXT, "
                        "a_time TEXT)")
            # Create table storage list file check integrity
            cur.execute("CREATE TABLE IF NOT EXISTS moniter_object("
                        "id	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "
                        "type INTEGER, " #0 file 1 dir 2 registry
                        "path TEXT(260), "
                        "state INTEGER DEFAULT 0) " #state == 0 new add, 1 added
                        )
            cur.execute("CREATE TABLE IF NOT EXISTS moniter_alert("
                        "id	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "
                        "time TEXT, "
                        "state TEXT, "
                        "path_object TEXT(260))")
            conn.commit()
            db_print("Create db successfully")
            return SUCCESS_CODE
    except sqlite3.Error as e:
        db_print(e)
        return ERROR_CODE

def remove_moniter_file_db():
    try:
        conn = get_connect_db(PATH_DB_MONITER)
        with conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM moniter_file ")
            conn.commit()
            return SUCCESS_CODE
    except sqlite3.Error as e:
        # print("Error %s:" % e.args[0])
        db_print(e)
        return ERROR_CODE

def remove_moniter_object_db():
    try:
        conn = get_connect_db(PATH_DB_MONITER)
        with conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM moniter_object ")
            conn.commit()
            return SUCCESS_CODE
    except sqlite3.Error as e:
        # print("Error %s:" % e.args[0])
        db_print(e)
        return ERROR_CODE

def remove_alert_moniter_db():
    try:
        conn = get_connect_db(PATH_DB_MONITER)
        with conn:
            cur = conn.cursor()
            
            cur.execute("DELETE FROM moniter_alert")
            conn.commit()
            return SUCCESS_CODE
    except sqlite3.Error as e:
        db_print("Error %s:" % e.args[0])
        db_print(e)
        return ERROR_CODE


# Get hash record from database
def get_moniter_record(type_obj, path_obj):
    try:
        conn = get_connect_db(PATH_DB_MONITER)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT * " +
                        "FROM moniter_object " +
                        "WHERE path = ? AND type = ?", (path_obj, type_obj))
            return cur.fetchone()
    except sqlite3.Error as e:
        db_print(e)
        return ERROR_CODE

def insert_moniter_file(path, c_time, m_time, a_time):
    try:
        conn = get_connect_db(PATH_DB_MONITER)
        with conn:
            cur = conn.cursor()

            cur.execute("INSERT INTO " + "moniter_file " +
                        "VALUES(?, ?, ?, ?, ?)", (None, path, c_time, m_time, a_time))
            conn.commit()
            return SUCCESS_CODE
    except sqlite3.Error as e:
        # print("Error %s:" % e.args[0])
        db_print(e)
        return ERROR_CODE

def insert_many_moniter_file(records):
    try:
        conn = get_connect_db(PATH_DB_MONITER)
        with conn:
            cur = conn.cursor()
            cur.executemany("INSERT INTO " + "moniter_file " +
                        "VALUES(?, ?, ?, ?, ?)", records)
            conn.commit()
            return SUCCESS_CODE
    except sqlite3.Error as e:
        # print("Error %s:" % e.args[0])
        db_print(e)
        return ERROR_CODE

def update_many_moniter_file(records):
    try:
        conn = get_connect_db(PATH_DB_MONITER)
        with conn:
            cur = conn.cursor()
            cur.executemany("UPDATE " + 
                "moniter_file SET c_time = ?, m_time = ?, a_time = ?" +
                "WHERE id = ?", records)
            conn.commit()
            return SUCCESS_CODE
    except sqlite3.Error as e:
        # print("Error %s:" % e.args[0])
        db_print(e)
        return ERROR_CODE


def update_moniter_file(id, c_time, m_time, a_time):
    try:
        conn = get_connect_db(PATH_DB_MONITER)
        with conn:
            cur = conn.cursor()
            cur.execute("UPDATE " + 
                "moniter_file SET c_time = ?, m_time = ?, a_time = ?" +
                "WHERE id = ?", (c_time, m_time, a_time, id))
            conn.commit()
            return SUCCESS_CODE
    except sqlite3.Error as e:
        # print("Error %s:" % e.args[0])
        db_print(e)
        return ERROR_CODE
def get_moniter_file(path):
    try:
        conn = get_connect_db(PATH_DB_MONITER)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT * " + 
                "FROM moniter_file " +
                "WHERE path = ?", (path,))
            
            return cur.fetchone()
    except sqlite3.Error as e:
        # print("Error %s:" % e.args[0])
        db_print(e)
        return ERROR_CODE
def insert_moniter_object(type_obj, path):
    try:
        conn = get_connect_db(PATH_DB_MONITER)
        with conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO " + "moniter_object " +
                        "VALUES(?, ?, ?, ?)", (None, type_obj, path, 0))
            conn.commit()
            return SUCCESS_CODE
    except sqlite3.Error as e:
        db_print("Error %s:" % e.args[0])
        return ERROR_CODE

def insert_moniter_alert(time, state, path_object):
    try:
        conn = get_connect_db(PATH_DB_MONITER)
        with conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO " + "moniter_alert " +
                        "VALUES(?, ?, ?, ?)", (None, time, state, path_object))
            conn.commit()
            return SUCCESS_CODE
    except sqlite3.Error as e:
        # print("Error %s:" % e.args[0])
        db_print(e)
        return ERROR_CODE

#insert or update
#Return SUCCESS_CODE or ERROR_CODE
def insert_or_update_moniter_object(path, type):
    try:
        conn = get_connect_db(PATH_DB_MONITER)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT * " +
                        "FROM moniter_object " +
                        "WHERE path = ?", (path,))
            res = cur.fetchone()
            
            if res is None: 
                cur.execute("INSERT INTO syscheck_object " +
                            "VALUES(?, ?, ?, ?, ?)", (None, type, path, 0))
                conn.commit()
                db_print('insert a record to moniter_object')
            elif res[1]!= type:
                cur.execute("UPDATE moniter_object " +
                            "SET type = ?, state = ? WHERE id = ?", (type, 0, res[0]))
                conn.commit()
        return SUCCESS_CODE
    except sqlite3.Error as e:
        db_print(e)
        return ERROR_CODE

def update_first_add_sts(checkId):
    try:
        conn = get_connect_db(PATH_DB_MONITER)
        with conn:
            cur = conn.cursor()
            cur.execute("UPDATE moniter_object " +
                        "SET state = ? WHERE id = ?", (1, checkId))
            conn.commit()
        return SUCCESS_CODE
    except sqlite3.Error as e:
        db_print(e)
        return ERROR_CODE


#Remove sys check record by path_type
def remove_moniter_object(path, type):
    try:
        conn = get_connect_db(PATH_DB_MONITER)
        with conn:
            cur = conn.cursor()
            cur.execute("DELETE " +
                        "FROM moniter_object " +
                        "WHERE path = ? AND type = ?", (path, type))
            if(cur.rowcount >0):
                db_print("remove {} record(s)".format(cur.rowcount))
            conn.commit()
        return SUCCESS_CODE
    except sqlite3.Error as e:
        db_print(e)
        return ERROR_CODE

def get_moniter_object(path, type):
    try:
        conn = get_connect_db(PATH_DB_MONITER)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT * " +
                        "FROM moniter_object WHERE path=? AND type =?",(path, type))
            return cur.fetchone()
    except sqlite3.Error as e:
        db_print(e)
        return ERROR_CODE


def del_moniter_file_by_id(id):
    try:
        conn = get_connect_db(PATH_DB_MONITER)
        with conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM moniter_file WHERE id = ?", (id, ))
            conn.commit()
            return SUCCESS_CODE
    except sqlite3.Error:
        print(ERROR_QUERY_DB)
        return ERROR_CODE


def get_list_moniter_object():
    try:
        conn = get_connect_db(PATH_DB_MONITER)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT * " +
                        "FROM moniter_object ")
            return cur.fetchall()
        return SUCCESS_CODE
    except sqlite3.Error as e:
        db_print(e)
        return ERROR_CODE

def get_list_alert():
    try:
        conn = get_connect_db(PATH_DB_MONITER)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM " + "moniter_alert ORDER BY  time DESC, id DESC;")
            return cur.fetchall()
    except sqlite3.Error as e:
        db_print(e)
        return ERROR_CODE


def db_get_last_alert_id():
    try:
        conn = get_connect_db(PATH_DB_MONITER)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT id FROM " + " moniter_alert ORDER BY id DESC LIMIT 1")
            return cur.fetchone()
    except sqlite3.Error as e:
        db_print(ERROR_QUERY_DB)
        return ERROR_CODE

#get alert list with id gather than id
def get_list_alert_from_id(id):
    try:
        conn = get_connect_db(PATH_DB_MONITER)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM " + "moniter_alert WHERE id > ? ORDER BY time DESC", (id, ))
            return cur.fetchall()
    except sqlite3.Error as e:
        db_print(ERROR_QUERY_DB)
        return ERROR_CODE

def get_list_moniter_file():
    try:
        conn = get_connect_db(PATH_DB_MONITER)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM " + "moniter_file")
            return cur.fetchall()
    except sqlite3.Error as e:
        db_print(e)
        return ERROR_CODE

def get_list_file_from_dir_path_db(path_dir):
    try:
        conn = get_connect_db(PATH_DB_MONITER)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT id, path, c_time, m_time, a_time FROM moniter_file WHERE path_file LIKE ? "
                        "AND path_file NOT LIKE ?", (path_dir+"/%", path_dir + "/%/%"))
            return cur.fetchall()
    except sqlite3.Error as e:
        db_print("Error %s:" % e.args[0])
        db_print(ERROR_QUERY_DB)
        return ERROR_CODE

def get_list_file_from_dir_path_and_child(path_dir):
    try:
        conn = get_connect_db(PATH_DB_MONITER)
        with conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM moniter_file WHERE path LIKE ?", (path_dir +"/%",))
            return cur.fetchall()
    except sqlite3.Error as e:
        db_print("Error %s:" % e.args[0])
        db_print(ERROR_QUERY_DB)
        return ERROR_CODE




def insert_many_moniter_alert(record):
    res = ERROR_CODE
    if len(record) == 0:
        return SUCCESS_CODE
    try:
        conn = get_connect_db(PATH_DB_MONITER)
        with conn:
            cur = conn.cursor()
            cur.executemany("INSERT INTO moniter_alert " +
                            "VALUES(?, ?, ?, ?)", record) 
            conn.commit()
            res = SUCCESS_CODE
    except sqlite3.Error as e:
        db_print(e)
    return res


#delete many record by lis id records to db
#Return ERROR_CODE if error, else return SUCCESS_CODE
def delete_many_moniter_file(records):
    res = ERROR_CODE
    try:
        conn = get_connect_db(PATH_DB_MONITER)
        with conn:
            cur = conn.cursor()
            cur.executemany("DELETE FROM  moniter_file "+
                            "WHERE id = ?", records)
            conn.commit()
            res = SUCCESS_CODE   
    except sqlite3.Error as e:
        db_print(e)
    return res

def deleteDb():
    try:
        conn = get_connect_db(PATH_DB_MONITER)
        with conn:
            cur = conn.cursor()
            cur.execute("DROP TABLE IF EXISTS moniter_object")
            cur.execute("DROP TABLE IF EXISTS moniter_file")
            cur.execute("DROP TABLE IF EXISTS moniter_alert")
            conn.commit()
            return SUCCESS_CODE
    except sqlite3.Error as e:
        db_print(e)
        return ERROR_CODE


def resetDb():
    deleteDb()
    create_moniter_db()


def test():
    print(get_moniter_object(r'F:\BKCS\z_More\File-Audit-Script-1.25\python', 1))
    print(get_list_moniter_object())
    pass

if __name__ == '__main__':
    test()