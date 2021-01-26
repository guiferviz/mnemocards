"""Module for automatic generation of TSV-files for vocabulary cards."""

import os
from itertools import count
from googletrans import Translator
from itertools import count
from time import sleep
from mnemocards.utils import get_hash_id


def get_translation(words, src="auto", dest="en"):

    if isinstance(words, str):
        words = [words]

    words = list(set(words))

    translator = Translator()
    try:
        translations = translator.translate(words, src=src, dest=dest)
        return translations
    except AttributeError:
        print("Translation time-out, retrying in 3 seconds")
        sleep(3)
        return False


def create_tsv_line(translation):
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


def generate_tsv_configs(words, full_deck_name, new_deck_name, src="auto", dest="en"):

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


def scrape_words_from_file(data_dir, word_file):
    filename = os.path.join(data_dir, word_file)
    with open(filename, "r+") as file:
        words_list = []
        for word in file:
            words_list.append(word.strip())
    return words_list


def collect_tsv_configs(args):
    all_words = []
    all_words += scrape_words_from_file(args.data_dir, args.word_file)
    if args.recursive:
        for root, dirs, files in os.walk(args.data_dir):
            # Ignore hidden folders.
            dirs[:] = [d for d in dirs if not d[0] == "."]
            for d in dirs:
                d = os.path.join(root, d)
                all_words += scrape_words_from_file(d, args.word_file)
    tsv_configs = generate_tsv_configs(all_words)
    return tsv_configs


def save_tsv_files(tsv_configs, output_dir, language_pair):
    print("Writing packages to a file...")
    for one_config in tsv_configs:
        filename = os.path.join(output_dir, f"{language_pair}.tsv")
        with open(filename, 'w') as file:
            file.write(one_config)


def make_tsv(args):
    if not os.path.exists(args.data_dir):

        raise Exception("Data dir does not exist")
    tsv_configs = collect_tsv_configs(args)
    save_tsv_files(tsv_configs, args.output_dir, args.language_pair)

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
