"""
Script : Host Finder
Description : Finding available hosts belonging to your local network.
"""

import sys
import time
import ipaddress
import threading
import subprocess
import argparse
import netifaces as nic


class HostFinder:
    def __init__(self, threads: int = 100, quiet: bool = False):
        self.hosts = []
        self.alive = []
        self.quiet = quiet
        self.nthreads = threads

    def print(self, msg:str):
        if not self.quiet:
            print(msg)

    def get_ips(self, cidr) -> list:
        """Return all usable IPs in a CIDR range"""
        self.print(f">> Scanning network: {cidr}")
        network = ipaddress.IPv4Interface(cidr).network
        self.hosts = [str(ip) for ip in ipaddress.IPv4Network(network).hosts()]
        return self.hosts

    def send_ping_to_host(self, ipaddr: str):
        """Ping host and add to live_hosts if reachable"""
        param = '-n' if sys.platform == 'win32' else '-c'
        command = ['ping', param, '1', ipaddr]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if result.returncode == 0:
            self.print(f"[+] {ipaddr}")
            if self.quiet:
                print(ipaddr)
            self.alive.append(ipaddr)

    def ping_sweep(self, hosts: list) -> list:
        """Perform ping sweep with threading"""
        threads = []
        for ip in hosts:
            thread = threading.Thread(target=self.send_ping_to_host, args=(ip,))
            threads.append(thread)
            while threading.active_count() > self.nthreads:
                time.sleep(0.1)
            thread.start()

        for thread in threads:
            thread.join()

        return self.alive


    def get_interface_cidr(self, interface: str) -> str:
        """Get CIDR notation from network interface"""
        try:
            iface_data = nic.ifaddresses(interface)[nic.AF_INET][0]
            ip_addr = iface_data['addr']
            netmask = iface_data['netmask']
            cidr = f"{ip_addr}/{ipaddress.IPv4Network(f'0.0.0.0/{netmask}').prefixlen}"
            return cidr
        except (ValueError, KeyError):
            raise ValueError(f"Interface '{interface}' not found or doesn't have an IPv4 address.")


def parse_arguments():
    parser = argparse.ArgumentParser(description="Find active hosts in your local network.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--cidr', '-c', type=str, help='CIDR notation (e.g. 192.168.1.0/24)')
    group.add_argument('--interface', '-i', type=str, help='Network interface (e.g. eth0, tun0)')
    parser.add_argument('--quiet', '-q', action='store_true', help='Suppress console output (for redirection to file)')
    parser.add_argument('--threads', '-t', type=int, default=100, help='Number of concurrent threads (default: 100)')
    return parser.parse_args()


def main():
    finder = HostFinder()
    args = parse_arguments()
    if args.quiet:
        finder.quiet = True
    if args.cidr:
        cidr = args.cidr
    else:
        cidr = finder.get_interface_cidr(args.interface)
    try:
        finder.nthreads = args.threads
        hosts = finder.get_ips(cidr)
        live_hosts = finder.ping_sweep(hosts)
        finder.print(f"\n>> Active hosts - {len(live_hosts)}")
    except Exception as e:
        print(f"[!] Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
