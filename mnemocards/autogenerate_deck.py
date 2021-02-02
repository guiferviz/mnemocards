"""Module for automatic generation of deck based on list of words in one language."""
import os
import json

from shutil import rmtree

from mnemocards.generate import build, save_packages


def autogenerate(args):
    if not os.path.exists(args.data_dir):
        raise Exception("Data dir does not exist")
    packages = build(args)
    save_packages(packages, args.output_dir)
    media_path = os.path.join(args.data_dir, ".media")
    if os.path.exists(media_path):
        rmtree(media_path)
