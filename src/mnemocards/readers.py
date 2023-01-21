import abc
import csv
import io
import json
import pathlib
from typing import Any, List, Type

from mnemocards import utils
from mnemocards.types import PathLike

try:
    import toml

    toml_exists = True
except ImportError:
    toml_exists = False

try:
    import xmltodict

    xmltodict_exists = True
except ImportError:
    xmltodict_exists = False

try:
    import yaml

    pyyaml_exists = True
except ImportError:
    pyyaml_exists = False


class Reader(abc.ABC, utils.PydanticType):
    extensions = []

    def load(self, path_like: PathLike, **options) -> Any:
        with open(path_like, "r") as f:
            content = f.read()
            return self.loads(content, **options)

    @abc.abstractmethod
    def loads(self, content: str, **options) -> Any:
        raise NotImplementedError()


def get_reader_subclasses() -> List[Type]:
    return Reader.__subclasses__()


def get_reader_by_extension(extension: str) -> Type:
    for i in get_reader_subclasses():
        if extension in i.extensions:
            return i


class InferReader(Reader):
    def _get_reader(self, path_like: PathLike) -> Reader:
        path = pathlib.Path(str(path_like))
        extension = path.suffix[1:]
        reader = get_reader_by_extension(extension)
        if reader is None:
            raise ValueError(f"I cannot infer reader for file `{path}`")
        return reader()

    def load(self, path_like: PathLike, **options) -> Any:
        reader = self._get_reader(path_like)
        return reader.load(path_like, **options)

    def loads(self, content: str, **options) -> Any:
        raise NotImplementedError(
            "I cannot infer the file type from the file content."
            " Use `load` with a file name with a valid extension."
        )


class CSV(Reader):
    extensions = ["csv"]

    def loads(self, content: str, **options) -> Any:
        string_io = io.StringIO(content)
        reader = csv.DictReader(string_io, **options)
        return [i for i in reader]


class TSV(CSV):
    extensions = ["tsv"]

    def loads(self, content: str, **options) -> Any:
        options.setdefault("delimiter", "\t")
        return super().loads(content, **options)


class JSON(Reader):
    extensions = ["json"]

    def loads(self, content: str, **options) -> Any:
        return json.loads(content, **options)


class TOML(Reader):
    extensions = ["toml"]

    def __init__(self):
        if not toml_exists:
            raise ImportError("toml package is required to read toml files")

    def loads(self, content: str, **options) -> Any:
        return toml.loads(content, **options)


class YAML(Reader):
    extensions = ["yaml", "yml"]

    def __init__(self):
        if not pyyaml_exists:
            raise ImportError("pyyaml package is required to read yaml files")

    def loads(self, content: str, **options) -> Any:
        return yaml.full_load(content, **options)


class XML(Reader):
    extensions = ["xml"]

    def __init__(self):
        if not xmltodict_exists:
            raise ImportError("xmltodict package is required to read xml files")

    def loads(self, content: str, **options) -> Any:
        return xmltodict.parse(content, **options)
