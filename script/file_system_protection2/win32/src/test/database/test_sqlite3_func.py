import sqlite3
import os
import sys
# sys.path.append(os.path.abspath('..\\..\\database'))
# from sqlite3_func import *

path_db = os.path.dirname(__file__) + "\\test.db"


SUCCESS_CODE = 0
ERROR_CODE = 1
ERROR_CREATE_DB = "Error when create db"
SUCCESS_CREATE_DB_MSG = "Create success"
# Check sqlite3 version for Python
def sqlite_version():
    try:
        conn = sqlite3.connect(path_db)
        cur = conn.cursor()
        cur.execute('SELECT SQLITE_VERSION()')

        data = cur.fetchone()
        print("SQLite version: %s" % data)

        if conn:
            conn.close()
    except sqlite3.Error as e:
        print("Error %s:" % e.args[0])
        sys.exit(1)

#test create db
def test_create():
    try:
        conn = sqlite3.connect(path_db)
        with conn:
            cur = conn.cursor()
            # Create table storage hash string for file
            cur.execute("CREATE TABLE IF NOT EXISTS hash_file("
                        "id_file INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,"
                        "path_file TEXT(260), "
                        "hash_str TEXT(64))")
            print(SUCCESS_CREATE_DB_MSG + "hash_file.db")
            # Create table storage hash string for registry
            cur.execute("CREATE TABLE IF NOT EXISTS hash_registry("
                        "id_registry INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,"
                        "name_registry TEXT(260), "
                        "hash_str TEXT(64))")
            print(SUCCESS_CREATE_DB_MSG + "hash_registry.db")
            # Create table storage list file check integrity
            cur.execute("CREATE TABLE IF NOT EXISTS syscheck_object("
                        "id_obj	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "
                        "type INTEGER, "
                        "path TEXT(260), "
                        "state INTEGER DEFAULT 0, "
                        "ignore INTEGER DEFAULT 0)")
            print(SUCCESS_CREATE_DB_MSG + "syscheck.db")
            cur.execute("CREATE TABLE IF NOT EXISTS alert_integrity("
                        "id	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT, "
                        "time TEXT, "
                        "state TEXT, "
                        "path_object TEXT(260))")
            return SUCCESS_CODE
    except sqlite3.Error:
        print(ERROR_CREATE_DB)
        return ERROR_CODE



def insert():
    try:
        conn = sqlite3.connect(path_db)
        with conn:
            cur = conn.cursor()
            # sql = "CREATE TABLE IF NOT EXISTS Cars(Id INT, Name TEXT, Price INT" + ")"
            # cur.execute(sql)
            # cur.execute("select md5(?)", ("foo",))
            cur.execute("CREATE TABLE IF NOT EXISTS Cars(Id INT, Name TEXT, Price INT)")
            cur.execute("INSERT INTO Cars VALUES(2,'Mercedes',57127)")
            cur.execute("INSERT INTO Cars VALUES(3,'Skoda',9000)")
            cur.execute("INSERT INTO Cars VALUES(4,'Volvo',29000)")
            cur.execute("INSERT INTO Cars VALUES(5,'Bentley',350000)")
            cur.execute("INSERT INTO Cars VALUES(6,'Citroen',21000)")
            cur.execute("INSERT INTO Cars VALUES(7,'Hummer',41400)")
            cur.execute("INSERT INTO hash_table VALUES(8,'Volkswagen',21600)")
            cur.execute("SELECT id_file, path_file, hash_str FROM hash_file WHERE path_file = ?", (path_file,))
    except sqlite3.Error as e:
        print("Error %s:" % e.args[0])
        sys.exit(1)


def select():
    try:
        conn = sqlite3.connect(path_db)
        cur = conn.cursor()
        cur.execute("SELECT * FROM Cars")

        rows = cur.fetchall()
        for row in rows:
            print(row[0], row[1], row[2])

    except sqlite3.Error as e:
        print("Error %s:" % e.args[0])
        sys.exit(1)


def para_query():
    try:
        conn = sqlite3.connect(path_db)
        with conn:
            cur = conn.cursor()
            u_id = 2
            price = 620000000
            cur.execute("UPDATE Cars SET Price = ? WHERE Id = ?", (price, u_id))
            print("Number of rows updated: %d" % cur.rowcount)
    except sqlite3.Error as e:
        print("Error %s:" % e.args[0])
        sys.exit(1)


def delete():
    try:
        conn = sqlite3.connect(path_db)
        with conn:
            cur = conn.cursor()
            d_id = 8
            cur.execute("DELETE FROM Cars WHERE Id = ?", (d_id, ))
            list_id = [(1, ), (2, )]
            cur.executemany("DELETE FROM Cars WHERE Id = ?", list_id)
            cur.execute("DROP TABLE Cars")
    except sqlite3.Error as e:
        print("Error %s:" % e.args[0])
        sys.exit(1)

if __name__ == "__main__":
    sqlite_version()
    test_create()
    insert()
    delete()
    select()
    para_query()


