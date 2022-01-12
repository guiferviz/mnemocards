import yaml

from .reader import Reader
from .register import add_reader


@add_reader
class YAML(Reader):
    extensions = ["yaml", "yml"]

    def loads(self, string, **options):
        return yaml.safe_load(string, **options)
