from mnemocards.any2dict.toml_reader import TOML


TOML_TXT = """
[[cards]]
front = "front1"
back = "back1"

[[cards]]
front = "front2"
back = "back2"
"""


def test_toml_reader():
    actual_dict = TOML().loads(TOML_TXT)
    expected_dict = dict(
        cards=[
            dict(front="front1", back="back1"),
            dict(front="front2", back="back2"),
        ],
    )
    assert actual_dict == expected_dict
