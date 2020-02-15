from postal.core.client import Client


help = "Login to the postal build and management server"

def arguments(parser):
    parser.add_argument('-a', '--address', type=str, default='localhost', help='postal server address or host')
    parser.add_argument('-p', '--port', type=str, default='8000', help='postal server port')

def main(args=None):
    proxy = Client(args.address, args.port)
    print(proxy.is_even(1))
    print(proxy.is_even(2))
