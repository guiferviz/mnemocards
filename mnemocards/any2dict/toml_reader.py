import toml

from .reader import Reader
from .register import add_reader


@add_reader
class TOML(Reader):
    extensions = ["toml"]

    def loads(self, string, **options):
        return toml.loads(string, **options)
