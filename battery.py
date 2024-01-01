import json
class Battery:
    capacity = 100 #highest capacity of the battery
    charge = capacity #At first charging level is full which equal to the capacity

# This function is used for using battery discharge calculation
    def discharge(amount):
        if amount <= Battery.charge:  #How much battery voltage drained
            Battery.charge -= amount
        else:
            Battery.charge = 0

# This function is calculated for battery charging amount and charge system.
    def charge_battery(amount):
        if amount <= Battery.capacity - Battery.charge: # how much battery has been charged after giving the chaging portal
            Battery.charge += amount
        else:
            Battery.charge = Battery.capacity


    def get_charge_level(self): #this function got the battery's charging level
        return Battery.charge


    def get_capacity(self): #this function returns the total battery capacity
        return Battery.capacity


    def get_batt_info(self): #this function print the battery voltage and information
        return f"Battery Level: {Battery.charge/Battery.capacity * 100:.2f}%, Capacity: {Battery.capacity}mAh"


    def GetBattLvl(): #This function seds the selective or pre determined battery voltage
    # Here, we directly return the desired battery level as 12.5 volts.
        data = Battery._read_json_file()
        return data.get('BTT','Battery Voltage can not be retrieved')

    def GetLogs(): #Log function if you want any information or any info has been received for the client
        logs = 'Nothing Alarms'
        return logs

    def GetSignctrNum(): #return string number from the server
        SignctrNum = '80000136'
        return SignctrNum
        
    def GetLogContents():
        log_filename='sign_controller_log.txt'
        try:
            with open(log_filename,'r')as log_file:
                log_contents = log_file.read()
                return log_contents
        except FileNotFoundError:
            return f"Log file '{log_filename}' not found."
            



    def GetBattVoltThresh():
        data = Battery._read_json_file()
        return data.get('BVL', 'Battery Threshold not found')

    def _read_json_file():
        try:
            with open("response.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}
        return data








