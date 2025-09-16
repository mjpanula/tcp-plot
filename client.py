import socket
import time
import random

HOST = "172.17.38.30"  # The server's hostname or IP address
PORT = 65432  # The port used by the server

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        random_value = random.uniform(-1, 1)
        s.sendall(str(random_value).encode())
        