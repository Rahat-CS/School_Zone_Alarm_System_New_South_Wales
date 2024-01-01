import socket

def handle_udp_message(message):
    if message.startswith("<BTT?>"):
        # Handle battery voltage request
        return '<BTT="12.52">'

    # Add more handling logic for other messages if needed

    # If the message is unknown or not supported
    return 'Unknown Request'

def udp_server(server_port):
    # Create a UDP socket
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Bind the socket to the specified port
    udp_socket.bind(('', server_port))

    print("UDP Server started. Listening on port", server_port)

    while True:
        data, addr = udp_socket.recvfrom(1024)  # 1024 is the buffer size, adjust as needed

        # Decode the received data
        message = data.decode()

        print("Received message:", message)

        # Handle the received message
        response = handle_udp_message(message)

        # Send the response back to the client
        udp_socket.sendto(response.encode(), addr)

if __name__ == "__main__":
    # Server port to listen on
    server_port = 10080

    udp_server(server_port)
