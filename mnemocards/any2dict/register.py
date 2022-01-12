from .reader import Reader


_READERS = []


def add_reader(reader):
    if not issubclass(reader, Reader):
        raise TypeError(f"{type(reader)} should be a subclass or mnemocards.Reader")
    _READERS.append(reader)
    return reader


def get_reader_by_extension(extension):
    for i in _READERS:
        if extension in i.extensions:
            return i
