import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from classes import ipinfo, traceroute, networkscan, arp, portscanner, myip, networkint, speedtest

def run_tool(tool):
    try:
        output_text.delete(1.0, tk.END)
        ip = ip_entry.get()
        port = port_entry.get()
        mask = mask_entry.get()

        if tool == 'ipinfo':
            result = ipinfo.ipinfo(ip) if ip else "Please enter an IP address."
        elif tool == 'traceroute':
            result = traceroute.traceroute(ip) if ip else "Please enter an IP address."
        elif tool == 'networkscan':
            result = networkscan.networkscan(ip, mask or '24') if ip else "Please enter an IP address."
        elif tool == 'arp':
            result = arp.arp_scan()
        elif tool == 'portscan':
            result = portscanner.scan_ports(ip, port) if ip and port else "Please enter IP and port."
        elif tool == 'myip':
            result = myip.get_ip_details()
        elif tool == 'networkint':
            result = networkint.list_network_interfaces()
        elif tool == 'speedtest':
            result = speedtest.speed_test()
        else:
            result = "Unknown tool."

        if result is None:
            result = "[✓] Task completed successfully."
        output_text.insert(tk.END, result)

    except Exception as e:
        output_text.insert(tk.END, f"[!] Error running {tool}: {e}")

root = tk.Tk()
root.title("NetToolkit Dashboard")
root.geometry("900x600")
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

paned = tk.PanedWindow(root, sashrelief=tk.RAISED)
paned.pack(fill=tk.BOTH, expand=1)

# LEFT PANEL: Tool Selection
left_frame = tk.Frame(paned, padx=10, pady=10)
left_frame.grid_rowconfigure(0, weight=1)
left_frame.grid_columnconfigure(0, weight=1)

tools = ['ipinfo', 'traceroute', 'networkscan', 'arp', 'portscan', 'myip', 'networkint', 'speedtest']
for idx, tool in enumerate(tools):
    b = tk.Button(left_frame, text=tool.capitalize(), width=18, command=lambda t=tool: run_tool(t))
    b.grid(row=idx, column=0, sticky="ew", pady=2)

paned.add(left_frame)

# RIGHT PANEL: Inputs + Output
right_frame = tk.Frame(paned, padx=10, pady=10)
right_frame.grid_rowconfigure(3, weight=1)
right_frame.grid_columnconfigure(1, weight=1)

tk.Label(right_frame, text="IP Address:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
ip_entry = tk.Entry(right_frame)
ip_entry.grid(row=0, column=1, sticky="ew", pady=5)

tk.Label(right_frame, text="Port / Range:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
port_entry = tk.Entry(right_frame)
port_entry.grid(row=1, column=1, sticky="ew", pady=5)

tk.Label(right_frame, text="Subnet Mask:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
mask_entry = tk.Entry(right_frame)
mask_entry.grid(row=2, column=1, sticky="ew", pady=5)

output_text = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD)
output_text.grid(row=3, column=0, columnspan=2, sticky="nsew", pady=10)

paned.add(right_frame)

root.mainloop()