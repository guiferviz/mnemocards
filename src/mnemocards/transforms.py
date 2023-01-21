import abc
import functools
from typing import Any, Dict, List

from mnemocards import utils


class Transform(abc.ABC, utils.PydanticType):
    @abc.abstractmethod
    def __call__(self, note: Dict[str, Any]) -> Dict[str, Any]:
        raise NotImplementedError()


class SetProperty(Transform):
    def __init__(self, **property_value_map: Dict[str, Any]):
        self.property_value_map = property_value_map

    def __call__(self, note: Dict[str, Any]) -> Dict[str, Any]:
        for k, v in self.property_value_map.items():
            note[k] = v
        return note


class AppendToProperty(Transform):
    def __init__(self, **property_value_map: Dict[str, Any]):
        self.property_value_map = property_value_map

    def __call__(self, note: Dict[str, Any]) -> Dict[str, Any]:
        for k, v in self.property_value_map.items():
            value = note.get(k, [])
            value.append(v)
            note[k] = value
        return note


def apply_transforms(
    value: Dict[str, Any],
    transforms: List[Transform],
) -> Dict[str, Any]:
    return functools.reduce(lambda value, fun: fun(value), transforms, value)
