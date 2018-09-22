from __future__ import print_function

import sys

from detox import __version__
from detox.proc import Detox


def parse(args):
    from tox.session import prepare
    return prepare(args)


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    if args and args[0] == "--version":
        print("detox {}".format(__version__))
        return
    config = parse(args)
    detox = Detox(config)
    detox.startloopreport()
    retcode = detox.runtestsmulti(config.envlist)
    raise SystemExit(retcode)
