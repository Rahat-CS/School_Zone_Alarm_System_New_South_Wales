from battery import Battery
from alarm import GetAlarmRing
from display import Display
# from dump_data import handle_dmp_request
from communication import Communication
from signcontroller import SignController
import json
import os
import requests
import re

def download_firmware(url, save_path):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
            return True
        else:
            print(f"Failed to download firmware. Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error downloading firmware: {e}")
        return False

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
            reply = handle_dmp_request()
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
        elif request == '<RBT>':
            reply = SignController.GetSignToReboot()
        elif request == '<SCK>':
            reply = SignController.GetSignSelfCheck()
        elif request == '<SYN?>':
            reply = SignController.GetSynchronization()
        elif request == '<TFL>':
            reply = SignController.GetSignTestFlash()
        if request.startswith('<RBT>'):
            reply = '<ACK>', SignController.GetReboot()

        elif request.startswith('<UFW='):
            url = request.split('=', 1)[1][:-1]  # Extract URL from request
            firmware_save_path = 'firmware_file_name.extension'  # Specify where to save the downloaded file
            if download_firmware(url, firmware_save_path):
                reply = '<ACK> Firmware downloaded successfully'
            else:
                reply = '<NAK> Firmware download failed'

        elif request.startswith('<') and ' ' and ('?') not in request:
            parts = request.split('="', 1)
            if len(parts) == 2 and parts[0].startswith('<') and parts[1].endswith('>'):
                key = parts[0][1:]
                value = parts[1][:-2].strip()

                # Check for special cases of BVL, PWM, ECT, CTD, TMO, TTO, and STD values
                # Additional validation logic for keys/values...

                if os.path.exists('response.json'):
                    with open('response.json', 'r') as json_file:
                        existing_data = json.load(json_file)
                else:
                    existing_data = {}

                existing_data[key] = value

                with open('response.json', 'w') as json_file:
                    json.dump(existing_data, json_file, indent=4)
            else:
                reply = "Unknown Request"

        else:
            reply = "Unknown Request"

        replies.append(reply)

    reply_data = '; '.join(replies)

    return reply_data
