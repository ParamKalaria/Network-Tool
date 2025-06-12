import psutil
from tabulate import tabulate

def list_network_interfaces():
    table_data = []
    interfaces = psutil.net_if_addrs()

    for interface, addresses in interfaces.items():
        mac_address = "N/A"  # Default MAC address placeholder

        for addr in addresses:
            if addr.family.name == "AF_LINK":  # MAC Address
                mac_address = addr.address
            else:  # IP Addresses (IPv4 or IPv6)
                table_data.append([
                    interface,
                    addr.family.name,
                    addr.address,
                    addr.netmask if addr.netmask else "N/A",
                    mac_address  # MAC Address is displayed separately
                ])

    headers = ["Interface", "Family", "Address", "Netmask", "MAC Address"]
    return tabulate(table_data, headers, tablefmt="grid")

