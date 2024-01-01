import subprocess
import time
import json
import os

def get_wifi_signal_level(interface):
    try:
        # Run the iwconfig command and capture its output
        output = subprocess.check_output(["iwconfig", interface]).decode("utf-8")

        # Find the line that contains "Signal level"
        signal_line = [line for line in output.split('\n') if "Signal level" in line][0]

        # Extract the signal level value from the line
        signal_level = signal_line.split("Signal level=")[1].split(" dBm")[0]

        return int(signal_level)
    except Exception as e:
        print(f"Error: {e}")
        return None

def update_response_json(signal_level):
    key = "RSS"  # Choose a key for the JSON data
    if os.path.exists('response.json'):
        with open('response.json', 'r') as json_file:
            existing_data = json.load(json_file)
    else:
        existing_data = {}
    
    # Convert signal_level to string before storing in JSON
    existing_data[key] = str(signal_level)
    
    with open('response.json', 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)


if __name__ == "__main__":
    interface = "wlan0"  # Replace with your actual wireless interface

    while True:
        signal_level = get_wifi_signal_level(interface)

        if signal_level is not None:
            print(f"Signal level on {interface}: {signal_level} dBm")
            update_response_json(signal_level)
        else:
            print(f"Failed to retrieve signal level on {interface}")

        time.sleep(300)  # Adjust the interval between measurements as needed
