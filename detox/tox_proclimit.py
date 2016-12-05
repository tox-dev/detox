import argparse
import multiprocessing

from tox import hookimpl


@hookimpl
def tox_addoption(parser):
    def positive_integer(value):
        ivalue = int(value)
        if ivalue <= 0:
            raise argparse.ArgumentTypeError(
                "%s is an invalid positive int value" % value)
        return ivalue

    parser.add_argument(
        "-n", "--num",
        type=positive_integer,
        action="store",
        default=multiprocessing.cpu_count(),
        dest="proclimit",
        help="limit the number of concurrent processes.")
