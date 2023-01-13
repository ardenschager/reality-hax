
import asyncio
import json
import websockets

import text2emotion as te

async def handle_websocket(websocket, path):
    try:
        # sync server game state to newly connected game client
        await websocket.send('connected')
        print('connected to' + str(websocket.id))
        # route and handle messages for duration of websocket connection
        async for message in websocket:
            response = {
                "word": message,
                "scores": te.get_emotion(message)
            }
            
            websocket.send(await websocket.send(json.dumps(response)))
    finally:
        # upon websocket disconnect remove client's player
        print("disconnected")

async def main():
    async with websockets.serve(
		handle_websocket,
		host="0.0.0.0", 
		port=8080,
	):
        await asyncio.Future()

asyncio.run(main())