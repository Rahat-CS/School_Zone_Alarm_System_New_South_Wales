import platform
import json
import os

def get_firmware_info():
    system_info = platform.uname()
    firmware_info = {
        "System": system_info.system,
        "Node Name": system_info.node,
        "Release": system_info.release,
        "Version": system_info.version,
        "Machine": system_info.machine,
        "Processor": system_info.processor
    }
    
    key = "FWV"  # Choose a key for the JSON data
    value = firmware_info["Version"]  # Getting the version info from firmware_info

    if os.path.exists('response.json'):
        with open('response.json', 'r') as json_file:
            existing_data = json.load(json_file)
    else:
        existing_data = {}

    existing_data[key] = value

    with open('response.json', 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)

    return firmware_info

if __name__ == "__main__":
    firmware_info = get_firmware_info()
    for key, value in firmware_info.items():
        print(f"{key}: {value}")
