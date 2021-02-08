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
        return result.stdout, 200

@app.route('/interactive', methods=['POST'])
async def interactive():
    id = str(uuid.uuid4())
    cmd = (await request.form)['command']
    coroutines[id] = asyncio.create_subprocess_exec(*shlex.split(cmd), stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    return id, 200

async def sending(process):
    response = ''
    while True:
        try:
            char = await asyncio.wait_for(process.stdout.read(1), 0.05)
            response += char.decode('utf-8')
        except asyncio.TimeoutError:
            if response:
                await websocket.send(response)
                print(response)
                response = ''

async def receiving(process):
    while True:
        data = await websocket.receive()
        process.stdin.write(data)
        await process.stdin.drain()

async def polling(process):
    await process.wait()
    raise EOFError

@app.websocket('/ws/<string:id>')
async def ws(id):
    try:
        coroutine = coroutines.pop(id, None)
        if not coroutine:
            return 'invalid id', 403
        process = await coroutine
        producer = asyncio.create_task(sending(process))
        consumer = asyncio.create_task(receiving(process))
        monitor = asyncio.create_task(polling(process))
        tasks = asyncio.gather(producer, consumer, monitor)
        await tasks
    except asyncio.CancelledError: # terminate process if websocket is closed
        process.terminate()
    except EOFError: # don't terminate process if EOFError is raised
        pass
    finally:
        tasks.cancel()
    

if __name__ == "__main__":
    app.run()