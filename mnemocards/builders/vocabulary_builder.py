
import csv
import os
import uuid

import genanki

from mnemocards import ASSETS_DIR
from mnemocards.utils import get_hash_id


css = open(f"{ASSETS_DIR}/css/vocabulary.css").read()
CARD_MODEL = genanki.Model(
    get_hash_id("404aed54-6cdd-4397-b0d1-6af8c197f593"),
    "Vocabulary model",
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
                </style>
                <div class="origin word">{{YourLanguageWord}}</div>
                <div class="origin comment">{{YourLanguageExplanation}}</div>
            ''',
            "afmt": '''
                <style>
                    .card {
                        background: {{CardColor}};
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
    get_hash_id("434aed54-6cdd-4397-b0d1-6af8c197f593"),
    "Vocabulary model (Japanese)",
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
                </style>
                <div class="origin word">{{YourLanguageWord}}</div>
                <div class="origin comment">{{YourLanguageExplanation}}</div>
            ''',
            "afmt": '''
                <style>
                    .card {
                        background: {{CardColor}};
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


class MyNote(genanki.Note):

    def __init__(self, note_id, **kwargs):
        super().__init__(**kwargs)
        self.note_id = note_id

    @property
    def guid(self):
        return self.note_id


class VocabularyBuilder(object):
    def __init__(self):
        pass
    def build_cards(self, data_dir, src, deck_config):
        cards = []
        filename = os.path.join(data_dir, src["file"])
        assets_dir = os.path.join(data_dir, src.get("assets", "assets"))
        with open(filename, "r") as csvfile:
            reader = csv.reader(csvfile, delimiter="\t", quotechar='"')
            iterator = iter(reader)
            # Skip header if header is true in the configuration file.
            if src["header"]:
                next(iterator)
            audio_files = []
            color = src["card_color"]
            show_p = "true" if src["pronunciation_in_reverse"] else ""
            for i, row in enumerate(iterator):
                note_id, ylw, yle, lylw, lylp, lyle, card_tags = row
                tags = src["card_properties"]["tags"]
                furigana = src.get("furigana", False)
                assert type(tags) == list
                tags.extend(card_tags.split(","))
                my_note = MyNote(
                    note_id,
                    model=CARD_MODEL_JAPANESE if furigana else CARD_MODEL,
                    fields=[
                        ylw, yle, lylw, lylp, lyle, color, show_p
                    ],
                    tags=tags
                )
                cards.append(my_note)
        return cards

