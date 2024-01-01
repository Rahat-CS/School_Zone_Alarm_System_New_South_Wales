from battery import Battery
from alarm import GetAlarmRing
from display import Display
# from dump_data import handle_dmp_request
from communication import Communication
from signcontroller import SignController
#from flash_pattern import flash_led, turn_off_all_leds, control_leds
import json
import os
import re
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

def handle_request(data):
    reply = "Error"
    data = data.strip().decode()
    requests = data.split(';')
    print("Request:", data)
    data_list = []
    replies = []
    session = True

    for request in requests:
        if request == '<BTT?>':
            reply = Battery.GetBattLvl()
        elif request == '<LOG?>':
            reply = Battery.GetLogContents()
        elif request == '<ADN?>':
            reply = Battery.GetSignctrNum()
        elif request == '<BVL?>':
            reply = Battery.GetBattVoltThresh()
        elif request == '<DIS>':
            reply = Display.GetDisplaySystem(int)
        elif request == '<ALR>':
            reply = GetAlarmRing.GetAlarmStat()
        elif request == '<ECT?>':
            reply = GetAlarmRing.GetElectricalCurAlarm()
        elif request == '<DRT?>':
            reply = GetAlarmRing.GetAlarmforDisp()
        elif request == '<TTV?>':
            reply = GetAlarmRing.GetTimeTableVersion()
        elif request == '<TTO?>':
            reply = GetAlarmRing.GetOperationDuration()
        elif request == '<DIP>':
            reply = Display.GetDisplayVOlt()
        elif request == '<ESC?>':
            reply = Display.GetDisplayElementCur()
        elif request == '<PWM?>':
            reply = Display.GetFlashingDisplayElement()
        elif request == '<DER?>':
            reply = Display.GetDisplayErrorByte()
        elif request == '<SOP?>':
            reply = Display.GetStateofDisplay()
        elif request == '<CMC?>':
            reply = Communication.GetCMCAddress()
        elif request == '<CTD?>':
            reply = Communication.GetReconnection()
        elif request == '<ITT?>':
            reply = Communication.GetCallSchedule()
        elif request == '<STD?>':
            reply = Communication.GetConnectionClose()
        elif request == '<TMO?>':
            reply = Communication.GetCommunicationTimeout()
        elif request == '<CEL?>':
            reply = Communication.GetCellInfoFromMobile()
        elif request == '<GPS?>':
            reply = Communication.GetGpsComm()
        elif request == '<FPN?>':
            reply = SignController.GetSignControllerPattern()
        elif request == '<FWV?>':
            reply = SignController.GetFirmwareVersion()
        elif request == '<MID?>':
            reply = SignController.GetParameterforSign()
        elif request == '<SGN?>':
            reply = SignController.GetSignId()
        elif request == '<TTB?>':
            reply = SignController.GetTimeTableSignController()
        elif request == '<TTC?>':
            reply = SignController.GetSigntoCalculateChecksum()
        elif request == '<DMP?>':
            # reply = handle_dmp_request()
            reply = '<DMP_NOT_IMPLEMENTED>'  # Assuming handle_dmp_request is not implemented
        elif request == '<DTE?>':
            reply = SignController.GetRtcOnSignControll()
        elif request == '<TMP?>':
            reply = SignController.GetSignTemp()
        elif request == '<RSS?>':
            reply = SignController.GetSignSignalStrength()
        elif request == '<STS?>':
            reply = SignController.GetSignStatus()
        elif request == '<SVN?>':
            reply = SignController.GetMoreFirmwareVersion()
        elif request == '<CLG>':
            reply = SignController.GetClearSignLog()
        #elif request == '<RBT>':
            #reply = SignController.GetSignToReboot()
        elif request == '<SCK>':
            reply = SignController.GetSignSelfCheck()
        elif request == '<SYN?>':
            reply = SignController.GetSynchronization()
        elif request == '<TFL>':
            # reply = SignController.GetSignTestFlash()
            reply = control_leds(digit)  # Assuming digit is defined
        elif request == '<RBT>':
            reply = '<ACK>'
            SignController.GetSignToReboot()
            # reply = '<ACK>'
        elif request.startswith('<') and ' ' and ('?') not in request:
            parts = request.split('="', 1)
            if len(parts) == 2 and parts[0].startswith('<') and parts[1].endswith('>'):
                key = parts[0][1:]
                value = parts[1][:-2].strip()

                # Check for special cases of BVL, PWM, ECT, CTD, TMO, TTO, and STD values
                if key == 'BVL' and not re.match(r'\d{2}\.\d{2}', value):
                    reply = '<REJ>'
                elif key == 'PWM' and value != '100':
                    reply = '<REJ>'
                elif key == 'ECT' and not re.match(r'\d{4},\d{4},\d{4}', value):
                    reply = '<REJ>'
                elif key == 'CTD' and (not re.match(r'\d{4}', value) or len(value) > 4):
                    reply = '<REJ>'
                elif key == 'TMO' and (not re.match(r'\d{6}', value) or len(value) > 6):
                    reply = '<REJ>'
                elif key == 'TTO' and not re.match(r'\d+,\d+,\d+', value):
                    reply = '<REJ>'
                elif key == 'STD' and (not re.match(r'\d{4}', value) or len(value) > 4):
                    reply = '<REJ>'
                elif key == 'DTE' and (not re.match(r'\d{0,9}', value) or len(value) > 10):
                    reply = '<REJ>'
                    
                elif key == 'TFL':
                    # Assuming 'value' contains the pattern and duration (e.g., "30,707")
                            # Importing here to ensure LEDs are controlled only when the TFL request is received
                     from flash_pattern import flash_led, turn_off_all_leds, control_leds
                     reply = '<ACK>' 

                else:
                    reply = '<ACK>'

                # Load existing data from the JSON file (if the file exists)
                if os.path.exists('response.json'):
                    with open('response.json', 'r') as json_file:
                        existing_data = json.load(json_file)
                else:
                    existing_data = {}

                # Update the existing data dictionary with the new key-value pair
                existing_data[key] = value

                # Save the updated data back to the JSON file
                with open('response.json', 'w') as json_file:
                    json.dump(existing_data, json_file, indent=4)
        else:
            reply = "Unknown Request"

        replies.append(reply)

    reply_data = '; '.join(replies)

    return reply_data
