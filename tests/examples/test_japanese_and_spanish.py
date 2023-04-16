from mnemocards.cli import CLI


def test_japanese_and_spanish():
    assert not CLI().run("examples/japanese_and_spanish")
