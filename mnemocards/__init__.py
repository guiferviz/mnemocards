"""Mnemocards.

Mnemocards sort description.
"""

import os

from mnemocards._version import __version__
from mnemocards.any2dict import Reader
from mnemocards.any2dict import add_reader


__author__ = "guiferviz"
__package_dir__ = os.path.dirname(os.path.abspath(__file__))
ASSETS_DIR = os.path.abspath(os.path.join(__package_dir__, "assets"))


def greet():
    """Print a silly sentence. """

    print("In addition to helping you memorize, this code helps you do other "
          "things that I don't remember")
