import shutil
from mnemocards.any2dict import any2dict

import pytest


@pytest.fixture
def directory(tmp_path):
    root = tmp_path / "cards"
    root.mkdir()
    top_csv = root / "top.csv"
    top_csv.write_text("a,b\n1,2\n3,4")
    top_json = root / "top.json"
    top_json.write_text('{"a": 1}')
    sub = root / "sub"
    sub.mkdir()
    sub_tsv = sub / "sub.tsv"
    sub_tsv.write_text("a\tb\n1\t2")
    subsub = sub / "sub"
    subsub.mkdir()
    subsub_tsv = subsub / "sub.tsv"
    subsub_tsv.write_text("a\tb\n1\t2")
    yield root
    shutil.rmtree(str(root))


def test_any2dict(directory):
    actual = any2dict(directory, max_recursion_level=3)
    expected = {
        "cards": {
            "top.csv": [
                dict(a="1", b="2"),
                dict(a="3", b="4"),
            ],
            "top.json": {
                "a": 1,
            },
            "sub": {
                "sub": {},
                "sub.tsv": [
                    dict(a="1", b="2"),
                ],
            },
        },
    }
    assert actual == expected


@pytest.fixture
def unknown_dir(tmp_path):
    root = tmp_path / "cards"
    root.mkdir()
    top_unknown = root / "top.unknown"
    top_unknown.touch()
    yield root
    shutil.rmtree(str(root))


def test_unknown_format(unknown_dir):
    with pytest.raises(ValueError):
        any2dict(unknown_dir)
