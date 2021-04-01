import calendar
import json 
data = [line.strip() for line in open("/opt/modsecurity/var/log/audit.log", 'r')]

dic = {'method':{},'port':{},'status':{}}
dateDic = {}
hourDic = {}
curhour = 0
curdate = 0
curyear = 0
request = []
row = []
for i in range(0,len(data)):
	if "-B--" in data[i]:
		row.append(data[i+1])
		row.append(data[i+3].split(":")[1])
		method = data[i+1].split(" ")[0]
		if method not in dic['method'].keys():
			dic['method'][method]= 1
		else:
			dic['method'][method] = dic['method'][method] + 1
	if "-A--" in data[i]:
		request.append(row)
		row = []
		row.append(data[i+1].split(" ")[3])
		row.append(data[i+1].split(" ")[5])
		port = data[i+1].split(" ")[-1]
		if port not in dic['port'].keys():
			dic['port'][port] = 1
		else:
			dic['port'][port] = dic['port'][port] + 1
		time = data[i+1].split(" ")[0][1:]
		row.append(time)

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
		row.append(data[i+1])
		status = data[i+1].split(" ")[1]
		if status not in dic['status'].keys():
			dic['status'][status] = 1
		else:
			dic['status'][status] = dic['status'][status] + 1



print(json.dumps(request))  

