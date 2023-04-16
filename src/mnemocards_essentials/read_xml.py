import itertools
from typing import Any, Iterable

import xmltodict

from mnemocards import NoteDict, Path, PydanticTask


def _get_first_list_property(value) -> list:
    if len(value) != 1:
        raise ValueError("Dictionary with more than one entry")
    return next(iter(value.values()))


class ReadXml(PydanticTask):
    """Read a XML file.

    Attributes:
        path: Path (directory + filename) of the XML file to read.
    """

    path: Path
    options: dict[str, Any] = {}

    def process(self, notes: Iterable[NoteDict]) -> Iterable[NoteDict]:
        content = open(self.path, "r").read()
        dictionary = xmltodict.parse(content, **self.options)
        rows = _get_first_list_property(_get_first_list_property(dictionary))
        return itertools.chain(notes, rows)
