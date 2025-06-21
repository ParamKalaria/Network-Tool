from scapy.all import IP, TCP, sr1
from tabulate import tabulate

def scan_ports(target, port_input):
    try:
        # Determine port list
        if '-' in port_input:
            start, end = map(int, port_input.split('-'))
            ports = range(start, end + 1)
        elif port_input.lower() == 'full':
            ports = range(1, 65536)
        else:
            ports = [int(port_input)]
        
        results = []
        for port in ports:
            try:
                pkt = IP(dst=target)/TCP(dport=port, flags="S")
                resp = sr1(pkt, timeout=0.5, verbose=False)
                if resp and resp.haslayer(TCP) and resp[TCP].flags == 0x12:
                    results.append([port, "Open"])
                else:
                    results.append([port, "Closed/Filtered"])
            except Exception as e:
                results.append([port, f"Error: {e}"])

        return(tabulate(results, headers=["Port", "Status"], tablefmt="grid"))

    except ValueError:
        return("Invalid port input. Use a number, a range (e.g. 20-80), or 'full'.")
    except Exception as e:
        return(f"Unexpected error: {e}")