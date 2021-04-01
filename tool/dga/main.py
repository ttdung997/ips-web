
import sys
from lib.connect_sqlite import Database
from lib.DnsQuery import DnsQuery
from lib.dga_detection import DgaPredict
from lib.dga_preprocess import DgaCheckClass
from lib.connect_mysql import myDatabase
import os
import random


list_dga = {0: 'geodo',2: 'murofet',3: 'pykspa',19: 'fobber',5: 'ramnit',6: 'Volatile',12: 'locky',9: 'simda',10: 'ramdo',11: 'suppobox',7: 'ranbyus',13: 'tempedreve',14: 'qadars',15: 'symmi',16: 'banjori',1: 'beebone',18: 'hesperbot',8: 'qakbot',22: 'corebot',20: 'dyre',21: 'cryptowall',17: 'tinba',4: 'padcrypt',23: 'P',24: 'bedep',25: 'matsnu',26: 'ptgoz',27: 'necurs',28: 'pushdo',29: 'cryptolocker',30: 'dircrypt',31: 'shifu',32: 'bamital',33: 'kraken',34: 'nymaim',35: 'shiotob',36: 'virut'}

get_custom_domain = ("SELECT * FROM bkcs_custom_domain ")
filter_custom_domain = ("SELECT COUNT(1) FROM bkcs_custom_domain WHERE domain = ? ")  
check_domain =("SELECT COUNT(1) FROM bkcs_history_daily WHERE domain = ? ") 
select_config = ("select value From bkcs_config where parameter = ?")


select_host = ("SELECT * FROM bkcs_host_moniter LIMIT 1")

add_history = ("INSERT INTO bkcs_host_history "
              "(IPaddress,Domain,Date,Time,Safe,Infected) "
              "VALUES (?,?,?,?,?,?)")
add_host = ("INSERT INTO bkcs_host_moniter"
              "(Safe,Infected,Dga) "
              "VALUES (?,?,?,?)")
update_host =("UPDATE bkcs_host_moniter SET Safe = ?,Infected =?,Dga = ?")
check_host =("SELECT COUNT(1) FROM bkcs_host_moniter")
    

def domain_preprocess(lineDomain):
		if("www" in lineDomain):
			lineDomain=lineDomain[4:]
		parts =lineDomain.split(".")
		if len(parts) > 3 or '.com.vn' in lineDomain or '.edu.vn' in lineDomain:
			lineDomain = parts[-3] + '.'  + parts[-2] + '.' + parts[-1]
		else:
			lineDomain = parts[-2] + '.' + parts[-1]
		return lineDomain
def domain_filler(fillerDomain,lineDomain):
	filerkey = 0
	if fillerDomain in lineDomain:
		# print(fillerDomain+" - "+lineDomain)
		if(fillerDomain[-1] == lineDomain[-1]):
			filerkey =  1
		elif fillerDomain[-1] == lineDomain.split(".")[-2][-1]:
			filerkey =  1
		# print(filerkey)
	return filerkey

def data_Thread():
	Alexalist =[]
	Alexalines = [line.rstrip('\n') for line in open('DNSlog/alexa')]
	for i in range(0,len(Alexalines)):
		Alexalist.append(Alexalines[i])
	#DNS moniter 
	sql_db = Database()

	sql_db.connectDB()
	fillerList=[]
	fillerDNS = sql_db.get_table(get_custom_domain)
	for row in fillerDNS:
		fillerList.append(row)
	filter_key = 0
	j=0

	myDgaPredict = DgaPredict()
	myDgaPredict.loadModelInit()


	# while j < 10:
		# command = os.system("sudo dnslog " + myDir)
		# print("-------------------------------		# print("-----------------------------------------------------")
	lines = [line.rstrip('\n') for line in open('/opt/siem-log/dga/log/dns.txt')]
	for i in range(0,len(lines)):
		# print(lines[i])
		words =lines[i].split("||")
		# print(words)
		
		lineDate = words[1].split(' ')[0]
		LineTime = words[1].split(' ')[1] + words[1].split(' ')[2]
		LineIpAddress = words[3]
		lineDomain = words[4]
		if lineDomain[-1] == '.':
			lineDomain = lineDomain[:-1]
		domain_data = (lineDomain,)
		filter_key = 0
		lineDomain = domain_preprocess(lineDomain)
		for fillerDomain in Alexalist:
			try:
				filter_key = domain_filler(fillerDomain,lineDomain)
				if(filter_key  == 1):
					print('break looop alaxa')

					print("___________________________________________")
					break
			except:
				continue	
		if(filter_key == 0):
			for fillerDomain in fillerList:
				try:
					# print(fillerDomain[1])
					filter_key = domain_filler(fillerDomain[1],lineDomain)
					if(filter_key  == 1): 
						print("bkeak loop")

						print("___________________________________________")
						break	
				except:
					continue
			
		if(filter_key == 0):
			check_domain_key = sql_db.check_table(check_domain,domain_data)
			if(check_domain_key  == 0): 
				count = 1 
			else: 
				count = check_domain_key+1
			query_data = (lineDate[-10:],LineTime,lineDomain, count)

			# print("________________________________")
			print(lineDomain)
			lineDomain= lineDomain.split(" ")[0]

			
			pInfected = myDgaPredict.predict_binary(lineDomain)[0]
			pSafe = 1-pInfected
			checkKey = sql_db.check_table_null(check_host)
			
			p0 = float(sql_db.query_select(select_config,('p0',)).fetchone()[0])
			dga = myDgaPredict.predict(lineDomain)
			# print(checkKey)
			if(checkKey == 0):
				safe0 = float(sql_db.query_select(select_config,('safe',)).fetchone()[0])
				Infected0 = float(sql_db.query_select(select_config,('infected',)).fetchone()[0])
				safe = pSafe*p0*safe0
				infected = pInfected*((1-p0)*safe0+Infected0)
				safe = safe/(safe+ infected)
				infected = 1-safe
				data = (safe,infected,dga)
				sql_db.query_table(add_host,data)
			else:
				host = sql_db.query_select_null(select_host).fetchone()
				# print(host)
				safe0 = host[2]
				Infected0 = host[3]
				safe = pSafe*p0*safe0
				infected = pInfected*((1-p0)*safe0+Infected0)
				safe = safe/(safe+ infected)
				infected = 1-safe
				data = (safe,infected,dga)
				sql_db.query_table(update_host,data)
			
			data = (LineIpAddress,lineDomain,lineDate,LineTime,safe,infected)
			print("last query")
			print(data)
			sql_db.query_table(add_history,data)


				

if __name__ == "__main__":
	data_Thread()