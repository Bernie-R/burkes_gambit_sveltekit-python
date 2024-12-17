# server/server.py
import asyncio
import websockets
from handleconnections import handle_connection

async def main():
    async with websockets.serve(handle_connection, "0.0.0.0", 8765, ping_interval=20, ping_timeout=20, close_timeout=5):
        print("WebSocket server started")
        await asyncio.Future()  # run forever

asyncio.run(main())
