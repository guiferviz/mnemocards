
import json
import os
import re

from github import Github

from mnemocards.utils import read_config, write_config


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

def list_gists(github, i_patter, e_patter):
    repos = []
    re_include = re.compile(i_patter) if i_patter is not None else None
    re_exclude = re.compile(e_patter) if e_patter is not None else None
    no_alphanum = re.compile("[^a-z0-9]")
    for gist in github.get_user().get_gists():
        name = gist.description
        add = True
        if re_include is not None:
            add = re_include.match(name)
        if add and re_exclude is not None:
            add = not re_exclude.match(name)
        if add:
            # Get the first word in lowercase.
            name = name.lower().split()[0]
            # Remove any non-alphanumeric character.
            name = no_alphanum.sub("_", name.strip())
            print("+ Including:", gist.description)
            # Generate ssh url.
            url = f"git@gist.github.com:{gist.id}.git"
            # Add the url and the name.
            # We will use that name later to clone on a folder of that name.
            repos.append([url, name])
        else:
            print("- Excluding:", gist.description)
    return repos

def read_key(filename):
    filename = os.path.expanduser(filename)
    with open(filename) as file:
        return file.read().strip()

def gists(api_key_file, include_patter, exclude_patter):
    key = read_key(api_key_file)
    g = Github(key)
    conf = read_config()
    conf["repos"] = list_gists(g, include_patter, exclude_patter)
    write_config(conf)

