import socket
import struct

HOST = "0.0.0.0"  # Standard loopback interface address (localhost)
PORT = 65432  # Port to listen on (non-privileged ports are > 1023)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print(f"Connected by {addr}")
        float_values = []
        while True:
            data = conn.recv(1024)
            if not data:
                break
            # Unpack all floats from the received binary data
            for i in range(0, len(data), 4):
                if i + 4 <= len(data):
                    value = struct.unpack('!f', data[i:i+4])[0]
                    float_values.append(value)
            print(f"Received floats: {float_values}")
            