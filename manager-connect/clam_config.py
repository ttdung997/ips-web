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
ruleset_url = url + '/clam/'
url  = url + "/get/clamlist"

# quit()
while(1):
	print(url)
	# url = 'http://dascam.com.vn:8000/tool/clam_signature'
	data = {'key': key}
	resp = requests.post(url=url,data = data)
	# print(resp)

	data = resp.json() # Check the JSON Response Content documentation below
	# [{'name': 'logical-signature', 'content': 'Sig1;Target:0;(0&1&2&3)&(4|1);6b6f74656b;616c61;7a6f6c77;73746566616e;deadbeef', 'type': 'ldb'}, {'name': 'info-signature', 'content': 'name:size:sha256', 'type': 'info'}]

	rules = data[0][name]
	# print(rules)
	for rule in rules:
		print(ruleset_url + rule + ".zip")
		urllib.request.urlretrieve(ruleset_url + rule + ".zip" , "/tmp/" +rule + ".zip")
		cmd = "bash ../manager-connect/shell.sh " + rule
		p = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
		(output, err) = p.communicate()
		p_status = p.wait()
	time.sleep(7200)