import subprocess
import time
import json
import os

def get_battery_voltage():
    try:
        # Run the 'read_ai' command and capture the output
        result = subprocess.check_output(["read_vi", "0"]).decode("utf-8").strip()
        
        # Extract the voltage value from the output (e.g., "volt=1.20V" -> "1.20")
        voltage = result.split('=')[1].rstrip('V')
        
        return float(voltage)
    except subprocess.CalledProcessError as e:
        print("Error running read_vi:", e)
        return None

# Set the time interval (in seconds) for voltage measurements
interval_seconds = 10  # Adjust this value as needed

try:
    while True:
        # Get and print the battery voltage
        battery_voltage = get_battery_voltage()
        if battery_voltage is not None:
            print(f"Battery Voltage: {battery_voltage} V")
            # Write the battery voltage to the JSON file
            key = "BTT"  # Choose a key for the JSON data
            value = battery_voltage
            if os.path.exists('response.json'):
                with open('response.json', 'r') as json_file:
                    existing_data = json.load(json_file)
            else:
                existing_data = {}
            existing_data[key] = f"{battery_voltage:.2f}"
            with open('response.json', 'w') as json_file:
                json.dump(existing_data, json_file, indent=4)
                
        else:
            print("Failed to retrieve battery voltage.")
        
        # Wait for the specified interval before the next measurement
        time.sleep(interval_seconds)
except KeyboardInterrupt:
    # Stop the script when Ctrl+C is pressed
    pass
