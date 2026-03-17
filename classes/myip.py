import requests
from tabulate import tabulate

_IPV4_URL = "https://api4.ipify.org?format=json"
_IPV6_URL = "https://api6.ipify.org?format=json"
_COUNTRY_URL = "https://api.iplocation.net/?ip={ip}"

def _fetch(url):
    try:
        resp = requests.get(url, timeout=5)
        return resp.json()
    except Exception:
        return None

def get_ip_details():
    try:
        ipv4_data = _fetch(_IPV4_URL)
        ipv6_data = _fetch(_IPV6_URL)

        ipv4 = ipv4_data.get("ip", "N/A") if ipv4_data else "N/A"
        ipv6 = ipv6_data.get("ip", "N/A") if ipv6_data else "N/A (no IPv6 connectivity)"

        country = "N/A"
        if ipv4 != "N/A":
            country_data = _fetch(_COUNTRY_URL.format(ip=ipv4))
            if country_data:
                country = country_data.get("country_name", "N/A")

        rows = [
            ["IPv4 Address", ipv4],
            ["IPv6 Address", ipv6],
            ["Country",      country],
        ]
        return tabulate(rows, headers=["Field", "Value"], tablefmt="grid")

    except requests.exceptions.RequestException as e:
        return f"Error fetching IP details: {e}"