import asyncio
import threading
import subprocess

async def start_camera_server():
    proc = await asyncio.create_subprocess_exec(
        'python', 'camera_server.py',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    print(f'Camera server stdout: {stdout.decode()}')
    print(f'Camera server stderr: {stderr.decode()}')

async def start_joystick_server():
    proc = await asyncio.create_subprocess_exec(
        'python', 'joystick_server.py',
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await proc.communicate()
    print(f'Joystick server stdout: {stdout.decode()}')
    print(f'Joystick server stderr: {stderr.decode()}')

async def main():
    # Start camera server
    camera_task = asyncio.create_task(start_camera_server())

    # Start joystick server
    joystick_task = asyncio.create_task(start_joystick_server())

    # Wait for both servers to start
    await asyncio.gather(camera_task, joystick_task)

if __name__ == "__main__":
    asyncio.run(main())
