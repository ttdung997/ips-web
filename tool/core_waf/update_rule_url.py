import re
import sys
import os 
 # zabbix_get -s 127.0.0.1 -p 10050 -k waf.command[python,/var/www/html/firewall/core_waf/add_rule_url.py,DGA,5063,sdjflsdkgf.net]
# /var/www/html/firewall/core_waf/add_rule_url.py

path = '/opt/modsecurity/etc/custom/'
File = os.listdir(os.path.expanduser(path))
if (sys.argv[1] != sys.argv[2]):
	print sys.argv[4]
	for i in File:
		f = open(path + i, 'rb')
		result = f.read()
		f.close()
		if (sys.argv[8] != '0'):
			print '-----------------------------------------------'+i+'----------------------------------------------------------'
			# print result
			find_rule = re.findall(r'SecRule SERVER_NAME '+ sys.argv[8] +r' "chain, id:'+ sys.argv[9] +r', phase:1, log, t:none, t:urlDecodeUni, deny, capture, tag:\''+ sys.argv[2] +r'\'"\nSecRule REQUEST_URI "'+ sys.argv[4] +r'" "t:none, t:urlDecodeUni, capture, setvar:\'tx.msg=end\'"\n', result, re.DOTALL)
			print find_rule
			if len(find_rule) != 0:
				print '5'
				replace = re.sub(r'SecRule SERVER_NAME '+ sys.argv[8] +r' "chain, id:'+ sys.argv[9] +r', phase:1, log, t:none, t:urlDecodeUni, deny, capture, tag:\''+ sys.argv[2] +r'\'"\nSecRule REQUEST_URI "'+ sys.argv[4] +r'" "t:none, t:urlDecodeUni, capture, setvar:\'tx.msg=end\'"\n','', result, re.DOTALL)
		else:
			find_rule = re.findall(r'SecRule REQUEST_URI "'+ sys.argv[4] +r'" "id:'+ sys.argv[9] +r', phase:1, log, t:none, t:urlDecodeUni, deny, capture, tag:\''+ sys.argv[2] +r'\', msg:\'one\'"', result, re.MULTILINE)
			if len(find_rule) != 0:
				print '6'
				replace = re.sub(r'SecRule REQUEST_URI "'+ sys.argv[4] +r'" "id:'+ sys.argv[9] +r', phase:1, log, t:none, t:urlDecodeUni, deny, capture, tag:\''+ sys.argv[2] +r'\', msg:\'one\'"','', result, re.MULTILINE)
		if len(find_rule) != 0:
			print '9'
			f = open(path + i, 'wb')
			f.write("\n" + replace)
			f.close()
	f = open(path + sys.argv[1] + '.conf', 'ab')
	if (sys.argv[7] != '0'):
		print '7'
		rule = 'SecRule SERVER_NAME '+ sys.argv[7] +' "chain, id:'+ sys.argv[9] +', phase:1, log, t:none, t:urlDecodeUni, deny, capture, tag:\''+ sys.argv[1] +'\'"\nSecRule REQUEST_URI "'+ sys.argv[3] +'" "t:none, t:urlDecodeUni, capture, setvar:\'tx.msg=end\'"\n'
		print rule
	else:
		print '8'
		rule = 'SecRule REQUEST_URI "'+ sys.argv[3] +'" "id:'+ sys.argv[9] +', phase:1, log, t:none, t:urlDecodeUni, deny, capture, tag:\''+ sys.argv[1] +'\', msg:\'one\'"\n'
	f.write(rule)
	f.close()

else:
	print 'same group'
	f = open(path + sys.argv[1] + '.conf', 'rb')
	content = f.read()
	f.close()
	if (sys.argv[8] != '0' and sys.argv[7] != '0'):
		print '1'
		replace = re.sub(r'SecRule SERVER_NAME '+ sys.argv[8] +r' "chain, id:'+ sys.argv[9] +r', phase:1, log, t:none, t:urlDecodeUni, deny, capture, tag:\''+ sys.argv[2] +r'\'"\nSecRule REQUEST_URI "'+ sys.argv[4] +r'" "t:none, t:urlDecodeUni, capture, setvar:\'tx.msg=end\'"\n', 'SecRule SERVER_NAME '+ sys.argv[7] +' "chain, id:'+ sys.argv[9] +', phase:1, log, t:none, t:urlDecodeUni, deny, capture, tag:\''+ sys.argv[1] +'\'"\nSecRule REQUEST_URI "'+ sys.argv[3] +'" "t:none, t:urlDecodeUni, capture, setvar:\'tx.msg=end\'"\n', content, re.DOTALL)
	elif (sys.argv[8] == '0' and sys.argv[7] == '0'):
		print '2'
		replace = re.sub(r'SecRule REQUEST_URI "'+ sys.argv[4] +r'" "id:'+ sys.argv[9] +r', phase:1, log, t:none, t:urlDecodeUni, deny, capture, tag:\''+ sys.argv[2] +r'\', msg:\'one\'"', 'SecRule REQUEST_URI "'+ sys.argv[3] +'" "id:'+ sys.argv[9] +', phase:1, log, t:none, t:urlDecodeUni, deny, capture, tag:\''+ sys.argv[1] +'\', msg:\'one\'"', content, re.MULTILINE)
	elif (sys.argv[8] == '0' and sys.argv[7] != '0'):
		print '3'
		replace = re.sub(r'SecRule REQUEST_URI "'+ sys.argv[4] +r'" "id:'+ sys.argv[9] +r', phase:1, log, t:none, t:urlDecodeUni, deny, capture, tag:\''+ sys.argv[2] +r'\', msg:\'one\'"', 'SecRule SERVER_NAME '+ sys.argv[7] +' "chain, id:'+ sys.argv[9] +', phase:1, log, t:none, t:urlDecodeUni, deny, capture, tag:\''+ sys.argv[1] +'\'"\nSecRule REQUEST_URI "'+ sys.argv[3] +'" "t:none, t:urlDecodeUni, capture, setvar:\'tx.msg=end\'"\n', content, re.DOTALL)
	elif (sys.argv[8] != '0' and sys.argv[7] == '0'):
		print '4'
		replace = re.sub(r'SecRule SERVER_NAME '+ sys.argv[8] +r' "chain, id:'+ sys.argv[9] +r', phase:1, log, t:none, t:urlDecodeUni, deny, capture, tag:\''+ sys.argv[2] +r'\'"\nSecRule REQUEST_URI "'+ sys.argv[4] +r'" "t:none, t:urlDecodeUni, capture, setvar:\'tx.msg=end\'"\n', 'SecRule REQUEST_URI "'+ sys.argv[3] +'" "id:'+ sys.argv[9] +', phase:1, log, t:none, t:urlDecodeUni, deny, capture, tag:\''+ sys.argv[1] +'\', msg:\'one\'"\n', content, re.DOTALL)
	f = open(path + sys.argv[1] + '.conf', 'wb')
	f.write("\n"+replace)
	f.close()

# if (sys.argv[1] != sys.argv[2]):
# 	f = open(path + sys.argv[2] + ".conf", "rb")
# 	content = f.read()
# 	f.close()