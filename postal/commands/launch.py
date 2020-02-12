from postal.settings import config
from postal.utils import shell


help = "Rebuild and restart stack"

def arguments(parser):
    pass

def main(args):
    shell(f'docker-compose -p {config["stack"]} -f {config["compose"]} down --remove-orphans')
    shell(f'docker-compose -p {config["stack"]} -f {config["compose"]} build')
    shell(f'docker-compose -p {config["stack"]} -f {config["compose"]} up -d --force-recreate')
