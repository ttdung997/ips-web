import re
import sys

path = "/opt/modsecurity/etc/custom/"
f = open(path + sys.argv[1] + ".conf", 'rb')
content = f.read()
f.close()

replace = re.sub(r'.*id:'+ sys.argv[2] +r'.*', '', content, re.MULTILINE)

f = open(path + sys.argv[1] + ".conf", 'wb')
f.write(replace)
f.close()