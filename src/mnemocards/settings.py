from typing import List, Optional

import pydantic

from mnemocards.sinks import Sink
from mnemocards.sources import Source
from mnemocards.transforms import Transform


class RecipeModel(pydantic.BaseModel, extra=pydantic.Extra.forbid):
    name: Optional[str] = None
    sources: List[Source]
    transforms: List[Transform] = []
    sinks: List[Sink]
