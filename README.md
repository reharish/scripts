# HackyScripts

## wifi-password.py

A simple python script which gives wifi names and passwords as a result.

``` sh
python3 wifi-password.py

```

## host-finder.py

Scans a given CIDR range or a network interface to find active hosts on the network
by performing a ping sweep. Supports threaded execution and quiet output for file redirection.

``` bash
    python3 host-finder.py --cidr 192.168.1.0/24
    python3 host-finder.py --interface tun0 --quiet > live_hosts.txt
```
