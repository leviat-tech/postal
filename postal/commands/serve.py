from postal.core.server import Server


help = "Start the postal build and management server"


async def count(value, update=None):
    for v in range(value):
        await update(v)
    return value

def ping():
    return True

def arguments(parser):
    parser.add_argument('-a', '--address', type=str, default='localhost', help='address to listen on')
    parser.add_argument('-p', '--port', type=int, default=8000, help='port to listen on')

def main(args=None):
    server = Server(args.address, args.port)
    server.register(ping, 'ping')
    server.serve()
