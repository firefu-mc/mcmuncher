#!/usr/bin/env python
import argparse
import setuptools
import sys
import mcfirefu
import mcfirefu.submodule.trim_chunks
import mcfirefu.submodule.view_stats

__version__ = 4.0

submodules = {
    "trim-chunks": mcfirefu.submodule.trim_chunks,
    "view-stats": mcfirefu.submodule.view_stats,
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", action="version", version='McMuncher ' + str(__version__))
    subparsers = parser.add_subparsers(dest="subcommand")

    for i in submodules:
        subparser = subparsers.add_parser(i, help=submodules[i].get_help())
        submodules[i].add_arguments(subparser)

    mcfirefu.args = parser.parse_args()

    subcommand = mcfirefu.args.subcommand
    if subcommand in submodules:
        submodules[subcommand].run()

    return

if __name__=="__main__":
    main()
