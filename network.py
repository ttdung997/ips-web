
import os

os.system("timeout 15 ifstat > /tmp/network.txt")
while 1:
	os.system("timeout 15 ifstat > /tmp/network2.txt")
	os.system("head -n 1 /tmp/network.txt >  /tmp/network3.txt")
	os.system("tail -n 2 /tmp/network.txt >>  /tmp/network3.txt")
	os.system("tail -n 10 /tmp/network2.txt >>  /tmp/network3.txt")
	os.system("cp /tmp/network3.txt  /tmp/network.txt")
	# a=1
