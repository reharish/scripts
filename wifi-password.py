"""

Wi-Fi Passwords (Linux only)

Author : @reharish
Description : This script lists Wi-Fi SSIDs and their passwords
from Linux.

Note:
    Requires root privileges to access `/etc/NetworkManager/system-connections/`.
    Works only on Linux with NetworkManager-managed connections.
"""

import os
import sys
import configparser

SYS_CONN_PATH = "/etc/NetworkManager/system-connections"

def is_supported_platform() -> bool:
    """Check if the script is running on a supported platform (Linux)."""
    return sys.platform == "linux"

def get_wifi_credentials(path: str) -> list:
    """
    Extract SSID and password from NetworkManager connection files.

    Args:
        path (str): Path to the NetworkManager system-connections directory.

    Returns:
        list: List of tuples in the format (ssid, password).
    """
    credentials = []
    files = os.listdir(path)

    for conf_file in files:
        config_path = os.path.join(path, conf_file)

        config = configparser.ConfigParser()
        try:
            with open(config_path, 'r') as f:
                config.read_file(f)

            if config.get("connection", "type", fallback="") != "wifi":
                continue

            ssid = config.get("wifi", "ssid", fallback="UNKNOWN")
            password = config.get("wifi-security", "psk", fallback="OPEN")

            credentials.append((ssid, password))

        except Exception as e:
            # Skip unreadable or malformed files
            continue

    return credentials

def main():
    if not is_supported_platform():
        print(f"Unsupported platform: {sys.platform}")
        sys.exit(1)

    if not os.path.isdir(SYS_CONN_PATH):
        print(f"Error: NetworkManager system-connections directory not found at: {SYS_CONN_PATH}")
        sys.exit(1)

    try:
        credentials = get_wifi_credentials(SYS_CONN_PATH)

        if not credentials:
            print("No Wi-Fi credentials found.")
            return

        max_len = max(len(ssid) for ssid, _ in credentials)
        print(f"{'SSID'.ljust(max_len)} : PASSWORD")
        print("-" * (max_len + 12))

        for ssid, password in credentials:
            print(f"{ssid.ljust(max_len)} : {password}")

    except Exception as e:
        print(f"[!] Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
