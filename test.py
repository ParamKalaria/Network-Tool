import tkinter as tk
from tkinter import messagebox
from pystray import Icon, Menu, MenuItem
from PIL import Image, ImageDraw
import threading

# ======== Import Your Modules =========
from classes import ipinfo, traceroute, networkscan, arp, portscanner, myip, networkint, speedtest

# ======== Define Services =========
services = {
    "ipinfo": {"func": ipinfo.ipinfo, "args": ["IP"]},
    "traceroute": {"func": traceroute.traceroute, "args": ["IP"]},
    "networkscan": {"func": networkscan.networkscan, "args": ["IP", "Mask"]},
    "arp": {"func": arp.arp_scan, "args": []},
    "portscan": {"func": portscanner.scan_ports, "args": ["IP", "Port"]},
    "myip": {"func": myip.get_ip_details, "args": []},
    "networkint": {"func": networkint.list_network_interfaces, "args": []},
    "speedtest": {"func": speedtest.speed_test, "args": []}
}

# ======== Dynamic Service Window =========
def open_service_window(service_name):
    meta = services.get(service_name)
    if not meta:
        messagebox.showerror("Error", f"Service '{service_name}' not found.")
        return

    window = tk.Toplevel()
    window.title(f"{service_name.capitalize()} Tool")
    window.minsize(400, 300)
    window.grid_rowconfigure(0, weight=1)
    window.grid_columnconfigure(0, weight=1)

    main_frame = tk.Frame(window)
    main_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    main_frame.grid_columnconfigure(1, weight=1)

    for i in range(len(meta["args"]) + 2):
        main_frame.grid_rowconfigure(i, weight=0)
    main_frame.grid_rowconfigure(len(meta["args"]), weight=1)

    entries = {}
    for i, arg in enumerate(meta["args"]):
        tk.Label(main_frame, text=f"{arg}:").grid(row=i, column=0, sticky="e", padx=5, pady=5)
        entry = tk.Entry(main_frame)
        entry.grid(row=i, column=1, sticky="ew", padx=5, pady=5)
        entries[arg] = entry

    output_box = tk.Text(main_frame, wrap=tk.WORD, height=8)
    output_box.grid(row=len(meta["args"]), column=0, columnspan=2, sticky="nsew", padx=5, pady=10)

    def resize_window_based_on_output():
        content = output_box.get("1.0", "end-1c")
        line_count = content.count("\n") + 1
        ideal_height = min(max(300, line_count * 20), 900)
        window.geometry(f"800x{ideal_height}")

    def run_tool():
        def worker():
            try:
                args = [entries[arg].get() for arg in meta["args"]]
                result = meta["func"](*args) if args else meta["func"]()
                output_box.delete("1.0", tk.END)
                output_box.insert(tk.END, result if result else "[✓] Task completed successfully.")
                output_box.after(100, resize_window_based_on_output)
            except Exception as e:
                output_box.insert(tk.END, f"[!] Error: {e}")
                output_box.after(100, resize_window_based_on_output)
        threading.Thread(target=worker, daemon=True).start()

    tk.Button(main_frame, text="Run", command=run_tool).grid(
        row=len(meta["args"])+1, column=0, columnspan=2, sticky="ew", padx=5, pady=5
    )

# ======== Tray Menu Setup =========
def make_menu_action(service_name):
    def action(icon, item):
        open_service_window(service_name)
    return MenuItem(service_name.capitalize(), action)

def create_tray_icon():
    image = Image.new('RGB', (64, 64), color='black')
    draw = ImageDraw.Draw(image)
    draw.rectangle((16, 16, 48, 48), fill='cyan')

    menu_items = [make_menu_action(name) for name in services]
    icon = Icon("NetToolkit", image, menu=Menu(*menu_items))
    icon.run_detached()

# ======== Main Launcher =========
def main():
    root = tk.Tk()
    root.title("NetToolkit Background Launcher")
    root.geometry("300x100")
    root.resizable(False, False)
    tk.Label(root, text="NetToolkit is running.\nUse system tray to launch tools.", padx=10, pady=10).pack()

    threading.Thread(target=create_tray_icon, daemon=True).start()
    root.mainloop()

if __name__ == "__main__":
    main()