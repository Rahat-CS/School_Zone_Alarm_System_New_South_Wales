import socket
import time
import select
import json
from case import handle_request

UDP_PORT = 10080

with open('response.json', 'r') as file:
    data = json.load(file)

# Constants for CTD and STD
CTD = int(data['CTD'])  # Connect Time Delay in seconds
STD = int(data['STD'])  # Connection Timeout in seconds
TMO = int(data['TMO'])

def get_server_ip():
    try:
        udp_send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        broadcast_address = ('<broadcast>', 10080)
        message = "Hello, Server!"
        udp_send_socket.sendto(message.encode(), broadcast_address)

        udp_listen_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        udp_listen_socket.bind(('', 10080))
        data, server_address = udp_listen_socket.recvfrom(1024)
        server_ip, _ = server_address
        print(f"Received response from {server_ip}")
        return server_ip

    except Exception as e:
        print(f"Error fetching server IP: {e}")
        return None

def GetSignId():
    signId = '577-0402'
    return signId

def GetStatus():
    status = '82'
    return status

def main():
    server_ip = get_server_ip()
    if not server_ip:
        print("Failed to fetch server IP. Exiting...")
        return

    while True:
        try:
            start_time = time.time()

            # TCP client part
            host = server_ip
            port = 8007

            szasSrv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            szasSrv.connect((host, port))

            firstMsg = GetSignId() + ";" + GetStatus()
            print(firstMsg)

            szasSrv.sendall(firstMsg.encode())
            session = True

            last_activity_time = time.time()

            while session:
                rlist, _, _ = select.select([szasSrv], [], [], STD)
                if szasSrv in rlist:
                    data = szasSrv.recv(1024)
                    if not data:
                        continue

                    last_activity_time = time.time()
                    reply = handle_request(data)
                    szasSrv.sendall(reply.encode())
                    if '<END>' in data.decode():
                        print("Ending the session")
                        szasSrv.close()
                        session = False
                else:
                    elapsed_time = time.time() - start_time

                    if elapsed_time > STD:
                        print("Connection timed out. Closing the connection.")
                        szasSrv.close()
                        session = False
                    else:
                        print("Connection timeout. Closing the connection and attempting reconnection.")
                        szasSrv.close()
                        session = False

            print("Session has ended. Reconnecting...")
            time.sleep(CTD)

        except Exception as e:
            print(f"Error: {e}")
            print(f"Retrying connection after {CTD} seconds...")
            time.sleep(CTD)

if __name__ == "__main__":
    main()
