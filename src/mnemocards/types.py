import os
import pathlib
from typing import Any, Dict, TypeVar

PathLike = TypeVar("PathLike", pathlib.Path, str, bytes, os.PathLike)
NoteDict = Dict[str, Any]
