
import argparse
import os

from mnemocards import __version__


PROGRAM_DESCRIPTION = """
  _   _   _   _   _   _   _   _   _   _  
 / \ / \ / \ / \ / \ / \ / \ / \ / \ / \ 
( M | n | e | m | o | c | a | r | d | s )
 \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ \_/ 

I will help you to generate flashcards!
Use this scripts to easily generate Anki Decks from text files.
Among other utilities, mnemocards helps you to import Anki packages
to your current collection.
"""
PARSER = argparse.ArgumentParser(description=PROGRAM_DESCRIPTION,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
# Global arguments.
# TODO: add logging.
# PARSER.add_argument("-l", "--logging-level", dest="log_level", default="DEBUG",
#                    choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
#                    help="Logging level.")
PARSER.add_argument("-v", "--version",
                    action="version",
                    default=argparse.SUPPRESS,
                    version=f"Mnemocards (version {__version__})",
                    help="show program's version number and exit")
# A required command.
SUBPARSERS = PARSER.add_subparsers(dest="command")
SUBPARSERS.required = True
# Gist command.
help_txt = """
Use the GitHub API to get your list of repositories or gists.
The list of repos or gists (using the `ssh` protocol) is stored in the global
configuration file (~/.mnemocards).
Be aware that this command will overwrite your repos list in the configuration
file.
Once this command is executed successfully, you can run the `pull` command to
truly clone them.

This is very useful if you want to store all your cards in a series of gists
or normal GitHub repositories.
If you do not want to get your list automatically, you can always write
manually the list of repositories to clone in the configuration file.
"""
GIS_PARSER = SUBPARSERS.add_parser("github", help=help_txt)
help_txt = """
File with the GitHub API key to use in order to get the list of repos/gists.
The default API key file is `~/.gh_key`.
We recommend you to get an API key with the minimum permissions (gist or
repo permission, depends on what do you want to use).
"""
GIS_PARSER.add_argument("--api-key", "-k",
                        type=str,
                        default="~/.gh_key",
                        help=help_txt)
help_txt = """
Parent directory where your repos will be cloned.
"""
GIS_PARSER.add_argument("--dir", "-d",
                        type=str,
                        default=".",
                        help=help_txt)
help_txt = """
If the name of the repo match this pattern, the repo is going to be added to
the list.
If not, the repo is going to be ignored.
Write any regular expression you want.
You can also use one capturing group `()` inside of the regex to extract that
part of the name and use it as a clone directory.
Ex: use `mnemocards github -i "guiferviz/cards_([^ _]*)"` to match only
repositories from your user `guiferviz` that start with `cards_`.
The letters following that prefix will be used to clone the repository into a
folder with that name.
If you have a repo called `guiferviz/cards_programming`, that repo is going to
be cloned in `./programming`.
Instead of `.` you can use any other directory with the option: `-d`.

The include pattern is checked first, the exclude patter is applied later.
"""
GIS_PARSER.add_argument("--include", "-i",
                        type=str,
                        help=help_txt)
help_txt = """
If the name of the repo match this pattern, the repo is going to be ignored.
Write any regular expression you want.

The include pattern is checked first, the exclude patter is applied later.
"""
GIS_PARSER.add_argument("--exclude", "-e",
                        type=str,
                        help=help_txt)
help_txt = """
Instead of getting the list of all your repos, get the list of all your gists.
Note that now the include and exclude patters are applied to the gist
description.
"""
GIS_PARSER.add_argument("--gists", "-g",
                        action="store_true",
                        help=help_txt)
# Clone command.
help_txt = """
Reads the global configuration file and search for a list of repositories to clone or pull.

This method launch git commands to the shell, so use `ssh` protocol in the URLs in order to avoid using passwords.
"""
CLO_PARSER = SUBPARSERS.add_parser("pull", help=help_txt)
# Push command.
help_txt = """
Add, commit and upload all the local changes in all the repositories in your global configuration.
This command is simply a utility to help you keep your cards always safe.

Note that this command is going to add ALL the files in the directory and commit everything with a generic commit message.
You must add a `.gitignore` to prevent all files from being automatically uploaded.
You must also do the commits manually if you want to use a more descriptive message.

This method launch git commands to the shell, so use `ssh` protocol in the URLs in order to avoid using password.
"""
PUS_PARSER = SUBPARSERS.add_parser("push", help=help_txt)
# Generate command.
GEN_PARSER = SUBPARSERS.add_parser("generate",
                                   help="Generate Anki cards as crazy.")
GEN_PARSER.add_argument("data_dir", metavar="DATA_DIR",
                        type=str,
                        help="Directory with the configuration and text "
                             "data to use for generating the Anki cards.")
GEN_PARSER.add_argument("--config-file", "-f",
                        type=str,
                        default="cards_config.json",
                        help="Configuration file to search in the DATA_DIR.")
GEN_PARSER.add_argument("--recursive", "-r",
                        help="Search recursively for configuration files "
                             "in the given DATA_DIR.",
                        action="store_true")
GEN_PARSER.add_argument("--output-dir", "-o",
                        type=str,
                        default=".",
                        help="Output directory where the packages are going "
                             "to be saved. Current directory by default.")
# Import command.
help_txt = """
Import a list of already generated apkg files.
You can import any apkg, they don't necessarily have to be generated with mnemocards.
"""
IMP_PARSER = SUBPARSERS.add_parser("import", help=help_txt)
help_txt = """
If your collection is in the default location (`~/.local/share/Anki2/`) you can specify only the profile name.
You cannot use this option as the same time as `-c`.
"""
IMP_PARSER.add_argument("--profile-name", "-p",
                        type=str,
                        help=help_txt)
help_txt = """
Specify the full path of the collection file.
If you use this option with `-p` (profile name), the profile name has
preference over the full collection path.
"""
IMP_PARSER.add_argument("--collection-path", "-c",
                        type=str,
                        help=help_txt)
help_txt = """
List of packages to import.
"""
IMP_PARSER.add_argument("apkgs", nargs="+", help=help_txt)
# Clean command.
help_txt = """
DANGER!!!
Use at your own risk.
This command deletes notes and cards, make sure you have a backup of your collection.

After importing packages, removes all the cards from the decks that have not been imported.
This is useful when you delete a card from your text files that you use for generating the apkg.
By default, if the apkg file does not contain that card but the collection does, that card is not going to be deleted from the collection.

How does this works?
When you import a package, even if the cards have not been modified, a timestamp is updated for those cards present in the package.
If there is any card with a lower timestamp it means that that it was not imported with the last imported apkg.
So this command deletes all those cards that are in the collection but were not imported.
"""
CLE_PARSER = SUBPARSERS.add_parser("clean", help=help_txt)
help_txt = """
If your collection is in the default location (`~/.local/share/Anki2/`) you can specify only the profile name.
You cannot use this option as the same time as `-c`.
"""
CLE_PARSER.add_argument("--profile-name", "-p",
                        type=str,
                        help=help_txt)
help_txt = """
Specify the full path of the collection file.
If you use this option with `-n` (profile name), the profile name has
preference over the full collection path.
"""
CLE_PARSER.add_argument("--collection-path", "-c",
                        type=str,
                        help=help_txt)
# Maketsv command.
help_txt = """
This command generates vocabulary-type TSV-files based on a txt file with words.
Text file should contain one words or phrase per line.
The command will take each line, translate it to your language and tranform it to one TSV line according to vocabulary type.
"""
MAKETSV_PARSER = SUBPARSERS.add_parser("maketsv", help=help_txt)

MAKETSV_PARSER.add_argument(
    "data_dir",
    metavar="DATA_DIR",
    type=str,
    help="Directory with the text file for translation "
    "and generation of TSV file.",
)
help_txt = """
Language pair you want generated in the following format: 
"language-from_language-to"
Default pair is from english to spanish. In the command line it will look "en_es"

Language codes for all supporte languages can be found here:
https://py-googletrans.readthedocs.io/en/latest/#googletrans-languages
"""
MAKETSV_PARSER.add_argument(
    "--language-pair",
    "-l",
    type=str,
    default="en_es",
    help=help_txt,
)
MAKETSV_PARSER.add_argument(
    "--word-file",
    "-w",
    type=str,
    default="words.txt",
    help="Text file with words to search in the DATA_DIR.",
)
MAKETSV_PARSER.add_argument(
    "--recursive",
    "-r",
    help="Search recursively for words files "
    "in the given DATA_DIR.",
    action="store_true",
)
MAKETSV_PARSER.add_argument(
    "--output-dir",
    "-o",
    type=str,
    default=".",
    help="Output directory where the generated TSV files "
    "are going to be saved. Current directory by default.",
)

# ID generator command.
help_txt = """
This command generates unique ID that you can use if for creating Unique ID
for your cards or decks. It prints id in your terminal and you'll need to copy
it to config.json or cards.tsv
"""

IDGEN_PARSER = SUBPARSERS.add_parser("id", help=help_txt)


# Hi command. Easter egg :)
EGG_PARSER = SUBPARSERS.add_parser("hi", add_help=False)


def parse_args():
    args = PARSER.parse_args()
    return args
