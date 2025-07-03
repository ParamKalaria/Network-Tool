from classes import ipinfo
from classes import traceroute
from classes import networkscan
from classes import arp
from classes import portscanner
from classes import myip
from classes import networkint
from classes import speedtest
from tabulate import tabulate
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
        ip = sys.argv[2] if len(sys.argv) > 2 else None
        if not ip:
            print("No IP address specified. Please provide an IP address as a command line argument.")
            exit()
        print(ipinfo.ipinfo(ip))
        

    




    elif task == 'traceroute':
        
        ip = sys.argv[2] if len(sys.argv) > 2 else None
        if not ip:
            print("No IP address specified. Please provide an IP address as a command line argument.")
            exit()
        print(traceroute.traceroute(ip))
       

    




    elif task == 'networkscan':
       
        ip = sys.argv[2] if len(sys.argv) > 2 else None
        if not ip:
            print("No IP address specified. Please provide an IP address as a command line argument.")
            exit()
        
        subnet_mask = sys.argv[3] if len(sys.argv) > 3 else '24'
        if not sys.argv[3:]:
            print("No subnet mask specified. Defaulting to /24.")
            exit()
        print(networkscan.networkscan(ip, subnet_mask))
        







    elif task == 'arp':
        print(arp.arp_scan())
        




    elif task == 'portscan':       
        ip = sys.argv[2] if len(sys.argv) > 2 else None
        if not ip:
            print("No IP address specified. Please provide an IP address as a command line argument.")
            exit()
        
        port_input = sys.argv[3] if len(sys.argv) > 3 else None
        if not port_input:
            print("No port or port range specified. Please provide a port or port range as a command line argument.")
            exit()
        
        print(portscanner.scan_ports(ip, port_input))
            
        



    
    
    elif task == 'myip':        
        print(myip.get_ip_details())
        





    elif task == 'networkint':       
        print(networkint.list_network_interfaces())
        



    elif task == 'speedtest':       
        print(speedtest.speed_test())
       




    elif task == 'help':        
        help_tasks = [
            ["ipinfo <ip_address>",            "Get information about an IP address"],
            ["traceroute <ip_address>",        "Perform a traceroute to an IP"],
            ["networkscan <ip> [subnet_mask]", "Scan a network (default mask: /24)"],
            ["arp",                            "Perform an ARP scan on the system"],
            ["portscan <ip> <port|range|full>","Scan ports on the given IP"],
            ["myip",                           "Get your public IP and country"],
            ["networkint",                     "List all network interfaces"],
            ["speedtest",                      "Measure internet speed and ping"],
            ["help",                           "Show this help message"]
        ]

        print(tabulate(help_tasks, headers=["Command", "Description"], tablefmt="fancy_grid"))



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

