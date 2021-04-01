import sys
import os
import re

path = "/opt/modsecurity/etc/group/"
File = os.listdir(os.path.expanduser(path))

for i in File:
	f =open(path + i, 'rb')
	content = f.read()
	f.close()
	replace = re.sub(r'.*' + sys.argv[1] + r'\"', '', content, re.MULTILINE)
	f =open(path + i, 'wb')
	f.write(replace)
	f.close()
