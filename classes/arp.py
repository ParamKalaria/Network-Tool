import os
import platform
import subprocess
import re
from tabulate import tabulate

def scan():
    system = platform.system()
    
    if system == "Windows":
        command = "arp -a"
    elif system == "Linux":
        command = "arp -n"
    else:
        return "Unsupported OS"

    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output = result.stdout
    arp_entries = re.findall(r'([-.0-9]+)\s+([-0-9a-fA-F:]+)', output)    
    return arp_entries



def arp_scan():
    arp_table = scan()
    if isinstance(arp_table, list):
        print(tabulate(arp_table, headers=["IP Address", "MAC Address"], tablefmt="grid"))
    else:
        print(arp_table)