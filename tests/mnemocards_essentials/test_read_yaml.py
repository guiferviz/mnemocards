import pytest

from mnemocards_essentials import ReadYaml

INPUT_FILE_CONTENT = """
- front: front1
  back: back1
- front: front2
  back: back2
"""


@pytest.fixture
def input_file(tmp_path):
    file = tmp_path / "input_file.yaml"
    file.write_text(INPUT_FILE_CONTENT)
    return str(file)


def test_read_yaml(input_file):
    actual = ReadYaml(path=input_file).process([])
    expected = [
        dict(front="front1", back="back1"),
        dict(front="front2", back="back2"),
    ]
    assert list(actual) == expected
