import re
import sys
import base64
import os

path = '/opt/modsecurity/etc/custom/'
File = os.listdir(os.path.expanduser(path))

if sys.argv[1] == sys.argv[2]:
	f = open(path + sys.argv[1] + '.conf', 'rb')
	content = f.read()
	f.close()

	old_rule = base64.b64decode(sys.argv[3])
	rule = base64.b64decode(sys.argv[4])
	new = content.replace(old_rule, rule)

	f = open(path + sys.argv[1] + '.conf', 'wb')
	f.write("\n" + new + "\n")
	f.close()
else:
	old_rule = base64.b64decode(sys.argv[3])
	rule = base64.b64decode(sys.argv[4])
	for i in File:
		f = open(path + i, 'rb')
		result = f.read()
		f.close()
		find = result.rfind(old_rule)
		flog = open(path +'log', 'ab')
		flog.write('File: '+ i)
		flog.write('\n-----------------------------------------------------------------\n')
		flog.write('Result: '+result)
		flog.write('\n-----------------------------------------------------------------\n')
		flog.write('Old_rule: '+old_rule)
		flog.write('\n-----------------------------------------------------------------\n')
		flog.write("Find: "+str(find))
		flog.write('\n---------------------------------------------------------------------\n')
		if find >= 0:
			flog.write("OK")
			flog.write('\n----------------------------------------------------------------\n')
			new = result.replace(old_rule, '')
			f = open(path + i, 'wb')
			flog.write('new: '+new)
			flog.close()
			f.write(new + "\n")
			f.close()
		else:
			flog.close()
	f = open(path + sys.argv[1] + '.conf', 'ab')
	f.write("\n" + rule + "\n")
	f.close()
