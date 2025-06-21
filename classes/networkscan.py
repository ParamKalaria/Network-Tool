import ipaddress
from icmplib import multiping
from tabulate import tabulate

def networkscan(ip, subnet_mask):
    try:
        subnet_mask = int(subnet_mask)
        if not (1 <= subnet_mask <= 32):
            print("Subnet mask must be between 1 and 32.")
            return

        network = ipaddress.ip_network(f"{ip}/{subnet_mask}", strict=False)
        ip_list = [str(host) for host in network.hosts()]
        if not ip_list:
            print(f"No usable hosts found in {ip}/{subnet_mask}")
            return

        results = multiping(ip_list, count=1, timeout=2)
        output = [[ip_addr, "Active" if resp.is_alive else "Inactive"]
                  for ip_addr, resp in zip(ip_list, results)]
        
        print(tabulate(output, headers=["IP Address", "Status"], tablefmt="grid"))

    except ValueError:
        print("Invalid subnet mask. Please provide a number between 1 and 32.")
    except Exception as e:
        print(f"Unexpected error: {e}")