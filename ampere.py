import subprocess
import time
import sys
import os
import json

def get_led_ampere(light):
    try:
        # Run the 'read_vi' command for the specified channel and capture the output
        result = subprocess.check_output(["read_ai", str(light)]).decode("utf-8").strip()

        # Extract the voltage value from the output (e.g., "ampere=1.20mA" -> "1.20")
        ampere = result.split('=')[1].rstrip('mA')

        # Convert ampere to float and format it as "04d" (4 digits with leading zeros)
        ampere_formatted = "{:04d}".format(int(float(ampere)))

        return ampere_formatted
    except subprocess.CalledProcessError as e:
        print(f"Error  running 'read_ai'{e}")
        return None

# Set the time interval (in seconds) for voltage measurements
interval_seconds = 1  # Adjust this value as needed

# Specify the VI channels you want to read (0, 1, and 2)
lights = [0, 1, 2]

try:
    while True:
        ampere_values = []  # Store ampere values for all lights
        for light in lights:
            # Get the LED ampere for the current channel
            led_ampere = get_led_ampere(light)
            if led_ampere is not None:
                ampere_values.append(f"{led_ampere}")
            else:
                ampere_values.append(f"Failed to retrieve ampere for Channel {light}")

        # Print ampere values for all lights on the same line with commas
        ampere_str = ",".join(ampere_values)
        sys.stdout.write("\r" + ampere_str)
        sys.stdout.flush()

        # Save ampere_str to a JSON file
        key = "ECT"  # Choose a key for the JSON data
        if os.path.exists('response.json'):
            with open('response.json', 'r') as json_file:
                existing_data = json.load(json_file)
        else:
            existing_data = {}
        existing_data[key] = ampere_str
        with open('response.json', 'w') as json_file:
            json.dump(existing_data, json_file, indent=4)

        # Wait for the specified interval before the next measurement
        time.sleep(interval_seconds)
except KeyboardInterrupt:
    # Stop the script when Ctrl+C is pressed
    pass
