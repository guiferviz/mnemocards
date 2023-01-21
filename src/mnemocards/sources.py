import abc
from typing import Any, Dict, Iterable, List

import pydantic

from mnemocards import readers, utils
from mnemocards.transforms import Transform, apply_transforms


class Source(abc.ABC, utils.PydanticType, pydantic.BaseModel, Iterable):
    @abc.abstractmethod
    def __iter__(self) -> Iterable[Dict[str, Any]]:
        raise NotImplementedError()


class File(Source):
    path: str
    reader: readers.Reader = readers.InferReader()
    transforms: List[Transform] = []

    def __iter__(self) -> Iterable[Dict[str, Any]]:
        output = self.reader.load(self.path)
        for i in output:
            assert type(i) == dict
            yield apply_transforms(i, self.transforms)
