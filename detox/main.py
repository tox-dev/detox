import sys
import argparse
import py
import detox
from detox.proc import Detox

def parse(args):
    import tox._config
    return tox._config.parseconfig(args, "detox")

def main(args=None):
    if args is None:
        args = sys.argv[1:]
    config = parse(args)
    detox = Detox(config)
    detox.runtestsmulti(config.envlist)
