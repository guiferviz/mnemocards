import unittest
import os

from mnemocards import auto_generate_tsv as tsv


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


class AutoGenerateTsvUnitTestSuit(unittest.TestCase):

    data_dir, word_file = '/home/otterman/python_projects/active/mnemocards/tests/test_card_folder', 'words.txt'
    word_file_path = [data_dir, word_file]
    word_list = ['concert', 'shit happens', 'brook no nonsense', 'ridge']
    word_list_tranlated = ['концерт', 'дерьмо случается',
                           'не терпеть глупосте', 'гребень']

    def test_words_file_scraped(self):

        scraped_words = tsv.scrape_words_from_file(
            *self.word_file_path)
        self.assertEqual(scraped_words, self.word_list)

    def test_tsv_are_saved(self):

        test_tsv_config = open("test_tsv_config.tsv", 'r')
        output_dir = "test_card_folder"
        language_pair = "en_ru"

        tsv.save_tsv_files([test_tsv_config.read()],
                           output_dir, language_pair)

        test_tsv_config.seek(0)
        result_tsv = open("test_card_folder/en_ru.tsv", 'r')

        self.assertEqual(test_tsv_config.read(), result_tsv.read())

        test_tsv_config.close()
        result_tsv.close()
        os.remove('test_card_folder/en_ru.tsv')

    def test_tsv_config_generated(self):
        pass

    def test_words_are_collected(self):
        args = {'command': 'maketsv', 'data_dir': '.', 'language_pair': 'en_ru',
                'output_dir': '.', 'recursive': True, 'word_file': 'words.txt'}

        pass

    def test_words_are_translated(self):
        translations = tsv.get_translation(self.word_list, 'en', 'ru')
        expected_type = "<class 'googletrans.models.Translated'>"
        self.assertEqual(str(type(translations[0])), expected_type)
        self.assertIn(translations[0].text, self.word_list_tranlated)


if __name__ == "__main__":
    unittest.main()
