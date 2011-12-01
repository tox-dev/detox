import sys
import argparse
import py
import detox
from detox.proc import Detox

class VersionAction(argparse.Action):
    def __call__(self, *args, **kwargs):
        py.builtin.print_("%s imported from %s" %(detox.__version__,
                          detox.__file__))
        raise SystemExit(0)

class CountAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        if hasattr(namespace, self.dest):
            setattr(namespace, self.dest, int(getattr(namespace, self.dest))+1)
        else:
            setattr(namespace, self.dest, 0)

def parse(args):
    parser = argparse.ArgumentParser(description="detox",)
    parser.add_argument("--version", nargs=0, action=VersionAction,
        dest="version",
        help="report version information to stdout.")
    parser.add_argument("-v", nargs=0, action=CountAction, default=0,
        dest="verbosity",
        help="increase verbosity of reporting output.")
    parser.add_argument("-c", action="store", default="tox.ini",
        dest="configfile",
        help="use the specified config file.")
    parser.add_argument("-e", action="append", dest="envlist", default=[],
        metavar="env",
        help="run tests for specified environments (ALL selects all).")
    return parser.parse_args(args)

def main(args=None):
    if args is None:
        args = sys.argv[1:]
    opts = parse(args)
    toxargs = ["-e", ",".join(opts.envlist)]
    detox = Detox(py.path.local("setup.py"), toxargs)
    detox.runtestsmulti(opts.envlist)
