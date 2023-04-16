import itertools
from typing import Any, Iterable

import toml

from mnemocards import NoteDict, Path, PydanticTask


def _get_first_list_property(value) -> list:
    if len(value) != 1:
        raise ValueError("Dictionary with more than one entry")
    return next(iter(value.values()))


class ReadToml(PydanticTask):
    """Read a TOML file.

    Attributes:
        path: Path (directory + filename) of the TOML file to read.
        options: Extra parameters to pass to the `toml.loads` function.
    """

    path: Path
    options: dict[str, Any] = {}

    def process(self, notes: Iterable[NoteDict]) -> Iterable[NoteDict]:
        file = open(self.path, "r")
        dictionary = toml.load(file, **self.options)
        rows = _get_first_list_property(dictionary)
        return itertools.chain(notes, rows)
