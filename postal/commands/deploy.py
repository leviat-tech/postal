import os
from postal.core.rpc import Proxy


help = "Deploy stack from origin repository or working dir"

def arguments(parser):
    parser.add_argument('-b', '--branch', type=str, help='deploy specific branch from origin')
    parser.add_argument('-w', '--working', action='store_true', help='deploy working directory')

def main(args=None):
    proxy = Proxy()
    if args.working:
        destination = proxy.send(os.getcwd())
        proxy.swarm_deploy(stack=args.stack, dir=destination)
    # else:
    #     proxy.swarm_deploy(destination)
