"""
Script: host-finder

Author: reharish
Description:
    Scans a given CIDR range or a network interface to find active hosts on the network
    by performing a ping sweep. Supports threaded execution and quiet output for file redirection.

Usage Examples:
    python3 host-finder.py --cidr 192.168.1.0/24
    python3 host-finder.py --interface tun0 --quiet > live_hosts.txt

"""

import sys
import time
import ipaddress
import threading
import subprocess
import argparse
import netifaces as nic


class HostFinder:
    """
    A class to discover live hosts on a local or routed network using ping sweep.

    Attributes:
        threads (int): Number of concurrent threads to use.
        quiet (bool): Flag to suppress console output.
    """

    def __init__(self, threads: int = 100, quiet: bool = False):
        self.hosts = []
        self.alive = []
        self.quiet = quiet
        self.nthreads = threads

    def print(self, msg: str):
        """
        Conditionally print messages based on the quiet flag.

        Args:
            msg (str): The message to print.
        """
        if not self.quiet:
            print(msg)

    def get_ips(self, cidr: str) -> list:
        """
        Generate all usable IP addresses in a given CIDR block.

        Args:
            cidr (str): CIDR notation string (e.g., "192.168.1.0/24").

        Returns:
            list: List of usable IPv4 addresses as strings.
        """
        self.print(f">> Scanning network: {cidr}")
        network = ipaddress.IPv4Interface(cidr).network
        self.hosts = [str(ip) for ip in ipaddress.IPv4Network(network).hosts()]
        return self.hosts

    def send_ping_to_host(self, ipaddr: str):
        """
        Ping a host and record it if reachable.

        Args:
            ipaddr (str): IP address to ping.
        """
        param = '-n' if sys.platform == 'win32' else '-c'
        command = ['ping', param, '1', ipaddr]
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode == 0:
            self.print(f"[+] {ipaddr}")
            if self.quiet:
                print(ipaddr)
            self.alive.append(ipaddr)

    def ping_sweep(self, hosts: list) -> list:
        """
        Perform a multithreaded ping sweep across a list of IPs.

        Args:
            hosts (list): List of IP addresses to scan.

        Returns:
            list: List of alive IP addresses.
        """
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
        """
        Retrieve CIDR notation for a given network interface.

        Args:
            interface (str): Name of the network interface (e.g., "eth0", "tun0").

        Returns:
            str: CIDR notation string (e.g., "192.168.1.10/24").

        Raises:
            ValueError: If the interface is not found or has no IPv4 address.
        """
        try:
            iface_data = nic.ifaddresses(interface)[nic.AF_INET][0]
            ip_addr = iface_data['addr']
            netmask = iface_data['netmask']
            cidr = f"{ip_addr}/{ipaddress.IPv4Network(f'0.0.0.0/{netmask}').prefixlen}"
            return cidr
        except (ValueError, KeyError):
            raise ValueError(f"Interface '{interface}' not found or doesn't have an IPv4 address.")


def parse_arguments():
    """
    Parse and return command-line arguments.

    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Find active hosts in your local network.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--cidr', '-c', type=str, help='CIDR notation (e.g. 192.168.1.0/24)')
    group.add_argument('--interface', '-i', type=str, help='Network interface (e.g. eth0, tun0)')
    parser.add_argument('--quiet', '-q', action='store_true', help='Suppress console output (for redirection to file)')
    parser.add_argument('--threads', '-t', type=int, default=100, help='Number of concurrent threads (default: 100)')
    return parser.parse_args()


def main():
    """
    Main execution function: parses arguments, resolves IP list, performs scan, and displays results.
    """
    finder = HostFinder()
    args = parse_arguments()

    finder.quiet = args.quiet
    finder.nthreads = args.threads

    try:
        cidr = args.cidr if args.cidr else finder.get_interface_cidr(args.interface)
        hosts = finder.get_ips(cidr)
        live_hosts = finder.ping_sweep(hosts)
        finder.print(f"\n>> Active hosts - {len(live_hosts)}")
    except Exception as e:
        print(f"[!] Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
