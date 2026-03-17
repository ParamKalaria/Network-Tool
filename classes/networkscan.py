import ipaddress
import subprocess
import platform
from tabulate import tabulate
from concurrent.futures import ThreadPoolExecutor, as_completed

def _ping(ip):
    system = platform.system()
    if system == "Windows":
        cmd = ["ping", "-n", "1", "-w", "1000", str(ip)]
    else:
        cmd = ["ping", "-c", "1", "-W", "1", str(ip)]
    try:
        result = subprocess.run(cmd, capture_output=True, timeout=3)
        return str(ip), result.returncode == 0
    except Exception:
        return str(ip), False

def networkscan(ip, subnet_mask):
    try:
        subnet_mask = int(subnet_mask)
        if not (1 <= subnet_mask <= 32):
            return "Subnet mask must be between 1 and 32."

        network = ipaddress.ip_network(f"{ip}/{subnet_mask}", strict=False)
        ip_list = [str(host) for host in network.hosts()]
        if not ip_list:
            return f"No usable hosts found in {ip}/{subnet_mask}"

        output = []
        max_workers = min(100, len(ip_list))
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(_ping, addr): addr for addr in ip_list}
            for future in as_completed(futures):
                addr, alive = future.result()
                if alive:
                    output.append([addr, "Active"])

        if not output:
            return "No active hosts found in the subnet."

        output.sort(key=lambda x: list(map(int, x[0].split('.'))))
        return tabulate(output, headers=["IP Address", "Status"], tablefmt="grid")

    except ValueError:
        return "Invalid subnet mask. Please provide a number between 1 and 32."
    except Exception as e:
        return f"Unexpected error: {e}"