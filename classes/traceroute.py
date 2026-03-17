import subprocess
import platform
import re
from tabulate import tabulate

def traceroute(destination, max_hops=30):
    system = platform.system()
    if system == "Windows":
        cmd = ["tracert", "-h", str(max_hops), "-d", destination]
    else:
        cmd = ["traceroute", "-m", str(max_hops), "-n", destination]

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        lines = result.stdout.splitlines()

        results = []
        for line in lines:
            match = re.match(r'\s*(\d+)\s+(.+)', line)
            if not match:
                continue
            hop = match.group(1)
            rest = match.group(2).strip()
            ip_match = re.search(r'(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})', rest)
            ip = ip_match.group(1) if ip_match else "*"
            rtt_match = re.search(r'(\d+)\s+ms|<(\d+)\s+ms', rest)
            if rtt_match:
                rtt = f"{rtt_match.group(1) or rtt_match.group(2)} ms"
            else:
                rtt = "*"
            results.append([hop, ip, rtt])

        if not results:
            return "No traceroute results found."
        return tabulate(results, headers=["Hop", "IP Address", "RTT"], tablefmt="grid")

    except subprocess.TimeoutExpired:
        return "Traceroute timed out."
    except FileNotFoundError:
        return "Traceroute command not found on this system."
    except Exception as e:
        return f"Traceroute failed: {e}"