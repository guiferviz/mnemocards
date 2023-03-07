import itertools
from typing import Iterable

from mnemocards import NoteDict, PydanticTask
from mnemocards_essentials import readers


def get_first_list_property(value, depth=10):
    if type(value) == list:
        return value
    if type(value) == dict:
        if len(value) != 1:
            raise ValueError("Dictionary with more than one entry")
        first_value = next(iter(value.values()))
        return get_first_list_property(first_value, depth - 1)
    raise TypeError("unknown data type returned by a reader")


class File(PydanticTask):
    """Read a file.

    Attributes:
        path: Path (directory and filename) of the file to read.
        reader: Class used to read the given file.
    """

    path: str
    reader: readers.Reader = readers.InferReader()

    def process(self, notes: Iterable[NoteDict]) -> Iterable[NoteDict]:
        notes_from_file = self.reader.load(self.path)
        notes_from_file = get_first_list_property(notes_from_file)
        return itertools.chain(notes, notes_from_file)
