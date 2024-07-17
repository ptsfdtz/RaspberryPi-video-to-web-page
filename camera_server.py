import cv2
import asyncio
import websockets

async def video_stream(websocket, path):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("无法打开摄像头")
        return

    target_width = 320
    target_height = 240
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, target_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, target_height)

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("摄像头读取失败")
                break

            frame = cv2.resize(frame, (target_width, target_height))
            ret, jpeg = cv2.imencode('.jpg', frame)
            await websocket.send(jpeg.tobytes())
    finally:
        cap.release()

start_server = websockets.serve(video_stream, "192.168.10.103", 8000)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
