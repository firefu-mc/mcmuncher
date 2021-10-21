#!/usr/bin/env python
import argparse
import setuptools
import sys
import app
import app.submodule.trim_chunks
import app.submodule.copy_dimensions
import app.submodule.view_stats

__version__ = 4.0

submodules = {
    "trim-chunks": app.submodule.trim_chunks,
    "copy-dimensions": app.submodule.copy_dimensions,
    "view-stats": app.submodule.view_stats,
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--version", action="version", version='McMuncher ' + str(__version__))
    subparsers = parser.add_subparsers(dest="subcommand")

    for i in submodules:
        subparser = subparsers.add_parser(i, help=submodules[i].get_help())
        submodules[i].add_arguments(subparser)

    app.args = parser.parse_args()

    subcommand = app.args.subcommand
    if subcommand in submodules:
        submodules[subcommand].run()

    return

if __name__=="__main__":
    main()
