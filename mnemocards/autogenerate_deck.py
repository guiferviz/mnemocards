"""Module for automatic generation of deck based on list of words in one language."""
import os
import json

from mnemocards.generate import build, save_packages


def autogenerate(args):
    if not os.path.exists(args.data_dir):
        raise Exception("Data dir does not exist")
    packages = build(args)
    save_packages(packages, args.output_dir)
    print("Writing packages to a file...")
