from __future__ import print_function

import sys

from tox.session import prepare as tox_prepare

from detox import __version__
from detox.proc import Detox


def main(args=None):
    args = sys.argv[1:] if args is None else args
    if args and args[0] == "--version":
        print("detox {} running as plugin in tox:".format(__version__))
        # fall through to let tox add its own version info ...
    config = tox_prepare(args)
    detox = Detox(config)
    if not hasattr(config.option, "quiet_level") or not config.option.quiet_level:
        detox.startloopreport()
    return detox.runtestsmulti(config.envlist)
