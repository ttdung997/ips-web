import re
import sys

f = open('/opt/modsecurity/etc/custom/'+sys.argv[1]+'.conf', 'ab')
rule = 'SecRule REMOTE_ADDR '+ '"' +str(sys.argv[2])+ '"' +' "id:'+str(sys.argv[3])+', phase:1, deny, log, tag:\''+ sys.argv[1] +'\'"\n'
f.write("\n" + rule)
