import asyncio
import websockets
import json

async def receive_joystick_data():
    async with websockets.connect('ws://192.168.10.103:12345') as websocket:
        await websocket.send("get_joystick_data")
        data = await websocket.recv()
        joystick_data = json.loads(data)
        print("左摇杆:", joystick_data['left_stick'])
        print("右摇杆:", joystick_data['right_stick'])
        print("扳机:", joystick_data['triggers'])

asyncio.get_event_loop().run_until_complete(receive_joystick_data())
