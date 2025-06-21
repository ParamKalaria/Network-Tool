from scapy.all import IP, ICMP, sr1
from tabulate import tabulate
import time

def traceroute(destination, max_hops=30):
    try:
        results = []

        for ttl in range(1, max_hops + 1):
            try:
                packet = IP(dst=destination, ttl=ttl) / ICMP()
                start_time = time.time()
                reply = sr1(packet, timeout=1, verbose=False)
                end_time = time.time()

                if reply is None:
                    results.append([ttl, "*", "-"])
                else:
                    rtt = round((end_time - start_time) * 1000, 2)
                    results.append([ttl, reply.src, f"{rtt} ms"])
                    if reply.src == destination:
                        break
            except Exception as hop_error:
                results.append([ttl, "Error", str(hop_error)])

        return(tabulate(results, headers=["Hop", "IP Address", "RTT"], tablefmt="grid"))
    except Exception as e:
        return(f"Traceroute failed: {e}")