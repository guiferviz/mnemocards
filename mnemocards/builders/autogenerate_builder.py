import os
import csv

from gtts import gTTS

from mnemocards.utils import get_hash_id
from mnemocards.utils import NoteID

from mnemocards.builders.vocabulary_builder import VocabularyBuilder, CARD_MODEL, CARD_MODEL_JAPANESE
from mnemocards.builders.vocabulary_builder import remove_parentheses, remove_spaces
from mnemocards import autogenerate_tsv as tsv


class AutogenerateBuilder(VocabularyBuilder, object):

    def __init__(self):
        pass

    def parse_src(self, data_dir, src):
        settings = {}
        settings["color"] = src.get("card_color", "#f5f5f5")
        settings["show_p"] = "true" if src.get(
            "pronunciation_in_reverse", False) else ""
        settings["tsv_as_source"] = src.get("use_tsv_for_generation", False)
        settings["filename"] = os.path.join(data_dir, src["word_file"])

        if settings["tsv_as_source"]:
            settings["filename"] = os.path.join(data_dir, src["tsv_file"])

        settings["generate_audio"] = src.get("audio", False)
        settings["lang"] = src.get("lang", None)

        if settings["generate_audio"]:

            settings["media_dir"] = self.prepare_media_dir(data_dir, {})

        settings["furigana"] = src.get("furigana", False)
        settings["card_properties"] = src.get("card_properties", None)
        settings["save_tsv"] = src.get("save_tsv", False)

        settings["tags"] = []

        if src.get("card_properties", None):
            settings["tags"] = src["card_properties"].get("tags", [])

        return settings

    def build_cards_from_words(self, settings):
        notes, media = [], []
        words = tsv.scrape_words_from_file(settings["filename"])
        translations = tsv.get_translation(
            words, settings["lang"]["original"], settings["lang"]["translation"])
        cards = [tsv.prepare_card_fields(trans) for trans in translations]
        for card in cards:
            card["tags"] = settings["tags"]

            if settings["generate_audio"]:
                clean_text = remove_parentheses(card["lylw"])
                if settings["furigana"]:
                    # If you leave those spaces you get wrong
                    # pronunciations, like in `スペイン 人`.
                    # Instead of `supein jin` it pronounces it as
                    # `supein hito` because the kanji `人` alone is
                    # pronounced as `hito`.
                    clean_text = remove_spaces(clean_text)
                hash_text = get_hash_id(clean_text, bytes=8)
                sound_file = f'{settings["media_dir"]}/{hash_text}.mp3'
                if not os.path.exists(sound_file):
                    print(f"Creating audio file {sound_file}")
                    lang = settings["lang"]["original"]
                    tts = gTTS(clean_text, lang=lang)
                    tts.save(sound_file)
                card["lylp"] += f" [sound:{hash_text}.mp3]"
                media.append(sound_file)
            note = NoteID(
                card["card_id"],
                model=CARD_MODEL_JAPANESE if settings["furigana"] else CARD_MODEL,
                fields=[
                    card["ylw"], card["yle"], card["lylw"], card["lylp"], card["lyle"], settings["color"], settings["show_p"]
                ],
                tags=card["tags"]
            )
            notes.append(note)
        return notes, media

    def build_cards_from_tsv(self):
        pass

    def build_cards(self, data_dir, src, deck_config, clean_audio=True):

        # Get data from config.
        settings = self.parse_src(data_dir, src)

        # Read TSV file.
        builder = self.build_cards_from_words
        if settings["tsv_as_source"]:
            notes, media = self.build_cards_from_tsv(settings)

        notes, media = builder(settings)

        # Remove unused audio files.
        # TODO: this should be optional. Add an argument to force clean.
        # FIXME: if you reuse the same media folder for another vocabulary
        # builder you are going to delete media files from the other cards...
        # if settings["generate_audio"]:
        #     rmtree(settings['media_dir'])

        return notes, media

        with open(filename, "r") as csvfile:
            reader = csv.reader(csvfile, delimiter="\t", quotechar='"')
            iterator = iter(reader)
            # Skip header if header is true in the configuration file.
            next(iterator)
            for i, row in enumerate(iterator):
                note_id, ylw, yle, lylw, lylp, lyle, row_tags = row
                assert type(tags) == list
                note_tags = tags.copy()
                note_tags.extend(row_tags.split(","))
                # Generate audio.
                if settings["generate_audio"]:
                    clean_text = remove_parentheses(lylw)
                    if settings["furigana"]:
                        # If you leave those spaces you get wrong
                        # pronunciations, like in `スペイン 人`.
                        # Instead of `supein jin` it pronounces it as
                        # `supein hito` because the kanji `人` alone is
                        # pronounced as `hito`.
                        clean_text = remove_spaces(clean_text)
                    hash_text = get_hash_id(clean_text, bytes=8)
                    sound_file = f"{media_dir}/{hash_text}.mp3"
                    if not os.path.exists(sound_file):
                        print(f"Creating audio file {sound_file}")
                        lang = generate_audio["lang"]
                        tts = gTTS(clean_text, lang=lang)
                        tts.save(sound_file)
                    lylp += f" [sound:{hash_text}.mp3]"
                    media.append(sound_file)
                # Create note.
                note = NoteID(
                    note_id,
                    model=CARD_MODEL_JAPANESE if furigana else CARD_MODEL,
                    fields=[
                        ylw, yle, lylw, lylp, lyle, color, show_p
                    ],
                    tags=note_tags
                )
                notes.append(note)

        return notes, media
