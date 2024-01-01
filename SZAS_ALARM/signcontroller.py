import json
from datetime import datetime, timedelta
import os

class SignController:

    def GetSignControllerPattern():
        data = SignController._read_json_file()
        return data.get('FPN', 'Flash pattern not found')

    def GetSignId():
        data = SignController._read_json_file()
        return data.get('SGN', 'Sign Id Not Found')

    def GetFirmwareVersion():  
        data = SignController._read_json_file()
        return data.get('FWV', 'Firmware Version is Not Defined Properly')

    def GetParameterforSign():  
        ParameterforSign = "'Mfr'','Ser','hw','sw','imei','imsi'"
        return ParameterforSign

    def GetTimeTableSignController():  
        data = SignController._read_json_file()
        return data.get('TTB', 'Time table on Sign Controller is not found')

    def GetSigntoCalculateChecksum():  
        SigntoCalculateChecksum = '797D'
        return SigntoCalculateChecksum

    def GetSigntoDumpTraceData():  
        SigntoDumpTraceData = '<intelhex_format>'
        return SigntoDumpTraceData

    def GetRtcOnSignControll():  
        data = SignController._read_json_file()
        return data.get('DTE', 'DTE for RTC tick is not set')

    def GetSignTemp():  
        data = SignController._read_json_file()
        return data.get('TMP', 'Temperature for sign is not defined')

    def GetSignSignalStrength():
        data = SignController._read_json_file()
        return data.get('RSS', 'SignSignal Strength is not detected')

    def GetSignStatus():  
        SignStatus = '25'
        return SignStatus

    def GetMoreFirmwareVersion():  
        MoreFirmwareVersion = 'SVN1244'
        return MoreFirmwareVersion

    def GetClearSignLog():  
        try:
            log_file_path = "sign_controller_log.txt"  

            # Clear the log file
            with open(log_file_path, 'w') as file:
                file.truncate(0)

            return '25'
        except Exception as e:
            return f'Error clearing log file: {e}'

    def GetSignToReboot():
        SignToReboot = os.system('sudo reboot')
        return '<ACK>'

    def GetSignSelfCheck():  
        SignSelfCheck = '0'
        return SignSelfCheck

    def GetSynchronization():  
        data = SignController._read_json_file()
        return data.get('SYN', 'offset value is not set properly')

    def GetSignTestFlash():  
        SignTestFlash = ' if test flash cycle not performed '
        return SignTestFlash

    def GetUpdateFirmwireofSign():  
        UpdateFirmwireofSign = 'URL Is Sent'
        return UpdateFirmwireofSign

    def _read_json_file():
        try:
            with open("response.json", "r") as file: 
                data = json.load(file)
        except FileNotFoundError:
            data = {}
        return data

    def validate_schedule(value):
        parts = value.split(',')
        if len(parts) != 7:
            return False, "Invalid number of elements"

        try:
            ena = int(parts[0])
            if ena not in [4, 5, 6]:
                return False, "ENA value must be 4, 5, or 6"

            times = parts[1:]

            for time in times[:ena]:
                if len(time) != 4 or not time.isdigit():
                    return False, "Invalid time format"

                hours = int(time[:2])
                minutes = int(time[2:])

                if hours < 0 or hours > 23 or minutes < 0 or minutes > 59:
                    return False, "Invalid time range"

            # Convert times to integers for comparison
            times_int = [int(time) for time in times[:ena]]
            print("Times as integers:", times_int)

            # Check for ascending order
            for i in range(len(times_int) - 1):
                if times_int[i] >= times_int[i + 1]:
                    return False, "Invalid times sequence"

                # Check if times are less than 5 minutes apart
                if times_int[i + 1] - times_int[i] < 5:
                    return False, "Times are less than 5 minutes apart"

        except ValueError:
            return False, "Invalid values"

        return True, "Valid schedule"
