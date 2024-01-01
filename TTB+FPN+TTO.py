from datetime import datetime, timedelta, time as dt_time
import time
import json
import RPi.GPIO as GPIO  # Assuming you are using Raspberry Pi GPIO

def _read_json_file():
    try:
        with open("response.json", "r") as file:  # JSON file for sign controller.
            data = json.load(file)
    except FileNotFoundError:
        data = {}
    return data

# Assuming LEDs are connected to GPIO pins, adjust it based on your setup
LED_GREEN = 13
LED_YELLOW = 20
LED_RED = 22

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_GREEN, GPIO.OUT)
GPIO.setup(LED_YELLOW, GPIO.OUT)
GPIO.setup(LED_RED, GPIO.OUT)


def calculate_day_index(current_datetime, start_date):
    days_difference = (current_datetime - start_date).days
    return (start_date.weekday() + days_difference)

def check_active_segment(current_datetime, start_dates, durations, activity_arrays):
    for start_date, duration, activity_array in zip(start_dates, durations, activity_arrays):
        end_date = start_date + duration

        if start_date <= current_datetime <= end_date:
            current_time = current_datetime.time()
            current_time_seconds = current_time.hour * 3600 + current_time.minute * 60 + current_time.second
            current_day_index = calculate_day_index(current_datetime, start_date)
            print(current_day_index)

            if activity_array[current_day_index] == 4 and (
                (current_time_seconds >= 8 * 3600) and 
                (current_time_seconds < (8 * 3600 + 5400)) or 
                (current_time_seconds >= (8 * 3600 + 5400 + 18000)) and 
                (current_time_seconds < (8 * 3600 + 5400 + 18000 + 5400))
            ):
                print(activity_array[current_day_index])
                return True

            elif activity_array[current_day_index] == 3 and (800 <= current_time.hour * 100 + current_time.minute < 1305):
                print(activity_array[current_day_index])
                return True

            elif activity_array[current_day_index] == 2 and (1430 <= current_time.hour * 100 + current_time.minute < 1600):
                print(activity_array[current_day_index])
                return True

    else:
        return False

    return False

def extract_binary_data(binary_string):
    binary_data = binary_string.replace(" ", "")  # Remove any spaces if present
    num_bits_per_day = 2
    days = []

    while binary_data:
        # Take the rightmost 2 bits
        day_bits = binary_data[-num_bits_per_day:]

        # Convert the 2 bits to an integer (0-3) representing 1-4 days
        day = int(day_bits, 2) + 1
        days.append(day)

        # Remove the processed bits from the binary data
        binary_data = binary_data[:-num_bits_per_day]

    return days[::-1]  # Reverse the list to match the original order (LSB to MSB)

def process_hex_string(hex_string):
    hex_bytes = bytes.fromhex(hex_string)
    total_segments = hex_bytes[0]

    start_dates = []
    durations = []
    activity_arrays = []

    index = 1
    for segment_number in range(total_segments):
        start_time = int.from_bytes(hex_bytes[index:index+4], byteorder='big')
        index += 4

        num_days = hex_bytes[index]
        index += 1

        num_digits = (num_days + 2) // 4  # Each 2 digits represent 1 day
        segment_data = hex_string[index*2:index*2+num_digits*2].upper()
        segment_data_binary = bin(int(segment_data, 16))[2:].zfill(num_digits*8)

        # Reverse the binary string to go from LSB to MSB (right to left)
        segment_data_binary = segment_data_binary[::-1]

        index += num_digits

        days = extract_binary_data(segment_data_binary)

        # Convert num_days to timedelta
        duration = timedelta(days=int(num_days))

        # Convert start_time to datetime
        start_date = datetime.fromtimestamp(start_time)

        start_dates.append(start_date)
        durations.append(duration)
        activity_arrays.append(days)

        # Print the information for the current segment
        print(f"Segment {segment_number + 1}")
        print(f"Start Date: {start_date}")
        print(f"Duration: {duration}")
        print(f"Activity Array: {days}")
        print()

    return start_dates, durations, activity_arrays

def control_leds(digit):
    binary_digit = bin(int(digit))[2:].zfill(3)  # Convert digit to binary (3 bits with leading zeros)

    if binary_digit[0] == '1':
        GPIO.output(LED_GREEN, GPIO.HIGH)
    else:
        GPIO.output(LED_GREEN, GPIO.LOW)

    if binary_digit[1] == '1':
        GPIO.output(LED_YELLOW, GPIO.HIGH)
    else:
        GPIO.output(LED_YELLOW, GPIO.LOW)

    if binary_digit[2] == '1':
        GPIO.output(LED_RED, GPIO.HIGH)
    else:
        GPIO.output(LED_RED, GPIO.LOW)

# Example usage with continuous checking and executing the flashing pattern
# hex_string = "03653f0e200cffc3ff655abda00cffc3ff656d32a00cffc3ff"
string = _read_json_file()
hex_string = string.get('TTB', 'TTB is not found here')
start_dates, durations, activity_arrays = process_hex_string(hex_string)

pattern = _read_json_file()
pattern1 = pattern.get('FPN', 'Flash Pattern is not defined')

while True:
    current_datetime = datetime.now()
    if check_active_segment(current_datetime, start_dates, durations, activity_arrays):
        for digit in pattern1:
            # if current_datetime.time() > dt_time(12, 37) or current_datetime.time() >= dt_time(16, 0):
            #   break
            control_leds(digit)
            #if current_datetime.time() > dt_time(9, 55) or current_datetime.time() >= dt_time(16, 0):
                #break
            time.sleep(1)  # Adjust the sleep duration as needed

            # Check if it's time to turn off the LEDs

        print("Flash pattern executed")

        # Turn off all LEDs after executing the flashing pattern
        GPIO.output(LED_GREEN, GPIO.LOW)
        GPIO.output(LED_YELLOW, GPIO.LOW)
        GPIO.output(LED_RED, GPIO.LOW)
        print("LEDs turned off after executing the flashing pattern")
    else:
        # Turn off all LEDs if not in the active segment
        GPIO.output(LED_GREEN, GPIO.LOW)
        GPIO.output(LED_YELLOW, GPIO.LOW)
        GPIO.output(LED_RED, GPIO.LOW)
        print("LEDs turned off")

    time.sleep(1)
