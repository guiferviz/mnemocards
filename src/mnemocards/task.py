from typing import Iterable

import pydantic

from mnemocards import utils
from mnemocards.types import NoteDict


class Task(utils.PydanticType):
    def start(self):
        pass

    def process(self, notes: Iterable[NoteDict]) -> Iterable[NoteDict]:
        for i in notes:
            yield self.process_one(i)

    def process_one(self, note: NoteDict) -> NoteDict:
        return note

    def end(self):
        pass


class PydanticTask(Task, pydantic.BaseModel):
    pass
