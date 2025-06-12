from classes import ipinfo
from classes import traceroute
from classes import networkscan
from classes import arp
from classes import portscanner

import sys


def task_select():
    global task, ip
    task = None
    ip = None



    task= sys.argv[1] if len(sys.argv) > 1 else None
    if not task:
        print("No task specified. Please provide a task as a command line argument.")
        exit(1)
    
    
   
   
   


    if task == 'ipinfo':
        try:
            ip = sys.argv[2] if len(sys.argv) > 2 else None
            if not ip:
                print("No IP address specified. Please provide an IP address as a command line argument.")
                exit(1)
            

            result = ipinfo.ipinfo(ip)
            print(result)
        except Exception as e:
            print(f"An error occurred: {e}")

    




    elif task == 'traceroute':
        try:
            ip = sys.argv[2] if len(sys.argv) > 2 else None
            if not ip:
                print("No IP address specified. Please provide an IP address as a command line argument.")
                exit(1)
            
            result = traceroute.traceroute(ip)
            print(result)
        except Exception as e:
            print(f"An error occurred: {e}")

    




    elif task == 'networkscan':
        try:
            ip = sys.argv[2] if len(sys.argv) > 2 else None
            if not ip:
                print("No IP address specified. Please provide an IP address as a command line argument.")
                exit(1)
            
            subnet_mask = sys.argv[3] if len(sys.argv) > 3 else '24'
            if not sys.argv[3:]:
                print("No subnet mask specified. Defaulting to /24.")
                exit(1)
            
            result = networkscan.networkscan(ip, subnet_mask)
            print(result)
        except Exception as e:
            print(f"An error occurred: {e}")







    elif task == 'arp':
        try:
            ip = sys.argv[2] if len(sys.argv) > 2 else None
            if not ip:
                print("No IP address specified. Please provide an IP address as a command line argument.")
                exit(1)
            
            
            result = arp.arp_scan(ip)
            print("ARP scan results:")
            for host in result:
                print(host)
        except Exception as e:
            print(f"An error occurred: {e}")




    elif task == 'portscan':
        try:
            ip = sys.argv[2] if len(sys.argv) > 2 else None
            if not ip:
                print("No IP address specified. Please provide an IP address as a command line argument.")
                exit(1)
            
            port_input = sys.argv[3] if len(sys.argv) > 3 else None
            if not port_input:
                print("No port or port range specified. Please provide a port or port range as a command line argument.")
                exit(1)
            
            result = portscanner.scan_ports(ip, port_input)
            print(result)
        except Exception as e:
            print(f"An error occurred: {e}")





    elif task == 'help':
        print("Available tasks:")
        print("  ipinfo <ip_address> - Get information about an IP address")
        print("  traceroute <ip_address> - Perform a traceroute to an IP address")
        print("  networkscan <ip_address> [subnet_mask] - Scan a network for active hosts (default subnet mask is /24)")
        print("  arp <ip_address> - Perform an ARP scan on the specified IP address")
        print("  portscan <ip_address> <port|port_range> - Scan ports on the specified IP address (e.g., 80, 1-100, full)")
        print("  help - Show this help message")





    else:
        print(f"Unknown task: {task}. Please provide a valid task.")
    exit(1)
    


def main():
    
    task_select()



if __name__ == "__main__":
    main()
