import RPi.GPIO as GPIO
import time
import json

def _read_json_file():
    try:
        with open("response.json", "r") as file:  # JSON file for sign controller.
            data = json.load(file)
        return data
    except FileNotFoundError:
        print("JSON file 'response.json' not found.")
    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {str(e)}")
    return {}  # Return an empty dictionary in case of errors.

# Define LED pins
LED_GREEN = 20
LED_YELLOW = 13
LED_RED = 22

# Set up GPIO mode and configure LED pins as outputs
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_GREEN, GPIO.OUT)
GPIO.setup(LED_YELLOW, GPIO.OUT)
GPIO.setup(LED_RED, GPIO.OUT)

# Function to turn off all LEDs
def turn_off_all_leds():
    GPIO.output(LED_GREEN, GPIO.LOW)
    GPIO.output(LED_YELLOW, GPIO.LOW)
    GPIO.output(LED_RED, GPIO.LOW)

# Function to flash an LED for a given duration
def flash_led(led_pin, duration):
    GPIO.output(led_pin, GPIO.HIGH)  # Turn the LED on
    time.sleep(duration)  # Wait for the specified duration
    GPIO.output(led_pin, GPIO.LOW)  # Turn the LED off

# Function to convert a digit to its binary representation and control the LEDs
def control_leds(digit):
    binary_digit = bin(int(digit))[2:].zfill(3)  # Convert digit to binary (3 bits with leading zeros)

    if binary_digit[0] == '1':
        GPIO.output(LED_GREEN, GPIO.HIGH)
        print("Green Led is on")
    else:
        GPIO.output(LED_GREEN, GPIO.LOW)

    if binary_digit[1] == '1':
        GPIO.output(LED_YELLOW, GPIO.HIGH)
        print("Yellow led is on")
    else:
        GPIO.output(LED_YELLOW, GPIO.LOW)

    if binary_digit[2] == '1':
        GPIO.output(LED_RED, GPIO.HIGH)
        print("Red Led is on")
    else:
        GPIO.output(LED_RED, GPIO.LOW)

# Read JSON file and extract 'FPN' value
pattern = _read_json_file()
pattern1 = pattern.get('FPN', 'offset value is not set properly')
print(pattern1)

# Total duration in seconds
total_duration = 5400

start_time = time.time()

try:
    while time.time() - start_time < total_duration:
        for digit in pattern1:
            control_leds(digit)
            time.sleep(1)

finally:
    turn_off_all_leds()  # Clean up by turning off all LEDs
    GPIO.cleanup()  # Clean up GPIO pins when done
