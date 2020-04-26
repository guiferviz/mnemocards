
from .context import mnemocards


def test_import():
    """Test that import mnemocards does not give any errors. """

    assert True


def test_genanki():
    """Test that the installed genanki package is my fork. """

    import genanki

    genanki.Deck("26f0a173-57c6-4f41-b1e7-e74ca62832bc", "MyDeck", conf=None)

