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
port = 3500

#create and bind socket
my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
my_socket.bind(("0.0.0.0", port))

#start listen
my_socket.listen()

location_history = []

# conn = psycopg2.connect(dbname="android_db", user="postgres", password="postgres", host="127.0.0.1", port="5432")

# cur = conn.cursor()

# cur.execute("SELECT version();")

# version = cur.fetchone()
# print(version)
# cur.close()
# conn.close()

# start data transmission
while True:
        #wait connection from Kotlin-client
        client_socket, address = my_socket.accept()
        print(f"Connection from: {address}")

        while True:
                #receive data
                data = client_socket.recv(4096)

                if len(data) != 0:
                        location_history.append(json.loads(data))
                        print(f"Received: {data.decode()}")
