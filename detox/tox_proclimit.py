import argparse
import multiprocessing

from tox import hookimpl


@hookimpl
def tox_addoption(parser):
    def positive_integer(value):
        ivalue = int(value)
        if ivalue <= 0:
            raise argparse.ArgumentTypeError("{} must be greater 0".format(value))
        return ivalue

    try:
        num_proc = multiprocessing.cpu_count()
    except Exception:
        num_proc = 2
    parser.add_argument(
        "-n",
        "--num",
        type=positive_integer,
        action="store",
        default=num_proc,
        dest="numproc",
        help="set the number of concurrent processes " "(default {}).".format(num_proc),
    )
