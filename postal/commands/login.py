import getpass
from postal.core import settings
from postal.core.rpc import Proxy


help = 'Login to the postal build and management server'

def arguments(parser):
    pass
    # parser.add_argument('-a', '--address', type=str, default='localhost', help='postal server address or host')
    # parser.add_argument('-p', '--port', type=str, default='8000', help='postal server port')

def main(args=None):
    # get input
    user = getpass.getuser()
    host = 'localhost'
    port = '22'
    user = input(f'Enter postal build server user (default {user}): ').strip() or user
    host = input(f'Enter postal build server host (default {host}): ').strip() or host
    port = input(f'Enter postal build server port (default {port}): ').strip() or port

    # test connection
    print(f'Connnecting to {user}@{host}:{port}')
    proxy = Proxy(user, host, port)
    try:
        if proxy.ping() == 'ok':
            print('Successfully connected to build server.')
        else:
            print('Failed to authenticate with build server.')
            return
    except Exception as exc:
        print(exc)
        print('Failed to connect to build server.')
        return

    # store config
    settings.set(user=user, host=host, port=port)
    print("Config saved.")
