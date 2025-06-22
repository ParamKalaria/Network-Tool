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

def clear_output():
    output_text.delete(1.0, tk.END)

def save_output():
    try:
        content = output_text.get(1.0, tk.END).strip()
        if not content:
            messagebox.showinfo("Save Output", "There is no output to save.")
            return
        with open("nettoolkit_output.txt", "w", encoding="utf-8") as f:
            f.write(content)
        messagebox.showinfo("Save Output", "Output saved to 'nettoolkit_output.txt'")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to save output: {e}")

root = tk.Tk()
root.title("Network Tool by Param Kalaria")
root.geometry("1000x600")
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)

# Horizontal splitter
paned = tk.PanedWindow(root, orient=tk.HORIZONTAL, sashrelief=tk.RAISED)
paned.grid(row=0, column=0, sticky="nsew")

# ==== LEFT PANEL ====
left_panel = tk.Frame(paned)
left_panel.grid_rowconfigure(1, weight=1)
left_panel.grid_columnconfigure(0, weight=1)

# Top-left: Input fields
input_frame = tk.Frame(left_panel, padx=10, pady=10)
input_frame.grid(row=0, column=0, sticky="new")

tk.Label(input_frame, text="IP Address:").grid(row=0, column=0, sticky="e", padx=5, pady=2)
ip_entry = tk.Entry(input_frame)
ip_entry.grid(row=0, column=1, sticky="ew", pady=2)

tk.Label(input_frame, text="Port / Range:").grid(row=1, column=0, sticky="e", padx=5, pady=2)
port_entry = tk.Entry(input_frame)
port_entry.grid(row=1, column=1, sticky="ew", pady=2)

tk.Label(input_frame, text="Subnet Mask:").grid(row=2, column=0, sticky="e", padx=5, pady=2)
mask_entry = tk.Entry(input_frame)
mask_entry.grid(row=2, column=1, sticky="ew", pady=2)

input_frame.grid_columnconfigure(1, weight=1)

# Bottom-left: Tool buttons
button_frame = tk.Frame(left_panel, padx=10, pady=10)
button_frame.grid(row=1, column=0, sticky="nsew")
for idx, tool in enumerate(['ipinfo', 'traceroute', 'networkscan', 'arp', 'portscan', 'myip', 'networkint', 'speedtest']):
    tk.Button(
        button_frame,
        text=tool.capitalize(),
        width=20,
        command=lambda t=tool: run_tool(t)
    ).grid(row=idx, column=0, sticky="ew", pady=2)

paned.add(left_panel, minsize=500)

# ==== RIGHT PANEL ====
right_frame = tk.Frame(paned, padx=10, pady=10)
right_frame.grid_rowconfigure(0, weight=1)
right_frame.grid_columnconfigure(0, weight=1)

# Output text area
output_text = scrolledtext.ScrolledText(right_frame, wrap=tk.WORD)
output_text.grid(row=0, column=0, columnspan=2, sticky="nsew", pady=(0, 10))

# Buttons for clear/save
utility_frame = tk.Frame(right_frame)
utility_frame.grid(row=1, column=0, columnspan=2, sticky="e", pady=5)

tk.Button(utility_frame, text="Clear Output", command=clear_output).pack(side=tk.RIGHT, padx=5)
tk.Button(utility_frame, text="Save Output", command=save_output).pack(side=tk.RIGHT)

paned.add(right_frame, minsize=500)

root.mainloop()