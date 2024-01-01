import socket

def send_udp_message(message, server_address, server_port):
    # Create a UDP socket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # Send the message to the server
        udp_socket.sendto(message.encode(), (server_address, server_port))

        # Receive the response from the server
        response, _ = udp_socket.recvfrom(1024)  # 1024 is the buffer size, adjust as needed

        return response.decode()
    finally:
        # Close the socket
        udp_socket.close()

if __name__ == "__main__":
    # Server address and port
    server_address = "127.0.0.1"  # Replace this with the actual server IP address
    server_port = 8007           # Replace this with the actual server UDP port

    # Send sign ID and status
    sign_id = "577-0402"
    status = "82"
    sign_status_msg = f'<SGN="{sign_id}";STS="{status}">'
    response = send_udp_message(sign_status_msg, server_address, server_port)
    print("Response:", response)

    # Request battery voltage
    battery_request_msg = "<BTT?>"
    response = send_udp_message(battery_request_msg, server_address, server_port)
    print("Response:", response)

    # Terminate session
    end_session_msg = "<END>"
    response = send_udp_message(end_session_msg, server_address, server_port)
    print("Response:", response)
