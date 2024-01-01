# hex_data = "016019bd503aff0ffc3ff0ffc3ff0ffc3ff0ffc3f"
#
# # Extract the number of timetable segments
# num_segments = int(hex_data[0:2], 16)
#
# segments = []
# start = 2  # Start index for the segment data
#
# # Loop through each segment
# for _ in range(num_segments):
#     segment = {}
#
#     # Extract the absolute start time for the timetabled operation
#     abs_start_time = hex_data[start:start+8]
#     segment["abs_start_time"] = abs_start_time
#
#     start += 8
#
#     # Extract the number of calendar entries
#     num_entries = int(hex_data[start:start+2], 16)
#     segment["num_entries"] = num_entries
#
#     start += 2
#
#     # Calculate the number of hex digits needed for calendar entries
#     num_hex_digits = num_entries * 2
#
#     # Extract the calendar entries (enablement bits)
#     entries_hex = hex_data[start:start+num_hex_digits]
#
#     # Convert hex entries to binary
#     entries_binary = bin(int(entries_hex, 16))[2:].zfill(num_entries * 8)  # Convert to binary and pad with zeros
#     segment["entries_binary"] = entries_binary
#
#     start += num_hex_digits
#
#     segments.append(segment)
#
# # Print the extracted information
# for i, segment in enumerate(segments, start=1):
#     print(f"Segment {i}:")
#     print("Absolute Start Time:", segment["abs_start_time"])
#     print("Number of Calendar Entries:", segment["num_entries"])
#     print("Calendar Entries (Enablement bits):", segment["entries_binary"])
#     print()
# hex_data = "016019bd503aff0ffc3ff0ffc3ff0ffc3ff0ffc3f615b6b504a0ffc3ff0ffc3ff0ffc3ff0ffc3ff0ffc3ff0ff"
#
# # Extract the number of timetable segments
# num_segments = int(hex_data[0:2], 16)
#
# segments = []
# start = 2  # Start index for the segment data
#
# # Loop through each segment
# for _ in range(num_segments):
#     segment = {}
#
#     # Extract the absolute start time for the timetabled operation
#     abs_start_time = hex_data[start:start+8]
#     segment["abs_start_time"] = abs_start_time
#
#     start += 8
#
#     # Extract the number of calendar entries
#     num_entries = int(hex_data[start:start+2], 16)
#     segment["num_entries"] = num_entries
#
#     start += 2
#
#     # Calculate the number of hex digits needed for calendar entries
#     num_hex_digits = num_entries * 2
#
#     # Extract the calendar entries (enablement bits)
#     entries_hex = hex_data[start:start+num_hex_digits]
#
#     # Convert hex entries to binary
#     entries_binary = bin(int(entries_hex, 16))[2:].zfill(num_entries * 2)  # Convert to binary and pad with zeros
#     segment["entries_binary"] = entries_binary
#
#     start += num_hex_digits
#
#     segments.append(segment)
#
# # Print the extracted information
# for i, segment in enumerate(segments, start=1):
#     print(f"Segment {i}:")
#     print("Absolute Start Time:", segment["abs_start_time"])
#     print("Number of Calendar Entries:", segment["num_entries"])
#     print("Calendar Entries (Enablement bits):", segment["entries_binary"])
#     print()
# def print_calendar(segment_number, start_time, num_days, hex_data):
#     print(f"Segment {segment_number} Calendar:")
#     print(f"Start Time: {start_time}")
#     print(f"Number of Days: {num_days}")
#     print(f"Hex Data: {hex_data}")
#     print()
#
# def process_hex_string(hex_string):
#     hex_bytes = bytes.fromhex(hex_string)
#     total_segments = hex_bytes[0]
#
#     index = 1
#     for segment_number in range(total_segments):
#         start_time = int.from_bytes(hex_bytes[index:index+4], byteorder='big')
#         index += 4
#
#         num_days = hex_bytes[index]
#         index += 1
#
#         num_digits = (num_days +2)// 4
#         segment_data = hex_bytes[index:index+num_digits].hex().upper()
#         index += num_digits
#
#         print_calendar(segment_number + 1, start_time, num_days, segment_data)
#
# if __name__ == "_main_":
#     hex_string = "036019bd503a0ff0ffc3ff0ffc3ff0ffc3ff0ffc3f607cabe098ffc3ff0ffc3fff0ffc3ff0ffc3ff0ffc3ff00000000ffc3fc0ffc3ff0ffc3ff0ffc3ff0ffc3f615b6b504a0ffc3ff0ffc3ff0ffc3ff0ffc3ff0ffc3ff0"
#     process_hex_string(hex_string)
# def print_calendar(segment_number, start_time, num_days, hex_data):
#     print(f"Segment {segment_number} Calendar:")
#     print(f"Start Time: {start_time}")
#     print(f"Number of Days: {num_days}")
#     print(f"Hex Data: {hex_data}")
#     print()
#
# def process_hex_string(hex_string):
#     hex_bytes = bytes.fromhex(hex_string)
#     total_segments = hex_bytes[0]
#
#     index = 1
#     for segment_number in range(total_segments):
#         start_time = int.from_bytes(hex_bytes[index:index+4], byteorder='big')
#         index += 4
#
#         num_days = hex_bytes[index]
#         index += 1
#
#         num_digits = (num_days +2)// 4
#         segment_data = hex_bytes[index:index+num_digits].hex().upper()
#         index += num_digits
#
#         print_calendar(segment_number + 1, start_time, num_days, segment_data)
#
# if __name__ == "_main_":
#     hex_string = "036019bd503a0ff0ffc3ff0ffc3ff0ffc3ff0ffc3f607cabe098ffc3ff0ffc3fff0ffc3ff0ffc3ff0ffc3ff00000000ffc3fc0ffc3ff0ffc3ff0ffc3ff0ffc3f615b6b504a0ffc3ff0ffc3ff0ffc3ff0ffc3ff0ffc3ff0"
#     process_hex_string(hex_string)
# def print_calendar(segment_number, start_time, num_days, hex_data,binary_data):
#     print(f"Segment {segment_number} Calendar:")
#     print(f"Start Time: {start_time}")
#     print(f"Number of Days: {num_days}")
#     print(f"Hex Data: {hex_data}")
#     print(f"Binary Conversion of Calendar:{binary_data}")
#     print()
#
# def process_hex_string(hex_string):
#     hex_bytes = bytes.fromhex(hex_string)
#     total_segments = hex_bytes[0]
#
#     index = 1
#     for segment_number in range(total_segments):
#         start_time = int.from_bytes(hex_bytes[index:index+4], byteorder='big')
#         index += 4
#
#         num_days = hex_bytes[index]
#         index += 1
#
#         num_digits = (num_days + 2) // 4
#         segment_data = hex_string[index*2:index*2+num_digits*2].upper()
#         segment_data_binary = bin(int(segment_data, 16))[2:].zfill(num_digits*8)
#         index += num_digits
#
#         print_calendar(segment_number + 1, start_time, num_days, segment_data, segment_data_binary)
#
# #if __name__ == "__main__":
# hex_string = "036019bd503a0ff0ffc3ff0ffc3ff0ffc3ff0ffc3f607cabe098ffc3ff0ffc3ff0ffc3ff0ffc3ff0ffc3ff00000000ffc3fc0ffc3ff0ffc3ff0ffc3ff0ffc3ff615b6b504a0ffc3ff0ffc3ff0ffc3ff0ffc3ff0ffc3ff0ff"
# process_hex_string(hex_string)
import socket
import time
from case1 import handle_request

UDP_PORT = 10080

def GetServerIP(UDPPortNo):
    serverAddress = '192.168.101.220'  # Server Address
    return serverAddress

def GetSignId():
    signId = '577-0402'
    return signId

def GetStatus():
    status = '82'
    return status

def request_rtc_from_cmc():
    # Simulating CMC's response with a sample RTC value
    tcmc = 1520628793  # Example RTC value from CMC
    return tcmc

def adjust_rtc(tcmc, rttm, rtta, rtc):
    rtc_difference = tcmc - rtc

    if (
        rttm <= rtta
        or rtc > tcmc + (3/2) * rttm
        or rtc < tcmc - (1/2) * rttm
    ):
        rtc = tcmc + (1/2) * rttm
        rtc_difference = rtc - tcmc

    return rtc, rtc_difference

def main():
    rtcsign = 1520628793
    TCP_IP_PORT = 8007
    cmc_ip = "127.0.0.1"  # Replace with the actual CMC IP address
    cmc_port = 10080
    sign_port = 8007

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

    # RTC synchronization
    tcmc = request_rtc_from_cmc()
    rttm = tcmc - rtcsign  # Assuming you have rtcsign defined
    rtc_difference = 0

    while session:
        data = szasSrv.recv(1024)
        if not data:
            continue
        decoded_data = data.decode()

        if decoded_data == "SYN":
            reply = handle_request(decoded_data)
        elif decoded_data == "sync_rtc":
            rtc, rtc_difference = adjust_rtc(tcmc, rttm, rtta, rtc)
            reply = f"RTTM: {rttm}, RTC Difference: {rtc_difference}"
        else:
            reply = "Unknown command"

        szasSrv.sendall(reply.encode())

    szasSrv.close()

    print("Session has ended")

    # Clean up
    szasSrv.close()

if __name__ == "__main__":
    main()
