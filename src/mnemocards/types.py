import os
import pathlib
from typing import Any, Dict, Union

PathLike = Union[pathlib.Path, str, bytes, os.PathLike]
NoteDict = Dict[str, Any]


# We need to subclass from the concrete Path class.
# https://stackoverflow.com/questions/29850801/subclass-pathlib-path-fails
class Path(type(pathlib.Path())):
    @classmethod
    def __get_validators__(cls):
        yield cls._to_absolute_path

    @classmethod
    def _to_absolute_path(cls, value):
        if type(value) == str:
            value = pathlib.Path(value)
        if isinstance(value, pathlib.Path):
            return value.absolute()
        raise TypeError("expecting a string with a path")
