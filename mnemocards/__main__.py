
import logging as l

from mnemocards._argument_parser import parse_args
from mnemocards import greet


def set_logging(args):
    """Set logging parameters. """
    # Transform args.log_level string to int.
    level = getattr(l, args.log_level)
    l.basicConfig(format=args.log_format,
                  filename=args.log_file,
                  level=level)

def main():
    """Main entry point.

    This function is called when you execute the module
    (for example using `mnemocards` or `python -m mnemocards`).
    """
    args = parse_args()
    set_logging(args)

    if args.command == "hello":
        greet()


if __name__ == "__main__":
    main()
