import pytest

from mnemocards_essentials import ReadJson

INPUT_FILE_CONTENT = """
[
    {
        "front": "front1",
        "back": "back1"
    },
    {
        "front": "front2",
        "back": "back2"
    }
]
"""


@pytest.fixture
def input_file(tmp_path):
    file = tmp_path / "input_file.json"
    file.write_text(INPUT_FILE_CONTENT)
    return str(file)


def test_read_json(input_file):
    actual = ReadJson(path=input_file).process([])
    expected = [
        dict(front="front1", back="back1"),
        dict(front="front2", back="back2"),
    ]
    assert list(actual) == expected
