import os
import csv

import genanki

from gtts import gTTS

from mnemocards import ASSETS_DIR
from mnemocards.utils import get_hash_id, NoteID, generate_furigana

from mnemocards.builders.vocabulary_builder import VocabularyBuilder
from mnemocards.builders.vocabulary_builder import remove_parentheses, remove_spaces
from mnemocards import maketsv as tsv


css = open(f"{ASSETS_DIR}/css/autogenerate.css").read()
CARD_MODEL = genanki.Model(
    get_hash_id("725b5570-eb22-4ca5-a2b2-817e04514cde"),
    "Autogenerated vocabulary model",
    fields=[
        # Visible fields.
        {"name": "YourLanguageWord"},
        {"name": "YourLanguageExplanation"},
        {"name": "LanguageYouLearnWord"},
        {"name": "LanguageYouLearnPronunciation"},
        {"name": "LanguageYouLearnExplanation"},
        # Configuration fields.
        {"name": "CardColor"},
        {"name": "ShowPronunciationInReverse"},
    ],
    templates=[
        {
            "name": "Vocabulary card",
            "qfmt": '''
                <style>
                    .card {
                        background: {{CardColor}};
                    }
                    .origin {
                        color: black;
                    }
                    .synonyms .line_2 {
                        color: #0000;
                    }
                </style>
                <div class="origin word">{{YourLanguageWord}}</div>
                <div class="origin comment">{{YourLanguageExplanation}}</div>
            ''',
            "afmt": '''
                <style>
                    .card {
                        background: {{CardColor}};
                    }
                    .origin {
                        color: black;
                    }
                    .destination {
                        color: black;
                    }
                </style>
                <div class="origin word">{{YourLanguageWord}}</div>
                <div class="origin comment">{{YourLanguageExplanation}}</div>
                <hr>
                <div class="destination word">{{LanguageYouLearnWord}}</div>
                <div class="destination fonetic">{{LanguageYouLearnPronunciation}}</div>
                <div class="destination comment">{{LanguageYouLearnExplanation}}</div>
            ''',
        },
        {
            "name": "Vocabulary card (reversed)",
            "qfmt": '''
                <style>
                    .card {
                        background: {{CardColor}};
                    }
                    .destination {
                        color: black;
                    }
                    .definitions .line_1{
						color: #0000
					}
					.definitions .line_2{
						color: #0000
					}
                </style>
                <div class="destination word">{{LanguageYouLearnWord}}</div>
                {{#ShowPronunciationInReverse}}
                <div class="destination fonetic">{{LanguageYouLearnPronunciation}}</div>
                {{/ShowPronunciationInReverse}}
                <div class="destination comment">{{LanguageYouLearnExplanation}}</div>
            ''',
            "afmt": '''
                <style>
                    .card {
                        background: {{CardColor}};
                    }
                    .origin {
                        color: black;
                    }
                    .destination {
                        color: black;
                    }
                </style>
                <div class="destination word">{{LanguageYouLearnWord}}</div>
                <div class="destination fonetic">{{LanguageYouLearnPronunciation}}</div>
                <div class="destination comment">{{LanguageYouLearnExplanation}}</div>
                <hr>
                <div class="origin word">{{YourLanguageWord}}</div>
                <div class="origin comment">{{YourLanguageExplanation}}</div>
            ''',
        },
    ],
    css=css,
)
CARD_MODEL_JAPANESE = genanki.Model(
    get_hash_id("fcac015f-d9dc-4f62-a8f9-0a1ef7a621e2"),
    "Autogenerated vocabulary model (Japanese)",
    fields=[
        # Visible fields.
        {"name": "YourLanguageWord"},
        {"name": "YourLanguageExplanation"},
        {"name": "LanguageYouLearnWord"},
        {"name": "LanguageYouLearnPronunciation"},
        {"name": "LanguageYouLearnExplanation"},
        # Configuration fields.
        {"name": "CardColor"},
        {"name": "ShowPronunciationInReverse"},
    ],
    templates=[
        {
            "name": "Vocabulary card",
            "qfmt": '''
                <style>
                    .card {
                        background: {{CardColor}};
                    }
                    .origin {
                        color: black;
                    }
                    .synonyms .line_2 {
                        color: #0000;
                    }
                </style>
                <div class="origin word">{{YourLanguageWord}}</div>
                <div class="origin comment">{{YourLanguageExplanation}}</div>
            ''',
            "afmt": '''
                <style>
                    .card {
                        background: {{CardColor}};
                    }
                    .origin {
                        color: black;
                    }
                    .destination {
                        color: black;
                    }
                </style>
                <div class="origin word">{{YourLanguageWord}}</div>
                <div class="origin comment">{{YourLanguageExplanation}}</div>
                <hr>
                <div class="destination word">{{furigana:LanguageYouLearnWord}}</div>
                <div class="destination fonetic">{{LanguageYouLearnPronunciation}}</div>
                <div class="destination comment">{{LanguageYouLearnExplanation}}</div>
            ''',
        },
        {
            "name": "Vocabulary card (reversed)",
            "qfmt": '''
                <style>
                    .card {
                        background: {{CardColor}};
                    }
                    .destination {
                        color: black;
                    }
                    .definitions .line_1{
						color: #0000
					}
					.definitions .line_2{
						color: #0000
					}
                </style>
                <div class="destination word">{{kanji:LanguageYouLearnWord}}</div>
                {{#ShowPronunciationInReverse}}
                <div class="destination fonetic">{{LanguageYouLearnPronunciation}}</div>
                {{/ShowPronunciationInReverse}}
                <div class="destination comment">{{LanguageYouLearnExplanation}}</div>
            ''',
            "afmt": '''
                <style>
                    .card {
                        background: {{CardColor}};
                    }
                    .origin {
                        color: black;
                    }
                    .destination {
                        color: black;
                    }
                </style>
                <div class="destination word">{{furigana:LanguageYouLearnWord}}</div>
                <div class="destination fonetic">{{LanguageYouLearnPronunciation}}</div>
                <div class="destination comment">{{LanguageYouLearnExplanation}}</div>
                <hr>
                <div class="origin word">{{YourLanguageWord}}</div>
                <div class="origin comment">{{YourLanguageExplanation}}</div>
            ''',
        },
    ],
    css=css,
)


class AutogenerateBuilder(VocabularyBuilder, object):

    def __init__(self):
        pass

    def parse_src_to_settings(self, data_dir, src):
        settings = {}
        settings["color"] = src.get("card_color", "#f5f5f5")
        settings["show_p"] = "true" if src.get(
            "pronunciation_in_reverse", False) else ""
        settings["tsv_as_source"] = src.get("use_tsv_for_generation", False)

        settings["filename"] = os.path.join(data_dir, src["file"])

        settings["generate_audio"] = src.get("audio", False)
        settings["lang"] = src.get("lang", {})
        if not settings["lang"]:
            settings["lang"]["original"] = "en"
            settings["lang"]["translation"] = "es"

        if settings["generate_audio"]:

            settings["media_dir"] = self.prepare_media_dir(data_dir, {})

        settings["one_translation"] = src.get("one_translation", False)

        settings["furigana"] = src.get("furigana", False)

        settings["furigana_type"] = src.get("furigana_type", "hira")

        settings["card_properties"] = src.get("card_properties", None)

        settings["tags"] = []

        if src.get("card_properties", None):
            settings["tags"] = src["card_properties"].get("tags", [])

        return settings

    def build_cards_from_words(self, settings):
        words = tsv.scrape_words_from_file(settings["filename"])
        translations = tsv.get_translation(
            words, settings["lang"]["original"], settings["lang"]["translation"])
        cards = [tsv.prepare_card_fields(
            trans) for trans in translations if tsv.prepare_card_fields(trans)]
        for card in cards:
            card["tags"] = settings["tags"]

        return cards

    def build_cards_from_tsv(self, settings):
        with open(settings["filename"], "r", encoding='utf8') as csvfile:
            reader = csv.reader(csvfile, delimiter="\t", quotechar='"')
            iterator = iter(reader)
            cards = []
            # Skip header that is present in every autogenerated TSV.
            next(iterator)
            for i, row in enumerate(iterator):
                card_id, ylw, yle, lylw, lylp, lyle, row_tags = row
                tags = settings["tags"]
                tags.extend(row_tags.split(","))
                card = {"card_id": card_id, "ylw": ylw, "yle": yle,
                        "lylw": lylw, "lylp": lylp, "lyle": lyle, "tags": tags}
                cards.append(card)
        return cards

    def build_notes_and_media(self, settings, cards):
        notes, media = [], []
        for card in cards:

            if settings["furigana"] and (settings["lang"]["original"] == "ja"):
                card["lylp"] = ""
                card["lylw"] = generate_furigana(
                    card["lylw"], settings["furigana_type"])

            if settings["one_translation"]:
                card["yle"] = ""

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
                    card["ylw"], card["yle"], card["lylw"], card["lylp"],
                    card["lyle"], settings["color"], settings["show_p"]],
                tags=card["tags"])
            notes.append(note)
        return notes, media

    def build_cards(self, data_dir, src, deck_config):

        # Get data from config.
        settings = self.parse_src_to_settings(data_dir, src)

        # Choose what builder to use - from words or TSV.
        builder = self.build_cards_from_words
        if "tsv" in settings["filename"].split('.')[-1]:
            builder = self.build_cards_from_tsv

        cards = builder(settings)
        #
        notes, media = self.build_notes_and_media(settings, cards)

        return notes, media
