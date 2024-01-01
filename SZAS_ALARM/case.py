from battery import Battery
from alarm import GetAlarmRing
from display import Display
from communication import Communication
from signcontroller import SignController
from datetime import datetime
import json
import re
import time
import os
import subprocess

def handle_request(data):
    reply = "Error"
    data = data.strip().decode()
    print("Request:", data)

    data_list = []
    requests = data.split(';')
    replies = []
    accumulated_data = []
    session = True

    for request in requests:
        key =None
        value= None
        if request == '<BTT?>':
            reply = Battery.GetBattLvl()
        elif request == '<LOG?>':
            reply = Battery.GetLogs()
        elif request == '<ADN?>':
            reply = Battery.GetSignctrNum()
        elif request == '<BVL?>':
            reply = Battery.GetBattVoltThresh()
        elif request == '<END>':
            reply = '<ACK>'
            session = False
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
            reply = SignController.GetSigntoDumpTraceData()
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
        elif request == '<RBT>':
            reply = SignController.GetSignToReboot()

             
        elif request.startswith('<') and ' ' not in request:
            parts = request.split('="', 1)
            if len(parts) == 2 and parts[0].startswith('<') and parts[1].endswith('>'):
                key = parts[0][1:]
                value = parts[1][:-2].strip()
                reply = "<ACK>"
            else:
                reply = "<REJ>"
                session = True
        #elif key == "ITT" and value:
         #   is_valid, message = SignController.validate_schedule(value)
          #  if is_valid:
           #     reply = "<ACK>"
            #else:
             #   reply = "<REJ>"
            #server_timeout = None
            #if reply.startswith('<TMO='):
               # timeout_value = re.search(r'<TMO="(\d+)">', reply)
                #if timeout_value:
                    #timeout_seconds = int(timeout_value.group(1))
                    #server_timeout = time.time() + timeout_seconds
            #if server_timeout and time.time() > server_timeout:
                #session = False
        else:
            reply = 'Unknown Request'
        if reply == "<ACK>":
            if os.path.exists('response.json'):
                with open('response.json', 'r') as json_file:
                    existing_data = json.load(json_file)
            else:
                existing_data = {}
            existing_data[key] = value
            with open('response.json', 'w') as json_file:
                json.dump(existing_data, json_file, indent=4)
                
        replies.append(reply)

    return reply
