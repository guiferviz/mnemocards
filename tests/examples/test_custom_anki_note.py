from mnemocards.cli import CLI


def test_japanese():
    assert not CLI().run("examples/custom_anki_note")
