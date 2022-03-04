import abc


class Reader(abc.ABC):
    extensions = []

    def load(self, path, **options):
        with open(path, "r") as f:
            string = f.read()
            return self.loads(string, **options)

    @abc.abstractmethod
    def loads(self, string, **options):
        raise NotImplementedError()
