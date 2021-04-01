import sqlite3
import itertools
import os
import numpy as np
import time

TABLES = {}
TABLES['bkcs_history_daily'] = (
    "CREATE TABLE `bkcs_history_daily` ("
    "  `id` INTEGER  PRIMARY KEY,"
    "  `date` TEXT NOT NULL,"
    "  `time` TEXT NOT NULL,"
    "  `domain` TEXT NOT NULL,"
    "  `count` INTEGER NOT NULL  DEFAULT 0"
    ")")
TABLES['bkcs_custom_domain'] = (
    "CREATE TABLE `bkcs_custom_domain` ("
    "  `id` INTEGER  PRIMARY KEY,"
    "  `domain` TEXT NOT NULL,"
    "  `type` INTEGER NOT NULL"
    ")")
TABLES['bkcs_system_domain'] = (
    "CREATE TABLE `bkcs_system_domain` ("
    "  `id` INTEGER  PRIMARY KEY,"
    "  `domain` TEXT NOT NULL"
    ")")
TABLES['bkcs_report'] = (
    "CREATE TABLE `bkcs_report` ("
    "  `id` INTEGER  PRIMARY KEY,"
    "  `domain` TEXT NOT NULL,"
    "  `PID` INTEGER NOT NULL,"
    "  `time` TEXT NOT NULL"
    ")")
TABLES['bkcs_dga_report'] = (
    "CREATE TABLE `bkcs_dga_report` ("
    "  `id` INTEGER  PRIMARY KEY,"
    "  `domain` TEXT NOT NULL,"
    "  `safe` TEXT NOT NULL,"
    "  `infected` TEXT NOT NULL,"
    "  `IsDGA` INTEGER NOT NULL,"
    "  `time` TEXT NOT NULL"
    ")")
TABLES['bkcs_dga_report2'] = (
    "CREATE TABLE `bkcs_dga_report2` ("
    "  `id` INTEGER  PRIMARY KEY,"
    "  `domain` TEXT NOT NULL,"
    "  `safe` TEXT NOT NULL,"
    "  `infected` TEXT NOT NULL,"
    "  `DGA` TEXT NOT NULL,"
    "  `IsDGA` INTEGER NOT NULL,"
    "  `time` TEXT NOT NULL"
    ")")
TABLES['bkcs_config'] = (
    "CREATE TABLE `bkcs_config` ("
    "  `id` INTEGER  PRIMARY KEY,"
    "  `parameter` TEXT NOT NULL,"
    "  `value` TEXT NOT NULL"
    ")")
TABLES['bkcs_dga_infomation'] = (
    "CREATE TABLE `bkcs_dga_infomation` ("
    "  `id` INTEGER  PRIMARY KEY,"
    "  `name` TEXT NOT NULL,"
    "  `dga` INTEGER NOT NULL,"
    "  `min_length` INTEGER NOT NULL,"
    "  `max_length` INTEGER NOT NULL,"
    "  `char_type` INTEGER NOT NULL,"
    "  `topLevelDomain` TEXT NOT NULL,"
    "  `domainPerday` TEXT NOT NULL",
    "  `Expression` TEXT NOT NULL",
    "  `trust` REAL NOT NULL"
    ")")
TABLES['bkcs_char_type'] = (
    "CREATE TABLE `bkcs_char_type` ("
    "  `id` INTEGER  PRIMARY KEY,"
    "  `name` TEXT NOT NULL,"
    "  `describe` TEXT NOT NULL"
    ")")
class Database():    
    def connectDB(self):
        try:
            self.con =  sqlite3.connect('data.db')
            self.cur = self.con.cursor()
            self.cur.execute("PRAGMA journal_mode=WAL;")
            print("Connect DB success")
        except sqlite3.Error as e:
            print("Database error: %s" % e)
            exit(1)
        except Exception as e:
            print("Exception in _query: %s" % e)
            exit(1)
         
                
    def create_table(self):
        for name, ddl in TABLES.iteritems():
            try:
                print("Creating table {}: ".format(name))
                self.cur.execute(ddl)
            except sqlite3.Error as e:
            	print("Database error: %s" % e)
            except Exception as e:
            	print("Exception in _query: %s" % e)
            else:
                print("OK")
                
    def query_table(self,query,data):
        try:
            # print query
            # print data
            self.cur.execute(query,data)
            self.con.commit()
            
            # print 'success'
        except sqlite3.Error as err:
            print(err)
            # exit(1)
    def query_select_null(self,query):
        try:
            mydata = self.cur.execute(query)
            return mydata
        except sqlite3.Error as err:
            print(err)
            exit(1)

    def query_select(self,query,data):
        try:
            mydata = self.cur.execute(query,data)
            return mydata
        except sqlite3.Error as err:
            print(err)
            exit(1)  
    def check_table_null(self,query):
        try:
            self.cur.execute(query)
            check =  self.cur.fetchone()[0]
            return check
        except sqlite3.Error as err:
            print(err)
            exit(1)

    def check_table(self,query,data):
        try:
            self.cur.execute(query,data)
            check =  self.cur.fetchone()[0]
            return check
        except sqlite3.Error as err:
            print(err)
            exit(1)
    def get_table(self,query):
        try:
            data = self.cur.execute(query)
            return data
        except sqlite3.Error as err:
            print(err)
            exit(1)
    def _del_(self):
        self.cur.close()
        self.con.close()

    def configInit(self):
        try:
            self.cur.execute("insert into bkcs_config values ('1','safe','1')")
            self.cur.execute("insert into bkcs_config values ('2','infected','0')")
            self.cur.execute("insert into bkcs_config values ('3','lastquery',date('now'))")
            self.con.commit()
        except sqlite3.Error as err:
            print(err)
    def configRestart(self):
        try:
            data = self.cur.execute("select value From bkcs_config where parameter = ?",('lastquery',))
            mydate = data.fetchone()[0]
            date =  time.strftime("%Y-%m-%d")
            if 1>0:
            # if mydate != date:
                self.cur.execute("DELETE FROM bkcs_dga_report2")
                self.cur.execute("DELETE FROM bkcs_dga_report")
                self.cur.execute("UPDATE bkcs_config SET value = '1' where parameter = 'safe'")
                self.cur.execute("UPDATE bkcs_config SET value = '0' where parameter = 'infected'")
                self.cur.execute("UPDATE bkcs_config SET value = date('now') where parameter = 'lastquery'")
                self.con.commit()
            else:
                print("not update")
        except sqlite3.Error as err:
                print(err)
    def changeConfig(self,safe,infected):
        try:
            self.cur.execute("UPDATE bkcs_config SET value = "+str(safe)+" where parameter = 'safe'")
            self.cur.execute("UPDATE bkcs_config SET value = "+str(infected)+" where parameter = 'infected'")
            self.con.commit()
        except sqlite3.Error as err:
            print(err)