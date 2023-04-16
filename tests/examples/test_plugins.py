from mnemocards.cli import CLI


def test_plugins():
    assert not CLI().run("examples/plugins")
