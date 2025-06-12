from scapy.all import IP, TCP, sr1
from tabulate import tabulate

def scan_ports(target, port_input):
    if '-' in port_input:
        start, end = map(int, port_input.split('-'))
        ports = range(start, end + 1)
    elif port_input.lower() == 'full':
        ports = range(1, 65536)
    else:
        ports = [int(port_input)]

    results = []
    for port in ports:
        pkt = IP(dst=target)/TCP(dport=port, flags="S")
        resp = sr1(pkt, timeout=0.5, verbose=False)
        if resp and resp.haslayer(TCP) and resp[TCP].flags == 0x12:
            results.append([port, "Open"])
        else:
            results.append([port, "Closed/Filtered"])

    return tabulate(results, headers=["Port", "Status"], tablefmt="grid")
