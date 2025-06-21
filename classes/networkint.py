import ipaddress
from icmplib import multiping
from tabulate import tabulate

def networkscan(ip, subnet_mask):
    try:
        # Validate subnet mask
        try:
            subnet_mask = int(subnet_mask)
            if not (1 <= subnet_mask <= 32):
                raise ValueError
        except ValueError:
            print("Invalid subnet mask. Please provide a number between 1 and 32.")
            return

        # Calculate network and hosts
        try:
            network = ipaddress.ip_network(f"{ip}/{subnet_mask}", strict=False)
            ip_list = [str(host) for host in network.hosts()]
            if not ip_list:
                print(f"No usable hosts found in {ip}/{subnet_mask}")
                return
        except Exception as e:
            print(f"Network parsing error: {e}")
            return

        # Perform ping scan
        try:
            results = multiping(ip_list, count=1, timeout=2)
            output = [[ip_addr, "Active" if resp.is_alive else "Inactive"]
                      for ip_addr, resp in zip(ip_list, results)]
        except Exception as e:
            print(f"ICMP scan failed: {e}")
            return

        # Display results
        try:
            print(tabulate(output, headers=["IP Address", "Status"], tablefmt="grid"))
        except Exception as e:
            print(f"Error formatting output: {e}")

    except KeyboardInterrupt:
        print("\nScan interrupted by user.")