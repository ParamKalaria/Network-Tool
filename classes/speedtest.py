import speedtest

def speed_test():
    try:
        st = speedtest.Speedtest()
        st.get_best_server()

        download_speed = st.download() / 1_000_000  # Convert to Mbps
        upload_speed = st.upload() / 1_000_000
        ping = st.results.ping

        print(f"Download Speed: {download_speed:.2f} Mbps")
        print(f"Upload Speed: {upload_speed:.2f} Mbps")
        print(f"Ping: {ping:.2f} ms")

    except speedtest.ConfigRetrievalError:
        print("Could not retrieve configuration. Check your internet connection.")
    except speedtest.NoMatchedServers:
        print("No suitable test server found.")
    except speedtest.SpeedtestException as e:
        print(f"Speedtest failed: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")