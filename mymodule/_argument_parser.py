
import argparse


parser = argparse.ArgumentParser(description=r"""

============
= MYMODULE =
============

This is mymodule!

""", formatter_class=argparse.RawTextHelpFormatter)

#####################
# Common arguments. #
#####################
parser.add_argument("-l", "--logging-level", dest="log_level", default="DEBUG",
                    choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
                    help="Logging level.")
parser.add_argument("-f", "--logging-file", dest="log_file", default=None,
                    help="Logging file. By default std out is use.")
parser.add_argument("-m", "--logging-message", dest="log_format", default="%(message)s",
                    help="Logging messages format. By default '%%(message)s' (only"
                         " prints the message). Use '%%(asctime)s %%(levelname)s: %%(message)s'"
                         " to get the time of each message. It uses the default logging module, for"
                         " more info: https://docs.python.org/3/library/logging.html#logrecord-attributes")

###############
# Subparsers. #
###############
subparsers = parser.add_subparsers(dest="command")
subparsers.required = True
# Tabular subparser.
tabular_parser = subparsers.add_parser("hello",
                                       help="Execute greet function.")
tabular_parser.add_argument("mandatory_arg",
                            metavar="MANDATORY_ARG",
                            help="Mandatory argument.")


def parse_args():
    return parser.parse_args()
