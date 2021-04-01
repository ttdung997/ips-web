import re
import sys

path = "/opt/modsecurity/etc/custom/"
f = open(path + sys.argv[1] + ".conf", 'rb')
content = f.read()
f.close()
print sys.argv[3]
if (sys.argv[4] != '0'):
	replace = re.sub(r'SecRule SERVER_NAME '+ sys.argv[4] +r' "chain, id:'+ sys.argv[2] +r', phase:1, log, t:none, t:urlDecodeUni, deny, capture, tag:\''+ sys.argv[1] +r'\'"\nSecRule REQUEST_URI "'+ sys.argv[3] +r'" "t:none, t:urlDecodeUni, capture, setvar:\'tx.msg=end\'"\n','', content, re.DOTALL)
	# print re.findall(r'SecRule SERVER_NAME '+ sys.argv[4] +r' "chain, id:'+ sys.argv[2] +r', phase:1, log, t:none, t:urlDecodeUni, deny, capture, tag:\''+ sys.argv[1] +r'\'"\nSecRule REQUEST_URI "'+ sys.argv[3] +r'" "t:none, t:urlDecodeUni, capture, setvar:\'tx.msg=end\'"\n', content, re.DOTALL)
else:
	# print 'hah'
	replace = re.sub(r'SecRule REQUEST_URI "'+ sys.argv[3] +r'" "id:'+ sys.argv[2] +r', phase:1, log, t:none, t:urlDecodeUni, deny, capture, tag:\''+ sys.argv[1] +r'\', msg:\'one\'"','', content, re.MULTILINE)
		

f = open(path + sys.argv[1] + ".conf", 'wb')
f.write(replace)
f.close()