#!/usr/bin/env python3
"""
Script : Net-Host
Description : Finding available host belong to your local network like net-discover
"""

import sys
import subprocess
import threading

from time import sleep

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

def get_all_ip_address(cidr_notation) -> tuple:
    """"""
    network_addr = ipaddress.IPv4Interface(cidr_notation).network
    all_hosts = [str(ip) for ip in ipaddress.IPv4Network(network_addr)]
    return all_hosts

def send_ping_to_host(ipaddr) -> bool:
    """Return true if the hosts is up"""
    output = subprocess.call(['ping', '-c', "1", ipaddr]
                             ,stdout=subprocess.PIPE)
    if not output:
        print("{} : alive".format(ipaddr))
    else:
        print("{} : 404".format(ipaddr))
        
def ping_sweep(hosts, thread):
    hosts.remove(hosts[0])
    hosts.remove(hosts[len(hosts)-1])
    for host in hosts:
        ping = threading.Thread(target=send_ping_to_host, args=(host,))
        while threading.active_count() >=thread:
            sleep(2)
        ping.start()
    
            
if __name__ == "__main__":
    
    print("IP ADDRESS {}".format(IP_ADDRESS))
    no_of_threads = 100
    alive_hosts = []
    all_hosts = get_all_ip_address(CIDR_NOTATION)
    ping_sweep(all_hosts, no_of_threads)
#    print(alive_hosts)
    sys.exit(0)
