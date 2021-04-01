import re
import sys
import os


path = "/opt/modsecurity/etc/custom/"
File = os.listdir(os.path.expanduser(path))
f = open(path + sys.argv[1]+'.conf', 'rb')
content = f.read()
f.close()
rule = 'SecRule REMOTE_ADDR '+ '"' +str(sys.argv[2])+ '"' +' "id:'+str(sys.argv[3])+', phase:1, deny, log, tag:\''+ sys.argv[1] +'\'"'

check = re.findall(r'.*id:'+ sys.argv[3] +r',.*', content, re.MULTILINE)
print 'check:'+ str(len(check))
if (len(check) != 0):
	f = open(path + sys.argv[1]+'.conf', 'wb')
	replace = re.sub(r'.*id:'+ sys.argv[3] +r',.*', rule, content, re.MULTILINE)
	f.write(replace)
	f.close()
else:
	for i in File:
		f = open(path + i, 'rb')
		result = f.read()
		f.close()
		find = re.findall(r'.*id:'+ sys.argv[3] +r',.*', result, re.MULTILINE)
		if (len(find) != 0):
			f = open(path + i, 'wb')
			replace = re.sub(r'.*id:'+ sys.argv[3] +r',.*', '', result, re.MULTILINE)
			f.write(replace)
			f.close()
	f = open(path + sys.argv[1]+'.conf', 'ab')
	print 'rule:' + rule
	f.write(rule + '\n')
	f.close()
