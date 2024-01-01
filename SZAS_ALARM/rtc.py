def read_rtc_tick():
    try:
        with open('/sys/rtc', 'rb') as rtc_file:
            rtc_data = rtc_file.read()
            if len(rtc_data) == 4:
                rtc_tick = int.from_bytes(rtc_data, byteorder='big')
                return rtc_tick
            else:
                return None
    except FileNotFoundError:
        print("RTC device not found.")
        return None
    except Exception as e:
        print(f"Error reading RTC: {e}")
        return None

rtc_tick = read_rtc_tick()

if rtc_tick is None:
    print("Failed to read RTC tick.")
else:
    print(f"RTC Tick value: {rtc_tick}")
