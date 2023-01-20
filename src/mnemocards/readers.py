import abc
import csv
import io
import json

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


class Reader(abc.ABC):
    extensions = []

    def load(self, path, **options):
        with open(path, "r") as f:
            string = f.read()
            return self.loads(string, **options)

    @abc.abstractmethod
    def loads(self, string, **options):
        raise NotImplementedError()


class CSV(Reader):
    extensions = ["csv"]

    def loads(self, string, **options):
        string = io.StringIO(string)
        reader = csv.DictReader(string, **options)
        return [i for i in reader]


class TSV(CSV):
    extensions = ["tsv"]

    def loads(self, string, **options):
        options.setdefault("delimiter", "\t")
        return super().loads(string, **options)


class JSON(Reader):
    extensions = ["json"]

    def loads(self, string, **options):
        return json.loads(string, **options)


class TOML(Reader):
    extensions = ["toml"]

    def loads(self, string, **options):
        if toml_exists:
            return self._parse(string, **options)
        raise ImportError("toml package is required to read toml files")

    def _parse(self, string: str, **options):
        return toml.loads(string, **options)


class YAML(Reader):
    extensions = ["yaml", "yml"]

    def loads(self, string: str, **options):
        if pyyaml_exists:
            return self._parse(string, **options)
        raise ImportError("pyyaml package is required to read yaml files")

    def _parse(self, string: str, **options):
        return yaml.safe_load(string, **options)


class XML(Reader):
    extensions = ["xml"]

    def loads(self, string: str, **options):
        if xmltodict_exists:
            return self._parse(string, **options)
        raise ImportError("xmltodict package is required to read xml files")

    def _parse(self, string: str, **options):
        return xmltodict.parse(string, **options)
