import sys
import base64

path = '/opt/modsecurity/etc/custom/'
f = open(path + sys.argv[1] + '.conf', 'rb')
content = f.read()
f.close()

rule = base64.b64decode(sys.argv[2])
find = content.find(rule)
# print(rule)
if find > 0:
	new = content.replace(rule, '')
	f = open(path + sys.argv[1] + '.conf', 'wb')
	f.write(new)
	f.close()