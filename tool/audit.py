import calendar
import json 
data = [line.strip() for line in open("/opt/modsecurity/var/log/audit.log", 'r')]

dic = {'method':{},'port':{},'status':{}}
dateDic = {}
hourDic = {}
curhour = 0
curdate = 0
curyear = 0
for i in range(0,len(data)):
	if "-B--" in data[i]:
		method = data[i+1].split(" ")[0]
		if method not in dic['method'].keys():
			dic['method'][method]= 1
		else:
			dic['method'][method] = dic['method'][method] + 1
	if "-A--" in data[i]:
		port = data[i+1].split(" ")[-1]
		if port not in dic['port'].keys():
			dic['port'][port] = 1
		else:
			dic['port'][port] = dic['port'][port] + 1
		time = data[i+1].split(" ")[0][1:]
		# print(time)
		date = time.split(":")[0]
		hour = time.split(":")[1]
		curyear = time.split(":")[2]
		curdate = date.split("/")[0] + "/" + date.split("/")[1] 
		if curdate not in dateDic.keys():
			dateDic[curdate]= 1
		else:
			dateDic[curdate] = dateDic[curdate] + 1
		curhour = int(hour)
		if hour + "-"+ curdate not in hourDic.keys():
			hourDic[hour + "-"+ curdate]= 1
		else:
			hourDic[hour + "-"+ curdate] = hourDic[hour + "-"+ curdate] + 1

	if "-F--" in data[i]:
		status = data[i+1].split(" ")[1]
		if status not in dic['status'].keys():
			dic['status'][status] = 1
		else:
			dic['status'][status] = dic['status'][status] + 1



# print(hourDic)

month = ['Jan','Feb','Mar','Apr','May','June','July','Aug','Sept','Oct','Nov','Dec']

display_hour ={}
for i in range(curhour,24):
	curday = int(curdate.split("/")[0])-1
	curmonth = curdate.split("/")[1]
	if curday == 0:
		curmonth = month[month.index(curmonth)-1]
		curday = calendar.monthrange(curyear,month.index(curmonth))[1]
	if str(i) + "-"+ str(curday)+"/"+  curmonth not in hourDic.keys():
		display_hour[str(curday)+"/"+  curmonth + "-" + str(i) + "h" ] =0
	else:
		display_hour[str(curday)+"/"+  curmonth + "-" + str(i) + "h"] = hourDic[str(i) + str(int(curdate.split("/")[0])-1)+"/"+  curdate.split("/")[1]]
for i in range(0,curhour+1):
	if str(i) + "-"+ curdate not in hourDic.keys():
		display_hour[curdate + "-" + str(i) + "h" ] = 0
	else:
		display_hour[curdate + "-" + str(i) + "h"] = hourDic[str(i) + "-"+ curdate]
	


# print(dateDic)
curday = int(curdate.split("/")[0])
curmonth = curdate.split("/")[1]

count = 0

display_date = {}

if curday > 15:
	startday = curday -15
	startmonth = curmonth
else:
	# print(month.index(curmonth) - 1 )
	if not month.index(curmonth) - 1 <= 0:
		startmonth = month[month.index(curmonth) - 1]
		startday = calendar.monthrange(curyear,month.index(startmonth))[1]-(15-curday)
	else:
		startday = 0
		startmonth  = curmonth

dateloop = startday
check = 0 
if month.index(curmonth) == 0:
	check =1

while count  <= 15:
	if check ==1:
		break
	if curmonth != startmonth:
		cache = str(dateloop) + "/" + month[month.index(curmonth-1)]
		if (cache) not in dateDic:
			display_date[cache] = 0
		else:
			display_date[cache] = dateDic[cache]
		dateloop = dateloop + 1
		if dateloop > calendar.monthrange(curyear,month.index(startmonth))[1]:
			dateloop = 1
	else:
		cache = str(dateloop) + "/" + month[month.index(curmonth)]
		if (cache) not in dateDic:
			display_date[cache] = 0
		else:
			display_date[cache] = dateDic[cache]

		dateloop = dateloop + 1	
	count = count + 1
if check == 1:
	for i in range(0,curday+1):
		cache = str(i) + "/" + month[month.index(curmonth)]
		if (cache) not in dateDic:
			display_date[cache] = 0
		else:
			display_date[cache] = dateDic[cache]



hourKey =[]
hourValue = []
for key,val in display_hour.items():
	hourKey.append(key)
	hourValue.append(val)
data = [dic, hourKey, hourValue, display_date]  
print(json.dumps(data))  

