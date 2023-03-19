import asyncio
import websockets
from handleconnections import handle_connection


async def main():
    async with websockets.serve(handle_connection, "0.0.0.0", 8765):
        print("WebSocket server started")
        await asyncio.Future()  # Run forever

asyncio.run(main())
