
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
#PARSER.add_argument("-l", "--logging-level", dest="log_level", default="DEBUG",
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
Use the GitHub API to get your list of gists.
The list of gists (using the `ssh` protocol) is stored in the global configuration file (~/.mnemocards).
Once this command is executed successfully, you can run the `clone` command to truly clone them.

This is very useful if you want to store all your cards in your gists.
If you do not like this approach, you can always write manually the list of repositories to clone.
"""
GIS_PARSER = SUBPARSERS.add_parser("gists", help=help_txt)
help_txt = """
File with the GitHub API key to use in order to get the list of gists.
The default API key file is `~/.gh_gist_key`.
We recommend you to get an API key only with the *read gist* permission.
"""
GIS_PARSER.add_argument("--api-key", "-k",
                        type=str,
                        default="~/.gh_gist_key",
                        help=help_txt)
help_txt = """
If the name of the gist match this pattern, the gist is going to be added to the list.
If not, the gist is going to be ignored.
Write any regular expression you want.

The include pattern is checked first, the exclude patter is applied later.
"""
GIS_PARSER.add_argument("--include", "-i",
                        type=str,
                        help=help_txt)
help_txt = """
If the name of the gist match this pattern, the gist is going to be ignored.
Write any regular expression you want.

The include pattern is checked first, the exclude patter is applied later.
"""
GIS_PARSER.add_argument("--exclude", "-e",
                        type=str,
                        help=help_txt)
# Clone command.
help_txt = """
Reads the global configuration file and search for a list of repositories to clone.

This method launch git commands to the shell, so use `ssh` protocol in the URLs in order to avoid using passwords.
"""
CLO_PARSER = SUBPARSERS.add_parser("clone", help=help_txt)
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
                             "to be saved")
# Import command.
help_txt = """
Import a list of already generated apkg files.
You can import any apkg, they don't necessarily have to be generated with mnemocards.
"""
IMP_PARSER = SUBPARSERS.add_parser("import", help=help_txt)
help_txt = """
If your collection is in the default location (`~/.local/share/Anki2/`) you can specify only the profile name.
You cannot use this option as the same time as `-p`.
"""
IMP_PARSER.add_argument("--profile-name", "-n",
                        type=str,
                        help=help_txt)
help_txt = """
Specify the full path of the collection file.
You cannot use this option as the same time as `-n`.
"""
IMP_PARSER.add_argument("--collection-path", "-p",
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
# Hi command. Easter egg :)
PUS_PARSER = SUBPARSERS.add_parser("hi", add_help=False)


def parse_args():
    args = PARSER.parse_args()
    return args

