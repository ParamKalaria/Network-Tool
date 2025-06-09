from classes import ipinfo

import sys

global task, ip
task = None



def cli_arg_check():
    task= sys.argv[1] if len(sys.argv) > 1 else None
    ip = sys.argv[2] if len(sys.argv) > 2 else None
    if not task:
        print("No task specified. Please provide a task as a command line argument.")
        return
    if not ip:
        print("No IP address specified. Please provide an IP address as a command line argument.")
        return
    if len(sys.argv) > 3:
        print("Too many arguments provided. Please provide only the task and the IP address.")
        return
    if len(sys.argv) < 2:
        print("Usage: python main.py <task> <ip_address>")
        return





def task_select():   
    if task:
        if task == 'ipinfo':
            try:
                result = ipinfo.ipinfo(ip)
                print(result)
            except Exception as e:
                print(f"An error occurred: {e}")
            return
        else:
            print(f"Unknown task: {task}. Please provide a valid task.")
    else:            
        print("No task specified. Please provide a task as a command line argument.")
        return

def main():
    
    task_select()



if __name__ == "__main__":
    main()
