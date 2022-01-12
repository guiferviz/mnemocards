import json

from .reader import Reader
from .register import add_reader


@add_reader
class JSON(Reader):
    extensions = ["json"]

    def loads(self, string, **options):
        return json.loads(string, **options)
