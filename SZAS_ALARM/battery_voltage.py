import subprocess
import time

def get_battery_voltage():
    try:
        # Run the 'read_ai' command and capture the output
        result = subprocess.check_output(["read_vi", "1"]).decode("utf-8").strip()

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
        else:
            print("Failed to retrieve battery voltage.")

        # Wait for the specified interval before the next measurement
        time.sleep(interval_seconds)
except KeyboardInterrupt:
    # Stop the script when Ctrl+C is pressed
    pass
