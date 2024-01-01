# server_connection.py

import socket
import time
from case import handle_request  # Import your handle_request function from the case module

UDP_PORT = 10080

def GetServerIP(UDPPortNo):
    serverAddress = '1921.168.101.231'  # Replace with your actual server IP
    return serverAddress

def GetSignId():
    signId = '577-0402'  # Replace with your sign ID
    return signId

def GetStatus():
    status = '82'  # Replace with your desired status
    return status

def main():
    TCP_IP_PORT = 8080
    cmc_ip = "127.0.0.1"  # Replace with your CMC IP
    cmc_port = 10080  # Replace with your CMC port
    sign_port = 8080  # Replace with your sign port

    # Simulate CMC sending UDP trigger message
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.sendto(f"{cmc_ip} {sign_port}".encode(), (cmc_ip, cmc_port))
    udp_socket.close()

    # Wait a little bit to ensure the UDP message reaches and the server starts
    time.sleep(5)

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
        reply = handle_request(data)  # Call the handle_request function from your case module
        szasSrv.sendall(reply.encode())

    szasSrv.close()

#if __name__ == "__main__":
 #   server_connection()
