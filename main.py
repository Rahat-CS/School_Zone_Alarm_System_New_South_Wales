import threading
from test1 import server_connection
from battery_test import get_battery_voltage

if __name__ == "__main__":
    # Create processes for server connection and battery measurement
    server_process = multiprocessing.Process(target=server_connection)
    battery_process = multiprocessing.Process(target=get_battery_voltage)

    # Start both processes
    server_process.start()
    battery_process.start()

    # Wait for both processes to finish
    server_process.join()
    battery_process.join()

    print("Both processes have finished.")
