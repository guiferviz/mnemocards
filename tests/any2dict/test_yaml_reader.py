import pytest

from mnemocards.any2dict.yaml_reader import YAML


YAML_TXT = """
- front: front1
  back: back1
- front: front2
  back: back2
"""


def test_yaml_reader():
    actual_dict = YAML().loads(YAML_TXT)
    expected_dict = [
        dict(front="front1", back="back1"),
        dict(front="front2", back="back2"),
    ]
    assert actual_dict == expected_dict


def test_fail_when_pyyaml_is_not_installed(mocker):
    mocker.patch("mnemocards.any2dict.yaml_reader.pyyaml_exists", False)
    yaml = YAML()
    with pytest.raises(ImportError) as excinfo:
        yaml.loads(YAML_TXT)
    assert "pyyaml" in str(excinfo.value)
