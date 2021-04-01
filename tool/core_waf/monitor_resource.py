import connect_db
import psutil
import time


db = connect_db.connect()
time.sleep(1)

while(1):
	cpu = psutil.cpu_percent()
	ram = psutil.virtual_memory().percent
	disk = psutil.disk_usage('/').percent
	date_time = time.strftime("%Y-%m-%d  %H:%M:%S", time.localtime())
	# print str(cpu) + " : " + str(ram) + " : " + str(disk)
	cursor = db.cursor()
	sql = "INSERT INTO resource_monitor (cpu, ram, disk, time) VALUES ("+ str(cpu) + ","  + str(ram) + "," + str(disk) + "," + "'"  + str(date_time) + "'" + ")"
	try:
		cursor.execute(sql)
		db.commit()
	except Exception,e :
		db.rollback()
		print e
	time.sleep(1)
