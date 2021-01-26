import unittest
import os
import pickle

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
                           'не терпеть глупостей', 'гребень']

    example_translation = {'translation': [['насмехаться', 'scoff', None, None, 3, None, None, [[]], [[['cce7c67b3f2439089dd6b428e0b83b88', 'en_ru_2020q2.md']]]], [None, None, "nasmekhat'sya", 'skôf']], 'all-translations': [['глагол', ['издеваться', 'насмехаться', 'глумиться', 'зубоскалить', 'жрать', 'засмеять', 'есть с жадностью'], [['издеваться', ['scoff', 'mock', 'flout', 'ride', 'guy', 'roast'], None, 0.24126123], ['насмехаться', ['mock', 'taunt', 'scoff', 'razz', 'sneer', 'deride'], None, 0.15822297], ['глумиться', ['mock', 'scoff', 'sneer', 'jeer', 'flout'], None, 0.017752126], ['зубоскалить', ['scoff'], None, 0.00995804], ['жрать', ['fress', 'scoff', 'knock back'], None, 0.0012080474], ['засмеять', ['laugh down', 'scoff'], None, 0.0009706933], ['есть с жадностью', ['gorge', 'raven', 'tuck into', 'guzzle', 'devour', 'scoff'], None, 0.00048052802]], 'scoff', 2], ['имя существительное', ['насмешка', 'жратва', 'посмешище', 'еда'], [['насмешка', ['mockery', 'ridicule', 'sneer', 'taunt', 'jibe', 'scoff'], None, 0.0028979548, None, 2], ['жратва', ['scoff'], None, 0.0019304542, None, 2], ['посмешище', ['mockery', 'laughing-stock', 'joke', 'derision', 'mock', 'scoff'], None, 0.0009706933, None, 3], ['еда', ['food', 'meal', 'eating', 'fare', 'meat', 'scoff'], None, 0.000721358, None, 2]], 'scoff', 1]], 'original-language': 'en', 'possible-translations': [['scoff', None, [['насмехаться', 0, True, False], ['Scoff', 0, True, False]], [[0, 5]], 'scoff', 0, 0]], 'confidence': 1.0, 'possible-mistakes': None, 'language': [['en'], None, [1.0], ['en']], 'synonyms': [['глагол', [[['make sport of'], 'm_en_gbus0909000.007'], [['fleer at', "bite one's thumb at", 'scout at'], 'm_en_gbus0909000.007'], [
        ['mock', 'deride', 'ridicule', 'sneer at', 'be scornful about', 'treat contemptuously', 'jeer at', 'jibe at', 'make fun of', 'poke fun at', 'laugh at', 'scorn', 'laugh to scorn', 'dismiss', 'pooh-pooh', 'make light of', 'belittle', 'taunt', 'tease', 'make a fool of', 'rag'], 'm_en_gbus0909000.007'], [["thumb one's nose at", 'take the mickey out of', 'poke mullock at'], 'm_en_gbus0909000.007'], [['eat', 'devour', 'consume', 'guzzle', 'gobble', 'wolf down', 'polish off', 'finish off', 'gulp down', 'bolt', 'put away', 'nosh', 'get outside of', 'pack away', 'demolish', 'shovel down', 'stuff(down)', "stuff one's face with", 'stuff oneself with', 'pig oneself on', 'pig out on', 'sink', 'gollop', 'shift', "get one's laughing gear round", 'gorb', 'scarf(down/up)', 'snarf(down/up)', 'inhale'], 'm_en_gbus0909010.007'], [['ingurgitate'], 'm_en_gbus0909010.007']], 'scoff'], ['имя существительное', [[['food', 'fare', 'eatables', 'refreshments', 'grub', 'nosh', 'chow', 'eats', 'feed', 'tuck', 'chuck'], 'm_en_gbus0909010.014'], [['victuals', 'vittles', 'meat'], 'm_en_gbus0909010.014']], 'scoff']], 'definitions': [['глагол', [['speak to someone or about something in a scornfully derisive or mocking way.', 'm_en_gbus0909000.007', '“You, a scientist?” he scoffed'], ['eat(something) quickly and greedily.', 'm_en_gbus0909010.007', 'she scoffed down several chops']], 'scoff'], ['имя существительное', [['an expression of scornful derision.', 'm_en_gbus0909000.014', 'scoffs of disbelief'], ['food.', 'm_en_gbus0909010.014']], 'scoff']], 'examples': [[['his army was the < b > scoff < /b > of all Europe', None, None, None, 3, 'm_en_gbus0909000.017']]], 'see-also': None}

    example_tsv_line = ""

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

    def test_translation_converts_to_tsv_line(self):
        translation = tsv.get_translation('scoff', 'en', 'ru')
        expected_line = self.example_tsv_line
        created_line = tsv.create_tsv_line(
            translation[0])
        self.assertEqual(created_line, expected_line)
    # ID	YourLanguageWord	YourLanguageExplanation	LanguageYouLearnWord	LanguageYouLearnPronunciation	LanguageYouLearnExplanation	Tags


if __name__ == "__main__":
    unittest.main()
