from __future__ import print_function

import sys

from detox import __version__
from detox.proc import Detox


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    if args and args[0] == "--version":
        print("detox {} running as plugin in tox:".format(__version__))
    config = parse(args)
    detox = Detox(config)
    if not hasattr(config.option, "quiet_level") or not config.option.quiet_level:
        detox.startloopreport()
    return detox.runtestsmulti(config.envlist)


def parse(args):
    from tox.session import prepare

    return prepare(args)
