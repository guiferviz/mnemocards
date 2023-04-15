import pytest

from mnemocards_essentials import ReadToml

INPUT_FILE_CONTENT = """
[[cards]]
front = "front1"
back = "back1"

[[cards]]
front = "front2"
back = "back2"
"""


@pytest.fixture
def input_file(tmp_path):
    file = tmp_path / "input_file.toml"
    file.write_text(INPUT_FILE_CONTENT)
    return str(file)


def test_read_toml(input_file):
    actual = ReadToml(path=input_file).process([])
    expected = [
        dict(front="front1", back="back1"),
        dict(front="front2", back="back2"),
    ]
    assert list(actual) == expected
