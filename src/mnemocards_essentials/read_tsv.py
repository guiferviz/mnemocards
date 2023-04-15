import csv
import itertools
from typing import Any, Iterable

from mnemocards import NoteDict, PydanticTask


class ReadTsv(PydanticTask):
    """Read a TSV file.

    Tab-separated values (TSV) is a simple, text-based file format for storing
    tabular data. Records are separated by newlines, and values within a record
    are separated by tab characters.

    Attributes:
        path: Path (directory + filename) of the TSV file to read.
        options: Extra parameters to pass to the python `csv.DictReader`.
    """

    path: str
    options: dict[str, Any] = {}

    def process(self, notes: Iterable[NoteDict]) -> Iterable[NoteDict]:
        file = open(self.path, "r")
        self.options.setdefault("delimiter", "\t")
        rows = csv.DictReader(file, **self.options)
        return itertools.chain(notes, rows)
