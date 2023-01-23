from typing import List, Optional, Type, Union

import pydantic

from mnemocards_anki import utils


# FIXME: deck config model needs a review, probably not working as expected.
class DeckConfig(pydantic.BaseModel, extra=pydantic.Extra.allow):
    id: int = None  # type: ignore
    name: str
    autoplay: bool = True
    max_taken: int = pydantic.Field(60, alias="maxTaken")
    mod: int = 0
    replayq: bool = True
    timer: int = 0
    usn: int = 0
    rev: Optional[dict] = None
    new: Optional[dict] = None
    lapse: Optional[dict] = None

    @pydantic.validator("id", pre=True, always=True)
    @classmethod
    def string_id_to_int_using_name_by_default(cls, id, values):
        name = values.get("name")
        if type(id) == str:
            id = utils.get_hash_id(id)
        if id or not name:
            return id
        return utils.get_hash_id(name)


class Deck(pydantic.BaseModel):
    name: str
    id: int = None  # type: ignore
    config: Optional[DeckConfig] = None

    @pydantic.validator("id", pre=True, always=True)
    @classmethod
    def string_id_to_int_using_name_by_default(cls, id, values):
        name = values.get("name")
        if type(id) == str:
            id = utils.get_hash_id(id)
        if id or not name:
            return id
        return utils.get_hash_id(name)

    def __hash__(self):
        return hash(self.id)


class NoteModel(pydantic.BaseModel):
    id: str
    tags: List[str] = []
    deck: Deck
    media_files: List[str]

    @pydantic.validator("tags", pre=True, always=True)
    @classmethod
    def tags_str_to_list(cls, tags: Union[List[str], str]) -> List[str]:
        if isinstance(tags, str):
            return tags.split(",")
        return tags


class CardSides(pydantic.BaseModel):
    name: str
    front: str
    back: str


class NoteType(pydantic.BaseModel):
    id: str
    name: str
    model: Type[NoteModel]
    card_sides: List[CardSides]
    css: str = ""

    def __hash__(self):
        return hash(self.id)
