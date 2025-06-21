from classes import ipinfo
from classes import traceroute
from classes import networkscan
from classes import arp
from classes import portscanner
from classes import myip
from classes import networkint
from classes import speedtest

import sys


def task_select():
    global task, ip
    task = None
    ip = None



    task= sys.argv[1] if len(sys.argv) > 1 else None
    if not task:
        print("No task specified. Please provide a task as a command line argument.")
        exit()
    
    
   
   
   


    if task == 'ipinfo':
        try:
            ip = sys.argv[2] if len(sys.argv) > 2 else None
            if not ip:
                print("No IP address specified. Please provide an IP address as a command line argument.")
                exit()
            

            ipinfo.ipinfo(ip)
        except Exception as e:
            print(f"An error occurred: {e}")

    




    elif task == 'traceroute':
        try:
            ip = sys.argv[2] if len(sys.argv) > 2 else None
            if not ip:
                print("No IP address specified. Please provide an IP address as a command line argument.")
                exit()
            
            traceroute.traceroute(ip)
        except Exception as e:
            print(f"An error occurred: {e}")

    




    elif task == 'networkscan':
        try:
            ip = sys.argv[2] if len(sys.argv) > 2 else None
            if not ip:
                print("No IP address specified. Please provide an IP address as a command line argument.")
                exit()
            
            subnet_mask = sys.argv[3] if len(sys.argv) > 3 else '24'
            if not sys.argv[3:]:
                print("No subnet mask specified. Defaulting to /24.")
                exit()
            
            networkscan.networkscan(ip, subnet_mask)
        except Exception as e:
            print(f"An error occurred: {e}")







    elif task == 'arp':
        try:
            arp.arp_scan()
        except Exception as e:
            print(f"An error occurred: {e}")




    elif task == 'portscan':
        try:
            ip = sys.argv[2] if len(sys.argv) > 2 else None
            if not ip:
                print("No IP address specified. Please provide an IP address as a command line argument.")
                exit()
            
            port_input = sys.argv[3] if len(sys.argv) > 3 else None
            if not port_input:
                print("No port or port range specified. Please provide a port or port range as a command line argument.")
                exit()
            
            portscanner.scan_ports(ip, port_input)
            
        except Exception as e:
            print(f"An error occurred: {e}")



    
    
    elif task == 'myip':
        try:
            myip.get_ip_details()            
        except Exception as e:
            print(f"An error occurred: {e}")





    elif task == 'networkint':
        try:
            networkint.list_network_interfaces()
        except Exception as e:
            print(f"An error occurred: {e}")



    elif task == 'speedtest':
        try:
            speedtest.speed_test()
        except Exception as e:
            print(f"An error occurred: {e}")




    elif task == 'help':
        print("Available tasks:")
        print("  ipinfo <ip_address> - Get information about an IP address")
        print("  traceroute <ip_address> - Perform a traceroute to an IP address")
        print("  networkscan <ip_address> [subnet_mask] - Scan a network for active hosts (default subnet mask is /24)")
        print("  arp - Perform an ARP scan on the System")
        print("  portscan <ip_address> <port|port_range> - Scan ports on the specified IP address (e.g., 80, 1-100, full)")
        print("  myip - Get your public IP address and country information")
        print("  networkint - List all network interfaces and their details")
        print("  speedtest - Perform a speed test to check download and upload speeds")
        print("  help - Show this help message")



    else:
        print(f"Unknown task: {task}. Please provide a valid task.")
    
    
    exit()
    

if __name__ == "__main__":
    try:
        task_select()
    except KeyboardInterrupt:
        print("\nProcess interrupted by user.")
        exit()
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        exit()

