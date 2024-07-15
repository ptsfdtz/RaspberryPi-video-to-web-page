import cv2
import socket
import struct
import pickle
import numpy as np

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(('192.168.10.103', 8000)) 

data = b""
payload_size = struct.calcsize("<L")

try:
    while True:
        while len(data) < payload_size:
            packet = client_socket.recv(4096)
            if not packet:
                break
            data += packet
        
        packed_msg_size = data[:payload_size]
        data = data[payload_size:]
        msg_size = struct.unpack("<L", packed_msg_size)[0]

        while len(data) < msg_size:
            packet = client_socket.recv(4096)
            if not packet:
                break   
            data += packet
        
        frame_data = data[:msg_size]
        data = data[msg_size:]

        frame = pickle.loads(frame_data)

        cv2.imshow('Received Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    client_socket.close()
    cv2.destroyAllWindows()
