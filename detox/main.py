import sys

from detox.proc import Detox


def parse(args):
    from tox.session import prepare
    return prepare(args)


def main(args=None):
    if args is None:
        args = sys.argv[1:]
    config = parse(args)
    detox = Detox(config)
    detox.startloopreport()
    retcode = detox.runtestsmulti(config.envlist)
    raise SystemExit(retcode)
