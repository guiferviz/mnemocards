import mnemocards
import unittest
from mnemocards.auto_generate_tsv import get_translation


class CustomModulesTest(unittest.TestCase):
    def test_mnemocards_import(self):
        """Test that import mnemocards does not give any errors. """

        import mnemocards

        assert True

    def test_genanki(self):
        """Test that the installed genanki package is my fork. """

        import genanki

        genanki.Deck(
            "26f0a173-57c6-4f41-b1e7-e74ca62832bc", "MyDeck", conf=None
        )


class TranslationModuleTestsuit(unittest.TestCase):
    def setUp(self):
        self.single_word = "concert"
        self.multiple_word = ["stiff", "countenance", "yield"]
        self.translator = get_translation

    def test_single_word_returns_translation(self):

        translation = self.translator("concert", "en", "ru")
        for item in translation:
            self.assertIn("концерт", item.extra_data["translation"][0][0])


if __name__ == "__main__":
    unittest.main()