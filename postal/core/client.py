import asyncio
import websockets
import json


class Client:

    def __init__(self, host, port):
        self.host = host
        self.port = port

    # call the remote function and return the servers final response as the function return value
    # all responses before the last one are "progress" updates
    def rpc(self, request):
        async def process():
            async with websockets.connect(f"ws://{self.host}:{self.port}") as websocket:
                await websocket.send(request)
                first = True
                response = None
                async for message in websocket:
                    if not first: print('progress', response)
                    first = False
                    response = message
                return response
        return asyncio.get_event_loop().run_until_complete(process())


    # proxy remote function calls for all undefined calls to dot operator eg: client.function_name
    def __getattr__(self, function):
        def proxy(*args, **kwargs):
            request = json.dumps({
                'function': function,
                'args': args,
                'kwargs': kwargs
                })
            return self.rpc(request)
        return proxy
