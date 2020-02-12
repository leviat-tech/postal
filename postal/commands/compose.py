import sys
from postal.settings import config
from postal.utils import shell


help = "Proxy a docker compose command"

def arguments(parser):
    pass

def main(args=None):
    sys.exit(shell(f'docker-compose -p {config["stack"]} -f {config["compose"]} {" ".join(sys.argv[1:])}'))
