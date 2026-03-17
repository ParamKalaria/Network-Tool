import queue
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from tabulate import tabulate

from classes import arp, ipinfo, myip, networkint, networkscan, portscanner, speedtest, traceroute


TOOLS = [
    ("IP Info", "ipinfo"),
    ("Traceroute", "traceroute"),
    ("Network Scan", "networkscan"),
    ("ARP Scan", "arp"),
    ("Port Scan", "portscan"),
    ("My IP", "myip"),
    ("Interfaces", "networkint"),
    ("Speed Test", "speedtest"),
    ("Help", "help"),
]

HELP_TASKS = [
    ["ipinfo <ip_address>", "Get information about an IP address"],
    ["traceroute <ip_address>", "Perform a traceroute to an IP"],
    ["networkscan <ip> [subnet_mask]", "Scan a network (default mask: /24)"],
    ["arp", "Perform an ARP scan on the system"],
    ["portscan <ip> <port|range|full>", "Scan ports on the given IP"],
    ["myip", "Get your public IPv4 and IPv6"],
    ["networkint", "List all network interfaces"],
    ["speedtest", "Measure internet speed and ping"],
    ["help", "Show this help message"],
]


class NetworkToolForm:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Tool")
        self.root.geometry("1150x700")
        self.root.minsize(900, 560)

        self._result_queue = queue.Queue()
        self._tool_buttons = []
        self.status_text = tk.StringVar(value="Ready")

        self._configure_style()
        self._build_layout()

    def _configure_style(self):
        style = ttk.Style()
        available = style.theme_names()
        if "vista" in available:
            style.theme_use("vista")
        elif "clam" in available:
            style.theme_use("clam")

        style.configure("Title.TLabel", font=("Segoe UI", 12, "bold"))
        style.configure("Status.TLabel", padding=(10, 5))
        style.configure("Tool.TButton", padding=(8, 6))

    def _build_layout(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        main = ttk.Frame(self.root, padding=10)
        main.grid(row=0, column=0, sticky="nsew")
        main.grid_rowconfigure(1, weight=1)
        main.grid_columnconfigure(1, weight=1)

        ttk.Label(main, text="Network Tool Dashboard", style="Title.TLabel").grid(
            row=0, column=0, columnspan=2, sticky="w", pady=(0, 10)
        )

        left = ttk.Frame(main)
        left.grid(row=1, column=0, sticky="nsew", padx=(0, 10))
        left.grid_columnconfigure(0, weight=1)

        input_group = ttk.LabelFrame(left, text="Inputs", padding=10)
        input_group.grid(row=0, column=0, sticky="ew")
        input_group.grid_columnconfigure(1, weight=1)

        ttk.Label(input_group, text="IP Address").grid(row=0, column=0, sticky="w", pady=4)
        self.ip_entry = ttk.Entry(input_group)
        self.ip_entry.grid(row=0, column=1, sticky="ew", pady=4, padx=(8, 0))

        ttk.Label(input_group, text="Port / Range").grid(row=1, column=0, sticky="w", pady=4)
        self.port_entry = ttk.Entry(input_group)
        self.port_entry.grid(row=1, column=1, sticky="ew", pady=4, padx=(8, 0))

        ttk.Label(input_group, text="Subnet Mask").grid(row=2, column=0, sticky="w", pady=4)
        self.mask_entry = ttk.Entry(input_group)
        self.mask_entry.insert(0, "24")
        self.mask_entry.grid(row=2, column=1, sticky="ew", pady=4, padx=(8, 0))

        tool_group = ttk.LabelFrame(left, text="Tools", padding=10)
        tool_group.grid(row=1, column=0, sticky="nsew", pady=(10, 0))
        tool_group.grid_columnconfigure(0, weight=1)
        tool_group.grid_columnconfigure(1, weight=1)

        for idx, (label, key) in enumerate(TOOLS):
            row = idx // 2
            col = idx % 2
            btn = ttk.Button(
                tool_group,
                text=label,
                style="Tool.TButton",
                command=lambda t=key: self.run_tool(t),
            )
            btn.grid(row=row, column=col, sticky="ew", padx=4, pady=4)
            self._tool_buttons.append(btn)

        right = ttk.LabelFrame(main, text="Output", padding=10)
        right.grid(row=1, column=1, sticky="nsew")
        right.grid_rowconfigure(0, weight=1)
        right.grid_columnconfigure(0, weight=1)

        self.output_text = scrolledtext.ScrolledText(right, wrap=tk.WORD, font=("Consolas", 10))
        self.output_text.grid(row=0, column=0, columnspan=2, sticky="nsew")

        ttk.Button(right, text="Clear", command=self.clear_output).grid(row=1, column=0, sticky="w", pady=(8, 0))
        ttk.Button(right, text="Save", command=self.save_output).grid(row=1, column=1, sticky="e", pady=(8, 0))

        status = ttk.Label(self.root, textvariable=self.status_text, style="Status.TLabel", relief=tk.SUNKEN, anchor="w")
        status.grid(row=1, column=0, sticky="ew")

    def _set_buttons_state(self, state):
        for btn in self._tool_buttons:
            btn.config(state=state)

    def _poll_result(self):
        try:
            result = self._result_queue.get_nowait()
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, result)
            self._set_buttons_state(tk.NORMAL)
            self.status_text.set("Ready")
        except queue.Empty:
            self.root.after(100, self._poll_result)

    def run_tool(self, tool):
        ip = self.ip_entry.get().strip()
        port = self.port_entry.get().strip()
        mask = self.mask_entry.get().strip()

        if tool == "help":
            result = tabulate(HELP_TASKS, headers=["Command", "Description"], tablefmt="fancy_grid")
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, result)
            self.status_text.set("Help loaded")
            return

        def task():
            try:
                if tool == "ipinfo":
                    result = ipinfo.ipinfo(ip) if ip else "Please enter an IP address."
                elif tool == "traceroute":
                    result = traceroute.traceroute(ip) if ip else "Please enter an IP address."
                elif tool == "networkscan":
                    result = networkscan.networkscan(ip, mask or "24") if ip else "Please enter an IP address."
                elif tool == "arp":
                    result = arp.arp_scan()
                elif tool == "portscan":
                    result = portscanner.scan_ports(ip, port) if ip and port else "Please enter IP and port."
                elif tool == "myip":
                    result = myip.get_ip_details()
                elif tool == "networkint":
                    result = networkint.list_network_interfaces()
                elif tool == "speedtest":
                    result = speedtest.speed_test()
                else:
                    result = "Unknown tool."
                self._result_queue.put(result if result is not None else "Task completed successfully.")
            except Exception as e:
                self._result_queue.put(f"Error running {tool}: {e}")

        self._set_buttons_state(tk.DISABLED)
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, f"Running {tool}...\n")
        self.status_text.set(f"Running {tool}...")
        threading.Thread(target=task, daemon=True).start()
        self.root.after(100, self._poll_result)

    def clear_output(self):
        self.output_text.delete(1.0, tk.END)
        self.status_text.set("Output cleared")

    def save_output(self):
        try:
            content = self.output_text.get(1.0, tk.END).strip()
            if not content:
                messagebox.showinfo("Save Output", "There is no output to save.")
                return

            target = filedialog.asksaveasfilename(
                title="Save Output",
                defaultextension=".txt",
                filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
                initialfile="nettoolkit_output.txt",
            )
            if not target:
                return

            with open(target, "w", encoding="utf-8") as file:
                file.write(content)
            self.status_text.set("Output saved")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save output: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkToolForm(root)
    root.mainloop()