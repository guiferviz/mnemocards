import csv
import io

from .reader import Reader
from .register import add_reader


class CSV(Reader):
    extensions = ["csv"]

    def loads(self, string, **options):
        string = io.StringIO(string)
        reader = csv.DictReader(string, **options)
        return [i for i in reader]


add_reader(CSV)
