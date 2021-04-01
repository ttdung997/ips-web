import sys
import os
import re

path = "/opt/modsecurity/etc/group/"
File = os.listdir(os.path.expanduser(path))

for i in File:
	f =open(path + i, 'rb')
	content = f.read()
	f.close()
	replace = re.sub(r'SecRuleRemoveByTag "'+ sys.argv[1] +r'"', 'SecRuleRemoveByTag "'+ sys.argv[2] +'"', content, re.MULTILINE)
	f =open(path + i, 'wb')
	f.write(replace)
	f.close()

f = open('/opt/modsecurity/etc/custom/'+ sys.argv[2] + '.conf', 'rb')
content = f.read()
f.close()

replace = content.replace(sys.argv[1], sys.argv[2])

f = open('/opt/modsecurity/etc/custom/'+ sys.argv[2] + '.conf', 'wb')
f.write(replace)
f.close()