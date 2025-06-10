import os
import platform
import subprocess
import re
from tabulate import tabulate

def arp_scan():
    system = platform.system()
    
    if system == "Windows":
        command = "arp -a"
    elif system == "Linux":
        command = "arp -n"
    else:
        return "Unsupported OS"

    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output = result.stdout

    # Extract IP and MAC addresses using regex
    arp_entries = re.findall(r'([-.0-9]+)\s+([-0-9a-fA-F:]+)', output)
    
    return arp_entries

# Fetch ARP table and display in tabulated format
arp_table = arp_scan()
if isinstance(arp_table, list):
    print(tabulate(arp_table, headers=["IP Address", "MAC Address"], tablefmt="grid"))
else:
    print(arp_table)