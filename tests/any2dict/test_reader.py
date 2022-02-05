import pytest

import mnemocards


@pytest.fixture
def txt_file(tmp_path):
    file = tmp_path / "reader.txt"
    file.write_text("hello")
    return file


def test_reader_load(mocker, txt_file):
    mocker.patch("mnemocards.Reader.__abstractmethods__", set())
    reader = mnemocards.Reader()  # type: ignore
    reader.loads = mocker.Mock()
    reader.load(str(txt_file))
    reader.loads.assert_called_once_with("hello")
