help = "Manage stack's config via injected production.env file"

def arguments(root_parser):
    root_parser.set_defaults(cmd=lambda _: root_parser.print_help())
    subparsers = root_parser.add_subparsers(help='')

    # ls
    parser = subparsers.add_parser('ls', help='')
    parser.set_defaults(cmd=ls)

    # set
    parser = subparsers.add_parser('set', help='')
    parser.add_argument('name', type=str, help='')
    parser.add_argument('value', type=str, help='')
    parser.set_defaults(cmd=set)

    # get
    parser = subparsers.add_parser('get', help='')
    parser.add_argument('name', type=str, help='')
    parser.set_defaults(cmd=get)

    # unset
    parser = subparsers.add_parser('rm', help='')
    parser.add_argument('name', type=str, help='')
    parser.set_defaults(cmd=rm)

    # import
    parser = subparsers.add_parser('import', help='')
    parser.set_defaults(cmd=imprt)

    # export
    parser = subparsers.add_parser('export', help='')
    parser.set_defaults(cmd=export)

def main(args=None):
    pass

def ls(args):
    proxy = Client(args.address, args.port)
    print(proxy.is_even(1))
    print(proxy.is_even(2))

def set(args):
    print('set')

def get(args):
    print('get')

def rm(args):
    print('rm')

def imprt(args):
    print('import')

def export(args):
    print('export')
