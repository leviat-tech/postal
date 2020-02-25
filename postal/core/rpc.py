import sys
import json
import uuid
from . import settings
from .utils import shell
from . import config
from . import swarm


# functions registered for rpc
registered = {
    'ping': lambda: 'ok',
    'config_dict': config.dict,
    'config_set': config.set,
    'config_get': config.get,
    'config_rm': config.rm,
    'config_load': config.load,
    'config_unload': config.unload,
    'swarm_proxy': swarm.proxy,
    'swarm_deploy': swarm.deploy,
}

# execute rpc locally (we use temporary files to allow stdin stdout and return values)
def call(cid):
    with open(f'/tmp/{cid}', 'r') as f: request = json.load(f)
    with open(f'/tmp/{cid}', 'w') as f: f.write('')
    response = registered[request['function']](*request['args'], **request['kwargs'])
    with open(f'/tmp/{cid}', 'w') as f: json.dump(response, f)

# rpc proxy
class Proxy:

    def __init__(self, user=None, host=None, port=None):
        s = settings.get()
        if not user and not s.get('user'):
            print('Not logged into remote server, unable to make remote calls. Please login.')
            sys.exit(1)
        self.user = user or s.get('user')
        self.host = host or s.get('host')
        self.port = port  or s.get('port')

    # send stack to remote
    def send(self, source):
        destination = f'/tmp/postal_stack_{uuid.uuid1()}'
        print('Uploading stack...', end=' ')
        if shell(f"scp -q -P {self.port} -r {source} {self.user}@{self.host}:{destination}"):
            print('Done.')
        else:
            print('Failed')
            sys.exit(1)
        return destination

    # call the remote function (use temporary files for input and output so we can still connect stdin and stdout)
    def rpc(self, request):
        call_id = f'postal_{uuid.uuid1()}'
        ssh = f'ssh {self.user}@{self.host} -p {self.port}'
        shell(f"{ssh} 'echo {json.dumps(request)} > /tmp/{call_id}'")
        shell(f"{ssh} 'postal call {call_id}'")
        response = shell(f" cat /tmp/{call_id}; rm /tmp/{call_id} 2> /dev/null", capture=True)
        return json.loads(response)

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
