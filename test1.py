import socket
import time
#from temperature_measure import get_cpu_temperature
#from battery_test import get_battery_voltage
from case1 import handle_request
 
UDP_PORT= 10080


def GetServerIP(UDPPortNo):
    serverAddress = '192.168.101.73' # Server Address
    return serverAddress

def GetSignId(): #this function pass the signature id to establish connection with CMC
    signId = '577-0402'
    return signId

def GetStatus(): #This function pass the status of the server to establish connection
    status = '82'
    return status
def server_connection():
    TCP_IP_PORT= 8007
    cmc_ip = "127.0.0.1"
    cmc_port = 10080
    sign_port = 8080

    # Simulate CMC sending UDP trigger message
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.sendto(f"{cmc_ip} {sign_port}".encode(), (cmc_ip, cmc_port))
    udp_socket.close()

    # Wait a little bit to ensure the UDP message reaches and the server starts
    time.sleep(0)

    # TCP client part
    host = GetServerIP(UDP_PORT)
    port = TCP_IP_PORT

    szasSrv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    szasSrv.connect((host, port))

    firstMsg = GetSignId() + ";" + GetStatus()
    print(firstMsg)

    szasSrv.sendall(firstMsg.encode())
    session = True
    while session:
        data = szasSrv.recv(1024)
        if not data:
            continue
        reply = handle_request(data)
        szasSrv.sendall(reply.encode())

    szasSrv.close()

    response = szasSrv.recv(1024)
    print("Received:", response.decode())

    print("Session has ended")

    # Clean up
    szasSrv.close()

if __name__ == "__main__":
    server_connection()
