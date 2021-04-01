import requests
import subprocess
import time
import urllib
import os


# url = "http://localhost:8000/modlist"


f = open("../manager-connect/config.txt", "r")
data = f.read().split(" |||")
name = data[0].split(":: ")[1]
url = data[1].split("::")[1]
key = data[2].split("::")[1]



output_dir = '/tmp'
ruleset_url = url + '/ruleset/'
url  = url + "/get/modlist"

# quit()
print(url)
# url = 'http://dascam.com.vn:8000/tool/clam_signature'
data = {'key': key}
resp = requests.post(url=url,data = data)
print(resp)

data = resp.json() 

rules = data[0][name]
# print(rules)
for rule in rules:
	if len(rule) > 1:
		print(ruleset_url + rule + ".zip")
		urllib.request.urlretrieve(ruleset_url + rule + ".zip" , "/tmp/" +rule + ".zip")
		cmd = "bash ../manager-connect/unzip.sh " + rule
		p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
		(output, err) = p.communicate()
		p_status = p.wait()
