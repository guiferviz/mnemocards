try:
    import toml

    toml_exists = True
except ImportError:
    toml_exists = False

from .reader import Reader
from .register import add_reader


@add_reader
class TOML(Reader):
    extensions = ["toml"]

    def loads(self, string, **options):
        if toml_exists:
            return self._parse(string, **options)
        raise ImportError("toml package is required to read toml files")

    def _parse(self, string: str, **options):
        return toml.loads(string, **options)
