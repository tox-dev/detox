import sys
import argparse
import py
import detox
from detox.proc import Detox

def parse(args):
    from tox.session import prepare
    return prepare(args)

def main(args=None):
    if args is None:
        args = sys.argv[1:]
    config = parse(args)
    #now = py.std.time.time()
    detox = Detox(config)
    detox.startloopreport()
    retcode = detox.runtestsmulti(config.envlist)
    #elapsed = py.std.time.time() - now
    #cumulated = detox.toxsession.report.cumulated_time
    #detox.toxsession.report.line(
    #    "detox speed-up: %.2f (elapsed %.2f, cumulated %.2f)" % (
    #        cumulated / elapsed, elapsed, cumulated), bold=True)
    return retcode
