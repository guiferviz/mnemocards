from mnemocards import PydanticTask


class GitRepo(PydanticTask):
    """Retrieve a Mnemocards project from an external Git repository.

    Attributes:
        repo_url: URL of the Git repository.
        clone_path: Local path where the repository will be cloned.
        config_path: Path to the configuration file within the repository.
    """

    url: str
    clone_path: str
    config_path: str = "mnemocards.yaml"

    def start(self):
        # git.Repo.clone_from(self.url, self.clone_path)
        pass
