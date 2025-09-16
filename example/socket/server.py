#Simple server on Python

import socket
import sys
import signal

print("START SERVER")

#CTRL+C handler
def handle_stop(signum, frame):
    print("STOP SERVER")
    sys.exit(0)

signal.signal(signal.SIGINT, handle_stop)

#define port number
port = 5000

#create and bind socket
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.bind(("0.0.0.0", port))

#start listen
my_socket.listen()

MESSAGE = "HELLO FROM SERVER"

#start data transmission
while True:
        # wait connection from C-client
        client_socket, address = my_socket.accept()

        print(f"Connection from: {address}")

        while True:
                #get data from client
                data = client_socket.recv(1024)

                if len(data) != 0:
                        print(f"RECEIVED FROM CLIENT: {data.decode()}")

                #send response
                client_socket.sendall(MESSAGE.encode('utf-8'))
