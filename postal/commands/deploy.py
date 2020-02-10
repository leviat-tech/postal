import sys
from postal import settings
from postal.utils import shell


help = "Deploy stack from origin repository or working dir"

def arguments(parser):
    parser.add_argument('-b', '--branch', type=str, help='deploy specific branch from origin')
    parser.add_argument('-w', '--working', action='store_true', help='deploy working directory')

def main(args=None):
    print('config', args)
