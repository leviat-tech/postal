import os
from .utils import shell


def proxy(args):
    return shell(f'docker {" ".join(args)}')

def deploy(stack, dir=None, repo=None):
    if dir:
        compose = 'stack/production.yml'
        shell(f'cd {dir} && docker-compose -p {stack} -f {compose} build')
        shell(f'cd {dir} && docker-compose -p {stack} -f {compose} push')
        shell(f'cd {dir} && docker stack deploy --with-registry-auth -c {compose} {stack}')
        shell(f'rm -rf {dir}', silent=True)
