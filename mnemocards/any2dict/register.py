from typing import List, Type

from .reader import Reader

_READERS: List[Type] = []


def add_reader(reader: Type):
    if not issubclass(reader, Reader):
        raise TypeError(
            f"{reader.__name__} should be a subclass of "
            f"{Reader.__module__}.{Reader.__name__}"
        )
    _READERS.append(reader)
    return reader


def get_reader_by_extension(extension) -> Type:
    for i in _READERS:
        if extension in i.extensions:
            return i
