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
print(f"按钮数量: {joystick.get_numbuttons()}")

async def handle_client(websocket, path):
    async for message in websocket:
        if message == "get_button_state":
            pygame.event.pump()
            button_states = {
                'button_0': joystick.get_button(0),
                'button_1': joystick.get_button(1),
                'button_2': joystick.get_button(2),
                'button_3': joystick.get_button(3),
                'button_4': joystick.get_button(4),
                'button_5': joystick.get_button(5),
                'button_6': joystick.get_button(6),
                'button_7': joystick.get_button(7)
            }
            await websocket.send(json.dumps(button_states))

start_server = websockets.serve(handle_client, "192.168.10.103", 8000)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
