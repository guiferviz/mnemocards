"""Unit-tests module. Tests should be run from mnemocards/tests folder."""
import unittest
import os
import pytest
import json
from shutil import rmtree
from mnemocards.builders.autogenerate_builder import AutogenerateBuilder as ab
from mnemocards import generate as gendeck
from mnemocards import maketsv as tsv


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
    word_file_path = [word_file, os.path.join(data_dir, "test_card_folder")]
    word_list = ['concert', 'shit happens', 'brook no nonsense', 'ridge']
    word_list_tranlated = ['концерт', 'дерьмо случается',
                           'не терпи ерунды', 'гребень']

    example_tsv_line = """c507ebf1-4f30-5423-9b61-14de4e116c03	концерт	<div class="synonyms"><div class="speechpart">Имя Существительное</div><div class="line_1">согласие</div><div class="line_2">['agreement', 'consent', 'harmony', 'accordance', 'accord', 'concert']</div><div class="line_1">соглашение</div><div class="line_2">['agreement', 'convention', 'deal', 'arrangement', 'contract', 'concert']</div><div class="speechpart">Имя Прилагательное</div><div class="line_1">концертный</div><div class="line_2">['concert', 'odeum']</div><div class="speechpart">Глагол</div><div class="line_1">сговариваться</div><div class="line_2">['conspire', 'arrange', 'agree', 'concert', 'come to an agreement', 'arrange things']</div><div class="line_1">договариваться</div><div class="line_2">['agree', 'negotiate', 'arrange', 'make arrangements', 'parley', 'concert']</div><div class="line_1">сообща принимать меры</div><div class="line_2">['concert']</div></div>	concert		<div class="definitions"><div class="speechpart">Имя Существительное</div><div class="line_1">a musical performance given in public, typically by several performers or of several separate compositions.</div><div class="line_2">a concert pianist</div><div class="line_1">agreement, accordance, or harmony.</div><div class="line_2">critics' inability to describe with any precision and concert the characteristics of literature</div><div class="speechpart">Глагол</div><div class="line_1">arrange (something) by mutual agreement or coordination.</div><div class="line_2">they started meeting regularly to concert their tactics</div></div>	"""

    example_tsv_filename = os.path.join(
        data_dir, "test_card_folder/correct_tsv_file.tsv")

    def test_words_file_scraped(self):
        print("testing that files with words scraped correctly")
        scraped_words = tsv.scrape_words_from_file(
            *self.word_file_path)
        self.assertEqual(scraped_words, self.word_list)

    def test_tsv_are_saved(self):
        print("testing that tsv-file saves on disk")
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

    @pytest.mark.slow
    def test_tsv_lines_generated(self):
        print("testing that tsv-lines generate correctly")
        expected_tsv_line = []
        with open(self.example_tsv_filename, 'r') as tsv_file:

            for line in tsv_file.readlines():
                expected_tsv_line += [line]

        generated_tsv_lines = tsv.generate_tsv_lines(self.word_list, "en_ru")

        correct_lines = 0

        for line in generated_tsv_lines:
            if line in expected_tsv_line:
                correct_lines += 1

        self.assertTrue(correct_lines >= 2)

    @pytest.mark.slow
    def test_words_are_translated(self):
        print("testing that words are translated")
        translations = tsv.get_translation(self.word_list, 'en', 'ru')
        expected_type = "<class 'googletrans.models.Translated'>"
        self.assertEqual(str(type(translations[0])), expected_type)
        self.assertIn(translations[0].text, self.word_list_tranlated)

    @pytest.mark.slow
    def test_translation_converts_to_tsv_line(self):
        # TODO: create plug object for translation
        print("testing tranlsation objects convert to tsv-lines")
        translation = tsv.get_translation('concert', 'en', 'ru')
        expected_line = self.example_tsv_line
        created_line = """"""
        card_fields = tsv.prepare_card_fields(translation[0])
        for item in card_fields:
            created_line += card_fields[item] + '\t'
        self.assertEqual(created_line, expected_line)


@pytest.mark.autogenerate
class AutoGenerateDeckUnitTestSuit(unittest.TestCase, ab):

    class TestArgs():
        def __init__(self):
            project_path = os.getcwd().split('/tests')[0]
            self.data_dir = os.path.join(
                project_path, "tests/test_card_folder")
            self.config_file = "cards_config.json"
            self.recursive = False
            self.output_dir = self.data_dir
    args = TestArgs()

    @classmethod
    def tearDown(self):
        media_dir = os.path.join(self.args.data_dir, ".media")
        if os.path.exists(media_dir):
            rmtree(media_dir)

    @pytest.mark.slow
    @pytest.mark.builder
    def test_generate_builds_package(self):
        print("testing main generate command builds from config")
        apkg_path = os.path.join(self.args.output_dir,
                                 "google_trans_deck.apkg")
        gendeck.generate(self.args)
        self.assertTrue(os.path.exists(apkg_path))
        # os.remove(apkg_path)

    def test_building_cards_from_tsv(self):
        print("testing card building from TSV")
        args = self.args
        configpath = os.path.join(args.data_dir, self.args.config_file)
        with open(configpath, 'r') as file:
            config = json.load(file)
        src = config["packages"][0]["decks"][1]["src"][0]
        self.assertTrue("tsv" in src["file"].split('.')[-1])
        settings = self.parse_src_to_settings(args.data_dir, src)
        cards = self.build_cards_from_tsv(settings)
        keys = ["card_id", "ylw", "yle", "lylw", "lylp", "lyle", "tags"]

        for card in cards:
            for field in card.keys():
                self.assertIn(field, keys)

    def test_build_notes_and_media(self):
        print("testing notes object and media path generates")
        args = self.args
        configpath = os.path.join(args.data_dir, self.args.config_file)
        with open(configpath, 'r') as file:
            config = json.load(file)
        src = config["packages"][0]["decks"][1]["src"][0]
        self.assertTrue("tsv" in src["file"].split('.')[-1])
        settings = self.parse_src_to_settings(args.data_dir, src)
        cards = self.build_cards_from_tsv(settings)
        notes, media = self.build_notes_and_media(settings, cards)
        for note in notes:
            self.assertIn("mnemocards.utils.NoteID object", str(note))
        self.assertEqual(len(notes), len(media))


if __name__ == "__main__":
    unittest.main()
