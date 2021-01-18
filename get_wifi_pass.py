#!/usr/bin/python3

import subprocess
import re

# collecting info's
wifiname = subprocess.getoutput("(ls /etc/NetworkManager/system-connections )").split("\n")
wifinames = subprocess.getoutput("(ls /etc/NetworkManager/system-connections  | cut -d '.' -f 1)")
wifis = wifinames.split("\n")


#print(wifis)


# filler
print("+---------------+")
print("+ Network Found +")
print("+---------------+")

# grepping out passwords i,e psk keys
for i in range(len(wifis)):
	connection_type = subprocess.getoutput("sudo cat '/etc/NetworkManager/system-connections/"+wifiname[i]+"' | grep type= | cut -d '=' -f 2")
	if connection_type == 'wifi':
		passwd = subprocess.getoutput("sudo cat '/etc/NetworkManager/system-connections/"+wifiname[i]+"' | grep psk= | cut -d '=' -f 2")
		#print(passwd)
		if re.search("Permission denied",passwd):
			print("make sure you run as Root")
			break
		else:
			if passwd == "":
				
				print("+",wifis[i],"=> NONE")
			else:
				print("+",wifis[i],"=>",passwd)
	
# filler
print()
