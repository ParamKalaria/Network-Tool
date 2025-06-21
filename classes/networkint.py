import psutil
from tabulate import tabulate

def list_network_interfaces():
    try:
        table_data = []
        interfaces = psutil.net_if_addrs()

        for interface, addresses in interfaces.items():
            mac_address = next((addr.address for addr in addresses if addr.family.name == "AF_LINK"), "N/A")

            for addr in addresses:
                if addr.family.name == "AF_LINK":
                    continue

                family = {
                    "AF_INET": "IPv4",
                    "AF_INET6": "IPv6"
                }.get(addr.family.name, "Unknown")

                table_data.append([
                    interface,
                    family,
                    addr.address,
                    addr.netmask or "N/A",
                    mac_address
                ])

        headers = ["Interface", "Type", "Address", "Netmask", "MAC Address"]
        return(tabulate(table_data, headers, tablefmt="grid"))

    except Exception as e:
        return(f"[!] Error fetching network interfaces: {e}")
