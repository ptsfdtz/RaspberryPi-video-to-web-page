import asyncio
import websockets
import pygame
import json

pygame.init()

pygame.joystick.init()

if pygame.joystick.get_count() == 0:
    print("没有手柄连接")
    exit()

joystick = pygame.joystick.Joystick(0)
joystick.init()

print(f"手柄名称: {joystick.get_name()}")
print(f"轴数量: {joystick.get_numaxes()}")

async def handle_client(websocket, path):
    async for message in websocket:
        if message == "get_joystick_data":
            pygame.event.pump()
            left_stick = [joystick.get_axis(0), joystick.get_axis(1)]  # Y轴方向反转
            right_stick = [joystick.get_axis(2), joystick.get_axis(3)]  # Y轴方向反转
            triggers = [(joystick.get_axis(4) + 1) / 2, (joystick.get_axis(5) + 1) / 2]  # 转换为0到1

            data = {
                'left_stick': left_stick,
                'right_stick': right_stick,
                'triggers': triggers
            }

            await websocket.send(json.dumps(data))

start_server = websockets.serve(handle_client, "0.0.0.0", 12345)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
