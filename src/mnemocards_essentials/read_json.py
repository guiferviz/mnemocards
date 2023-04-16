import itertools
import json
from typing import Iterable

from mnemocards import NoteDict, Path, PydanticTask


class ReadJson(PydanticTask):
    """Read a JSON file.

    Attributes:
        path: Path (directory + filename) of the JSON file to read.
    """

    path: Path

    def process(self, notes: Iterable[NoteDict]) -> Iterable[NoteDict]:
        file = open(self.path, "r")
        rows = json.load(file)
        return itertools.chain(notes, rows)
