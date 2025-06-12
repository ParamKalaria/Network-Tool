import psutil
from tabulate import tabulate

def list_network_interfaces():
    table_data = []
    interfaces = psutil.net_if_addrs()

    for interface, addresses in interfaces.items():
        mac_address = "N/A"  # Default MAC address placeholder

        for addr in addresses:
            family = "Unknown"
            if addr.family.name == "AF_INET":  # IPv4
                family = "IPv4"
            elif addr.family.name == "AF_INET6":  # IPv6
                family = "IPv6"
            elif addr.family.name == "AF_LINK":  # MAC Address
                mac_address = addr.address
                continue  # Skip adding MAC address to IP rows

            table_data.append([
                interface,
                family,
                addr.address,
                addr.netmask if addr.netmask else "N/A",
                mac_address  # MAC Address is displayed separately
            ])

    headers = ["Interface", "Type", "Address", "Netmask", "MAC Address"]
    print(tabulate(table_data, headers, tablefmt="grid"))

