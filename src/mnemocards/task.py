from typing import Iterable

import pydantic

from mnemocards import utils
from mnemocards.types import NoteDict


class Task(utils.PydanticType):
    """Basic unit of work."""

    def start(self):
        """Method called before processing any note."""
        pass

    def process(self, notes: Iterable[NoteDict]) -> Iterable[NoteDict]:
        """Method that contains the processing logic of the task.

        Arguments:
            notes: An iterable of notes to process.
        """
        for i in notes:
            note = self.process_one(i)
            if note:
                yield note

    def process_one(self, note: NoteDict) -> NoteDict:
        """Method called one per note.

        !!! note

            If you want to use this method you should not overwrite the process
            method. Otherwise this method will not be called.

        Arguments:
            note: A note to process.
        """
        return note

    def end(self):
        """Method called after processing all the notes."""
        pass


class PydanticTask(Task, pydantic.BaseModel):
    pass
