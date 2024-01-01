import json
from datetime import datetime
class GetAlarmRing:
    #AlarmRing = 'The alarm Element Section'
    def GetAlarmStat(): #functio if the alarm state is on or off.
        danger = 'Alarm is ON'
        return danger

    def GetAlarmforDisp():
        data = GetAlarmRing._read_json_file()
        return data.get('DRT', 'Operation Duration is not defined')


    def GetElectricalCurAlarm(): #get for the display electrical current threshold to ring left lantern, right lantern, Annulus type light
        data = GetAlarmRing._read_json_file()
        return data.get('ECT', 'Electrical alarm Threshold is not defined')



    def GetOperationDuration(): #get for the display electrical current threshold to ring left lantern, right lantern, Annulus type light
        data = GetAlarmRing._read_json_file()
        return data.get('TTO', 'Operation Duration is not defined')



    def GetTimeTableVersion(): #Get the time version of 32 characters
        data = GetAlarmRing._read_json_file()
        return data.get('TTV', 'Time Table Version is not set')

    def _read_json_file():
        try:
            with open("response.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}
        return data





