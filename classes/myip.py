import requests
from tabulate import tabulate



def get_ip_details():
    url = "https://api.myip.com/"

    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code != 200:
            return f"Error: Unable to fetch data, status code {response.status_code}"
        headers = ["ip", "country"]
        values = [data["ip"], data["country"]]
        print(tabulate([values], headers=headers, tablefmt="grid"))

    except requests.exceptions.RequestException as e:
        print("Error fetching IP details: {e}" )