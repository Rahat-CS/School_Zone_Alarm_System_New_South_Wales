import socket
import threading
from communication import Communication

def handle_tcp_connection(connection, address):
    print("TCP connection established with:", address)

    response = "Sign ID=577-0402, Status Word=82"
    connection.send(response.encode())
    connection.close()

def main():
    cmc_ip = "127.0.0.1"  # Replace with the actual CMC IP address
    cmc_port = 10080
    sign_port = 8007

    # Simulate CMC sending UDP trigger message
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.sendto(f"{cmc_ip} {sign_port}".encode(), (cmc_ip, cmc_port))
    udp_socket.close()

    # Start TCP server in a separate thread
    sign_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sign_socket.bind(("0.0.0.0", sign_port))
    sign_socket.listen(1)

    tcp_thread = threading.Thread(target=handle_tcp_connection, args=(sign_socket.accept()))
    tcp_thread.start()

    print("Waiting for TCP connection...")

if __name__ == "__main__":
    main()
