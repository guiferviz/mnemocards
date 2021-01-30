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


def prepare_card_fields(translation):
    main_translation = translation.extra_data["translation"]
    full_trans = translation.extra_data["all-translations"]
    definitions_trans = translation.extra_data["definitions"]

    ylw = main_translation[0][0]
    lylw = translation.origin

    if ylw.lower() == lylw.lower() and full_trans is None:
        return None

    card_id = str(generate_card_uuid(ylw + lylw))

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


def generate_tsv_lines(words, lang_pair):

    lang_pair = lang_pair.split('_')
    header = "ID\tYourLanguageWord\tYourLanguageExplanation\tLanguageYouLearnWord\tLanguageYouLearnPronunciation\tLanguageYouLearnExplanation\tTags\n"
    all_tsv_lines = []

    translations = False
    while translations == False:
        translations = get_translation(
            words, src=lang_pair[0], dest=lang_pair[1])

    for translation in translations:

        tsv_line = ''
        tsv_fields = prepare_card_fields(translation)

        if tsv_fields is None:
            continue

        for field in tsv_fields:
            tsv_line += field + '\t'

        tsv_line += '\n'
        all_tsv_lines += [tsv_line]

    all_tsv_lines = sorted(all_tsv_lines)
    all_tsv_lines.insert(0, header)
    return all_tsv_lines


def scrape_words_from_file(data_dir, word_file):
    filename = os.path.join(data_dir, word_file)
    if not os.path.exists(filename):

        raise Exception("""File with words for TSV generator doesn't exist.
Default file name for words "words.txt".
To get words from file with differen name use key [--word-file WORD_FILE]""")

    with open(filename, "r+") as file:
        words_list = []
        for word in file:
            words_list.append(word.strip())
    return words_list


def collect_tsv_lines(args):
    all_words = []
    all_words += scrape_words_from_file(args.data_dir, args.word_file)
    if args.recursive:
        for root, dirs, files in os.walk(args.data_dir):
            # Ignore hidden folders.
            dirs[:] = [d for d in dirs if not d[0] == "."]
            for d in dirs:
                d = os.path.join(root, d)
                all_words += scrape_words_from_file(d, args.word_file)
    tsv_lines = generate_tsv_lines(all_words, args.language_pair)
    return tsv_lines


def save_tsv_files(tsv_lines, output_dir, language_pair):
    print("Writing packages to a file...")

    filename = os.path.join(output_dir, f"{language_pair}.tsv")

    with open(filename, 'w') as file:
        for one_line in tsv_lines:
            file.write(one_line)


def make_tsv(args):
    if not os.path.exists(args.data_dir):

        raise Exception("Data dir does not exist")

    tsv_lines = collect_tsv_lines(args)
    save_tsv_files(tsv_lines, args.output_dir, args.language_pair)
