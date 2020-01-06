
import argparse
import os


PROGRAM_DESCRIPTION = """
################
#  Mnemocards  #
################

I will help you to generate flashcards!
Use this scripts to easily generate Anki Decks from text files.
"""[1:]  # Remove fist \n so it looks better when used in the argsparser.

PARSER = argparse.ArgumentParser(description=PROGRAM_DESCRIPTION)
PARSER.add_argument("data_dir", metavar="DATA_DIR",
                    type=str,
                    help="Directory with the configuration and text "
                         "data to use for generating the Anki cards.")
PARSER.add_argument("--config-file", "-f",
                    type=str,
                    default="cards_config.json",
                    help="Configuration file to search in the DATA_DIR.")
PARSER.add_argument("--recursive", "-r",
                    help="Search recursively for configuration files "
                         "in the given DATA_DIR.",
                    action="store_true")
PARSER.add_argument("--output-dir", "-o",
                    type=str,
                    default=".",
                    help="Output directory where the packages are going "
                         "to be saved")


def parse_args():
    args = PARSER.parse_args()
    if not os.path.exists(args.data_dir):
        raise Exception("Data dir does not exist")
    return args

