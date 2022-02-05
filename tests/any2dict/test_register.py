import pytest

import mnemocards
from mnemocards.any2dict.register import get_reader_by_extension


def test_add_reader_no_subclass_of_reader():
    with pytest.raises(TypeError) as excinfo:
        @mnemocards.add_reader
        class ReaderNotReader:
            pass
    assert "Reader" in str(excinfo.value)


@pytest.fixture
def my_reader(mocker):
    class MyReader:
        extensions = ["my_reader", "my"]
    mocker.patch("mnemocards.any2dict.register._READERS", [MyReader])
    return MyReader


def test_get_reader_by_extension(my_reader):
    reader = get_reader_by_extension("my_reader")
    assert reader == my_reader
    reader = get_reader_by_extension("my")
    assert reader == my_reader


def test_get_reader_by_extension_not_found():
    reader = get_reader_by_extension("unknown_extension")
    assert reader == None
