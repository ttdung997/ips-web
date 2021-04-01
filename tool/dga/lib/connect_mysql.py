import itertools
import os
import numpy as np
import mysql.connector
from mysql.connector import errorcode

config = {
  'user': 'root',
  'password': 'dungtt123',
  'host': '127.0.0.1',
  'database': 'zabbix',
  'raise_on_warnings': True,
}

class myDatabase():    
    def connectDB(self):
        try:
            self.con = mysql.connector.connect(**config)
            self.cur = self.con.cursor()
            print("Connect DB success")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)
                exit(1)
                
    def creat_table(self):
        for name, ddl in TABLES.iteritems():
            try:
                print("Creating table {}: ".format(name))
                self.cur.execute(ddl)
            except mysql.connector.Error as err:
                if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                    print("already exists.")
                else:
                    print(err.msg)
            else:
                print("OK")
                
    def query_table(self,query,data):
        try:
            self.cur.execute(query,data)
            self.con.commit()
            # print 'success'
        except mysql.connector.Error as err:
            print(err)
            exit(1)
    def check_table(self,query):
        try:
            self.cur.execute(query)
            check =  self.cur.fetchone()[0]
            # print(check)
            return check
        except mysql.connector.Error as err:
            print(err)
            exit(1)
    def select_table(self,query,data):
        try:
            self.cur.execute(query,data)
            data =  self.cur.fetchone()
            # print(data)
            return data
        except mysql.connector.Error as err:
            print(err)
            exit(1)
    def select_table_all(self,query):
        try:
            self.cur.execute(query)
            data =  self.cur
            # print(data)
            return data
        except mysql.connector.Error as err:
            print(err)
            return 0
    def select_table_all_con(self,query,data):
        try:
            self.cur.execute(query,data)
            data =  self.cur
            # print(data)
            return data
        except mysql.connector.Error as err:
            print(err)
            return 0
 
 
    def _del_(self):
        self.cur.close()
        self.con.close()
        

