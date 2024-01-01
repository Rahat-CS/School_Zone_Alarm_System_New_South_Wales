import socket
import sys

#TSI-SP-084 Issue 1.0

#Section 2.4.2 Default TCP PORT
TCP_IP_PORT = 8007
#Section 2.4.5 Default UDP PORT
UDP_PORT = 10080
#Sign ID
SIGN_ID = "8"


"""-------------------------------------------------------
Name: GetServerIP
This function listens to a given UDP Port passed as parameter
Once it receives a message, it will return the IP address of the sender

:param UDPPortNo: port no to listen to
:return: IP Address of the server
-------------------------------------------------------"""
def GetServerIP (UDPPortNo):
    serverAddress = '127.0.0.1'
     
    return serverAddress

def GetSignId():
    signId = '577-0402'
    return signId


def GetStatus():
    status = '82'
    return status

def GetBattLvl():
    battLvl = '12.52'
    return battLvl

def GetLogs():
    logs = 'Nothing Alarms'
    return logs

def GetSignctrNum():
    GetSignctrNum = "80000136"
    return GetSignctrNum

# Get TCP/IP Server Address
host = GetServerIP(UDP_PORT)
port = TCP_IP_PORT  # The port used by the server

szasSrv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
szasSrv.connect((host, port))

firstMsg = GetSignId() + ";" + GetStatus()

print(firstMsg)

szasSrv.sendall(firstMsg.encode())
session = True

while session:
    data = szasSrv.recv(1024)
    reply = "Error"

    # reformat received data including removing carriage return, line feed etc and decode to string
    data = data.strip().decode()
    
    print ("Request: ", data)
    match data:
        case '<BTT?>':
            reply = GetBattLvl()
            
        case '<LOG?>':
            reply = GetLogs()
 
        case '<ADN?':
            reply = GetSignctrNum()
            
        case '<END>':
            reply = '<ACK>'
            session = False
            
        case _:
            reply = 'Uknown Req'
    szasSrv.sendall(reply.encode())
   
print("Session has ended")



# Establish Connection

# Wait for Message from Server
class SigncontrollerNum:
    def __init__(self, tag, response):
        self.tag = tag
        self.response = response
        