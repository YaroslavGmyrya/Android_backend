import socket
import json
import sys
import signal

#CTRL+C handler
def handle_stop(signum, frame):
    print("Stop server")
    sys.exit(0)

print("Start server")

signal.signal(signal.SIGINT, handle_stop)

#define port number
port = 5000

#create and bind socket
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.bind(("0.0.0.0", port))

#start listen
my_socket.listen()

location_history = []

#start data transmission
while True:
        #wait connection from Kotlin-client
        client_socket, address = my_socket.accept()
        print(f"Connection from: {address}")

        while True:
                #receive data
                data = client_socket.recv(1024)

                if len(data) != 0:
                        location_history.append(json.loads(data))
                        print(f"Received: {data.decode()}")

