import json
class Display: #Display class for showing about the display issues.

    def GetDisplayVOlt(): #this function showing the voltage of the display
        DisplayVOlt = '0030'
        return DisplayVOlt

    #Display = 'The display system of the section'

    def GetDisplaySystem(value): ## this function shows the display value either it is on or off
        value = int(input("Enter value (1or 0)"))
        if value == 1: #display is on
            print("Display is on")
        else:
            print("Display is off") #display is off


    def GetDisplayElementCur(): #this function get 3 current from 3 light of the board 2 flashing and 2 annulas light
        DisplayElementCur= '0435.0429.1327' #1st 2 light for flashing and last 1 for annulas light ampere
        return DisplayElementCur

    def GetFlashingDisplayElement(): #this function get the duty cycle of the flashing display whose default value is 100

        data = Display._read_json_file()
        return data.get('PWM', 'Flashing Display Element is set to the default value')

    def GetDisplayErrorByte():
        DisplayErrorByte = '1'
        return DisplayErrorByte


    def GetStateofDisplay():

        data = Display._read_json_file()
        return data.get('SOP', 'Display State is not set')

    def _read_json_file():
        try:
            with open("response.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}
        return data





