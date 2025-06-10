from tabulate import tabulate
import subprocess
def traceroute(ip):
    

    try:
        # Run the traceroute command
        result = subprocess.run(['tracert', ip], capture_output=True, text=True, check=True)

        # Split the output into lines
        lines = result.stdout.strip().split('\n')

        # Prepare headers and rows for the table
        headers = ["Hop", "IP Address", "RTT"]
        rows = []

        for line in lines[1:]:  # Skip the first line which is usually a header
            parts = line.split()
            if len(parts) >= 3:
                hop = parts[0]
                ip_address = parts[1]
                rtt = ' '.join(parts[2:])  # Join remaining parts as RTT
                rows.append([hop, ip_address, rtt])

        return tabulate(rows, headers=headers, tablefmt="grid")

    except subprocess.CalledProcessError as e:
        return f"Error: {e.stderr.strip()}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"