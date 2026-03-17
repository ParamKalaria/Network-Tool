import socket
from tabulate import tabulate
from concurrent.futures import ThreadPoolExecutor, as_completed

_COMMON_SERVICES = {
    21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 143: "IMAP",
    443: "HTTPS", 445: "SMB", 3306: "MySQL", 3389: "RDP",
    5432: "PostgreSQL", 5900: "VNC", 6379: "Redis",
    8080: "HTTP-Alt", 8443: "HTTPS-Alt", 27017: "MongoDB"
}

def _check_port(target, port):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            if s.connect_ex((target, port)) == 0:
                return [port, "Open", _COMMON_SERVICES.get(port, "Unknown")]
    except Exception:
        pass
    return None

def scan_ports(target, port_input):
    try:
        if '-' in port_input:
            start, end = map(int, port_input.split('-'))
            ports = list(range(start, end + 1))
        elif port_input.lower() == 'full':
            ports = list(range(1, 65536))
        else:
            ports = [int(port_input)]

        results = []
        max_workers = min(500, len(ports))
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {executor.submit(_check_port, target, p): p for p in ports}
            for future in as_completed(futures):
                result = future.result()
                if result:
                    results.append(result)

        results.sort(key=lambda x: x[0])

        if not results:
            return "No open ports found."
        return tabulate(results, headers=["Port", "Status", "Service"], tablefmt="grid")

    except ValueError:
        return "Invalid port input. Use a number, a range (e.g. 20-80), or 'full'."
    except Exception as e:
        return f"Unexpected error: {e}"