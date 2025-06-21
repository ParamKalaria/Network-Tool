import requests
import json
import sys
from tabulate import tabulate

def ipinfo(ip):
    api = f"https://api.iplocation.net/?ip={ip}"
    response = requests.get(api)

    try:
        data = json.loads(response.content)

        ip_address = data.get("ip")
        country = data.get("country_name")
        isp = data.get("isp")

        # Table with headers at the top and data in a row
        headers = ["IP Address", "Country", "ISP"]
        row = [[ip_address, country, isp]]
        return(tabulate(row, headers=headers, tablefmt="grid"))

    except json.JSONDecodeError:
        return("Error: Could not decode JSON response.")
   

