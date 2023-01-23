from typing import List, Union

import pydantic

from mnemocards import NoteDict, PydanticTask
from mnemocards.utils import PydanticType
from mnemocards_anki import models


class NoteType(PydanticType):
    pass


class Configure(PydanticTask):
    tags: List[str] = []
    deck: models.Deck
    note_type: NoteType

    @pydantic.validator("tags", pre=True, always=True)
    @classmethod
    def tags_str_to_list(cls, tags: Union[List[str], str]) -> List[str]:
        if isinstance(tags, str):
            tags = [i.strip() for i in tags.split(",")]
        return tags

    def process_one(self, note: NoteDict) -> NoteDict:
        note["tags"] = note.get("tags", []) + self.tags
        note["deck"] = self.deck
        note["note_type"] = self.note_type
        return note
