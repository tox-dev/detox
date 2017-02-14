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

    num_proc = multiprocessing.cpu_count()
    parser.add_argument(
        "-n", "--num",
        type=positive_integer,
        action="store",
        default=num_proc,
        dest="numproc",
        help="set the number of concurrent processes "
             "(default %s)." % num_proc)
