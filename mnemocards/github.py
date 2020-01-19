
import json
import os
import re

from github import Github

from mnemocards.utils import read_config, write_config


def prepare_list(gh_repos, clone_dir, i_patter, e_patter, gists):
    repos = []
    re_include = re.compile(i_patter) if i_patter is not None else None
    re_exclude = re.compile(e_patter) if e_patter is not None else None
    no_alphanum = re.compile("[^a-z0-9]")
    for repo in gh_repos:
        # Gists do not have a legible name...
        name = repo.description if gists else repo.full_name
        name_processed = name
        # Filter repos based on the name.
        add = True
        if re_include is not None:
            find = re_include.findall(name)
            add = len(find) > 0
            if add:
                name_processed = find[0]
        if add and re_exclude is not None:
            add = not re_exclude.match(name)
        if add:
            # Choose a local folder in which the repos are going to be cloned
            # and add the repo to the final list.
            # Get the first word in lowercase.
            name_processed = name_processed.lower().split()[0]
            # Remove any non-alphanumeric character.
            name_processed = no_alphanum.sub("_", name_processed)
            # Create path.
            path = os.path.abspath(os.path.join(clone_dir, name_processed))
            # Create URL.
            print(f"+ Including: '{name}' in local folder '{path}'")
            if gists:
                # Gists does not have ssh_url property...
                url = f"git@gist.github.com:{repo.id}.git"
            else:
                url = repo.ssh_url
            # Add the URL and the name.
            # We will use that name later to clone on a folder of that name.
            repos.append([url, path])
        else:
            print(f"- Excluding: '{name}'")
    return repos


def read_key(filename):
    filename = os.path.expanduser(filename)
    with open(filename) as file:
        return file.read().strip()


def github(api_key_file,
           clone_dir=".",
           i_pattern=None, e_pattern=None,
           gists=False):
    # Read the GitHub key to use the API.
    key = read_key(api_key_file)
    # Get repo list from GitHub.
    g = Github(key)
    if gists:
        repos = g.get_user().get_gists()
    else:
        repos = g.get_user().get_repos()
    # Save that list in the main config.
    conf = read_config()
    conf["repos"] = prepare_list(repos, clone_dir, i_pattern, e_pattern, gists)
    write_config(conf)

