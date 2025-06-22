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
    elif system == "Darwin":
        command = "arp -a"
    else:
        return("Unsupported OS")

    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = result.stdout
        arp_entries = re.findall(r'([-.0-9]+)\s+([-0-9a-fA-F:]+)', output)
        if arp_entries:
            return (tabulate(arp_entries, headers=["IP Address", "MAC Address"], tablefmt="grid"))
        else:
            return ("No ARP entries found.")
    except Exception as e:
        return (f"Error executing ARP scan: {e}")