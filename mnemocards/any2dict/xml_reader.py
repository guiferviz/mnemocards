try:
    import xmltodict

    xmltodict_exists = True
except ImportError:
    xmltodict_exists = False

from .reader import Reader
from .register import add_reader


@add_reader
class XML(Reader):
    extensions = ["xml"]

    def loads(self, string: str, **options):
        if xmltodict_exists:
            return self._parse(string, **options)
        raise ImportError("xmltodict package is required to read xml files")

    def _parse(self, string: str, **options):
        return xmltodict.parse(string, **options)
