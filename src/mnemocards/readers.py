import abc
import csv
import io


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
