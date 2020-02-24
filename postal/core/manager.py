from .utils import shell


def proxy(args):
    return shell(f'docker {" ".join(args)}')
