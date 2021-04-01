import time
import itertools
import os
# import matplotlib
import numpy as np
# import redis
from lib.connect_sqlite import Database
	
class DnsQuery():

    def __init__(self, Id,Date,Time,IpAddress,Port,Request,Response,Domain):
        self.Id = Id
        self.Date = Date 
        self.Time = Time 
        self.IpAddress = IpAddress 
        self.Port = Port 
        self.Request = Request 
        self.Response = Response  
        self.Domain = Domain 
    def checkID(self,IdCheck,Response):
    	if(self.Id == IdCheck):
    		self.Response = Response
    def display(self):
    	# print self.Id+" || "+self.Date+" || "+self.Time+" || "+self.IpAddress+" || "+self.Request+" || "+self.Response
    	print(self.Id+" || "+self.Date+" || "+self.Time+" || "+self.Domain)



