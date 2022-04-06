import pathlib

from .register import get_reader_by_extension


def file2dict(path, **options):
    path = pathlib.Path(path)
    extension = path.suffix[1:]
    extension = options.pop("reader", extension)
    reader = get_reader_by_extension(extension)
    if reader is None:
        raise ValueError(f"I cannot infer reader for file {path}")
    reader = reader()
    return reader.load(path, **options)


def _any2dict(
    path: pathlib.Path,
    content: dict,
    level: int,
    options: dict,
):
    if level == 0:
        print("Max recursion level reached, stopping here")
        return content

    if path.is_dir():
        content_dir = {}
        for i in path.iterdir():
            _any2dict(i, content_dir, level - 1, options)
        content[path.stem] = content_dir
    elif path.is_file():
        task = file2dict(path, **options)
        content[path.name] = task
    return content


def _top_level_entry(dictionary):
     return dictionary[next(iter(dictionary))]


def any2dict(path: str, max_recursion_level: int = 10, **options):
    root = pathlib.Path(path)
    content = {}
    _any2dict(
        root,
        content,
        level=max_recursion_level,
        options=options,
    )
    return _top_level_entry(content)
