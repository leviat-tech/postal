from postal.core.rpc import Proxy

help = "Manage stack's config via injected production.env file"

def arguments(root_parser):
    root_parser.set_defaults(cmd=lambda _: root_parser.print_help())
    subparsers = root_parser.add_subparsers(help='')

    # ls
    parser = subparsers.add_parser('ls', help='')
    parser.set_defaults(cmd=lambda args: Proxy().config_ls(args.stack))

    # set
    parser = subparsers.add_parser('set', help='')
    parser.add_argument('name', type=str, help='')
    parser.add_argument('value', type=str, help='')
    parser.set_defaults(cmd=lambda args: Proxy().config_set(args.stack, args.name, args.value))

    # get
    parser = subparsers.add_parser('get', help='')
    parser.add_argument('name', type=str, help='')
    parser.set_defaults(cmd=lambda args: Proxy().config_get(args.stack, args.name))

    # unset
    parser = subparsers.add_parser('rm', help='')
    parser.add_argument('name', type=str, help='')
    parser.set_defaults(cmd=lambda args: Proxy().config_rm(args.stack, args.name))

    # import
    parser = subparsers.add_parser('import', help='')
    parser.set_defaults(cmd=lambda args: Proxy().config_load(args.stack))

    # export
    parser = subparsers.add_parser('export', help='')
    parser.set_defaults(cmd=lambda args: Proxy().config_unload(args.stack))

def main(args=None):
    pass
