
from lib.connect_sqlite import Database
# from lib.DgaDomain import DgaDomain

import os
import sys
import re
#id name dga min max type topl domain
class DgaCheckClass():
	def init(self):
		sql_db = Database()
		sql_db.connectDB()
		get_dga_info = ("SELECT * FROM bkcs_dga_infomation")
		DgaInfoList=[]

		DgaInfo = sql_db.get_table(get_dga_info)
		for row in DgaInfo:
			DgaInfoList.append(row)
		self.DgaInfoList = DgaInfoList
	def checkDGA(self,dga0):
		dgaID = 0
		dgaKey = 0
		for DgaInfo in self.DgaInfoList:
			if DgaInfo[2] == dga0:
				dgaKey = 1
				break
			dgaID = dgaID + 1

		if(dgaKey ==1):
			return dgaID
		else:
			return -1

	def compareDga(self,Domain,dga):
		dgaID = self.checkDGA(dga)
		# print(dgaID)
		if dgaID >= 0 :
			mytoplevelDomain=""
			DomainPart = Domain.split(".")
			if len(DomainPart)== 2:
				mytoplevelDomain = Domain.split(".")[-1]
			else:
				for i in range(1,len(DomainPart)):
					if i ==1:
						mytoplevelDomain = mytoplevelDomain+ DomainPart[i]
						continue
					mytoplevelDomain = mytoplevelDomain +"."+ DomainPart[i]
			Domain=DomainPart[0]
			compareValue = 0
			# print(self.DgaInfoList[dgaID][1])
			minLen = self.DgaInfoList[dgaID][3]
			maxLen = self.DgaInfoList[dgaID][4]
			charType = self.DgaInfoList[dgaID][5]
			topleveldomainList = self.DgaInfoList[dgaID][6]
			topleveldomainList =topleveldomainList.split(",")
			# print(mytoplevelDomain)
			
			if len(Domain) >= minLen and len(Domain) <= maxLen:
				compareValue  = compareValue + 1
				# print ("test 1")
			if charType == 1:
				reg=re.compile('^[a-y]+$')
				if reg.search(Domain):
					compareValue = compareValue + 1
			elif charType == 2:
				reg=re.compile('^[a-z]+$')
				if reg.search(Domain):
					compareValue = compareValue + 1
			elif charType == 3:
				reg=re.compile('^[a-z0-9]+$')
				if reg.search(Domain):
					compareValue = compareValue + 1
			elif charType == 4:
				fillerList = self.DgaInfoList[dgaID][8].split(',')
				for filler in fillerList:
					# print(filler)
					reg=re.compile(filler)
					# print(reg.search(Domain))
					if reg.search(Domain):
						compareValue = compareValue + 1
						break
			elif charType == 5:
				half_string = ['e','y','u','i','o','a']
				reg=re.compile('^[a-z]+$')
				if reg.search(Domain):
					countChar = 0
					for char in half_string:
						countChar = countChar + Domain.count(char)

				
					if int(len(Domain)/2) == countChar:
						compareValue = compareValue + 1
					
			# print(mytoplevelDomain)
			for tld in topleveldomainList:
				# print(tld)
				if mytoplevelDomain in str(tld.encode('ascii','ignore')):
					compareValue = compareValue + 1
					# print ("test 3")
					break

			# print(float(float(compareValue)/3))
			return float(float(compareValue)/3)
		else:
			return 0
