import subprocess
import time
import socket
import datetime
import os
import json
# Define the log file name
LOG_FILE = "sign_controller_log.txt"

# Dictionary to map event codes to descriptions
event_code_to_description = {
    "01": "Unexpected initialization of the sign",
    "02": "Sign housing door opened",
    "03": "Closure of sign housing door (recovery from open)",
    "04": "Configuration error",
    "05": "Firmware download error",
    "06": "Battery voltage below minimum threshold",
    "07": "Recovered from battery below minimum voltage",
    "08": "Failure of any of the Alert Displays",
    "09": "Recovered from Alert Display failure",
    "10": "CMC communications timeout",
    "11": "Commencement of timetabled operation",
    "12": "Cessation of timetabled operation",
    "13": "Locally triggered test flash request",
    "14": "Trace data available",
    "15": "Controller initialized due to an unresponsive modem",
    "16": "Mains power failure",
    "17": "Recovery from mains power failure",
    "18": "Battery needs replacement",
    "99": "Debuggin Aid (Customized)",}
    
def _read_json_file():
    try:
        with open("response.json", "r") as file: # JSON file for sign controller.
            data = json.load(file)
    except FileNotFoundError:
        data = {}
    return data

def get_battery_voltage():
    try:
        # Run the 'read_vi' command and capture the output
        result = subprocess.check_output(["read_vi", "1"]).decode("utf-8").strip()

        # Extract the voltage value from the output (e.g., "volt=1.20V" -> "1.20")
        voltage = result.split('=')[1].rstrip('V')

        return float(voltage)
    except subprocess.CalledProcessError as e:
        print("Error running read_vi:", e)
        return None

def log_event(event_code, event_data=None):
    timestamp = int(time.time())
    event_description = event_code_to_description.get(event_code, "Unknown Event")

    if event_data is not None:
        log_entry = f"{timestamp}: {event_code}: {event_description}, {event_data}\n"
    else:
        log_entry = f"{timestamp}: {event_code}: {event_description}\n"

    with open(LOG_FILE, "a") as log_file:
        log_file.write(log_entry)
        
        
server =_read_json_file()
SERVER_ADDRESS=server.get('CMC','Flash Pattern is not defined')


# Server communication parameters
#SERVER_ADDRESS = '192.168.101.220'
SERVER_PORT = 8007

# Sign information
SIGN_ID = '577-0402'
STATUS = '82'

def _read_json_file():
    try:
        with open("response.json", "r") as file:  # JSON file for sign controller.
            data = json.load(file)
    except FileNotFoundError:
        data = {}
    return data
# Battery voltage threshold
voltage = _read_json_file()
VOLTAGE_THRESHOLD = float (voltage.get('BVL', 'Battery Threshold is not defined'))

# Set the time interval (in seconds) for voltage measurements
interval_seconds = 10  # Adjust this value as needed

recovered_from_low_voltage = False

# Initialize the cyclic counter
cyclic_counter = 0

try:
    while True:
        # Get and print the battery voltage
        battery_voltage = get_battery_voltage()
        if battery_voltage is not None:
            print(f"Battery Voltage: {battery_voltage} V")

            # Update response.json with battery voltage information
            key = "BTT"  # Choose a key for the JSON data
            value = f"{battery_voltage:.2f}"

            if os.path.exists('response.json'):
                with open('response.json', 'r') as json_file:
                    existing_data = json.load(json_file)
            else:
                existing_data = {}

            existing_data[key] = value

            with open('response.json', 'w') as json_file:
                json.dump(existing_data, json_file, indent=4)

            if battery_voltage < VOLTAGE_THRESHOLD:
                if not recovered_from_low_voltage:
                    # Get the current time in ticks (cyclic counter)
                    current_time_ticks = str(cyclic_counter).zfill(3)
                    
                    # Communicate with the server and log the event
                    log_event("06-" + current_time_ticks, "Battery voltage below threshold at " + str(battery_voltage) + " V")
                    
                    # Increment the cyclic counter and wrap it to 000 when it reaches 999
                    cyclic_counter = (cyclic_counter + 1) % 1000
                    
                    recovered_from_low_voltage = False  # Reset the recovery flag

                    # Create a socket connection to the server
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
                        client_socket.connect((SERVER_ADDRESS, SERVER_PORT))

                        # Send sign information to the server
                        sign_info = 'sign id="{}"; STS="{}"'.format(SIGN_ID, STATUS)
                        client_socket.sendall(sign_info.encode())

                        # Close the connection
                        client_socket.close()
            else:
                if recovered_from_low_voltage:
                    # Get the current time in ticks (cyclic counter)
                    current_time_ticks = str(cyclic_counter).zfill(3)

                    # Log the recovery event (code 07)
                    log_event("07-" + current_time_ticks, "Recovered from battery below minimum voltage at " + str(battery_voltage) + " V")

                    # Increment the cyclic counter and wrap it to 000 when it reaches 999
                    cyclic_counter = (cyclic_counter + 1) % 1000

                    recovered_from_low_voltage = False  # Reset the recovery flag

        else:
            print("Failed to retrieve battery voltage.")

        # Wait for the specified interval before the next measurement
        time.sleep(interval_seconds)

except KeyboardInterrupt:
    # Stop the script when Ctrl+C is pressed
    pass
