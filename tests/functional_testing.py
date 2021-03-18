import unittest
import subprocess
import os
import json
from shutil import rmtree


class CardGeneratorTest(unittest.TestCase):
    """This test checks automatic generation of TSV files and cards"""

    def test_can_generate_tsv_file_from_command_line(self):
        """This test checks if maketsv command generates proper TSV file
        from list of words"""

        # Dan navigates his terminal to the folder for testing
        # and checks that current folder is the right one.
        mnemocards_folder = os.getcwd().split('/mnemocards')[0]
        card_folder = os.path.join(
            mnemocards_folder, "mnemocards/tests/test_card_folder")
        os.chdir(card_folder)

        current_folder = subprocess.getstatusoutput("echo $PWD")[1]
        right_folder = card_folder
        self.assertEqual(current_folder, right_folder)

        # he taps command into the terminal and checks that there is no
        # error and that corret message is displayed.
        s = subprocess.getstatusoutput("mnemocards maketsv . -l en_ru")
        self.assertNotIn("error", s[1])
        self.assertEqual("Writing tsv-config to en_ru.tsv...", s[1])

        # He checks that correct tsv file is generated.
        # The name of the file should be en_ru.tsv
        # He also checks if example file exist.
        generated_file_path = os.path.join(card_folder, "en_ru.tsv")
        example_file_path = os.path.join(card_folder, "correct_tsv_file.tsv")
        self.assertTrue(os.path.exists(example_file_path))
        self.assertTrue(os.path.exists(generated_file_path))

        # He checks that generated file is identical to the example file.
        generated_file = open(generated_file_path, 'r')
        generated_file_text = generated_file.read()
        generated_file.close()

        example_file = open(example_file_path, 'r')
        example_file_text = example_file.read()
        example_file.close()

        self.assertEqual(example_file_text, generated_file_text)

        # He removes generated file after all test passed.
        os.remove(generated_file_path)
        self.assertFalse(os.path.exists(generated_file_path))

        # He now knows that command maketsv works as intended.

    def test_can_generate_apkg_from_config(self):
        """This test checks that generate command works with configs file
        written for autogenerate type, for both generation from TSV made
        using maketsv and from list of words."""

        # Today Dan test new command, autogenerate.
        # Dan navigates his terminal to the folder for testing
        # and checks that current folder is the right one.
        mnemocards_folder = os.getcwd().split('/mnemocards')[0]
        card_folder = os.path.join(
            mnemocards_folder, "mnemocards/tests/test_card_folder")
        os.chdir(card_folder)
        current_folder = subprocess.getstatusoutput("echo $PWD")[1]
        right_folder = card_folder
        self.assertEqual(current_folder, right_folder)

        # he checks that file words.txt and card_config.json exist in the
        # current folder.
        config_path = os.path.join(card_folder, "cards_config.json")
        words_path = os.path.join(card_folder, "words.txt")
        self.assertTrue(os.path.exists(config_path))
        self.assertTrue(os.path.exists(words_path))

        # he taps command into the terminal and checks that there is no
        # error and that corret message is displayed.
        s = subprocess.getstatusoutput("mnemocards generate .")
        self.assertNotIn("Traceback", s[1])
        self.assertIn("Writing", s[1])

        # after that he checks, that new apkg file appeared in the folder.
        config_file = open(config_path, 'r')
        config = json.load(config_file)
        config_file.close()

        apkg_name = f'{config["packages"][0]["name"]}.apkg'
        apkg_path = os.path.join(card_folder, apkg_name)
        media_folder = os.path.join(card_folder, ".media")
        rmtree(media_folder)

        self.assertTrue(os.path.exists(apkg_path))
        # he then removes apkg file and finishes test.
        os.remove(apkg_path)
        self.assertFalse(os.path.exists(apkg_path))


if __name__ == "__main__":
    unittest.main()
