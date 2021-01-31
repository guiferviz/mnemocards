"""Unit-tests module. Tests should be run from mnemocards/tests folder."""

import unittest
import os
import pytest
from mnemocards import autogenerate_tsv as tsv
from mnemocards import autogenerate_deck as gendeck


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


@pytest.mark.maketsv
class AutoGenerateTsvUnitTestSuit(unittest.TestCase):

    data_dir = os.getcwd()
    word_file = 'words.txt'
    word_file_path = [os.path.join(data_dir, "test_card_folder"), word_file]
    word_list = ['concert', 'shit happens', 'brook no nonsense', 'ridge']
    word_list_tranlated = ['концерт', 'дерьмо случается',
                           'не терпеть глупостей', 'гребень']

    example_translation = {'translation': [['насмехаться', 'scoff', None, None, 3, None, None, [[]], [[['cce7c67b3f2439089dd6b428e0b83b88', 'en_ru_2020q2.md']]]], [None, None, "nasmekhat'sya", 'skôf']], 'all-translations': [['глагол', ['издеваться', 'насмехаться', 'глумиться', 'зубоскалить', 'жрать', 'засмеять', 'есть с жадностью'], [['издеваться', ['scoff', 'mock', 'flout', 'ride', 'guy', 'roast'], None, 0.24126123], ['насмехаться', ['mock', 'taunt', 'scoff', 'razz', 'sneer', 'deride'], None, 0.15822297], ['глумиться', ['mock', 'scoff', 'sneer', 'jeer', 'flout'], None, 0.017752126], ['зубоскалить', ['scoff'], None, 0.00995804], ['жрать', ['fress', 'scoff', 'knock back'], None, 0.0012080474], ['засмеять', ['laugh down', 'scoff'], None, 0.0009706933], ['есть с жадностью', ['gorge', 'raven', 'tuck into', 'guzzle', 'devour', 'scoff'], None, 0.00048052802]], 'scoff', 2], ['имя существительное', ['насмешка', 'жратва', 'посмешище', 'еда'], [['насмешка', ['mockery', 'ridicule', 'sneer', 'taunt', 'jibe', 'scoff'], None, 0.0028979548, None, 2], ['жратва', ['scoff'], None, 0.0019304542, None, 2], ['посмешище', ['mockery', 'laughing-stock', 'joke', 'derision', 'mock', 'scoff'], None, 0.0009706933, None, 3], ['еда', ['food', 'meal', 'eating', 'fare', 'meat', 'scoff'], None, 0.000721358, None, 2]], 'scoff', 1]], 'original-language': 'en', 'possible-translations': [['scoff', None, [['насмехаться', 0, True, False], ['Scoff', 0, True, False]], [[0, 5]], 'scoff', 0, 0]], 'confidence': 1.0, 'possible-mistakes': None, 'language': [['en'], None, [1.0], ['en']], 'synonyms': [['глагол', [[['make sport of'], 'm_en_gbus0909000.007'], [['fleer at', "bite one's thumb at", 'scout at'], 'm_en_gbus0909000.007'], [
        ['mock', 'deride', 'ridicule', 'sneer at', 'be scornful about', 'treat contemptuously', 'jeer at', 'jibe at', 'make fun of', 'poke fun at', 'laugh at', 'scorn', 'laugh to scorn', 'dismiss', 'pooh-pooh', 'make light of', 'belittle', 'taunt', 'tease', 'make a fool of', 'rag'], 'm_en_gbus0909000.007'], [["thumb one's nose at", 'take the mickey out of', 'poke mullock at'], 'm_en_gbus0909000.007'], [['eat', 'devour', 'consume', 'guzzle', 'gobble', 'wolf down', 'polish off', 'finish off', 'gulp down', 'bolt', 'put away', 'nosh', 'get outside of', 'pack away', 'demolish', 'shovel down', 'stuff(down)', "stuff one's face with", 'stuff oneself with', 'pig oneself on', 'pig out on', 'sink', 'gollop', 'shift', "get one's laughing gear round", 'gorb', 'scarf(down/up)', 'snarf(down/up)', 'inhale'], 'm_en_gbus0909010.007'], [['ingurgitate'], 'm_en_gbus0909010.007']], 'scoff'], ['имя существительное', [[['food', 'fare', 'eatables', 'refreshments', 'grub', 'nosh', 'chow', 'eats', 'feed', 'tuck', 'chuck'], 'm_en_gbus0909010.014'], [['victuals', 'vittles', 'meat'], 'm_en_gbus0909010.014']], 'scoff']], 'definitions': [['глагол', [['speak to someone or about something in a scornfully derisive or mocking way.', 'm_en_gbus0909000.007', '“You, a scientist?” he scoffed'], ['eat(something) quickly and greedily.', 'm_en_gbus0909010.007', 'she scoffed down several chops']], 'scoff'], ['имя существительное', [['an expression of scornful derision.', 'm_en_gbus0909000.014', 'scoffs of disbelief'], ['food.', 'm_en_gbus0909010.014']], 'scoff']], 'examples': [[['his army was the < b > scoff < /b > of all Europe', None, None, None, 3, 'm_en_gbus0909000.017']]], 'see-also': None}

    example_tsv_line = """c507ebf1-4f30-5423-9b61-14de4e116c03	концерт	<div class="synonyms speech_part">Имя Существительное</div><div class="synonyms line_1">концерт</div><div class="synonyms line_2">['concert', 'concerto']</div><div class="synonyms line_1">согласие</div><div class="synonyms line_2">['agreement', 'consent', 'harmony', 'accordance', 'accord', 'concert']</div><div class="synonyms line_1">соглашение</div><div class="synonyms line_2">['agreement', 'convention', 'deal', 'arrangement', 'contract', 'concert']</div><div class="synonyms speech_part">Имя Прилагательное</div><div class="synonyms line_1">концертный</div><div class="synonyms line_2">['concert', 'odeum']</div><div class="synonyms speech_part">Глагол</div><div class="synonyms line_1">сговариваться</div><div class="synonyms line_2">['conspire', 'arrange', 'agree', 'concert', 'come to an agreement', 'arrange things']</div><div class="synonyms line_1">договариваться</div><div class="synonyms line_2">['agree', 'negotiate', 'arrange', 'make arrangements', 'parley', 'concert']</div><div class="synonyms line_1">сообща принимать меры</div><div class="synonyms line_2">['concert']</div>	concert		<div class="definitions speech_part">Имя Существительное</div><div class="definitions line_1">a musical performance given in public, typically by several performers or of several separate compositions.</div><div class="definitions line_2">a concert pianist</div><div class="definitions line_1">agreement, accordance, or harmony.</div><div class="definitions line_2">critics' inability to describe with any precision and concert the characteristics of literature</div><div class="definitions speech_part">Глагол</div><div class="definitions line_1">arrange (something) by mutual agreement or coordination.</div><div class="definitions line_2">they started meeting regularly to concert their tactics</div>	"""

    example_tsv_filename = os.path.join(data_dir, "test_tsv_config.tsv")

    def test_words_file_scraped(self):

        scraped_words = tsv.scrape_words_from_file(
            *self.word_file_path)
        self.assertEqual(scraped_words, self.word_list)

    def test_tsv_are_saved(self):

        test_tsv_config = open(self.example_tsv_filename, 'r')
        output_dir = self.data_dir
        language_pair = "en_ru"

        tsv.save_tsv_files([test_tsv_config.read()],
                           output_dir, language_pair)

        test_tsv_config.seek(0)
        result_tsv_path = os.path.join(self.data_dir, "en_ru.tsv")
        result_tsv = open(result_tsv_path, 'r')

        self.assertEqual(test_tsv_config.read(), result_tsv.read())

        test_tsv_config.close()
        result_tsv.close()
        os.remove(result_tsv_path)

    def test_tsv_lines_generated(self):
        expected_tsv_line = []
        with open(self.example_tsv_filename, 'r') as tsv_file:

            for line in tsv_file.readlines():
                expected_tsv_line += [line]

        generated_tsv_lines = tsv.generate_tsv_lines(self.word_list, "en_ru")
        self.assertEqual(expected_tsv_line, generated_tsv_lines)

    def test_words_are_translated(self):
        translations = tsv.get_translation(self.word_list, 'en', 'ru')
        expected_type = "<class 'googletrans.models.Translated'>"
        self.assertEqual(str(type(translations[0])), expected_type)
        self.assertIn(translations[0].text, self.word_list_tranlated)

    def test_translation_converts_to_tsv_line(self):
        translation = tsv.get_translation('concert', 'en', 'ru')
        expected_line = self.example_tsv_line
        created_line = """"""
        for item in tsv.prepare_card_fields(translation[0]):
            created_line += item + '\t'
        self.assertEqual(created_line, expected_line)


@pytest.mark.autogenerate
class AutoGenerateDeckUnitTestSuit(unittest.TestCase):

    apkg_path = os.path.join(os.getcwd(), "google_trans_deck.apkg")

    class Args():
        def __init__(self):
            self.data_dir = "."
            self.config_file = "cards_config.json"
            self.recursive = True

    args = Args()

    def test_autogenerate_builds_package(self):
        gendeck.autogenerate(self.args)
        self.assertTrue(os.path.exists(self.apkg_path))


if __name__ == "__main__":
    unittest.main()
