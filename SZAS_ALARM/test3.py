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
print(CTD)
STD = int(data['STD'])  # Connection Timeout in seconds
print(STD)
TMO = int(data['TMO'])
print(TMO)

def GetSignId():
    signId = '577-0402'
    return signId

def GetStatus():
    status = '82'
    return status

try:
    # UDP communication to obtain server IP
    udp_send_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_send_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    broadcast_address = ('<broadcast>', 10080)
    message = "Hello, Server!"
    udp_send_socket.sendto(message.encode(), broadcast_address)

    udp_listen_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_listen_socket.bind(('', 10080))
    data, server_address = udp_listen_socket.recvfrom(1024)
    server_ip, server_port = server_address
    print(f"Received response from {server_ip}:{server_port}: {data.decode()}")
    print(server_address)

    # Save the server IP in response.json under key 'CMC'
    key = "CMC"  # Choose a key for the JSON data
    value = server_ip

    if os.path.exists('response.json'):
        with open('response.json', 'r') as json_file:
            existing_data = json.load(json_file)
    else:
        existing_data = {}

    existing_data[key] = value

    with open('response.json', 'w') as json_file:
        json.dump(existing_data, json_file, indent=4)

except Exception as e:
    print(f"Error: {e}")
    
def main():
    sign_port = 8007

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

            last_activity_time = time.time()  # Initialize the time for checking inactivity

            while session:
                rlist, _, _ = select.select([szasSrv], [], [], STD)
                if szasSrv in rlist:
                    data = szasSrv.recv(1024)
                    if not data:
                        continue

                    last_activity_time = time.time()  # Update the last activity time
                    reply = handle_request(data)
                    szasSrv.sendall(reply.encode())
                    if '<END>' in data.decode():
                        print("Ending the session")
                        szasSrv.close()
                        session = False
                else:
                    # Calculate elapsed time since the connection attempt started
                    elapsed_time = time.time() - start_time

                    if elapsed_time > TMO:
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
            time.sleep(CTD)  # Implement the CTD before retrying

if __name__ == "__main__":
    main()
