import pytest

from mnemocards_essentials import ReadTsv

INPUT_FILE_CONTENT = """front	back
front1	back1
front2	back2
"""


@pytest.fixture
def input_file(tmp_path):
    file = tmp_path / "input_file.tsv"
    file.write_text(INPUT_FILE_CONTENT)
    return str(file)


def test_read_tsv(input_file):
    actual = ReadTsv(path=input_file).process([])
    expected = [
        dict(front="front1", back="back1"),
        dict(front="front2", back="back2"),
    ]
    assert list(actual) == expected
