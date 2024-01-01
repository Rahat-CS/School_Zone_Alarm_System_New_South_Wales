import json
import time
import os

def get_cpu_temperature():
    try:
        # Open the CPU temperature file for reading
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as temp_file:
            temperature_str = temp_file.read()

        # Convert the temperature value to degrees Celsius
        temperature = float(temperature_str) / 1000.0

        return temperature
    except IOError as e:
        print(f"Error reading CPU temperature: {e}")
        return None

while True:
    # Get and print the CPU temperature
    cpu_temperature = get_cpu_temperature()
    if cpu_temperature is not None:
        print(f"CPU Temperature: {cpu_temperature:.2f} °C")

        key = "TMP"  # Choose "TMP" as the key for the JSON data
        value = cpu_temperature
        if os.path.exists('response.json'):
            with open('response.json', 'r') as json_file:
                existing_data = json.load(json_file)
        else:
            existing_data = {}
        existing_data[key] = f"{value:.2f}"
        with open('response.json', 'w') as json_file:
            json.dump(existing_data, json_file, indent=4)
    else:
        print("Failed to retrieve CPU temperature.")

    # Wait for 10 seconds before the next measurement
    time.sleep(10)
