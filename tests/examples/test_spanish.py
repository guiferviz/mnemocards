from mnemocards.cli import CLI


def test_spanish():
    assert not CLI().run("examples/spanish")
