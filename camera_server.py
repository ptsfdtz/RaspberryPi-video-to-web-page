import cv2
import socket
import struct
import pickle

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('192.168.10.103', 8000))
server_socket.listen(1)

print("等待客户端连接...")
client_socket, addr = server_socket.accept()
print(f"连接来自 {addr}")

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("无法打开摄像头")
    exit()

target_width = 480
target_height = 320
cap.set(cv2.CAP_PROP_FRAME_WIDTH, target_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, target_height)

try:
    while True:
        ret, frame = cap.read()
        if not ret:
            print("摄像头读取失败")
            break

        frame = cv2.resize(frame, (target_width, target_height))

        data = pickle.dumps(frame)
        client_socket.sendall(struct.pack("<L", len(data)))
        client_socket.sendall(data)

finally:
    client_socket.close()
    server_socket.close()
    cap.release()