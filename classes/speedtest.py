import requests
import time
from tabulate import tabulate

_CF_DOWN = "https://speed.cloudflare.com/__down?bytes={size}"
_CF_UP   = "https://speed.cloudflare.com/__up"

def speed_test():
    try:
        # Ping (round-trip for a 1 KB request)
        start = time.perf_counter()
        requests.get(_CF_DOWN.format(size=1024), timeout=10)
        ping = round((time.perf_counter() - start) * 1000, 2)

        # Download speed (10 MB)
        start = time.perf_counter()
        resp = requests.get(_CF_DOWN.format(size=10_000_000), stream=True, timeout=60)
        total = sum(len(chunk) for chunk in resp.iter_content(chunk_size=65536))
        elapsed = time.perf_counter() - start
        download_speed = (total * 8 / 1_000_000) / elapsed if elapsed > 0 else 0.0

        # Upload speed (5 MB)
        data = bytes(5_000_000)
        start = time.perf_counter()
        requests.post(_CF_UP, data=data, timeout=60)
        elapsed = time.perf_counter() - start
        upload_speed = (len(data) * 8 / 1_000_000) / elapsed if elapsed > 0 else 0.0

        table = [
            ["Download Speed", f"{download_speed:.2f} Mbps"],
            ["Upload Speed",   f"{upload_speed:.2f} Mbps"],
            ["Ping",           f"{ping:.2f} ms"],
        ]
        return tabulate(table, headers=["Metric", "Value"], tablefmt="fancy_grid")

    except requests.exceptions.ConnectionError:
        return "Speed test failed: No internet connection."
    except requests.exceptions.Timeout:
        return "Speed test failed: Connection timed out."
    except requests.exceptions.RequestException as e:
        return f"Speed test failed: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"