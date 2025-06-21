import speedtest
from tabulate import tabulate

def speed_test():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()

        download_speed = st.download() / 1_000_000  # Convert to Mbps
        upload_speed = st.upload() / 1_000_000
        ping = st.results.ping

        table = [
            ["Download Speed", f"{download_speed:.2f} Mbps"],
            ["Upload Speed", f"{upload_speed:.2f} Mbps"],
            ["Ping", f"{ping:.2f} ms"]
        ]
        return tabulate(table, headers=["Metric", "Value"], tablefmt="fancy_grid")
        

    except speedtest.ConfigRetrievalError:
        return("Could not retrieve configuration. Check your internet connection.")
    except speedtest.NoMatchedServers:
        return("No suitable test server found.")
    except speedtest.SpeedtestException as e:
        return(f"Speedtest failed: {e}")
    except Exception as e:
        return(f"Unexpected error: {e}")