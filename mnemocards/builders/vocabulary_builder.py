
import csv
import glob
import os
import re
import uuid

import genanki

from gtts import gTTS

from mnemocards import ASSETS_DIR
from mnemocards.utils import get_hash_id
from mnemocards.utils import NoteID


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
    get_hash_id("2d5e52ea-c9de-4d0f-bdf5-ee06ad815e61"),
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
                <div>{{type:LanguageYouLearnWord}}</div>
            ''',
            "afmt": '''
                <style>
                    .card {
                        background: {{CardColor}};
                    }
                </style>
                <div class="origin word">{{YourLanguageWord}}</div>
                <div class="origin comment">{{YourLanguageExplanation}}</div>
                <div>{{type:LanguageYouLearnWord}}</div>
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

RE_REMOVE_PAREN = re.compile("[\(\[].*?[\)\]]")


def remove_parentheses(text):
    return re.sub(RE_REMOVE_PAREN, "", text)


def remove_spaces(text):
    return text.replace(" ", "")


class VocabularyBuilder(object):

    def __init__(self):
        pass

    def prepare_media_dir(self, data_dir, audio_dict):
        media_dir = os.path.join(data_dir,
                audio_dict.get("media_dir", ".media"))
        if not os.path.exists(media_dir):
            os.makedirs(media_dir)
        return media_dir

    def build_cards(self, data_dir, src, deck_config, clean_audio=True):
        notes, media = [], []
        # Get data from config.
        header = src["header"]
        color = src.get("card_color", "#33AA33")
        show_p = "true" if src.get("pronunciation_in_reverse", False) else ""
        generate_audio = src.get("audio", {})
        media_dir = None
        if generate_audio is not None:
            media_dir = self.prepare_media_dir(data_dir, generate_audio)
        furigana = src.get("furigana", False)
        card_properties = src.get("card_properties", None)
        tags = []
        if card_properties is not None:
            tags = card_properties.get("tags", [])
        # Read TSV file.
        filename = os.path.join(data_dir, src["file"])
        with open(filename, "r", encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter="\t", quotechar='"')
            iterator = iter(reader)
            # Skip header if header is true in the configuration file.
            if header:
                next(iterator)
            for i, row in enumerate(iterator):
                note_id, ylw, yle, lylw, lylp, lyle, row_tags = row
                assert type(tags) == list
                note_tags = tags.copy()
                note_tags.extend(row_tags.split(","))
                # Generate audio.
                if generate_audio:
                    clean_text = remove_parentheses(lylw)
                    if furigana:
                        # If you leave those spaces you get wrong
                        # pronunciations, like in `スペイン 人`.
                        # Instead of `supein jin` it pronounces it as
                        # `supein hito` because the kanji `人` alone is
                        # pronounced as `hito`.
                        clean_text = remove_spaces(clean_text)
                    hash_text = get_hash_id(clean_text, bytes=8)
                    sound_file = os.path.join(f'{media_dir}', f'{hash_text}.mp3')
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
        # Remove unused audio files.
        # TODO: this should be optional. Add an argument to force clean.
        # FIXME: if you reuse the same media folder for another vocabulary
        # builder you are going to delete media files from the other cards...
        if generate_audio and clean_audio:
            all_audio_files = os.path.join(f'{media_dir}', '*.mp3')
            unused_audio_files = set(all_audio_files) - set(media)
            for i in unused_audio_files:
                print(f"Removing unused audio file {i}")
                os.remove(i)

        return notes, media

