from .csv_reader import CSV
from .register import add_reader


@add_reader
class TSV(CSV):
    extensions = ["tsv"]

    def loads(self, string, **options):
        options.setdefault("delimiter", "\t")
        return super().loads(string, **options)
