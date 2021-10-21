import os
import sys

args = None

def warn(*msg):
    msg = "".join(map(str, msg))

    sys.stderr.write(msg + os.linesep)

def verbose(*msg):
    if args.verbose:
        warn(*msg)
