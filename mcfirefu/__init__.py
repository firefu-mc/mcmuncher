import argparse
import os
import sys
from mcfirefu.pathtype import PathType

__version__ = 3.0

args = None

def warn(*msg):
    msg = "".join(map(str, msg))

    sys.stderr.write(msg + os.linesep)

def verbose(*msg):
    if args.verbose:
        warn(*msg)

def parse_args() -> argparse.Namespace:
    global args

    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", type=PathType(exists=True, type='dir'), metavar='DIR', help="Path to world directory")
    parser.add_argument("--bedrock", action=argparse.BooleanOptionalAction, help="List Bedrock game worlds, and prompt for selection")
    parser.add_argument("--keep-overworld", type=argparse.FileType('r', encoding='UTF-8'), metavar="FILE")
    parser.add_argument("--keep-nether", type=argparse.FileType('r', encoding='UTF-8'), metavar="FILE")
    parser.add_argument("--keep-end", type=argparse.FileType('r', encoding='UTF-8'), metavar="FILE")
    parser.add_argument("--dryrun", action=argparse.BooleanOptionalAction, help="Print what would happen, but don't save the changes")
    parser.add_argument("--verbose", action=argparse.BooleanOptionalAction, help="Print lots of information about which chunks are being selected")
    parser.add_argument("--version", action="version", version='McMuncher ' + str(__version__))
    args = parser.parse_args()

    if not args.directory and not args.bedrock:
        warn("error: Require 1 of --directory=DIR or --bedrock")
        parser.print_help()
        sys.exit(1)

    if args.directory and args.bedrock:
        warn("error: Cannot provide both --directory=DIR and --bedrock")
        parser.print_help()
        sys.exit(1)

    if not args.keep_overworld and not args.keep_nether and not args.keep_end:
        warn("error: Require at least 1 of --keep-overworld=FILE, --keep-nether=FILE or --keep-end=FILE options\n")
        parser.print_help()
        sys.exit(1)

    return
