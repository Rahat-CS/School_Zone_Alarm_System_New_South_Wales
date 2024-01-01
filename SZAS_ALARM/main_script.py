import socket
import time
import datetime
from communication import Communication
import threading
import json
from case import handle_request
import sys
#from battery import Battery, GetBattLvl,GetLogs,GetSignctrNum
#from display import Display, GetDisplaySystem,GetDisplayVOlt,GetDisplayElementCur
#from alarm import GetAlarmRing, GetAlarmStat , Get
from case import handle_request #import the functio from case class
TCP_IP_PORT = 8007 #define TCP port for the Server
UDP_PORT = 10080 #define UDP port for the client

def GetTCPPort():
    return TCP_IP_PORT

def GetUDPPort():
    return UDP_PORT

def GetServerIP(UDPPortNo):
    serverAddress = '127.0.0.1' # Server Address
    return serverAddress

def GetSignId(): #this function pass the signature id to establish connection with CMC
    signId = '577-0402'
    return signId

def GetStatus(): #This function pass the status of the server to establish connection
    status = '82'
    return status

# ... Other functions (GetLogs, GetSignctrNum) go here ...

# Get TCP/IP Server Address
host = GetServerIP(UDP_PORT)
port = TCP_IP_PORT  # The port used by the host server

# szasSrv = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #created the server connection with CMC and server.
# szasSrv.connect((host, port))
#
# firstMsg = GetSignId() + ";" + GetStatus() #If connection established successfully this will print the signId and status in the
#
# print(firstMsg)
#
# szasSrv.sendall(firstMsg.encode()) # Encoded the sign-controller
# session = True
# #reconnect_cooldown = 40
# # std_value = Communication.GetReconnection()
# # last_communication_time = time.time()
# # inactivity_timeout = float(std_value)
# # reconnect_cooldown = inactivity_timeout
# # # def reconnect():
# #     while True:
# #         try:
# #             szasSrv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# #             szasSrv.connect((host, port))
# #             print("Reconnected to the server.")
# #             return szasSrv
# #         except:
# #             print("Reconnection failed. Retrying...")
# #             time.sleep(5)
#
# #szasSrv = reconnect()
#
# while session:
#     data = szasSrv.recv(1024)
#     if not data:
#         continue

    #if std_value is None:
    #std_value = int(Communication.GetCommunicationTimeout())


    # reply = handle_request(data)

    # last_communication_time = time.time()
    #
    # if time.time() - last_communication_time > inactivity_timeout:
    #     print("Session closed due to inactivity.")
    #     session = False
    #
    # # Only attempt reconnection after the CTD time has passed
    # if time.time() - last_communication_time > reconnect_cooldown:
    #     szasSrv.close()  # Close the existing connection
    #     szasSrv = reconnect()

    #handle requested data or message of the client request.
    #reply = "Error"
    # if reconnect_cooldown > time.time():
    #     reply = "<REJECT>"







    # reformat received data including removing carriage return, line feed, etc., and decode to string
    #data = data.strip().decode()

    #print("Request: ", data)
 #   match data:
      #  case '<BTT?>':
           # reply = GetBattLvl()

       # case '<LOG?>':
          #  reply = GetLogs()

       # case '<ADN?>':
          #  reply = GetSignctrNum()

       # case '<END>':
         #   reply = '<ACK>'
          #  session = False

      # case '<ITT?>':
         #   reply = GetCallSchedule()

       # case '<DIS>':
        #    reply = GetDisplaySystem(0)

        #case '<ALR>':
         #   reply = GetAlarmStat()

       # case '<DIP>':
        #    reply = GetDisplayVOlt()

       # case '<ESC?>':
        #    reply = GetDisplayElementCur()

#     case _:
    #        reply = 'Unknown Req'............."""""


#     szasSrv.sendall(reply.encode()) #reply to the encoded message what will be the state of the system
#
# print("Session has ended")
# def inactivity_monitor(szasSrv, last_request_time, inactivity_timeout):
#     while True:
#         current_time = time.time()
#         if inactivity_timeout > 0 and (current_time - last_request_time) > inactivity_timeout:
#             print("Closing connection due to inactivity.")
#             szasSrv.close()
#             break
#         time.sleep(1)
def main():
    # inactivity_timeout_str = Communication.GetConnectionClose()
    # inactivity_timeout = int(inactivity_timeout_str)  # Get the inactivity timeout from 'STD' value
    szasSrv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    szasSrv.connect((host, port))

    firstMsg = GetSignId() + ";" + GetStatus()
    print(firstMsg)
    szasSrv.sendall(firstMsg.encode())
    session = True

    last_request_time = time.time()

    # #Start the inactivity monitor thread
    # monitor_thread = threading.Thread(target=Communication.inactivity_monitor, args=(szasSrv, last_request_time, inactivity_timeout))
    # monitor_thread.daemon = True
    # monitor_thread.start()

    while session:
        data = szasSrv.recv(1024)
        if not data:
            continue

        inactivity_timeout_str = Communication.GetConnectionClose()
        inactivity_timeout = int(inactivity_timeout_str)
        monitor_thread = threading.Thread(target=Communication.inactivity_monitor, args=(szasSrv, last_request_time, inactivity_timeout))
        monitor_thread.daemon = True
        monitor_thread.start()
        #last_request_time = time.time()

        current_time = time.time()
        last_request_time = current_time

        reply = handle_request(data)  # Use the Communication class to handle the request

        szasSrv.sendall(reply.encode())
        print("Current Time:", current_time)
        print("Last Request Time:", last_request_time)
        print("Inactivity Timeout:", inactivity_timeout)

    monitor_thread.join()  # Wait for the inactivity monitor thread to finish
    szasSrv.close()
    print("Session has ended")

if __name__ == "__main__":
    main()




