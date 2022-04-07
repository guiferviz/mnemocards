from typing import List, Optional

from pydantic import BaseModel, Extra


class DeckConfigModel(BaseModel, extra=Extra.allow):
    __root__: dict


class SourceModel(BaseModel):
    path: str
    generator: str
    media_output_dir: str = "media/"
    default_card_properties: Optional[dict]


class DeckModel(BaseModel):
    id: str
    name: str
    config: Optional[DeckConfigModel]
    sources: List[SourceModel]


class PackageModel(BaseModel):
    name: str
    decks: List[DeckModel]


class RecipeModel(BaseModel):
    packages: List[PackageModel]
