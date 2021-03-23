import argparse
import requests
import sys
import json

parser = argparse.ArgumentParser()
parser.add_argument("command", help="command to run", type=str)
parser.add_argument("-p", "--port", help="port to send request to", type=int, required=True)
parser.add_argument("-i", "--interactive", help="start an interactive process", action="store_true")
args = parser.parse_args()

data = json.dumps({'command': args.command, 'port': args.port})
headers = {'content-type': 'application/json'}

if not args.interactive:
    r = requests.post('http://localhost:8080/run', data=data, headers=headers)
    print(r.text)
    sys.exit()

import asyncio
import websockets
import tty

tty.setraw(sys.stdin.fileno())

async def connect_stdin_stdout():
    # https://stackoverflow.com/questions/64303607/python-asyncio-how-to-read-stdin-and-write-to-stdout
    loop = asyncio.get_event_loop()
    reader = asyncio.StreamReader()
    protocol = asyncio.StreamReaderProtocol(reader)
    await loop.connect_read_pipe(lambda: protocol, sys.stdin)
    w_transport, w_protocol = await loop.connect_write_pipe(asyncio.streams.FlowControlMixin, sys.stdout)
    writer = asyncio.StreamWriter(w_transport, w_protocol, reader, loop)
    return reader, writer

async def sending(websocket, reader):
    while True:
        data = await reader.read(1)
        await websocket.send(data)

async def receiving(websocket, writer):
    while True:
        message = await websocket.recv()
        writer.write(bytearray(message, 'utf-8'))
        await writer.drain()

response = requests.post('http://localhost:8080/interactive', data=data, headers=headers)

async def interactive_process(process_id):
    uri = "ws://localhost:8080/ws/" + process_id + '?port=' + str(args.port)
    reader, writer = await connect_stdin_stdout()
    try:
        async with websockets.connect(uri) as websocket:
            print('hey')
            producer = sending(websocket, reader)
            consumer = receiving(websocket, writer)
            awaitables = asyncio.gather(producer, consumer)
            await awaitables
    except websockets.ConnectionClosed:
        print('connection closed')
        writer.close()
        awaitables.cancel()

asyncio.run(interactive_process(response.text))