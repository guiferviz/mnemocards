import pytest

from mnemocards_essentials import ReadCsv

INPUT_FILE_CONTENT = """front,back
front1,back1
front2,back2
"""


@pytest.fixture
def input_file(tmp_path):
    file = tmp_path / "input_file.csv"
    file.write_text(INPUT_FILE_CONTENT)
    return str(file)


def test_read_csv(input_file):
    actual = ReadCsv(path=input_file).process([])
    expected = [
        dict(front="front1", back="back1"),
        dict(front="front2", back="back2"),
    ]
    assert list(actual) == expected
