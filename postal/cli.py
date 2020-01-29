import os
import sys
import argparse


def main():
    # arguments
    parser = argparse.ArgumentParser(description='')

    # parse args and execute command
    args = parser.parse_args()
    if hasattr(args, 'cmd'):
        sys.exit(args.cmd(args))
    else:
        parser.print_help()
