import os
import sys
from scapy.all import ARP, Ether, srp
from tabulate import tabulate


def check_privileges():
    if os.name == "nt":
        if not os.system("net session >nul 2>&1"):
            return True
    else:
        if os.geteuid() == 0:
            return True
    return False



def arp_scan(target_ip):

    if not check_privileges():
        sys.exit("Error: Please run this script as Administrator (Windows) or root (Linux).")

    target_ip = "10.1.1.1/24"
    arp = ARP(pdst=target_ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")
    packet = ether / arp
    result = srp(packet, timeout=3, verbose=False)[0]
    devices = [["IP Address", "MAC Address"]]
    for sent, received in result:
        devices.append([received.psrc, received.hwsrc])
    return tabulate(devices, headers="firstrow", tablefmt="grid")

arp_scan("10.1.1.1/24")