import asyncio
import websockets

async def handle_connection(websocket, path):
    print("New WebSocket connection:", websocket)

    while True:
        message = await websocket.recv()
        print("Received message:", message)

        response = "Hello from the Python server!"
        await websocket.send(response)

async def start_server():
    async with websockets.serve(handle_connection, "localhost", 8000):
        print("WebSocket server listening on ws://localhost:8000")

    await asyncio.Future()

asyncio.run(start_server())
