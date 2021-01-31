import unittest
import subprocess
import os


class CardGeneratorTest(unittest.TestCase):
    def test_can_generate_tsv_file_from_command_line(self):
        # Dan navigates his terminal to the folder for testing
        # and checks that current folder is the right one.
        card_folder = os.path.join(os.getcwd(), "tests/test_card_folder/")
        os.chdir(card_folder)

        current_folder = subprocess.getstatusoutput("echo $PWD")[1]
        right_folder = "/home/otterman/python_projects/active/mnemocards/tests/test_card_folder"
        self.assertEqual(current_folder, right_folder)

        # he taps command into the terminal and checks that there is no
        # error.
        s = subprocess.getstatusoutput("mnemocards maketsv .")
        self.assertNotIn("error", s[1])

        # checks that there the test opened file "card_config.json" and
        # and printed all the configs.
        # config_path = os.path.join(current_folder, "cards_config.json")
        config_file = open("cards_config.json", "r")
        config_text = config_file.read()
        config_file.close()
        print(config_text)
        self.assertEqual(config_text, s[1])
        self.fail("finish the test")


if __name__ == "__main__":
    unittest.main()
