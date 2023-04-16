import itertools
from typing import Iterable

import yaml

from mnemocards import NoteDict, Path, PydanticTask


class ReadYaml(PydanticTask):
    """Read a YAML file.

    Attributes:
        path: Path (directory + filename) of the YAML file to read.
    """

    path: Path

    def process(self, notes: Iterable[NoteDict]) -> Iterable[NoteDict]:
        content = open(self.path, "r").read()
        rows = yaml.safe_load(content)
        return itertools.chain(notes, rows)
