import os
import pathlib
from typing import TypeVar

PathLike = TypeVar("PathLike", pathlib.Path, str, bytes, os.PathLike)
