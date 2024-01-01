import json
import time
import socket
#from main_script import GetServerIP,GetSignId,GetStatus
class Communication:


    def GetCMCAddress():  #Get ip or hostname remotely
        data = Communication._read_json_file()
        return data.get('CMC', 'CMC Address is not found')

    #Communication ="This class showed us the communication message"
    # This class is created for the communication part of the coding



    def GetReconnection(): #4 digit sign request for reconnection to the server
        data = Communication._read_json_file()
        data1= data.get('CTD', 'CTD reconnection time is not set up')
        return data1


    def GetCallSchedule(): #return a call schedule for everyone call-home daily schedule times
        data = Communication._read_json_file()
        return data.get('ITT', 'Call Schedule is not found')


    def GetConnectionClose(): #return the connection close code for inactivity
        data = Communication._read_json_file()
        return data.get('STD', 'Communication Time out is not set')


    def GetCommunicationTimeout(): # this function returned how much time system is idol due to inactivity and set an alarm
        data = Communication._read_json_file()
        return data.get('TMO', 'Communication Timeout is not defined')


    def GetCellInfoFromMobile():
        CellInfoFromMobile = '4G,4436,22……,0E8259F,29,38,NOCONN'
        return CellInfoFromMobile

    def GetGpsComm():
        GpsComm = 'LAT,LONG,HDOP'
        return GpsComm

    def inactivity_monitor(szasSrv, last_request_time, inactivity_timeout):
        while True:
            current_time = time.time()
            if inactivity_timeout > 0 and (current_time - last_request_time) > inactivity_timeout:
                print("Closing connection due to inactivity.")
                szasSrv.close()
                break
            time.sleep(1)

    # def reconnect(szasSrv, host, port):
    #     data = Communication._read_json_file()
    #     ctd_value = data.get('CTD', '0')  # Get the reconnect cooldown value from JSON
    #     reconnection_time = time.time() + int(ctd_value)
    #    # print('CTD')
    #
    #     while time.time() < reconnection_time:
    #         time_left = reconnection_time - time.time()
    #         print(f"Reconnection cooldown active. Time left: {time_left:.2f} seconds")
    #         time.sleep(1)
    #
    #     try:
    #         szasSrv.close()
    #     except:
    #         pass
    #
    #     while True:
    #         try:
    #             szasSrv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #             szasSrv.connect((host, port))
    #             print("Reconnected to the server.")
    #             return szasSrv
    #         except:
    #             print("Reconnection failed. Retrying...")
    #             time.sleep(5)

    def reconnect(szasSrv, host, port):
        try:
            szasSrv.close()
        except:
            pass

        while True:
            try:
                szasSrv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                szasSrv.connect((host, port))
                print("Reconnected to the server.")
                return szasSrv
            except:
                print("Reconnection failed. Retrying...")
                time.sleep(5)



    def _read_json_file():
        try:
            with open("response.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            data = {}
        return data


    #def _write_json_file(data):
        #with open("CommunicationData.json", "w") as file:
           # json.dump(data, file)

