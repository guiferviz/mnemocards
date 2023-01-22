import itertools
from typing import Iterable

from mnemocards import NoteDict, PydanticTask
from mnemocards_essentials import readers


class File(PydanticTask):
    path: str
    reader: readers.Reader = readers.InferReader()

    def process(self, notes: Iterable[NoteDict]) -> Iterable[NoteDict]:
        notes_from_file = self.reader.load(self.path)
        return itertools.chain(notes, notes_from_file)
