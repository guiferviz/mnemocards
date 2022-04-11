from . import (
    csv_reader,
    json_reader,
    toml_reader,
    tsv_reader,
    xml_reader,
    yaml_reader,
)
from .any2dict import any2dict
from .reader import Reader
from .register import add_reader, get_reader_by_extension
