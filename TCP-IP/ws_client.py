import asyncio
import websockets


async def client():
    async with websockets.connect("ws://localhost:8765") as ws:
        for i in range(3):
            await ws.send(f"message {i}")
            response = await ws.recv()
            print(f"[CLIENT] Got: {response}")
            await asyncio.sleep(0.5)

if __name__ == "__main__":
    asyncio.run(client())
