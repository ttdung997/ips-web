import sys
import re

f = open("/opt/modsecurity/etc/group/group_websites_waf_"+sys.argv[1]+".conf", "rb")
content = f.read()
f.close()
if (sys.argv[2] == '1'): 
	replace = re.sub(r'.*SecRuleEngine Off', '#SecRuleEngine Off', content, re.MULTILINE)
else:
	replace = re.sub(r'.*SecRuleEngine Off', 'SecRuleEngine Off', content, re.MULTILINE)

f =open("/opt/modsecurity/etc/group/group_websites_waf_"+sys.argv[1]+".conf", "wb")
f.write(replace)
f.close()