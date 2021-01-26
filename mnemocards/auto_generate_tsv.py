"""Module for automatic generation of TSV-files for vocabulary cards."""

from itertools import count
from googletrans import Translator
from itertools import count
from time import sleep


def get_translation(words, src="auto", dest="en"):

    if isinstance(words, str):
        words = [words]

    words = set(words)
    words = list(words)

    translator = Translator()
    try:
        translations = translator.translate(words, src=src, dest=dest)
        return translations
    except AttributeError as er:
        print(f"{er}, retrying in 3 seconds")
        sleep(3)
        return False


def check_double_translations(all_trans, main_trans):
    """
    Determines if main translation is unique or has doubles in all-translations.
    """
    if (main_trans in all_trans) or (main_trans.lower() in all_trans):
        return True
    else:
        return any(
            check_double_translations(sublist, main_trans)
            for sublist in all_trans
            if isinstance(sublist, list)
        )


def make_cards(translation):
    main_trans = translation.extra_data["translation"]
    full_trans = translation.extra_data["all-translations"]
    main_trans = main_trans[0][0]
    orig = translation.origin

    if main_trans.lower() == orig.lower() and full_trans is None:
        return None

    forward_card = f"<h1>{orig}</h1>\t"
    backward_card = ""

    single_trans = (
        f'<div style="text-align: left; line-height: 110%">{main_trans}</div>'
    )

    if full_trans is not None:

        if not check_double_translations(full_trans, main_trans):
            forward_card += single_trans
            backward_card += single_trans.replace("text-align: left; ", "")

        for block in full_trans:

            part_of_speech = f'<div style="text-align: left; font-size: 70%; color: #4285f4; line-height: 120%">{block[0].title()}</div>'
            forward_card += part_of_speech

            counter = count(1)
            for word in block[2]:
                if next(counter) > 3:
                    continue
                variant = f'<div style="text-align: left; line-height: 110%">{word[0]}</div>'
                similar = f'<div style="text-align: left; color: #959392; font-size: 80%;">{word[1]}</div>'
                forward_card += variant + similar
                backward_card += variant.replace("text-align: left; ", "")

    else:
        forward_card += single_trans
        backward_card += single_trans.replace("text-align: left; ", "")

    backward_card += f'\t<div align="left">{orig}</div>'

    return [forward_card, backward_card]


def build_deck(words, full_deck_name, new_deck_name, src="auto", dest="en"):

    with open(new_deck_name + ".csv", "w") as new_deck_file, open(
        full_deck_name + ".csv", "a+"
    ) as full_deck_file:

        translations = False
        while translations == False:
            translations = get_translation(words, src, dest)

        # counter = count(1)
        card_pairs = []
        for translation in translations:

            pair = make_cards(translation)

            if pair is None:
                continue

            card_pairs.append(pair)

        for card_pair in sorted(card_pairs):
            for card in card_pair:
                new_deck_file.write(card)
                full_deck_file.write(card)
                new_deck_file.write("\n")
                full_deck_file.write("\n")


def list_from_file(filename):
    with open(filename, "r+") as f:
        words = []
        for word in f:
            words.append(word.strip())
        f.truncate(0)
    return words


# words = list_from_file("new_words.txt")
# build_deck(
#     words, "english_words_full_deck", "english_words_new_cards", "en", "ru"
# )

# from shutil import copyfile

# copyfile(
#     "./english_words_new_cards.csv",
#     "/mnt/c/Projects/english_words_new_cards.csv",
# )

# print("finished")


# translation = get_translation("shit happens", "en", "ru")
# for item in translation:
#     # print(item.src)
#     # print(item.dest)
#     # print(item.origin)
#     # print(item.text)
#     # print(item.pronunciation)
#     # print(item.extra_data)
#     for line in item.extra_data:
#         print(line, item.extra_data.get(line))
