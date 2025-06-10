import ipaddress
from icmplib import multiping
from tabulate import tabulate

def icmp_scan(network_base, subnet_mask):
    try:
        network = ipaddress.ip_network(f"{network_base}/{subnet_mask}", strict=False)
        ip_list = [str(ip) for ip in network.hosts()]  # Get usable hosts

        if not ip_list:
            print(f"No hosts found in subnet {network_base}/{subnet_mask}")
            return []

        ping_results = multiping(ip_list, count=1, timeout=2)
        responses = [[ip, "Active" if host.is_alive else "Inactive"] for ip, host in zip(ip_list, ping_results)]

    except KeyboardInterrupt:
        print("Scan interrupted by user.")
        return []

    except Exception as e:
        print(f"An error occurred: {e}")
        return []

    return responses




def networkscan(ip,subnet_mask):

    try:
        subnet_mask = int(subnet_mask)
        if subnet_mask < 1 or subnet_mask > 32:
            raise ValueError("Subnet mask must be between 1 and 32.")
    except ValueError as e:
        print(f"Invalid subnet mask: {e}")
        exit()


    scan_results = icmp_scan(ip, subnet_mask)


    print(f"\nScan Results for {ip}/{subnet_mask}:")
    return tabulate(scan_results, headers=["IP Address", "Status"], tablefmt="grid")