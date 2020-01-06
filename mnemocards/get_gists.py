
import json
import os
import re

from github import Github


GIST_API_KEY_FILE = "~/.gist"
GISTS_DIR = "~/gists"


def clone(git_url, gist_path):
    os.system(f"git clone {git_url} {gist_path}")

def pull(gist_path):
    os.system(f"cd {gist_path} && git pull")

def clone_pull_all(github):
    no_letters = re.compile("[^a-z]")
    tags = re.compile("#.*")
    for gist in github.get_user().get_gists():
        name = gist.description.lower()
        name = tags.sub("", name)
        name = no_letters.sub("_", name.strip())
        print("-----", name, "-----")
        gist_path = os.path.expanduser(f"{GISTS_DIR}/{name}")
        url = f"git@gist.github.com:{gist.id}.git"
        if os.path.exists(gist_path):
            pull(gist_path)
        else:
            clone(url, gist_path)

def get_gists():
    key = open(os.path.expanduser(GIST_API_KEY_FILE)).read().strip()
    g = Github(key)
    clone_pull_all(g)

def main():
    get_gists()


if __name__ == "__main__":
    main()

