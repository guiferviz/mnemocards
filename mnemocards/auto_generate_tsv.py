"""Module for automatic generation of TSV-files for vocabulary cards."""

import os
from itertools import count
from googletrans import Translator
from time import sleep
from mnemocards.utils import generate_card_uuid


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


def format_explanations(list_obj, explanation_name):
    """Formats either translation synonyms or definitions in original language.

    Args:
        list_obj (list): takes list from googletranslate object.
        explanation_name (str): either 'synonyms' or 'definitions' for
            naming a div class.

    Returns:
        [str]: formated explanation for TSV-file.
    """
    formatted_explanation = ''

    for block in list_obj:

        # todo написать тестовую строку с css как должно выглядеть в
        # карте. обязательно добавить класс.

        part_of_speech = f'<div class="{explanation_name} speech_part">{block[0].title()}</div>'
        formatted_explanation += part_of_speech

        explanation_block = 1

        if explanation_name == 'synonyms':
            explanation_block = 2

        counter = count(1)
        for line in block[explanation_block]:
            if next(counter) > 3:
                continue
            synonym_dest_lang = f'<div class="{explanation_name} line_1">{line[0]}</div>'

            if len(line) > 3:
                synonyms_orig_lang = f'<div class="{explanation_name} line_2">{line[1]}</div>'
            elif len(line) == 3:
                synonyms_orig_lang = f'<div class="{explanation_name} line_2">{line[-1]}</div>'
            else:
                synonyms_orig_lang = ''

            formatted_explanation += synonym_dest_lang + synonyms_orig_lang

    return formatted_explanation


def create_tsv_line(translation):
    main_translation = translation.extra_data["translation"]
    full_trans = translation.extra_data["all-translations"]
    definitions_trans = translation.extra_data["definitions"]

    ylw = main_translation[0][0]
    lylw = translation.origin

    if ylw.lower() == lylw.lower() and full_trans is None:
        return None

    card_id = generate_card_uuid(ylw + lylw)

    lylp = ''

    if len(main_translation[-1]) == 4:
        lylp = main_translation[-1][-1]

    yle = ''

    if full_trans is not None:
        yle += format_explanations(full_trans, 'synonyms')

    lyle = ''

    if definitions_trans is not None:
        lyle += format_explanations(definitions_trans, 'definitions')

    return [card_id, ylw, yle, lylw, lylp, lyle]


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
