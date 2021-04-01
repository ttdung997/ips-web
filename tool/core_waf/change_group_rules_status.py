import sys
import re

f = open("/opt/modsecurity/etc/group/group_websites_waf_"+sys.argv[1]+".conf", "rb")
content = f.read()
f.close()
if sys.argv[3] == '1':
	replace = re.sub(r'.*SecRuleRemoveByTag "'+ sys.argv[2] +r'"', '#SecRuleRemoveByTag "'+ sys.argv[2] +'"', content, re.MULTILINE)
else:
	replace = re.sub(r'.*SecRuleRemoveByTag "'+ sys.argv[2] +r'"', 'SecRuleRemoveByTag "'+ sys.argv[2] +'"', content, re.MULTILINE)

f = open("/opt/modsecurity/etc/group/group_websites_waf_"+sys.argv[1]+".conf", "wb")
f.write(replace)
f.close()
