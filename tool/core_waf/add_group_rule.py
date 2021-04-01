import sys
import os
import re

path = "/opt/modsecurity/etc/group/"
f = open("/opt/modsecurity/etc/custom/"+sys.argv[1]+".conf", "wb")
f.close()

File = os.listdir(os.path.expanduser(path))

for i in File:
	f =open(path + i, 'rb')
	content = f.read()
	f.close()
	replace = re.sub(r'</IfModule>', 'SecRuleRemoveByTag "'+ sys.argv[1] +'"', content, re.MULTILINE)
	f =open(path + i, 'wb')
	f.write(replace + '</IfModule>\n')
	f.close()

