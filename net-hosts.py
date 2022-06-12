#!/usr/bin/env python3
"""
Script : Net-Host
Description : Finding available host belong to your local network like net-discover
"""

import sys, subprocess
import netifaces as nic
import ipaddress

if len(sys.argv) == 1:
    print ("Enter the interface")
    sys.exit(1)

INTERFACE = sys.argv[1]
INF_DETAILS  = nic.ifaddresses(INTERFACE)[nic.AF_INET][0]
IP_ADDRESS = INF_DETAILS["addr"]
NETMASK = INF_DETAILS["netmask"]
CIDR_NOTATION = "{}/{}".format(IP_ADDRESS, NETMASK)

# print(CIDR_NOTATION)            # Debug

def get_local_ip_address(cidr_notation) -> tuple:
    pass

def send_ping_to_host(ipaddr) -> bool:
    """Return true if the hosts is up"""
    output = subprocess.call(['ping', '-c', "2", ipaddr],
                             stdout=subprocess.PIPE)
    alive_hosts(ipaddr) if not output
    

def ping_sweep():
    pass

if __name__ == "__main__":
    print(IP_ADDRESS)
    sys.exit(0)
