import MySQLdb

def connect():
	db = MySQLdb.connect("localhost","root","bkcsstudent","bkcs_http_detection2" )
	return db
