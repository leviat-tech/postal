import json
import asyncio
import websockets


class Server:

    def __init__(self, address, port):
        self.address = '127.0.0.1' if address == 'localhost' else address # websockets ipv6 workaround
        self.port = port
        self.functions = {}

    def register(self, function, name):
        self.functions[name] = function

    async def handle(self, websocket, path):
        data = json.loads(await websocket.recv())
        async def send(v):
            return await websocket.send(json.dumps(v))
        # result = await self.functions[data['function']](*data['args'], **data['kwargs'], update=send)
        result = self.functions[data['function']](*data['args'], **data['kwargs'])
        await send(result)

    def serve(self):

        server = websockets.serve(self.handle, self.address, self.port)
        asyncio.get_event_loop().run_until_complete(server)
        asyncio.get_event_loop().run_forever()
