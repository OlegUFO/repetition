import asyncio
import websockets


async def handler(websocket):
    print(f"[SERVER] Client connected: {websocket.remote_address}")
    try:
        async for message in websocket:
            print(f"[SERVER] Received: {message}")
            await websocket.send(f"echo: {message}")
    except websockets.ConnectionClosed:
        print(f"[SERVER] Client disconnected")

async def main():
    async with websockets.serve(handler, "localhost", 8765):
        print(f"[SERVER] Started on ws://localhost:8765")
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
