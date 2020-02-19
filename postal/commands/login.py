from postal.core import config
from postal.core.client import Client


help = 'Login to the postal build and management server'

def arguments(parser):
    pass
    # parser.add_argument('-a', '--address', type=str, default='localhost', help='postal server address or host')
    # parser.add_argument('-p', '--port', type=str, default='8000', help='postal server port')

def main(args=None):
    # get input
    host = input('Enter postal build server host: ')
    port = 8000
    user = input('Enter postal build server username: ')
    password = input('Enter postal build server password: ')

    # test connection
    proxy = Client(host, port)
    try:
        if proxy.ping():
            print('Successfully connected to build server.')
        else:
            print('Failed to authenticate with build server.')
            return
    except Exception as exc:
        print(exc)
        print('Failed to connect to build server.')
        return

    # store config
    config.set(host=host, port=8000, user=user)
    config.set_password(user, password)
    print("Config saved.")
