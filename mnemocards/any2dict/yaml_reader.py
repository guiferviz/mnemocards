try:
    import yaml
    pyyaml_exists = True
except ImportError:
    pyyaml_exists = False

from .reader import Reader
from .register import add_reader


@add_reader
class YAML(Reader):
    extensions = ["yaml", "yml"]

    def loads(self, string: str, **options):
        if pyyaml_exists:
            return self._parse(string, **options)
        raise ImportError("pyyaml package is required to read yaml files")

    def _parse(self, string: str, **options):
        return yaml.safe_load(string, **options)
