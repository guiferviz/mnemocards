from typing import List, Type, Union

import pydantic

from mnemocards import NoteDict, PydanticTask
from mnemocards.utils import PydanticType
from mnemocards_anki import models


class NoteType(PydanticType):
    id: str
    name: str
    model: Type[models.Note]
    css: str = ""
    card_sides: List[models.CardSides]


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
        note_model = self.note_type.model(**note)
        for k, v in note_model:
            note[k] = v
        return note
