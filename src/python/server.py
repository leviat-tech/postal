import subprocess
import asyncio
from asyncio.subprocess import PIPE, STDOUT
import uuid
import pdb
import shlex
from quart import Quart, request, websocket

app = Quart(__name__)

coroutines = {}

@app.route('/run', methods=['POST'])
async def run():
    cmd = (await request.form)['command']
    result = subprocess.run(
        shlex.split(cmd),
        capture_output=True,
        text=True
    )
    if result.stderr:
        return result.stderr, 500
    else:
        print(result.stdout)
        return result.stdout, 200

@app.route('/interactive', methods=['POST'])
async def interactive():
    id = str(uuid.uuid4())
    cmd = (await request.form)['command']
    coroutines[id] = asyncio.create_subprocess_exec(*shlex.split(cmd), stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    return id, 200

async def sending(process):
    data = True
    while data:
        data = await process.stdout.read(1)
        await websocket.send(data.decode('utf-8'))
    raise EOFError

async def receiving(process):
    while True:
        data = await websocket.receive()
        process.stdin.write(data)
        await process.stdin.drain()

@app.websocket('/ws/<string:id>')
async def ws(id):
    try:
        coroutine = coroutines.pop(id, None)
        if not coroutine:
            return 'invalid id', 403
        process = await coroutine
        producer = sending(process)
        consumer = receiving(process)
        awaitables = asyncio.gather(producer, consumer)
        await awaitables
    except asyncio.CancelledError: # terminate process if websocket is closed
        process.terminate()
    except EOFError:
        websocket.close()
    finally:
        awaitables.cancel()
    

if __name__ == "__main__":
    app.run()