from typing import List, Type, Union

import pydantic

from mnemocards.utils import PydanticType
from mnemocards_anki import utils


class Deck(pydantic.BaseModel, PydanticType):
    name: str
    id: int = None  # type: ignore

    @pydantic.validator("id", pre=True, always=True)
    @classmethod
    def string_id_to_int_using_name_by_default(cls, id, values):
        name = values.get("name")
        if type(id) == str:
            id = utils.get_hash_id(id, 4)
        if id or not name:
            return id
        return utils.get_hash_id(name, 4)

    def __hash__(self):
        return hash(self.id)


class Note(pydantic.BaseModel, extra=pydantic.Extra.allow):
    id: str
    tags: List[str] = []
    media_files: List[str] = []

    @pydantic.validator("tags", pre=True, always=True)
    @classmethod
    def tags_str_to_list(cls, tags: Union[List[str], str]) -> List[str]:
        if isinstance(tags, str):
            return tags.split(",")
        return tags

    def __hash__(self):
        return hash(self.id)


class CardSides(pydantic.BaseModel):
    name: str
    front: str
    back: str


class NoteType(pydantic.BaseModel):
    id: str
    name: str
    model: Type[Note]
    card_sides: List[CardSides]
    css: str = ""

    def __hash__(self):
        return hash(self.id)
