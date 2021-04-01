import sys
import connect_db


db = connect_db.connect()
cursor = db.cursor()
sql = "SELECT * FROM mod_group_rule"

cursor.execute(sql)
results = cursor.fetchall()
f = open("/opt/modsecurity/etc/group/group_websites_waf_"+sys.argv[1]+".conf", "wb")
content = "<IfModule mod_security2.c>\nSecRuleEngine Off\n"
for i in range(14):
	content += '#SecRuleRemoveByTag '
	content += '"'+ str(results[i][3]) +'"\n'
for i in range(14, len(results)):
	content += 'SecRuleRemoveByTag '
	content += '"'+ str(results[i][3]) +'"\n'
# for row in results:
# 	content += '#SecRuleRemoveByTag '
# 	content += '"'+ str(row[3]) +'"\n' 
content += '</IfModule>\n'
f.write(content)
f.close()