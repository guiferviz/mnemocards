import csv
import itertools
from typing import Any, Iterable

from mnemocards import NoteDict, PydanticTask


class ReadCsv(PydanticTask):
    """Read a CSV file.

    Comma-separated values (CSV) is a simple, text-based file format for
    storing tabular data. Records are separated by newlines, and values within
    a record are separated by comma `,` characters.

    Attributes:
        path: Path (directory + filename) of the CSV file to read.
        options: Extra parameters to pass to the python `csv.DictReader`.
    """

    path: str
    options: dict[str, Any] = {}

    def process(self, notes: Iterable[NoteDict]) -> Iterable[NoteDict]:
        file = open(self.path, "r")
        rows = csv.DictReader(file, **self.options)
        return itertools.chain(notes, rows)
