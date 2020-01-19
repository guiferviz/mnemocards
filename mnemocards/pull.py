
import os

from mnemocards.utils import read_config


def clone_repo(git_url, gist_path):
    os.system(f"git clone {git_url} {gist_path}")


def pull_repo(gist_path):
    os.system(f"cd {gist_path} && git pull")


def clone_or_pull(repo):
    url, path = repo
    if os.path.exists(path):
        pull_repo(path)
    else:
        clone_repo(url, path)


def clone_or_pull_all(repos):
    for repo in repos:
        clone_or_pull(repo)


def pull():
    conf = read_config()
    repos = conf.get("repos", [])
    if len(repos) == 0:
        raise Exception("No repository list in your config file")
    else:
        clone_or_pull_all(conf["repos"])

