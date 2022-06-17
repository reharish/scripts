#!/usr/bin/python3

# Author : @reharish
# Credits : ubuntu,@davidbombal and opensource projects
# Description : Script used to collect passwords from Linux system,
#	        which gives wifi names and passwords as a result.

import os, sys
import subprocess
# import re
import configparser

if sys.platform != "linux":
    print("unsupported platform : {}".format(sys.platform))
    sys.exit(1)

SYS_CONN = "/etc/NetworkManager/system-connections"
	
if __name__ == "__main__":

	try:
		
		all_connections = os.listdir(SYS_CONN)
		max_len = len(max(all_connections))-10
		print("## {} : PASSWORD \n".format("SSID".ljust(max_len)))
#		print(max_len)
		for conf_file in all_connections:
			config = configparser.ConfigParser()
			with open(os.path.join(SYS_CONN, conf_file), 'rt') as fp:
				config.read_file(fp)

			if config["connection"]["type"] == "wifi":
				ssid = config["wifi"]["ssid"]
				if config.has_option("wifi-security", "psk"):
					passwd = config["wifi-security"]["psk"]
				else:
					passwd = "OPEN"
				print("+  {} : {}".format(ssid.ljust(max_len), passwd))
	
	except Exception as e:
		print("ERR : {}".format(e))
		
sys.exit(0)
