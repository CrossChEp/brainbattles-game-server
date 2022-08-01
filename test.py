import websockets
import asyncio


async def listen():
    token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6NX0.OqHnovtoi9i9otnRX3-XXqqeX_Y_vcQjsjidAUkwd4A'
    game_token = 'whYnT6R0zq7NkJorp1a2To2qXlgvSdGA7uMYhFUW7PAGIo'
    url = f'ws://127.0.0.1:2000/api/game?token={token}&game_token={game_token}'

    async with websockets.connect(url) as websocket:
        while True:
            msg = input()
            await websocket.send(msg)
            data = await websocket.recv()
            print(data)


if __name__ == '__main__':
    asyncio.run(listen())
