import xmltodict

from .reader import Reader
from .register import add_reader


@add_reader
class XML(Reader):
    extensions = ["xml"]

    def loads(self, string, **options):
        return xmltodict.parse(string, **options)
