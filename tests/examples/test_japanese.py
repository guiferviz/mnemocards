from mnemocards.cli import CLI


def test_japanese():
    assert not CLI().run("examples/japanese")
