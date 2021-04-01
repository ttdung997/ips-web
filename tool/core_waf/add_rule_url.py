import re
import sys

path = '/opt/modsecurity/etc/custom/'
print(sys.argv)
f =open(path + sys.argv[1] + ".conf", 'ab')

if (len(sys.argv) > 4):
	rule = 'SecRule SERVER_NAME ' + sys.argv[4] + ' "chain, id:' + sys.argv[2] + ', phase:1, log, t:none, t:urlDecodeUni, deny, capture, tag:\'' + sys.argv[1] + '\'"\nSecRule REQUEST_URI "'+ sys.argv[3] +'" "t:none, t:urlDecodeUni, capture, setvar:\'tx.msg=end\'"\n' 
else:
	rule = 'SecRule REQUEST_URI "'+ sys.argv[3] +'" "id:' + sys.argv[2] + ', phase:1, log, t:none, t:urlDecodeUni, deny, capture, tag:\'' + sys.argv[1] + '\', msg:\'one\'"\n'
f.write("\n" + rule)
f.close()