import sys
from argparse import ArgumentParser
from . import commands
from .utils import proxy
from .settings import config


def main():

    # arguments
    help = """*All unmatched commands are proxied to docker compose with configured compose file selected*"""
    description = 'A light Docker control tool designed around compose and swarm'
    parser = ArgumentParser(description=description)
    parser.add_argument('-s', '--stack', type=str, help='specify the stack name (defaults to current folder)')
    subparsers = parser.add_subparsers(help=help)

    # development commands
    commands.register(subparsers, 'launch', commands.launch)
    commands.register(subparsers, 'enter', commands.enter)

    # swarm commands
    commands.register(subparsers, 'config', commands.config)
    commands.register(subparsers, 'deploy', commands.deploy)

    # proxied compose commands
    commands.register(subparsers, 'up', commands.compose, help='[Proxy] Bring docker compose stack up')
    commands.register(subparsers, 'down', commands.compose, help='[Proxy] Bring docker compose stack down')
    commands.register(subparsers, 'logs', commands.compose, help='[Proxy] Show docker logs for service')
    commands.register(subparsers, 'help', commands.compose, help='[Proxy] Show docker compose help')

    # commands.register(subparsers, 'remote', commands.deploy) # run remote commands on swarm? enter remote container?
    # commands.register(subparsers, 'track', commands.deploy) # remote stack logs?

    # management commands
    # commands.register(subparsers, 'serve', commands.serve)
    #commands.register(subparsers, 'login', commands.login)



    # proxy
    if proxy(parser): sys.exit(commands.compose.main())

    # parse args
    args = parser.parse_args()

    # execute command
    if hasattr(args, 'cmd'):
        sys.exit(args.cmd(args))
    else:
        parser.print_help()
