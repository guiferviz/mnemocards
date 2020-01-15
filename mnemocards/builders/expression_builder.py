
import csv
import os

import genanki

from mnemocards import ASSETS_DIR
from mnemocards.utils import get_hash_id
from mnemocards.utils import NoteID


css = open(f"{ASSETS_DIR}/css/vocabulary.css").read()
CARD_MODEL = genanki.Model(
    get_hash_id("42d0a1c1-2bb3-4f23-ba00-e89585d52328"),
    "Expressions model",
    fields=[
        # Visible fields.
        {"name": "Expression"},
        {"name": "Explanation"},
        {"name": "Meaning"},
        {"name": "Example"},
        # Configuration fields.
        {"name": "CardColor"},
    ],
    templates=[
        {
            "name": "Expression card",
            "qfmt": '''
                <style>
                    .card {
                        background: {{CardColor}};
                    }
                </style>
                <div class="origin word">{{Expression}}</div>
                <div class="origin comment">{{Explanation}}</div>
            ''',
            "afmt": '''
                <style>
                    .card {
                        background: {{CardColor}};
                    }
                </style>
                <div class="origin word">{{Expression}}</div>
                <div class="origin comment">{{Explanation}}</div>
                <hr>
                <div class="destination word">{{Meaning}}</div>
                <div class="destination comment">{{Example}}</div>
            ''',
        }
    ],
    css=css,
)


class ExpressionBuilder(object):

    def __init__(self):
        pass

    def build_cards(self, data_dir, src, deck_config):
        notes, media = [], []
        # Get data from config.
        header = src["header"]
        color = src["card_color"]
        card_properties = src.get("card_properties", None)
        tags = []
        if card_properties is not None:
            tags = card_properties.get("tags", [])
            assert type(tags) == list
        # Read TSV file.
        filename = os.path.join(data_dir, src["file"])
        with open(filename, "r") as csvfile:
            reader = csv.reader(csvfile, delimiter="\t", quotechar='"')
            iterator = iter(reader)
            # Skip header if header is true in the configuration file.
            if header:
                next(iterator)
            for i, row in enumerate(iterator):
                note_id, expr, expl, meaning, example, row_tags = row
                note_tags = tags.copy()
                note_tags.extend(row_tags.split(","))
                # Create note.
                note = NoteID(
                    note_id,
                    model=CARD_MODEL,
                    fields=[
                        expr, expl, meaning, example, color
                    ],
                    tags=note_tags
                )
                notes.append(note)

        return notes, media

