
import json
import os
import re

from github import Github

from mnemocards.utils import read_config, write_config


def list_gists(github, gists_dir, i_patter, e_patter):
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
            # Create path.
            path = os.path.abspath(os.path.join(gists_dir, name))
            # Add the url and the name.
            # We will use that name later to clone on a folder of that name.
            repos.append([url, path])
        else:
            print("- Excluding:", gist.description)
    return repos

def read_key(filename):
    filename = os.path.expanduser(filename)
    with open(filename) as file:
        return file.read().strip()

def gists(api_key_file, gists_dir, include_patter, exclude_patter):
    key = read_key(api_key_file)
    g = Github(key)
    conf = read_config()
    conf["repos"] = list_gists(g, gists_dir, include_patter, exclude_patter)
    write_config(conf)

