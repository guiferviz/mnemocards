import pytest

from mnemocards_essentials import ReadXml

INPUT_FILE_CONTENT = """
<cards>
    <card>
        <front>front1</front>
        <back>back1</back>
    </card>
    <card>
        <front>front2</front>
        <back>back2</back>
    </card>
</cards>
"""


@pytest.fixture
def input_file(tmp_path):
    file = tmp_path / "input_file.xml"
    file.write_text(INPUT_FILE_CONTENT)
    return str(file)


def test_read_xml(input_file):
    actual = ReadXml(path=input_file).process([])
    expected = [
        dict(front="front1", back="back1"),
        dict(front="front2", back="back2"),
    ]
    assert list(actual) == expected
