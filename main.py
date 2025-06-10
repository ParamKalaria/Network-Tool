from classes import ipinfo
from classes import traceroute
from classes import networkscan
from classes import arp

import sys

global task, ip
task = None

def task_select():
    task= sys.argv[1] if len(sys.argv) > 1 else None
    
   
   
   
    if not task:
        print("No task specified. Please provide a task as a command line argument.")
        exit(1)

    
    if task == 'help':
        print("Usage: python main.py <task> <ip_address>")
        exit(1)






    elif task == 'ipinfo':
        try:
            if not ip:
                print("No IP address specified. Please provide an IP address as a command line argument.")
                exit(1)
            ip = sys.argv[2] if len(sys.argv) > 2 else None
            result = ipinfo.ipinfo(ip)
            print(result)
        except Exception as e:
            print(f"An error occurred: {e}")
        return
    




    elif task == 'traceroute':
        try:
            if not ip:
                print("No IP address specified. Please provide an IP address as a command line argument.")
                exit(1)
            ip = sys.argv[2] if len(sys.argv) > 2 else None
            result = traceroute.traceroute(ip)
            print(result)
        except Exception as e:
            print(f"An error occurred: {e}")
        return
    




    elif task == 'networkscan':
        try:
            if not ip:
                print("No IP address specified. Please provide an IP address as a command line argument.")
                exit(1)
            ip = sys.argv[2] if len(sys.argv) > 2 else None
            
            if not sys.argv[3:]:
                print("No subnet mask specified. Defaulting to /24.")
                exit(1)
            subnet_mask = sys.argv[3] if len(sys.argv) > 3 else '24'
            result = networkscan.networkscan(ip, subnet_mask)
            print(result)
        except Exception as e:
            print(f"An error occurred: {e}")
        return






    elif task == 'arp':
        try:
            if not ip:
                print("No IP address specified. Please provide an IP address as a command line argument.")
                exit(1)
            ip = sys.argv[2] if len(sys.argv) > 2 else None
            
            result = arp.arp_scan(ip)
            print("ARP scan results:")
            for host in result:
                print(host)
        except Exception as e:
            print(f"An error occurred: {e}")
        return


    elif task == 'help':
        print("Available tasks:")
        print("  ipinfo <ip_address> - Get information about an IP address")
        print("  traceroute <ip_address> - Perform a traceroute to an IP address")
        print("  networkscan <ip_address> [subnet_mask] - Scan a network for active hosts (default subnet mask is /24)")
        print("  arp <ip_address> - Perform an ARP scan on the specified IP address")
        print("  help - Show this help message")
        return




    else:
        print(f"Unknown task: {task}. Please provide a valid task.")
    exit(1)
    


def main():
    
    task_select()



if __name__ == "__main__":
    main()
