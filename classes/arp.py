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
    elif system == "Darwin":  # macOS support
        command = "arp -a"
    else:
        print("Unsupported OS")
        return

    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        output = result.stdout
        arp_entries = re.findall(r'([-.0-9]+)\s+([-0-9a-fA-F:]+)', output)
        if arp_entries:
            print(tabulate(arp_entries, headers=["IP Address", "MAC Address"], tablefmt="grid"))
        else:
            print("No ARP entries found.")
    except Exception as e:
        print(f"Error executing ARP scan: {e}")